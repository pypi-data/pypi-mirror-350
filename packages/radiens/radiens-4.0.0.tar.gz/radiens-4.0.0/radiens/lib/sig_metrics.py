
import numpy as np
import pandas as pd
from radiens.grpc_radiens import common_pb2
from radiens.utils.constants import PRIMARY_CACHE_STREAM_GROUP_ID, TimeRange
from radiens.utils.enums import (ClientType, MetricID, MetricMode, MetricName,
                                 MetricStats)
from radiens.utils.util import from_dense_matrix, make_time_range


def metric_spec(metric: MetricID) -> dict:
    if metric.name in ['MAX_ABS', 'MAX_ABS_ISI']:
        return {'lbl': '|V_max|', 'units': 'uV'}
    if metric.name in ['MAX_MIN_DIFF_ABS', 'MAX_MIN_DIFF_ABS_ISI']:
        return {'lbl': '|V_pp|', 'units': 'uV'}
    if metric.name in ['SD', 'SD_ISI']:
        return {'lbl': '|V_sd|', 'units': 'uV'}
    if metric.name in ['RMS', 'RMS_ISI']:
        return {'lbl': 'V_rms', 'units': 'uV'}
    if metric.name in ['SNR']:
        return {'lbl': 'SNR', 'units': ''}
    if metric.name in ['EVENT_RATE']:
        return {'lbl': 'Spike Rate', 'units': 'spikes/sec'}
    if metric.name in ['EVENT_MAX_ABS']:
        return {'lbl': 'Spike |V_max|', 'units': 'uV'}
    if metric.name in ['EVENT_MAX_MIN_DIFF_ABS']:
        return {'lbl': 'Spike |V_pp|', 'units': 'uV'}
    if metric.name in ['MEAN_MAX_ABS']:
        return {'lbl': 'Avg. Spike |V_max|', 'units': 'uV'}
    if metric.name in ['EVENT_MEAN_MAX_MIN_DIFF_ABS']:
        return {'lbl': 'Avg. Spike |V_pp|', 'units': 'uV'}
    if metric.name in ['MAX_MIN_DIFF_ABS_AMPLIFIED']:
        return {'lbl': '|V_pp|^2 for V_pp > 2*SD', 'units': 'uV^2'}
    return {'lbl': 'unknown', 'units': 'unknown'}


def sort_metric_ids(metric_ids: list[MetricID]) -> list[MetricID]:
    '''Returns 'metric_ids' list sorted in ascending order by mode and name, respectively. '''
    x = []
    for i in metric_ids:
        x.append([i.mode.value, i.name.name])
    x.sort()
    s = []
    for i in x:
        s.append(MetricID(mode=MetricMode(i[0]), name=MetricName[i[1]]))
    return s


class SignalMetricsStatus():
    '''
    Container for signal metrics status
    '''

    def __init__(self, cache: common_pb2.KpiStatusReply, file: common_pb2.KpiFileStatus2 = None):
        if cache is None and file is None:
            raise ValueError('cache and file cannot both be None')
        self._d = {'file': None, 'cache': None}
        if cache not in [None]:
            self._d['cache'] = {
                'dsource_id': cache.streamGroupId,
                'num_packets_memory': cache.numPacketsMemory, 'num_sigs': cache.numSigs,
                'packet_dur_sec': cache.packetDur, 'update_period_sec': cache.updatePeriod, 'beta': cache.beta, 'is_tracking_cache': cache.isTrackingSignalCache,
                'num_packets': cache.numPackets, 'persistence_sec': cache.persistence, 'memory_bytes': cache.memoryBytes, 'TR': make_time_range(pbTR=cache.tR)}
        if file not in [None]:
            self._d['file'] = {'kpi': {}, 'source': {
            }, 'scanner_mode': 'sprinting' if file.dsource[0].isSprinting else 'off'}
            self._d['file']['kpi']['is_avail'] = file.dsource[0].kpi.isAvail
            self._d['file']['kpi']['is_complete'] = file.dsource[0].kpi.isComplete
            self._d['file']['kpi']['frac_complete'] = file.dsource[0].kpi.fracComplete
            self._d['file']['kpi']['file_path_and_name'] = file.dsource[0].kpi.filePathAndName
            self._d['file']['kpi']['TR'] = make_time_range(
                pbTR=file.dsource[0].kpi.kpiTR)
            self._d['file']['kpi']['packet_dur_sec'] = file.dsource[0].kpi.packetDurSec
            self._d['file']['kpi']['num_sigs'] = file.dsource[0].kpi.numAmp
            self._d['file']['kpi']['bytes_in_bundle_packet'] = file.dsource[0].kpi.bytesInBundlePkt
            self._d['file']['kpi']['num_packets'] = file.dsource[0].kpi.numPackets
            self._d['file']['kpi']['dataset_uid'] = file.dsource[0].kpi.datasetUID
            self._d['file']['source']['file_path_and_name'] = file.dsource[0].kpi.filePathAndName
            self._d['file']['source']['TR'] = make_time_range(
                pbTR=file.dsource[0].source.TR)
            self._d['file']['source']['dataset_uid'] = file.dsource[0].source.datasetUID
            self._d['file']['source']['dsource_id'] = file.dsource[0].source.dsourceID

    @ property
    def time_range(self) -> TimeRange:
        """
        Signal metrics time range of either the backing file (if available) or the backing cache.
        """
        if self._d['file'] not in [None]:
            return self._d['file']['kpi']['TR']
        return self._d['cache']['TR']

    @ property
    def TR(self) -> TimeRange:
        """
        Aliases signal metrics available time range
        """
        return self.time_range

    @ property
    def type(self) -> str:
        """
        Returns 'file' if the signal metrics are backed by a file or 'cache' if backed by a cache.
        """
        return 'file' if self._d['file'] not in [None] else 'cache'

    @ property
    def datasource_id(self) -> str:
        """
        Datasource ID of the linked dataset on the Radiens hub.
        """
        if self._d['file'] not in [None]:
            return self._d['file']['source']['dsource_id']
        return self._d['cache']['dsource_id']

    @ property
    def num_sigs(self) -> int:
        """
        Number of signals.
        """
        if self._d['file'] not in [None]:
            return self._d['file']['kpi']['num_sigs']
        return self._d['cache']['num_sigs']

    @ property
    def packet_dur_sec(self) -> float:
        """
        Packet duration in sec
        """
        if self._d['file'] not in [None]:
            return self._d['file']['kpi']['packet_dur_sec']
        return self._d['cache']['packet_dur_sec']

    @ property
    def num_packets(self) -> int:
        """
        Packet duration in sec
        """
        if self._d['file'] not in [None]:
            return self._d['file']['kpi']['num_packets']
        return self._d['cache']['num_packets']

    @ property
    def is_calculating_metrics(self) -> bool:
        """
        Returns True if radiens hub is calculating the signal metrics
        """
        if self._d['file'] not in [None]:
            return not self._d['file']['kpi']['is_complete']
        return True

    @ property
    def attributes(self) -> dict:
        """
        Signal metrics attributes (dict)
        """
        return self._d

    @ property
    def summary_table(self) -> pd.DataFrame:
        return pd.DataFrame({'dsource_id': [self.datasource_id],
                             'source': [self.type],
                             'time_range': [self.TR.sec],
                             'walltime': [self.TR.walltime],
                             'num_signals': [self.num_sigs],
                             'packet_dur_sec': [self.packet_dur_sec],
                             'num_packetes': [self.num_packets],
                             }).T

    def print(self):
        """
        Prints the status.
        """
        print('Signal metrics status')
        print(self.summary_table)

    def __repr__(self):
        return self.summary_table.__repr__()

    def __str__(self):
        return self.summary_table.__str__()


class SignalMetrics():
    '''
    Container for signal metrics
    '''

    def __init__(self, dsource_id: str,  resp=common_pb2.KpiBundlePacketMetrics):
        self._ntv_idxs = resp.ntvIdxs
        self._d = {'dsource_id': dsource_id,
                   'num_packets': resp.metrics.numPackets, 'num_sigs': resp.metrics.numSigs,
                   'num_metrics': resp.metrics.numMetrics, 'packet_dur_sec': resp.metrics.packetDurSec,
                   'time_range': make_time_range(pbTR=resp.metrics.tR), 'signal_type': common_pb2.SignalType.Name(resp.sigType)}
        self._metric_ids = []
        for m_id in resp.metrics.metric:
            self._metric_ids.append(
                MetricID(mode=MetricMode(m_id.mode), name=MetricName(m_id.name)))
        self._pkt_idxs = resp.metrics.pktIdxs
        self._val = np.reshape(np.ravel(from_dense_matrix(resp.metrics.val)),
                               (self._d['num_packets'], self._d['num_sigs'], self._d['num_metrics']))
        self._stats_packets = MetricStats(mean=resp.metrics.statsPkts.mean, sd=resp.metrics.statsPkts.sD,
                                          min=resp.metrics.statsPkts.min, max=resp.metrics.statsPkts.max)
        self._stats_ = MetricStats(mean=resp.metrics.stats.mean, sd=resp.metrics.stats.sD,
                                   min=resp.metrics.stats.min, max=resp.metrics.stats.max)

    @property
    def _client_type(self) -> ClientType:
        return ClientType.ALLEGO if self._d['dsource_id'] in [
            PRIMARY_CACHE_STREAM_GROUP_ID] else ClientType.VIDERE

    @ property
    def time_range(self) -> TimeRange:
        """
        Signal metrics time range
        """
        return self._d['time_range']

    @ property
    def TR(self) -> TimeRange:
        """
        Aliases signal metrics time range
        """
        return self._d['time_range']

    @ property
    def ntv_idxs(self) -> list:
        """
        Signal metrics native channel indices
        """
        return self._ntv_idxs

    @ property
    def settings(self) -> dict:
        """
        Signal metrics settings (dict)
        """
        return self._d

    @ property
    def metric_ids(self) -> list:
        """
        Ordered list of signal metric IDs.
        """
        return self._metric_ids

    @ property
    def packet_idxs(self) -> list:
        """
        Signal metrics packet indices
        """
        return self._pkt_idxs

    @ property
    def num_packets(self) -> int:
        """
        Signal metrics number of packets
        """
        return self._d['num_packets']

    @ property
    def num_sigs(self) -> int:
        """
        Signal metrics number of signals
        """
        return self._d['num_sigs']

    @ property
    def packet_dur_sec(self) -> int:
        """
        Signal metrics packet duration in seconds
        """
        return self._d['packet_dur_sec']

    @ property
    def val(self) -> np.ndarray:
        """
        Signal metrics settings as multi-dimensional np.ndarray, with dim 0=packet idx, dim 1=channel index, dim 2=metric index.
        The ordered metric IDs are available in obj.metric_ids.

        Examples:

        1. access packet 20, channel 23, and metric 1
            `val[20][23][1]`

        2. access channel 23, metric 1 over all packets:
            `val[:,23,1]`

        3. access metric 1 over all packets and channels:
            `z = y[:,:,1]`  # returns 2-D array, where dim 0=packet index and dim 1=channels
            `np.ravel(z)`  # returns 1-D array with packets flattened

        """
        return self._val

    @property
    def table(self) -> pd.DataFrame:
        return pd.DataFrame({'datasource ID': [self._d['dsource_id']],
                            'signal type': [self._d['signal_type']],
                             'time range (sec)': ['[{:.3f}, {:.3f}]'.format(*self._d['time_range'].sec)],
                             'wall time': ['{}'.format(self._d['time_range'].walltime)],
                             'num signals': [self._d['num_sigs']],
                             'num metrics': [self._d['num_metrics']],
                             'packet dur (sec)': [self._d['packet_dur_sec']],
                             'num packets': [self._d['num_packets']]}).T

    @ property
    def packet_stats(self) -> dict:
        """
        """
        pkt_stats = {}
        return pkt_stats

    def print(self):
        """
        Prints a summary of the metrics.
        """
        print('{}: Signal metrics'.format(self._client_type.name))
        print(self.table)

    def __repr__(self):
        return self.table.__repr__()

    def __str__(self):
        return self.table.__str__()
