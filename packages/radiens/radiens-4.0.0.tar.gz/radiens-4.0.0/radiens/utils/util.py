import datetime
import os
import re
import subprocess
from pathlib import Path
from sys import platform
from typing import Dict, List, Union

import grpc
import numpy as np
import pandas as pd
import radiens.utils.constants as constants
from radiens.exceptions.scan_for_server_error import (PIDParsingError,
                                                      PortParsingError,
                                                      UnexpectedTCPFormat)
from radiens.grpc_radiens import (biointerface_pb2, common_pb2,
                                  radiensserver_pb2, radiensserver_pb2_grpc)
from radiens.utils.constants import (ALL_SITES, BYTES_PER_SAMPLE,
                                     SELECTED_SITES, TIME_SPEC, KeyIdxs,
                                     NeighborsDesc, NeuronDesc,
                                     NeuronExtendedMetadata, SigSelect,
                                     SitePosition, TimeRange)
from radiens.utils.enums import KeyIndex, RadiensService
from radiens.utils.interceptors import (MetadataClientInterceptor,
                                        SessionMetaData)


def time_now():
    return datetime.datetime.now().strftime(TIME_SPEC)


def file_types(category='all'):
    '''
    File extensions for supported Radiens file types. 

    Parameters:
        category (str): optional, requested file category: 'all', 'recording', 'spikes', default='all'

    Returns:
        ext (list): list of requested category file extensions.

    Example:
        >>> file_types("recording")
        ['rhd', 'xdat', 'csv', 'hdf5', 'h5', 'nwb', 'kilosort2', 'nsx', 'pl2', 'tdt']

    '''
    rec = ['rhd', 'xdat', 'csv', 'hdf5', 'h5',
           'nwb', 'kilosort2', 'nsx', 'pl2', 'tdt']
    spikes = ['spikes']
    if category in ['recording']:
        return rec
    if category in ['spikes']:
        return spikes
    if category in ['all']:
        rec.extend(spikes)
        return rec
    raise ValueError("category must be 'rec', 'spikes', 'all'")


def is_xdat_file(p: Path) -> bool:
    return Path(p.parent, p.stem+'_data.xdat').expanduser().resolve().is_file()


def rm_xdat_file(p: Path) -> None:
    if not is_xdat_file(p):
        return
    Path(p.parent, p.stem+'_data.xdat').expanduser().resolve().unlink()
    Path(p.parent, p.stem+'_timestamp.xdat').expanduser().resolve().unlink()
    Path(p.parent, p.stem+'.xdat.json').expanduser().resolve().unlink()


def make_site_pos(probe, tissue):
    return SitePosition(probe_x=probe[0], probe_y=probe[1], probe_z=probe[2],
                        tissue_x=tissue[0], tissue_y=tissue[1], tissue_z=tissue[2])


def make_time_range(time_range: Union[list, np.ndarray] = None, timestamp: Union[list, np.ndarray] = None, fs: float = None, walltime: datetime.datetime = None, pbTR: common_pb2.TimeRange = None):
    '''
    Utility function to compose the TimeRange named tuple composed from either a time range or timestamp list. 

    Parameters:
        time_range (list | numpy.ndarray): time range in seconds as [time start, time end] (optional, default=None). 
        timestamp (list | numpy.ndarray): timestamp in seconds as [timestamp start, timestamp end]  (optional, default=None). 
        fs (float): sampling frequency in samples/sec (required, default=None)
        walltime (datetime.datetime): wall time of the time range start.
        pbTR : low-level system parameter not available to user.

    Notes:

    TimeRange named tuple fields: 
        `sec` (numpy.ndarray): [time start, time end]
        `timestamp` (numpy.ndarray): [timestamp start, timestamp end]
        `fs` (float): sampling frequency
        `walltime`: wall time of the time range start
        `dur_sec` (float): imputed time range duration equal to `TR.time_range[1]`-`TR.time_range[0]`.
        `N` (int): imputednumber of sample points equal to `TR.timestamp[1]`-`TR.timestamp[0]`.

    Either `timestamp` or `time_range` must be provided, with `timestamp` having preference. 
    `walltime` is optional.  `dur_sec` and `N` are imputed from the arguments. 

    System use only (not available to user)
    Either `pbTR` or (`fs` and either `time_range` or `timestamp`) must be provided as arguments. 
    `pbTR` has preference.  
    '''
    if isinstance(pbTR, common_pb2.TimeRange):
        return time_range_from_protobuf(pbTR)
    if fs in [None]:
        raise ValueError('missing fs')
    if walltime in [None]:
        walltime = datetime.datetime.min
    if isinstance(timestamp, (list, np.ndarray)):
        ts = np.array(timestamp).astype(np.int64)
        tr = np.array([ts[0]/fs, ts[1]/fs], dtype=np.float64)
    elif isinstance(time_range, (list, np.ndarray)):
        tr = np.array(time_range, dtype=np.float64)
        ts = np.array([tr[0]*fs, tr[1]*fs]).astype(np.int64)
    else:
        raise ValueError('missing both time_range and timestamp arg')
    return TimeRange(sec=tr, timestamp=ts, fs=fs, walltime=walltime, N=ts[1]-ts[0], dur_sec=tr[1]-tr[0])


def time_range_to_protobuf(tr: TimeRange) -> common_pb2.TimeRange:
    if not isinstance(tr, TimeRange):
        raise ValueError('argument must be a TimeRange')
    if len(tr.timestamp) != 2:
        raise ValueError('argument timestamp field does not have len=2')
    pbTR = common_pb2.TimeRange(timestamp=tr.timestamp.tolist(), fs=tr.fs)
    pbTimestamp = common_pb2.google_dot_protobuf_dot_timestamp__pb2.Timestamp()
    pbTimestamp.FromDatetime(tr.walltime)
    pbTR.wallTime.CopyFrom(pbTimestamp)
    return pbTR


def is_protobuf_time_range_empty(pbTR: common_pb2.TimeRange) -> bool:
    if pbTR.fs == 0 or (len(pbTR.timestamp) == 0 and len(pbTR.timeRangeSec) == 0):
        return True
    return False


def time_range_from_protobuf(pbTR: common_pb2.TimeRange) -> TimeRange:
    if not isinstance(pbTR, common_pb2.TimeRange):
        raise ValueError('argument must be a common_pb2.TimeRange')
    if pbTR.timestamp not in [None] and len(pbTR.timestamp) == 2:
        ts = np.array(pbTR.timestamp).astype(np.int64)
        tr = np.array([ts[0]/pbTR.fs, ts[1]/pbTR.fs], dtype=np.float64)
    elif pbTR.timeRangeSec not in [None] and len(pbTR.timeRangeSec) == 2:
        tr = np.array(pbTR.timeRangeSec).astype(np.float64)
        ts = np.array([tr[0]*pbTR.fs, tr[1]*pbTR.fs], dtype=np.int64)
    else:
        raise ValueError('unexpected pbTR = {}'.format(pbTR))
    if pbTR.wallTime not in [None]:
        wt = pbTR.wallTime.ToDatetime()
        if wt.year == 0:
            wt = datetime.datetime.min
    else:
        wt = datetime.datetime.min
    return make_time_range(timestamp=ts, fs=pbTR.fs, walltime=wt)


def sig_sel_to_protobuf(sig_sel: SigSelect) -> common_pb2.SigSelector:
    if not isinstance(sig_sel, SigSelect):
        raise ValueError('argument must be a SigSelect')
    if sig_sel.key_idx not in [KeyIndex.NTV]:
        raise ValueError('sig_sel must use KeyIndex.NTV as the key index')
    return common_pb2.SigSelector(ampNtvIdxs=sig_sel.amp.tolist(),
                                  ainNtvIdxs=sig_sel.gpio_ain.tolist(),
                                  dinNtvIdxs=sig_sel.gpio_din.tolist(),
                                  doutNtvIdxs=sig_sel.gpio_dout.tolist())


def _parse_ntv_idxs(ntv_idxs: Union[list[int], np.array, str] = None) -> np.array:
    if ntv_idxs is None:
        return np.array([], dtype=np.int64)
    if isinstance(ntv_idxs, str):
        if ntv_idxs == "all":
            return np.array([ALL_SITES], dtype=np.int64)
        if ntv_idxs == "sel":
            return np.array([SELECTED_SITES], dtype=np.int64)
        raise Exception(f"Invalid site selection {ntv_idxs}")
    return np.array(ntv_idxs, dtype=np.int64)


def make_signal_selector(
        amp: Union[list, np.array, str] = None,
        ain: Union[list, np.array, str] = None,
        din: Union[list, np.array, str] = None,
        dout: Union[list, np.array, str] = None,
) -> SigSelect:
    return SigSelect(
        amp=_parse_ntv_idxs(amp),
        gpio_ain=_parse_ntv_idxs(ain),
        gpio_din=_parse_ntv_idxs(din),
        gpio_dout=_parse_ntv_idxs(dout),
        key_idx=KeyIndex.NTV,
    )


def make_neighbors_desc(nbr: biointerface_pb2.NeighborDescriptor):
    if not isinstance(nbr, biointerface_pb2.NeighborDescriptor):
        raise ValueError('arg must be pb.NeighborDescriptor')
    return NeighborsDesc(radius_um=nbr.radius, ntv_idxs=nbr.ntvChanIdx, distance_um=nbr.distance, theta_deg=nbr.thetaDeg,
                         phi_deg=nbr.phiDeg, N=nbr.num, pos=make_site_pos(nbr.SiteCenterUm, nbr.SiteCenterTcsUm))


def make_neuron_desc(msg: biointerface_pb2.NeuronDescriptor):
    if not isinstance(msg, biointerface_pb2.NeuronDescriptor):
        raise ValueError('arg must be pb.NeuronDescriptor')
    return NeuronDesc(id=msg.neuronID, ntv_idx=msg.siteNtvChanIdx, label=msg.spikeLabel,
                      pos=make_site_pos(msg.posProbe, msg.posTissue), spike_count=msg.spikeCount,
                      spike_rate=msg.spikeRate, mean_abs_peak_waveform=msg.meanAbsPeakWfm, snr=msg.snr,
                      metadata=NeuronExtendedMetadata(neuron_uid=msg.metaData.neuronCatalogUID,
                                                      ensemble_uid=msg.metaData.ensembleUID,
                                                      func_assembly_uid=msg.metaData.funcAssemblyUID,
                                                      dataset_uid=msg.metaData.datasetUID,
                                                      probe_uid=msg.metaData.probeUID))


def from_dense_matrix(mtx: common_pb2.DenseMatrix) -> np.ndarray:
    return np.reshape(np.frombuffer(mtx.data, dtype=np.float64), (mtx.rows, mtx.cols))


class Histogram():
    '''
    Container for histogram data sets.
    '''

    def __init__(self, msg: common_pb2.Histogram):
        if not isinstance(msg, common_pb2.Histogram):
            raise ValueError('msg wrong type')
        self._stats = np.array(msg.stats, dtype=np.float64)
        self._counts = np.array(msg.counts, dtype=np.float64)
        self._dividers = np.array(msg.dividers, dtype=np.float64)
        self._num_bins = np.array(msg.numBins, dtype=np.int64)
        self._is_pdf = msg.numBins

    @property
    def stats(self):
        return self._stats

    @property
    def counts(self):
        return self._counts

    @property
    def dividers(self):
        return self._dividers

    @property
    def num_bins(self):
        return self._num_bins

    @property
    def scale(self):
        return 'pdf' if self._is_pdf else 'counts'


def ntv_to_dset_dict(idxs: KeyIdxs) -> dict[int, int]:
    return {n: d for n, d in zip(idxs.ntv, idxs.dset)}


def dset_to_ntv_dict(idxs: KeyIdxs) -> dict[int, int]:
    return {d: n for n, d in zip(idxs.ntv, idxs.dset)}


def generic_repr(self) -> str:
    class_name = self.__class__.__name__
    fields = [(f, type(getattr(self, f)).__name__) for f in dir(
        self) if not f.startswith('_') and not callable(getattr(self, f))]
    df = pd.DataFrame(fields, columns=['Field', 'Type'])
    df_str = df.to_string(index=False)
    header, rows = df_str.split('\n', 1)
    header_line = '-' * len(header)
    formatted_str = f'{header}\n{header_line}\n{rows}'
    return f'{class_name} with attribues: \n{formatted_str}'


def equal_key_idxs(key_idxs: list[KeyIdxs]) -> bool:
    if len(key_idxs) == 0:
        return False
    ntv = key_idxs[0].ntv
    dset = key_idxs[0].dset
    sys = key_idxs[0].sys
    for k in key_idxs[1:]:
        if k.ntv != ntv or k.dset != dset or k.sys != sys:
            return False
    return True


def is_concatable_trs(trs: list[TimeRange]) -> bool:
    """
    Checks if a list of TimeRange objects are concatable based on their fs and timestamp fields.
    """
    if len(trs) == 0:
        return False
    fs = trs[0].fs
    last_end = trs[0].timestamp[1]
    for tr in trs[1:]:
        if tr.fs != fs:
            return False
        if tr.timestamp[0] != last_end:
            return False
        last_end = tr.timestamp[1]
    return True


def time_range_chunks(tr: TimeRange, num_chunks: int) -> list[TimeRange]:
    """
    Divides a TimeRange object into a list of TimeRange objects based on the number of chunks.
    """
    if num_chunks < 1:
        raise ValueError('num_chunks must be >= 1')
    if num_chunks == 1:
        return [tr]
    total_samps = tr.timestamp[1] - tr.timestamp[0]
    num_samps_per_chunk = int(total_samps / num_chunks)
    start_read = tr.timestamp[0]
    trs = []
    for i in range(num_chunks):
        chunk_time_range = make_time_range(timestamp=[
            start_read,
            min(start_read + num_samps_per_chunk, tr.timestamp[1])
        ], fs=tr.fs)
        trs.append(chunk_time_range)
        start_read += num_samps_per_chunk
    return trs


def calc_num_chans(sig_sel: SigSelect) -> int:
    return len(sig_sel.amp) + len(sig_sel.gpio_ain) + len(sig_sel.gpio_din) + len(sig_sel.gpio_dout)


def calc_sig_size_bytes(sig_sel: SigSelect, tr: TimeRange) -> int:
    return calc_num_chans(sig_sel) * (tr.timestamp[1] - tr.timestamp[0]) * BYTES_PER_SAMPLE


def is_dev():
    if os.getenv('ALLEGO_PROD') == '1' or os.getenv("RADIENS_PROD") == '1':
        return False
    return os.getenv('RADIENS_DEV') == '1'


def is_qa():
    return os.getenv('RADIENS_QA') == '1'


def get_app_client_id():
    if is_dev() or is_qa():
        return constants.APP_CLIENT_ID_DEV
    return constants.aPP_CLIENT_ID_PROD


def get_user_app_data_dir():
    if platform in ['linux', 'linux2']:
        return Path(Path.home(), '.config', 'radiens')
    elif platform == 'darwin':
        return Path(Path.home(), 'Library', 'Application Support', 'radiens')
    elif platform == 'win32':
        return Path(Path.home(), 'AppData', 'Roaming', 'radiens')
    else:
        return None


def get_radiens_port_dict(req: List[RadiensService] | None = None) -> Dict[RadiensService, str]:
    radiens_servers = None
    if platform in ['linux', 'linux2', 'darwin']:
        radiens_servers = discover_radiens_servers_unix()
    elif platform == 'win32':
        radiens_servers = discover_radiens_servers_windows()
    else:
        return None
    _req = list(RadiensService) if req is None else req
    return extract_all_radiens_ports(radiens_servers, _req)


def extract_all_radiens_ports(server_spec: List, req: List[RadiensService]) -> Dict[str, str]:

    # port dict with all values set to None
    port_dict = dict.fromkeys(RadiensService, None)

    for addr in server_spec:
        with new_insecure_channel(addr) as chan:
            # check if core
            try:
                stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
                stub.Healthcheck(radiensserver_pb2.RadiensHealthcheckRequest())
            except:
                pass
            else:
                port_dict[RadiensService.CORE] = addr.split(':')[1]

            # check if dev1
            try:
                stub = radiensserver_pb2_grpc.RadiensDev1Stub(chan)
                stub.Healthcheck(radiensserver_pb2.RadiensHealthcheckRequest())
            except:
                pass
            else:
                port_dict[RadiensService.DEV] = addr.split(':')[1]

            # check if radiens-py
            try:
                stub = radiensserver_pb2_grpc.PyRadiens1Stub(chan)
                stub.Healthcheck(radiensserver_pb2.RadiensHealthcheckRequest())
            except:
                pass
            else:
                port_dict[RadiensService.RADIENSPY] = addr.split(':')[1]

            # check if spikesorter
            try:
                stub = radiensserver_pb2_grpc.RadiensSpikeSorter1Stub(chan)
                stub.Healthcheck(radiensserver_pb2.RadiensHealthcheckRequest())
            except:
                pass
            else:
                port_dict[RadiensService.SORTER] = addr.split(':')[1]

            # check if dash
            try:
                stub = radiensserver_pb2_grpc.DashboardsStub(chan)
                stub.Healthcheck(radiensserver_pb2.RadiensHealthcheckRequest())
            except:
                pass
            else:
                port_dict[RadiensService.DASH] = addr.split(':')[1]

    return port_dict


def discover_radiens_servers_windows():
    server_spec = []
    proc = subprocess.run(
        ['tasklist.exe', '/FI', 'IMAGENAME eq {}'.format(constants.SERVER_NAME_WINDOWS)], stdout=subprocess.PIPE)
    lines = proc.stdout.decode('utf-8').split('\n')
    for l in lines:
        if re.search(constants.SERVER_NAME_WINDOWS, l) is not None:
            try:
                pid_start, pid_end = re.search(r'\d+', l).span()
                pid = int(l[pid_start:pid_end])
            except ValueError:
                raise PIDParsingError()
            else:
                ports = get_windows_server_ports(pid)
                for port in ports:
                    server_spec.append('localhost:{}'.format(port))
    return server_spec


def get_windows_server_ports(pid):
    ports = []
    proc = subprocess.run(
        ["netstat.exe", "-a", "-o", "-n", "-p", "TCP"], stdout=subprocess.PIPE)
    lines = proc.stdout.decode('utf-8').split('\n')
    for l in lines:
        if re.search(r'LISTENING\s+{}\b'.format(pid), l) is not None:
            try:
                port_start, port_end = re.search(r':\d+', l).span()
                port = int(l[port_start+1:port_end])
            except ValueError:
                raise PortParsingError()
            else:
                ports.append(port)
    return ports


def discover_radiens_servers_unix():
    server_spec = []
    proc = subprocess.run(['lsof', '-i', '-n', '-P'], stdout=subprocess.PIPE)
    lines = proc.stdout.decode('utf-8').split('\n')
    for l in lines:
        rad_proc = re.search(r'radienss', l)
        tcp_listen = re.search(r'(LISTEN)', l)
        if rad_proc is not None and tcp_listen is not None:
            ip_start = re.search(r'TCP', l).end()+1
            port_end = tcp_listen.start()-1
            try:
                ip, port = l[ip_start:port_end].split(':')
            except ValueError:
                raise UnexpectedTCPFormat()
            else:
                ip = 'localhost' if ip == '*' else ip
                server_spec.append(':'.join([ip, port]))
    return server_spec


def is_allego_addr(addr: str) -> bool:
    port = int(addr.split(':')[-1])
    return port == constants.ALLEGO_CORE_PORT or port == constants.PCACHE_PORT or port == constants.KPI_PORT or port == constants.NEURONS1_PORT


def new_insecure_channel(ip_address):
    return grpc.insecure_channel(
        ip_address,
        options=[('grpc.max_receive_message_length', -1)]
    )


def new_server_channel(ip_address):
    chan = new_insecure_channel(ip_address)
    user = SessionMetaData()  # singleton
    user.lazy_set_auth()
    return grpc.intercept_channel(chan, MetadataClientInterceptor(user._id_token, user._hardware_uid))
