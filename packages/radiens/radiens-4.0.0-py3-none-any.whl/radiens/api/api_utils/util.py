import os
import socket
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Union

import grpc
import numpy as np
import pandas as pd
import radiens.utils.util as util
from radiens.grpc_radiens import allegoserver_pb2, common_pb2
from radiens.utils.constants import DEFAULT_HUB_ID, DEFAULT_IP
from radiens.utils.enums import RadiensFileType, RadiensService


def parse_stim_param_resp(resp: allegoserver_pb2.StimParamsReply):
    resp_dict = dict()
    for stim_sys_chan_idx, params in resp.params.items():
        resp_dict[stim_sys_chan_idx] = {}
        resp_dict[stim_sys_chan_idx]['stim_shape'] = params.stimShape
        resp_dict[stim_sys_chan_idx]['stim_polarity'] = params.stimPolarity
        resp_dict[stim_sys_chan_idx]['first_phase_duration_us'] = params.firstPhaseDuration
        resp_dict[stim_sys_chan_idx]['second_phase_duration_us'] = params.secondPhaseDuration
        resp_dict[stim_sys_chan_idx]['interphase_delay_us'] = params.interphaseDelay
        resp_dict[stim_sys_chan_idx]['first_phase_amplitude_uA'] = params.firstPhaseAmplitude
        resp_dict[stim_sys_chan_idx]['second_phase_amplitude_uA'] = params.secondPhaseAmplitude
        resp_dict[stim_sys_chan_idx]['baseline_voltage'] = params.baselineVoltage
        resp_dict[stim_sys_chan_idx]['trigger_edge_or_level'] = params.triggerEdgeOrLevel
        resp_dict[stim_sys_chan_idx]['trigger_high_or_low'] = params.triggerHighOrLow
        resp_dict[stim_sys_chan_idx]['enabled'] = params.enabled
        resp_dict[stim_sys_chan_idx]['post_trigger_delay_us'] = params.postTriggerDelay
        resp_dict[stim_sys_chan_idx]['pulse_or_train'] = params.pulseOrTrain
        resp_dict[stim_sys_chan_idx]['number_of_stim_pulses'] = params.numberOfStimPulses
        resp_dict[stim_sys_chan_idx]['pulse_train_period_us'] = params.pulseTrainPeriod
        resp_dict[stim_sys_chan_idx]['refactory_period_ms'] = params.refractoryPeriod
        resp_dict[stim_sys_chan_idx]['pre_stim_amp_settle_us'] = params.preStimAmpSettle
        resp_dict[stim_sys_chan_idx]['post_stim_amp_settle_us'] = params.postStimAmpSettle
        resp_dict[stim_sys_chan_idx]['maintain_amp_settle_us'] = params.maintainAmpSettle
        resp_dict[stim_sys_chan_idx]['enable_amp_settle'] = params.enableAmpSettle
        resp_dict[stim_sys_chan_idx]['post_stim_charge_recovery_on_us'] = params.postStimChargeRecovOn
        resp_dict[stim_sys_chan_idx]['post_stim_charge_recovery_off_us'] = params.postStimChargeRecovOff
        resp_dict[stim_sys_chan_idx]['enable_charge_recovery'] = params.enableChargeRecovery
        resp_dict[stim_sys_chan_idx]['trigger_source_is_keypress'] = params.triggerSourceIsKeypress
        resp_dict[stim_sys_chan_idx]['trigger_source_idx'] = params.triggerSourceIdx
        resp_dict[stim_sys_chan_idx]['stim_sys_chan_idx'] = params.stimSysChanIdx

    return resp_dict


def stim_params_dict_to_req(req_dict: dict):
    return allegoserver_pb2.StimParams(
        baselineVoltage=req_dict['baseline_voltage'],
        firstPhaseDuration=req_dict['first_phase_duration_us'],
        enabled=req_dict['enabled'],
        enableAmpSettle=req_dict['enable_amp_settle'],
        enableChargeRecovery=req_dict['enable_charge_recovery'],
        firstPhaseAmplitude=req_dict['first_phase_amplitude_uA'],
        interphaseDelay=req_dict['interphase_delay_us'],
        maintainAmpSettle=req_dict['maintain_amp_settle_us'],
        numberOfStimPulses=req_dict['number_of_stim_pulses'],
        postStimAmpSettle=req_dict['post_stim_amp_settle_us'],
        postStimChargeRecovOff=req_dict['post_stim_charge_recovery_off_us'],
        postStimChargeRecovOn=req_dict['post_stim_charge_recovery_on_us'],
        postTriggerDelay=req_dict['post_trigger_delay_us'],
        preStimAmpSettle=req_dict['pre_stim_amp_settle_us'],
        pulseOrTrain=req_dict['pulse_or_train'],
        pulseTrainPeriod=req_dict['pulse_train_period_us'],
        refractoryPeriod=req_dict['refactory_period_ms'],
        secondPhaseAmplitude=req_dict['second_phase_amplitude_uA'],
        secondPhaseDuration=req_dict['second_phase_duration_us'],
        stimPolarity=req_dict['stim_polarity'],
        stimShape=req_dict['stim_shape'],
        stimSysChanIdx=req_dict['stim_sys_chan_idx'],
        triggerEdgeOrLevel=req_dict['trigger_edge_or_level'],
        triggerHighOrLow=req_dict['trigger_high_or_low'],
        triggerSourceIsKeypress=req_dict['trigger_source_is_keypress'],
        triggerSourceIdx=req_dict['trigger_source_idx'],
    )


def to_radiens_file_type(p: str | Path) -> RadiensFileType:
    p = Path(p)
    ext = p.suffix.lower()
    if ext in ['.rhd']:
        return RadiensFileType(common_pb2.RHD)
    if ext in ['.xdat', '']:
        return RadiensFileType(common_pb2.XDAT)
    if ext in ['.csv']:
        return RadiensFileType(common_pb2.CSV)
    if ext in ['.hdf5', '.h5']:
        return RadiensFileType(common_pb2.HDF5)
    if ext in ['.nex5']:
        return RadiensFileType(common_pb2.NEX5)
    if ext in ['.nwb']:
        return RadiensFileType(common_pb2.NWB)
    if ext in ['.kilosort2', '.bin']:
        return RadiensFileType(common_pb2.KILOSORT2)
    if ext in ['.nsx']:
        return RadiensFileType(common_pb2.NSX)
    if ext in ['.tdt']:
        return RadiensFileType(common_pb2.TDT)
    if ext in ['.spikes']:
        return RadiensFileType(common_pb2.SPIKES)
    if ext in ['.oebin', '.oe_dat']:
        return RadiensFileType(common_pb2.OE_DAT)
    raise ValueError('{} is invalid or unknown file extension'.format(ext))


def ext_to_radiens_file_type(ext: str):
    return to_radiens_file_type(Path('file.' + ext))


def to_suffix(file_type: RadiensFileType) -> str:
    if file_type == RadiensFileType.RHD:
        return ".rhd"
    elif file_type == RadiensFileType.XDAT:
        return ".xdat"
    elif file_type == RadiensFileType.CSV:
        return ".csv"
    elif file_type == RadiensFileType.HDF5:
        return ".h5"
    elif file_type == RadiensFileType.NEX5:
        return ".nex5"
    elif file_type == RadiensFileType.NWB:
        return ".nwb"
    elif file_type == RadiensFileType.KILOSORT2:
        return ".bin"
    elif file_type == RadiensFileType.NSX:
        return ".nsx"
    elif file_type == RadiensFileType.TDT:
        return ".tdt"
    elif file_type == RadiensFileType.SPIKES:
        return ".spikes"
    elif file_type == RadiensFileType.OE_DAT:
        return ".oebin"
    else:
        raise ValueError(
            f"Invalid {RadiensFileType.__name__} value: {file_type}")


def to_file_ext(file_type: common_pb2.RadixFileTypes):
    return common_pb2.RadixFileTypes.Name(file_type).lower()


def path_to_source_sink_transform(p: Path) -> common_pb2.DataSourceSinkTransformParams:
    return common_pb2.DataSourceSinkTransformParams(dsrcName=p.expanduser().resolve().stem, path=str(p.expanduser().resolve().parent), fileType=to_radiens_file_type(p).value)


def source_sink_transform_to_path(pb_node: common_pb2.DataSourceSinkTransformParams) -> Path:
    return Path(pb_node.datasourceSinkParams.path, pb_node.datasourceSinkParams.dsrcName +
                '.{}'.format(to_file_ext(pb_node.datasourceSinkParams.fileType)))


def to_matrix_from_protobuf_radix_matrix(arg: common_pb2.RadixMatrixBytes) -> np.ndarray:
    return np.reshape(np.frombuffer(arg.data, dtype=np.float32), (arg.shape[0], arg.shape[1])).astype(np.float64)


def to_matrix_from_protobuf_dense_matrix(arg: common_pb2.DenseMatrix) -> np.ndarray:
    return np.reshape(np.frombuffer(arg.data, dtype=np.float64), (arg.rows, arg.cols)).astype(np.float64)


class BaseClient:
    """
    """

    def __init__(self):
        self._client_id = ''  # '_-_'+str(uuid.uuid4())[4:13]
        self._base_hubs = {DEFAULT_HUB_ID: {
            'ip_address': DEFAULT_IP,
            'ports': util.get_radiens_port_dict(),
        }}

    def _server_address(self, hub_id, service: RadiensService):
        # creates server address from hub and service
        try:
            return '{}:{}'.format(self._hubs()[hub_id]['ip_address'], self._hubs()[hub_id]['ports'][service])
        except KeyError:
            raise AssertionError(
                'invalid service name = {}'.format(service.name))

    def _hubs(self) -> dict:
        return self._base_hubs

    def _id(self) -> str:
        return self._client_id


def get_dataset_id(
        df_avail: pd.DataFrame,
        self_id: str,
        hub: str,
        dataset_idx: int = None,
        dataset_id: str = None,
        path: Union[Path, str] = None,
        fail_hard: bool = False) -> any:
    if dataset_idx is None and dataset_id is None:
        if isinstance(path, (str, Path)):
            try:
                return df_avail.loc[df_avail['dataset ID'] == Path(path).stem + self_id]['dataset ID'].values[0], Path(path)
            except Exception:
                if fail_hard:
                    raise ValueError(
                        '{} is not a linked data file on hub {}'.format(Path(path), hub))
                print('no op, {} is not a linked data file on hub {}'.format(
                    Path(path), hub))
                return None, None
        else:
            raise ValueError(
                'path must be a string or Path when dataset_idx and dataset_id are both None')
    if dataset_idx is not None:
        try:
            return df_avail.loc[[int(dataset_idx)]]['dataset ID'].values[0], None
        except Exception as ex:
            if fail_hard:
                raise ValueError(
                    '{} is not an available dataset index on hub {}'.format(dataset_idx, hub))
            print('no op, {} is not an available dataset index on hub {}'.format(
                dataset_idx, hub))
            return None, None
    if dataset_id is not None:
        try:
            return df_avail.loc[df_avail['dataset ID'] == dataset_id]['dataset ID'].values[0], None
        except Exception as ex:
            if fail_hard:
                raise ValueError(
                    'no op, {} is not an available dataset ID on hub {}'.format(dataset_id, hub))
            print('no op, {} is not an available dataset ID on hub {}'.format(
                dataset_id, hub))
            return None, None
    raise ValueError(
        'dataset index, dataset ID, and path arguments are all invalid')


def get_dataset_idx_from_id(df_avail: pd.DataFrame, dataset_id: str) -> str:
    return df_avail.loc[df_avail['dataset ID'] == dataset_id]['index'].values[0]


def scan_for_open_port() -> int:
    host = "localhost"
    host_ip = socket.gethostbyname(host)
    for port in range(50000, 65535):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host_ip, port))
        except socket.error:
            return port
        else:
            s.close()
    return None


def launch_server() -> int:
    port = scan_for_open_port()
    this_path = Path(os.path.realpath(__file__))
    server_file = Path(this_path.parent, '..', 'api_server.py').resolve()
    if port is None:
        raise RuntimeError('did not find open port')
    try:
        subprocess.Popen([sys.executable, str(
            server_file), str(port)], shell=True)
    except subprocess.OSError:
        raise RuntimeError('failed to start radiens-py process')
    return 'localhost:{}'.format(port)


def server_start_script() -> int:
    return str(Path(Path(os.path.realpath(__file__)).parent, '..', 'api_server.py').resolve())
