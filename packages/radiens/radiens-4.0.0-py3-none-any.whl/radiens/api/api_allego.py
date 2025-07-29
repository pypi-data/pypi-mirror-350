import sys
import warnings

import grpc
import numpy as np
import pandas as pd
from radiens.api.api_utils.util import (parse_stim_param_resp,
                                        stim_params_dict_to_req)
from radiens.exceptions.grpc_error import handle_grpc_error
from radiens.grpc_radiens import (allegoserver_pb2, allegoserver_pb2_grpc,
                                  biointerface_pb2, common_pb2, datasource_pb2,
                                  spikesorter_pb2)
from radiens.lib.allego_lib import AllegoState
from radiens.lib.channel_metadata import ChannelMetadata
from radiens.lib.sig_metrics import SignalMetrics, SignalMetricsStatus
from radiens.lib.spike_sorter import Dashboard, SorterState
from radiens.lib.spikes import SpikesMetadata, SpikesSet
from radiens.utils.constants import (DEFAULT_STIM_PARAMS, HEADSTAGE_ALIAS,
                                     PRIMARY_CACHE_STREAM_GROUP_ID,
                                     PROBE_ALIAS, SPIKE_SORTER_ID)
from radiens.utils.enums import (ClientType, DioMode, Port, RecordMode,
                                 StreamMode, SystemMode, WorkspaceApp)
from radiens.utils.util import new_server_channel

# ====== life cycle ======


def restart(addr, mode: SystemMode):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            stub.Restart(allegoserver_pb2.RestartRequest(
                mode=mode.enum))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)

# ====== workspace ======


def workspace_save(addr, is_force_overwrite=True, tags='', notes=''):
    annotate = common_pb2.AnnotateBundle(tags=tags, notes=notes)
    req = common_pb2.WorkspaceControlRequest(cmd=common_pb2.WSPACE_Save,
                                             annotation=annotate, isForceOverwrite=is_force_overwrite)
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            stub.WorkspaceControl(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)


def workspace_save_as(addr, wspace_id: str, is_force_overwrite=True, tags='', notes=''):
    annotate = common_pb2.AnnotateBundle(tags=tags, notes=notes)
    req = common_pb2.WorkspaceControlRequest(cmd=common_pb2.WSPACE_Save,
                                             workspaceID=wspace_id,
                                             annotation=annotate, isForceOverwrite=is_force_overwrite)
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            stub.WorkspaceControl(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)


def workspace_switch(addr, wspace_id: str):
    req = common_pb2.WorkspaceControlRequest(cmd=common_pb2.WSPACE_Switch,
                                             workspaceID=wspace_id)
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            stub.WorkspaceControl(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)


def workspace_delete(addr, wspace_id: str):
    req = common_pb2.WorkspaceControlRequest(cmd=common_pb2.WSPACE_Delete,
                                             workspaceID=wspace_id)
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            stub.WorkspaceControl(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)


def workspace_current(addr):
    req = common_pb2.GetWorkspaceRequest(
        cmd=common_pb2.GET_WSPACE_Current, appMask=common_pb2.Allego)
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            resp = stub.GetWorkspace(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)
        d = {'ID': [], 'app': [], 'last_used': [], 'last_modified': [],
             'is_modified': [], 'notes': [], 'tags': []}
        for _, v in resp.workspaceDesc.items():
            d['ID'].append(v.iD)
            d['app'].append(WorkspaceApp.parse(v.app).name)
            d['last_used'].append(v.timestampLastUsed)
            d['last_modified'].append(v.timestampModified)
            d['is_modified'].append(v.isModified)
            d['tags'].append(v.annotation.tags)
            d['notes'].append(v.annotation.notes)
        return pd.DataFrame(d)


def workspace_list(addr):
    req = common_pb2.GetWorkspaceRequest(
        cmd=common_pb2.GET_WSPACE_List, appMask=common_pb2.Allego)
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            resp = stub.GetWorkspace(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)
        d = {'ID': [], 'app': [], 'last_used': [], 'last_modified': [],
             'is_modified': [], 'notes': [], 'tags': []}
        for _, v in resp.workspaceDesc.items():
            d['ID'].append(v.iD)
            d['app'].append(WorkspaceApp.parse(v.app).name)
            d['last_used'].append(v.timestampLastUsed)
            d['last_modified'].append(v.timestampModified)
            d['is_modified'].append(v.isModified)
            d['tags'].append(v.annotation.tags)
            d['notes'].append(v.annotation.notes)
        return pd.DataFrame(d)

# ====== getters ======


def get_stream_loop_dur_ms(addr) -> float:
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            res = stub.GetConfig(common_pb2.StandardRequest())
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)
        return res.streamLoopDurMs


def get_sensors(addr):
    req = common_pb2.SignalGroupIDRequest()
    req.streamGroupId = PRIMARY_CACHE_STREAM_GROUP_ID
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            res = stub.ListSensorSpecs(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)
        hstages = {}
        for _, v in enumerate(res.headstages):
            hstages[v.name.strip('hstg__')] = v.channelCount
        probes = {}
        for _, v in enumerate(res.probes):
            probes[v.name.strip('probe__')] = v.channelCount
        return {'headstages': hstages, 'probes': probes}


def get_cfg_status(addr):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            res = stub.GetConfigAndStatus(common_pb2.StandardRequest())
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)
        return AllegoState(res)


def get_signal_group(addr, stream_group_id=None):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            req = common_pb2.SignalGroupIDRequest()
            req.streamGroupId = stream_group_id

            raw = stub.GetSignalGroup(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)
        return ChannelMetadata(raw)


def get_signals(addr, stream_group_id: str, samp_freq: float):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.Pcache1Stub(chan)
        req = common_pb2.GetSignalsRequest(streamGroupId=stream_group_id)
        req.params.wdwSec = 1  # no resampling
        req.params.chanHeightPx = 0  # ain scaling hack
        req.params.ampFsrUv = sys.float_info.max  # no clipping
        req.params.plotWidthPoints = samp_freq  # no resampling
        req.params.gpioOnTop = False
        req.params.ainFsrV = 1
        req.params.componentID = 'allego_python_client'
        req.params.isHeatmap = True  # no amp scaling or offset
        req.params.clipToRange = False
        req.params.resampleType = common_pb2.ResampleRoutine.NAIVE

        try:
            raw = stub.GetSignals(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)

        sigarray = np.frombuffer(raw.data, dtype=np.float32)
        sigarray = np.reshape(sigarray, (raw.shape[0], raw.shape[1]))
        time_range = [raw.timeRange[0], raw.timeRange[1]]

        return sigarray, time_range


def get_digital_out_states(addr):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            res = stub.GetDIOReg(common_pb2.StandardRequest())
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)
        else:
            return {
                'digital_outs_mode': DioMode.parse(res.mode).name,
                'states': [{'chan_idx': i.ntvChanIdx, 'state': i.manualState} for i in res.doutChanRegisters]
            }


def get_dac_register(addr):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            res = stub.GetDACReg(common_pb2.StandardRequest())
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)
        ch = []
        for chan in res.analogOutChannels:
            ch.append({'amp_ntv_chan_idx': chan.PriNtvChanIdx,
                       'aout_ntv_chan_idx': chan.AnalogOutNtvChanIdx,
                       'stream': chan.Stream,
                       'stream_offset_idx': chan.StreamOffsetIdx})
        return {
            'dac': ch,
            'gain': res.gain,
            'high_pass': {'enable': res.highpassReg.enable,
                          'cutoff_freq': res.highpassReg.cutoffFreq}}


def get_stim_params(addr):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            resp = stub.GetStimParams(common_pb2.StandardRequest())
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)
    return parse_stim_param_resp(resp)

# ======= setters ========


def set_dac_high_pass(addr, enable: bool, cutoff_freq: float):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            stub.SetDACHighPass(allegoserver_pb2.DACHighPassRegister(enable=enable,
                                                                     cutoffFreq=cutoff_freq))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)
        return get_dac_register(addr)


def set_digital_out_manual(addr, dout1_state: bool, dout2_state: bool):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)

        req1 = allegoserver_pb2.DIOModeManualRequest()
        req1.chanIdx = 0
        req1.state = dout1_state

        req2 = allegoserver_pb2.DIOModeManualRequest()
        req2.chanIdx = 1
        req2.state = dout2_state

        try:
            stub.SetDIOManual(req1)
            stub.SetDIOManual(req2)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)


def set_fs(addr, fs: int):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            stub.SetConfigCore(
                allegoserver_pb2.SetConfigCoreRequest(sampFreq=float(fs)))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)


def set_sensor(addr, port: Port, hstage: str, probe: str):
    status = get_cfg_status(addr)
    if port not in status.port_num_channels:
        raise ValueError(
            'port {} is not valid or is connected'.format(port.name))

    sensors = get_sensors(addr)
    if hstage in HEADSTAGE_ALIAS.keys():
        pb_hstage = 'hstg__{}'.format(HEADSTAGE_ALIAS[hstage])
    elif hstage in sensors['headstages'].keys():
        pb_hstage = 'hstg__{}'.format(hstage)
    else:
        raise ValueError(
            'headstage {} is not an alias nor an available headstage ID'.format(hstage))

    if probe in PROBE_ALIAS.keys():
        pb_probe = 'probe__{}'.format(PROBE_ALIAS[probe])
    elif probe in sensors['probes'].keys():
        pb_probe = 'probe__{}'.format(probe)
    else:
        raise ValueError(
            'probe {} is not an alias nor an available probe ID'.format(hstage))

    hstg_num_chan = sensors['headstages'][pb_hstage.strip('hstg__')]
    probe_num_chan = sensors['probes'][pb_probe.strip('probe__')]
    if status.port_num_channels[port] != hstg_num_chan:
        warnings.warn('port {} number of channels={} does not match headstage number of channels={}'.format(
                      port.name, status.port_num_channels[port], hstg_num_chan))
    if hstg_num_chan != probe_num_chan:
        warnings.warn('headstage {} number of channels={} does not match probe number of channels={}'.format(
                      sensors['headstages'][pb_hstage.strip('hstg__')], hstg_num_chan, probe_num_chan))

    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            stub.SetSensor(common_pb2.SetSensorRequest(streamGroupId=PRIMARY_CACHE_STREAM_GROUP_ID,
                                                       port=port.enum, headstageId=pb_hstage, probeId=pb_probe))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)


def set_manual_stim_trigger(addr, trigger: int):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            stub.ManualStimTriggerToggle(allegoserver_pb2.ManualStimTriggerToggleRequest(
                trigger=trigger))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)


def set_stim_step(addr, stim_step_enum: int):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            stub.SetStimStep(allegoserver_pb2.StimStepMessage(
                stimStep=stim_step_enum))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)


def set_stim_params(addr, stim_params_req: dict):
    with new_server_channel(addr) as chan:
        if 'stim_sys_chan_idx' not in stim_params_req:
            raise KeyError(
                "Required key stim_sys_chan_idx not found in request.")
        stim_sys_chan_idx = stim_params_req['stim_sys_chan_idx']

        curr_params = None
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            curr_params_raw = stub.GetStimParams(common_pb2.StandardRequest())
            curr_params = parse_stim_param_resp(curr_params_raw)
        except grpc.RpcError as ex:
            warnings.warn(
                "can't retrieve any current stim parameters. Continuing with assuming defaults for parameters unspecified in request")

        curr_chan_params = None
        if curr_params is None or curr_params == {}:
            curr_chan_params = DEFAULT_STIM_PARAMS
        else:
            curr_chan_params = curr_params[stim_sys_chan_idx]

        for param, val in curr_chan_params.items():
            if param not in stim_params_req:
                stim_params_req[param] = val

        req = stim_params_dict_to_req(stim_params_req)
        try:
            stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
            stub.SetStimParams(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)


def set_stream_state(addr, state: StreamMode):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            stub.SetStreamState(
                allegoserver_pb2.SetStreamRequest(mode=state.pb_value))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)


def set_record_state(addr, state: RecordMode):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            stub.SetRecordState(
                allegoserver_pb2.SetRecordRequest(mode=state.pb_value))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)


def set_recording_config(addr, filename: str, filepath: str, index: int, time_stamp: bool):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            stub.SetConfigRecording(allegoserver_pb2.ConfigRecording(baseFileName=filename,
                                                                     baseFilePath=filepath,
                                                                     dataSourceIdx=int(
                                                                         index),
                                                                     timeStamp=time_stamp))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)


def set_time_to_cache_head(addr, stream_group_id=None):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.Pcache1Stub(chan)
        req = common_pb2.SignalGroupIDRequest()
        req.streamGroupId = stream_group_id
        try:
            stub.SetTimeRangeToHead(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)

# ==========================
# ====== KPIs ==============
# ==========================


def set_kpi_params(addr, dsource_id,  req):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.Kpi1Stub(chan)
        try:
            stub.SetKpiParam(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)


def get_kpi_status(addr):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.Kpi1Stub(chan)
        try:
            resp = stub.GetKpiStatus(common_pb2.GetKpiStatusRequest(
                streamGroupId=PRIMARY_CACHE_STREAM_GROUP_ID))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)
        return SignalMetricsStatus(resp)


def get_kpi_metrics(addr, req):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.Kpi1Stub(chan)
        try:
            resp = stub.KpiGetMetrics(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)
        return SignalMetrics(PRIMARY_CACHE_STREAM_GROUP_ID, resp)


def get_kpi_params(addr):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.Kpi1Stub(chan)
        try:
            resp = stub.GetKpiParam(datasource_pb2.DataSourceRequest(
                dsourceID=[PRIMARY_CACHE_STREAM_GROUP_ID]))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)
        p = {'ntv_idx': [], 'chan_enabled': [], 'thr_activated': [], 'thr': [], 'thr_sd': [], 'thr_wdw': [],
             'shadow': [], 'weak_thr_activated': [],  'weak_thr': [], 'weak_thr_sd': [], 'thr_wdw_pts': [], 'shadow_pts': []}
        for v in resp.rec:
            p['ntv_idx'].append(v.ntvChanIdx)
            p['chan_enabled'].append(v.isEnabled)
            p['thr_activated'].append(v.isSetThr)
            p['thr'].append(np.array(v.thr))
            p['thr_sd'].append(np.array(v.thrSd))
            p['thr_wdw'].append(np.around(np.array(v.thrWdw) * 1000.0, 5))
            p['shadow'].append(np.around(np.array(v.shadow) * 1000.0, 5))
            p['weak_thr_activated'].append(np.array(v.isSetWeakThr))
            p['weak_thr'].append(np.array(v.weakThr))
            p['weak_thr_sd'].append(np.array(v.weakThrSd))
            p['thr_wdw_pts'].append(v.thrWdwPts)
            p['shadow_pts'].append(v.shadowPts)
        return pd.DataFrame(p)

# ==========================
# ====== spike sorter ======
# ==========================


def sorter_cmd(addr, cmd):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.Neurons1Stub(chan)
        try:
            stub.SpikeSorterCommand(spikesorter_pb2.SpikeSorterCommandRequest(
                cmd=cmd, subCmd=spikesorter_pb2.SORTER_SUBCMD_NULL, spikeSorterID=''))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)


def sorter_set_params(addr, msg):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.Neurons1Stub(chan)
        try:
            stub.SpikeSorterSetParams(msg)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)


def sorter_get_params(addr):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.Neurons1Stub(chan)
        try:
            resp = stub.SpikeSorterGetParam(
                spikesorter_pb2.SpikeSorterStandardRequest(spikeSorterID=''))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)
        p = {'ntv_idx': [], 'chan_enabled': [], 'thr_activated': [], 'thr': [], 'thr_sd': [], 'thr_wdw': [],
             'shadow': [], 'weak_thr': [], 'thr_wdw_pts': [], 'shadow_pts': []}
        for v in resp.rec:
            p['ntv_idx'].append(v.ntvChanIdx)
            p['chan_enabled'].append(v.isEnabled)
            p['thr_activated'].append(v.isSetThr)
            p['thr'].append(np.array(v.thr))
            p['thr_sd'].append(np.array(v.thrSd))
            p['thr_wdw'].append(np.around(np.array(v.thrWdw) * 1000.0, 5))
            p['shadow'].append(np.around(np.array(v.shadow) * 1000.0, 5))
            p['weak_thr'].append(np.array(v.weakThr))
            p['thr_wdw_pts'].append(v.thrWdwPts)
            p['shadow_pts'].append(v.shadowPts)
        return pd.DataFrame(p)


def sorter_get_state(addr):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.Neurons1Stub(chan)
        try:
            resp = stub.SpikeSorterGetState(
                spikesorter_pb2.SpikeSorterStandardRequest(spikeSorterID=''))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)
        return SorterState(resp)


def sorter_get_raster_data(addr, msg):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.Neurons1Stub(chan)
        try:
            resp = stub.SpikeSorterGetRasterData(msg)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)

        sigarray = np.frombuffer(resp.GPIOData, dtype=np.float32)
        sigarray = np.reshape(sigarray, (resp.GPIOShape[0], resp.GPIOShape[1]))
        return {'time_range': resp.timeRange, 'timestamp_range': resp.timeStampRange,
                'spikes': {'ntv_chan_idx': resp.spikeTimestampsByChannel.ntvChanIdx,
                           'timestamps': resp.spikeTimestampsByChannel.spikeTimestamps,
                           'labels': resp.spikeTimestampsByChannellabels},
                'gpio_data': sigarray}


def sorter_get_dashboard(addr):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.Neurons1Stub(chan)
        try:
            resp = stub.SpikeSorterGetDashboard(
                spikesorter_pb2.SpikeSorterStandardRequest(spikeSorterID=''))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)
    return Dashboard(resp)


def get_spikes(addr, req):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.Neurons1Stub(chan)
        try:
            resp = stub.BiointerfaceGetSpikesDense(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)
        return SpikesSet(resp)


def get_neurons(addr, req):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.Neurons1Stub(chan)
        try:
            resp = stub.BiointerfaceGetNeurons(
                biointerface_pb2.BiointerfaceGetNeuronsRequest(req))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)
        return resp


def get_spikes_spec(addr):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.Neurons1Stub(chan)
        try:
            resp = stub.SpikesGetSpec(
                spikesorter_pb2.SpikeSorterStandardRequest(spikeSorterID=SPIKE_SORTER_ID))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, ClientType.ALLEGO)
        return SpikesMetadata(resp)
