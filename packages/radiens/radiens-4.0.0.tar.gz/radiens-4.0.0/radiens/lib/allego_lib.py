from collections import namedtuple
from pathlib import Path
from pprint import pprint
from typing import Dict

import pandas as pd
from radiens.grpc_radiens import allegoserver_pb2, common_pb2, datasource_pb2
from radiens.lib.dataset_metadata import FileSetDescriptor
from radiens.utils.enums import Port, SystemMode

PORT_SPEC = namedtuple("PortSpec", ['port_num_chans', 'probe_name', 'probe_num_sites',
                                    'headstage_name', 'headstage_num_chans'])

STREAMING_SPEC = namedtuple(
    "StreamSpec", ['mode', 'time_range', 'hw_mem_level'])

RECORDING_SPEC = namedtuple("RecordingSpec", ['mode', 'file_name', 'dur_sec', 'error',
                                              'path', 'base_name', 'index', 'timestamp'])
GPIO_SPEC = namedtuple("GPIOSpec", ['ain', 'din', 'dout'])

STATUS_SPEC = namedtuple("StatusSpec", ['streaming', 'recording', 'ports',
                                        'connected', 'gpio', 'sample_freq', 'mode'])


class AllegoState():
    '''
    Container for Allego state.
    '''

    def __init__(self, raw=allegoserver_pb2.ConfigAndStatus):
        self._stream = STREAMING_SPEC(mode=allegoserver_pb2.StreamMode.Name(raw.streaming.streamMode),
                                      time_range=raw.streaming.primaryCacheTRange,
                                      hw_mem_level=raw.streaming.hardwareMemoryLevel)
        _path = str(
            Path(raw.recording.activeFileName).expanduser().absolute().parent)
        _base_name = Path(Path(raw.recording.activeFileName)).stem
        _idx = -1
        _tstamp = ''
        if '__uid' in _base_name and len(_base_name) > _base_name.index('__uid')+6:
            uid_idx = _base_name.index('__uid')
            _tstamp = _base_name[uid_idx+5:]
            _idx_idx = _base_name[:uid_idx].rfind('_')
            if _idx_idx > 0:
                _idx = int(_base_name[_idx_idx+1:uid_idx])
                _base_name = _base_name[:_idx_idx]
        elif '_' in _base_name:
            _idx_idx = _base_name.rfind('_')
            if _idx_idx > 0 and len(_base_name) > _idx_idx+1:
                try:
                    _idx = int(_base_name[_idx_idx+1:])
                except ValueError:
                    _idx = -1
                else:
                    _base_name = _base_name[:_idx_idx]
        self._recording = RECORDING_SPEC(mode=allegoserver_pb2.RecordMode.Name(raw.recording.recordMode),
                                         file_name=raw.recording.activeFileName,
                                         dur_sec=raw.recording.duration,
                                         error=raw.recording.error,
                                         base_name=_base_name,
                                         index=_idx,
                                         timestamp=_tstamp,
                                         path=_path)
        self._port_spec = {}
        for k, port in enumerate(raw.ports):
            self._port_spec[Port.parse(port.port)] = port.channelCount
        self._is_connected = raw.isConnected
        self._gpio_spec = GPIO_SPEC(
            ain=raw.gpioChannelCount.nAux, din=raw.gpioChannelCount.nDin, dout=raw.gpioChannelCount.nDout)
        self._fs = raw.baseSampFreq
        self._cable_lengths = {p: None for p in Port.all()}
        self._cable_delay_specs = {p: None for p in Port.all()}
        for p in Port.all():
            try:
                self._cable_lengths[p] = eval(
                    'raw.cableLengths.{}'.format(p.name))
            except:
                self._cable_lengths[p] = None
        for k, v in raw.cableDelays.cableDelays.items():
            self._cable_delay_specs[Port.parse(k)] = {
                'delay': v.cableDelay,
                'is_auto': v.isAuto,
            }

        self._backbone_mode = SystemMode.parse(raw.backboneMode)

    @property
    def sample_freq(self) -> float:
        """
        Current system sample frequency in samples/sec [Hz]
        """
        return self._fs

    @property
    def system_mode(self) -> SystemMode:
        """
        Current Allego mode, e.g. 'sim-spikes', etc.
        """
        return self._backbone_mode

    @property
    def port_num_channels(self) -> Dict[Port, int]:
        """
        Number of channels on each connected port.
        """
        return self._port_spec

    @property
    def cable_delay_spec(self) -> Dict[Port, dict]:
        """
        Cable delay specification for each system port
        """
        return self._cable_delay_specs

    @property
    def cable_length_ft(self) -> Dict[Port, int]:
        """
        Headstage cable length in feet for each system port
        """
        return self._cable_lengths

    @property
    def recording(self) -> RECORDING_SPEC:
        """
        Recording status
        """
        return self._recording

    @property
    def stream(self) -> STREAMING_SPEC:
        """
        Streaming status
        """
        return self._stream

    @property
    def connected(self) -> bool:
        """
        Returns true if there is a headstage connected on any channel.
        """
        return self._is_connected

    @property
    def base_name(self) -> str:
        """
        Returns true if there is a headstage connected on any channel.
        """

    def print(self, detail: str = 'brief'):
        if detail not in ['brief', 'verbose']:
            raise ValueError('detail must be [`brief`, `verbose`]')
        print('ALLEGO status:')
        if self.connected in [False]:
            print('not connected')
            return
        if detail in ['brief', 'verbose']:
            print('stream       : {}'.format(self.stream.mode))
            print('  time range : [0.000, {:.3f}] sec'.format(
                self.stream.time_range[1]))
            print('  HW memory  : {} '.format(self.stream.hw_mem_level))
            print('recording         : {}'.format(self.recording.mode))
            print('  duration        : {:.3f} sec'.format(
                self.recording.dur_sec))
            print('  file name       : {}'.format(
                Path(self.recording.file_name).stem))
            print('  base name       : {}'.format(self.recording.base_name))
            print('  path            : {}'.format(self.recording.path))
            print('  index           : {}'.format(self.recording.index))
            print('  file timestamp  : {}'.format(self.recording.timestamp))
        if detail in ['verbose']:
            print('settings   ')
            print('  sample freq   : {:.0f}'.format(self.sample_freq))
            print('  port channels : {}'.format(
                Port.map_into_keys_as_names(self.port_num_channels)))
            print('  cable lengths : {}'.format(
                Port.map_into_keys_as_names(self.cable_length_ft)))
