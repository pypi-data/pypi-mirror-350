
from pathlib import Path

import grpc
import numpy as np
import pandas as pd
from radiens.api.api_utils.util import to_suffix
from radiens.exceptions.grpc_error import handle_grpc_error
from radiens.grpc_radiens import (biointerface_pb2, common_pb2, datasource_pb2,
                                  radiens_dev_pb2, radiensserver_pb2_grpc,
                                  spikesorter_pb2)
from radiens.lib.dataset_metadata import DatasetMetadata
from radiens.lib.sig_metrics import SignalMetrics, SignalMetricsStatus
from radiens.lib.signals_snapshot import PSD, Signals
from radiens.utils.constants import TimeRange
from radiens.utils.enums import ClientType, RadiensFileType, RasterMode
from radiens.utils.util import new_server_channel


def set_datasource(addr, req: datasource_pb2.DataSourceSetSaveRequest):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            res = stub.SetDataSourceFromFile(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.VIDERE)
        spike_files = []
        for f in res.associatedDsrcs:
            if RadiensFileType.parse(f.fileType) == RadiensFileType.SPIKES:
                spike_files.append(
                    Path(f.path, f.baseName+to_suffix(RadiensFileType.SPIKES)))
        return DatasetMetadata(res), spike_files


def unlink_datasource(addr, datasetIDs: list):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            res = stub.ClearDataSource(
                datasource_pb2.DataSourceRequest(dsourceID=datasetIDs)
            )
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.VIDERE)
        return list(res.sortedID)


def list_datasource_ids(addr):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            res = stub.ListDataSourceIDs(datasource_pb2.DataSourceRequest())
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.VIDERE)
        return list(res.sortedID)


def convert_kilosort_output(addr, req: radiens_dev_pb2.WrangleRequest):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensSpikeSorter1Stub(chan)
        try:
            stub.SpikeSorterWrangleData(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.VIDERE)
        return


def get_signals(addr, req):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            raw = stub.GetHDSnapshotPy(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.VIDERE)
        return Signals(raw)


def get_psd(addr, req):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            resp = stub.GetPSD(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.VIDERE)
        if req.isReturnPSD:
            return PSD(resp)


def get_spike_waveforms(addr, dsource_id: str, time_range: list):
    if len(time_range) != 2:
        raise ValueError("time range must be a list of length 2")
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            req = biointerface_pb2.SpikesGetSpikesRequest(spikeLabels=[])
            req.dsourceID = dsource_id
            req.mode = biointerface_pb2.NeuronsSignalMode.SpikeWaveforms
            req.timeStart = time_range[0]
            req.timeStop = time_range[1]
            req.maxSpikesPerChannel = 1000  # arbitrary for now (TODO)

            raw = stub.SpikesGetSpikesDense(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.VIDERE)

        _waveforms = np.reshape(
            np.frombuffer(raw.data, dtype=np.float32),
            (raw.totalNSpikes, raw.waveformNPoints),
        )

        return _waveforms


def get_spikes_timestamps(addr, dsource_id: str, time_range: TimeRange):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            req = spikesorter_pb2.SpikeSorterGetRasterDataRequest(
                spikeSorterID=dsource_id,
                timeWindow=1,
                # fs * timeWindow/plotWidthPoints = sampFactor (1)
                plotWidthPoints=time_range.fs,
                componentID="",
                mode=RasterMode.CHANNELS.pb_value,
                timeRange=time_range.sec,
                labeledOnly=True,
                primarySiteOnly=True,
            )

            raw = stub.SpikesGetRasterData(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.VIDERE)

        timestamps = np.empty_like(raw.spikeTimestamps, dtype=np.float64)
        labels = np.empty_like(raw.spikeTimestamps, dtype=np.int32)
        dset_idxs = np.empty_like(raw.spikeTimestamps, dtype=np.int32)

        for (i, msg) in enumerate(raw.spikeTimestamps):
            timestamps[i] = msg.spikeTimestamp
            labels[i] = msg.label
            dset_idxs[i] = msg.dataIdxs[0]
        return {"timestamps": timestamps, "labels": labels, "dset_idxs": dset_idxs}


# ==========================
# ====== KPIs ==============
# ==========================


def set_kpi_calculate(addr, req) -> None:
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            stub.KpiCalculate(common_pb2.KpiStandardRequest(req))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.VIDERE)


def set_kpi_clear(addr, dsource_id) -> None:
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            stub.KpiClear(common_pb2.KpiStandardRequest(
                dsourceID=[dsource_id]))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.VIDERE)


def set_kpi_params(addr, req):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            stub.SetKpiParam(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.VIDERE)


def set_kpi_packet_dur(addr, req):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            stub.SetKpiPacketDur(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.VIDERE)


def get_kpi_metrics(addr, dsource_id, req) -> SignalMetrics:
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            resp = stub.KpiGetMetrics(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.VIDERE)
        return SignalMetrics(dsource_id, resp)


def get_kpi_status(addr, dsource_id) -> SignalMetricsStatus:
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            resp = stub.GetKpiStatus(
                common_pb2.GetKpiStatusRequest(streamGroupId=dsource_id)
            )
            resp2 = stub.GetDataSourceKpiFileStatus2(
                datasource_pb2.DataSourceRequest(dsourceID=[dsource_id])
            )
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.VIDERE)
        return SignalMetricsStatus(resp, resp2)


def get_kpi_params(addr, dsource_id) -> pd.DataFrame:
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            resp = stub.GetKpiParam(
                datasource_pb2.DataSourceRequest(dsourceID=[dsource_id])
            )
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.VIDERE)
        p = {
            "ntv_idx": [],
            "chan_enabled": [],
            "thr_activated": [],
            "thr": [],
            "thr_sd": [],
            "thr_wdw": [],
            "shadow": [],
            "weak_thr_activated": [],
            "weak_thr": [],
            "weak_thr_sd": [],
            "thr_wdw_pts": [],
            "shadow_pts": [],
        }
        for v in resp.rec:
            p["ntv_idx"].append(v.ntvChanIdx)
            p["chan_enabled"].append(v.isEnabled)
            p["thr_activated"].append(v.isSetThr)
            p["thr"].append(np.array(v.thr))
            p["thr_sd"].append(np.array(v.thrSd))
            p["thr_wdw"].append(np.around(np.array(v.thrWdw) * 1000.0, 5))
            p["shadow"].append(np.around(np.array(v.shadow) * 1000.0, 5))
            p["weak_thr_activated"].append(np.array(v.isSetWeakThr))
            p["weak_thr"].append(np.array(v.weakThr))
            p["weak_thr_sd"].append(np.array(v.weakThrSd))
            p["thr_wdw_pts"].append(v.thrWdwPts)
            p["shadow_pts"].append(v.shadowPts)
        return pd.DataFrame(p)


def command_dashboard(addr, req) -> str:
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.DashboardsStub(chan)
        try:
            stub.CommandDashboard(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.VIDERE)


def summa_list_sessions(addr, req) -> str:
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.DashboardsStub(chan)
        try:
            resp = stub.ListSessions(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.VIDERE)
        d = {}
        for session in resp.session:
            d[session.summaID] = {"dsource_ids": session.dsourceIDs}
        return d


def summa_clear_sessions(addr, req) -> str:
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.DashboardsStub(chan)
        try:
            stub.ClearAllSessions(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.VIDERE)


def summa_launch_session_analysis(addr, req) -> str:
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.DashboardsStub(chan)
        try:
            resp = stub.LaunchSessionAnalysis(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.VIDERE)
        return resp


def summa_get_session_analysis(addr, req) -> str:
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.DashboardsStub(chan)
        try:
            resp = stub.GetSessionAnalysis(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.VIDERE)
        return resp
