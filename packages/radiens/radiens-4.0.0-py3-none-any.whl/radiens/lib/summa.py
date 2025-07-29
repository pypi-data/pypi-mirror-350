from collections import OrderedDict, namedtuple

import numpy as np
import pandas as pd
from radiens.grpc_radiens import radiensserver_pb2
from radiens.lib.channel_metadata import ChannelMetadata
from radiens.lib.spikes import SpikesMetadata
from radiens.utils.enums import MetricID, MetricMode, MetricName
from radiens.utils.util import (Histogram, from_dense_matrix,
                                is_protobuf_time_range_empty, make_time_range)


class SummaStatus:
    """
    Container for Summa analysis status
    """

    def __init__(self, msg: radiensserver_pb2.SummaState):
        if not isinstance(msg, radiensserver_pb2.SummaState):
            raise ValueError("status wrong type")
        self._d = {
            "summa_id": msg.summaID,
            "is_complete": msg.isComplete,
            "frac_complete": msg.fracComplete,
            "msg": msg.msg,
            "dsource_walltime": {
                "start": msg.dsrcWalltimeStart,
                "end": msg.dsrcWalltimeEnd,
            },
            "analysis_walltime_start": msg.analysisWallTimeStart,
            "analysis_elapsed_time_sec": msg.analysisElapsedSec,
            "packet_dur_sec": msg.packetDurSec,
        }

    @property
    def id(self) -> str:
        """
        Signal metrics time range of either the backing file (if available) or the backing cache.
        """
        return self._d["summa_id"]

    @property
    def is_complete(self) -> bool:
        """
        Signal metrics time range of either the backing file (if available) or the backing cache.
        """
        return self._d["is_complete"]

    @property
    def frac_complete(self) -> float:
        """
        Signal metrics time range of either the backing file (if available) or the backing cache.
        """
        return self._d["frac_complete"]

    @property
    def packet_dur_sec(self) -> float:
        """
        Signal metrics time range of either the backing file (if available) or the backing cache.
        """
        return self._d["packet_dur_sec"]

    def string(self) -> str:
        return "SUMMA:{} - started @ {} (duration: {:.3f} sec); {} ({:.2f}/1.00), packet dur={:.3f} sec".format(
            self.id,
            self._d["analysis_walltime_start"],
            self._d["analysis_elapsed_time_sec"],
            "complete" if self.is_complete else "working",
            self.frac_complete,
            self.packet_dur_sec,
        )


class SummaAggregateStats:
    """
    Container for Summa analysis status
    """

    def __init__(self, msg: radiensserver_pb2.SummaAggregateStats):
        if not isinstance(msg, radiensserver_pb2.SummaAggregateStats):
            raise ValueError("msg wrong type")

        self._metric_ids = []
        for m_id in msg.metricID:
            self._metric_ids.append(
                MetricID(mode=MetricMode(m_id.mode),
                         name=MetricName(m_id.name))
            )
        self._hist = OrderedDict()
        for k, hist in enumerate(msg.hist):
            self._hist[self._metric_ids[k]] = Histogram(hist)

    @property
    def metric_ids(self) -> list:
        """
        Signal metrics time range of either the backing file (if available) or the backing cache.
        """
        return self._metric_ids

    @property
    def histogram(self) -> OrderedDict:
        """
        Signa metric histograms aggregated over all sites and all requested datasources.
        """
        return self._hist


class SummaDatasourceStats:
    """
    Container for Summa analysis status
    """

    def __init__(self, msg: radiensserver_pb2.SummaDatasourceAnalysisPkg):
        if not isinstance(msg, radiensserver_pb2.SummaDatasourceAnalysisPkg):
            raise ValueError("msg wrong type")
        self._ntv_idxs = np.array(msg.ntvIdxs, dtype=np.int64)
        self._hist = []
        for hist in msg.hist:
            self._hist.append(Histogram(hist))
        self._recs = []
        for rec in msg.recs:
            self._recs.append(from_dense_matrix(rec))
        self._hist_recs = []
        for hist in self._hist_recs:
            self._hist_recs.append(Histogram(hist))
        self._metric_ids = []
        for m_id in msg.metricID:
            self._metric_ids.append(
                MetricID(mode=MetricMode(m_id.mode),
                         name=MetricName(m_id.name))
            )

    @property
    def metric_ids(self) -> list:
        """
        Signal metrics time range of either the backing file (if available) or the backing cache.
        """
        return self._metric_ids

    @property
    def histogram(self) -> Histogram:
        """
        Signal metrics time range of either the backing file (if available) or the backing cache.
        """
        return self._hist


class SummaAnalysis:
    """
    Container for Summa signal analysis
    """

    def __init__(self, msg: radiensserver_pb2.SummaAnalysisReply):
        if not isinstance(msg, radiensserver_pb2.SummaAnalysisReply):
            raise ValueError("message wrong type")
        self._d = {
            "summa_id": msg.summaID,
            "all_dsource_ids": msg.allDsourceIDs,
            "req_available_dsource_ids": msg.reqAvailDsourceIDs,
            "status": SummaStatus(msg.state),
        }
        self._agg_stats = SummaAggregateStats(msg.aggStats)

        if len(self._d["all_dsource_ids"]) != len(msg.allDsourceSpec):
            raise ValueError("inconsistent number of datasource specs")
        self._dsrc_spec = {}
        for k, spec in enumerate(msg.allDsourceSpec):
            x = {"SG": ChannelMetadata(
                spec.sG), "TR": make_time_range(pbTR=spec.tR)}

            spec.niSpec.tR is None if is_protobuf_time_range_empty(
                spec.niSpec.tR
            ) else SpikesMetadata(spec.niSpec)
            self._dsrc_spec[self._d["all_dsource_ids"][k]] = x

        if len(self._d["req_available_dsource_ids"]) != len(msg.reqAvailDsourceStats):
            raise ValueError("inconsistent number of datasource stats")
        self._dsrc_stats = {}
        for k, stats in enumerate(msg.reqAvailDsourceStats):
            self._dsrc_stats[
                self._d["req_available_dsource_ids"][k]
            ] = SummaDatasourceStats(stats)

    @property
    def id(self) -> str:
        """
        Summa analysis ID
        """
        return self._d["summa_id"]

    @property
    def status(self) -> SummaStatus:
        """
        Status of the Summa analysis session.
        """
        return self._d["status"]

    @property
    def all_dsource_info(self) -> dict:
        """
        Summary information on all datasources included in this Summa analysis.
        """
        return self._dsrc_spec

    @property
    def aggregate_stats(self) -> SummaAggregateStats:
        """
        Summary statistics aggregated over the requested datasources.
        """
        return self._agg_stats

    @property
    def datasource_stats(self) -> dict:
        """
        Summary statistics on each of the requested datasources.
        """
        return self._dsrc_stats
