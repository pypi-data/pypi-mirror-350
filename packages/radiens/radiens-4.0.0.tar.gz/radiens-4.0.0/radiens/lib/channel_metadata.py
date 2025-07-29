from collections import namedtuple

import numpy as np
import pandas as pd
from radiens.grpc_radiens import common_pb2
from radiens.utils.constants import KeyIdxs
from radiens.utils.enums import Port, SignalType, SignalUnits


def _parse_sig_units(sig_units) -> dict:
    parsed = {}
    for (sig_type_enum, sig_unit_enum) in sig_units.units.items():
        parsed[SignalType.parse(sig_type_enum)
               ] = SignalUnits.parse(sig_unit_enum)
    return parsed


class ChannelMetadata():
    '''
    Container for channel metadata.
    '''

    def __init__(self, raw: common_pb2.SignalGroup = None):
        """

        """
        self._d = {'dataset_uid': '', 'fs': 0.0, 'source_label': '',
                   'neighbor_max_radius_um': 0.0, 'signal_units': {}, 'has_discrete': False}
        if raw is not None:
            self._d = {'dataset_uid': raw.datasetUID, 'fs': raw.sampFreq, 'source_label': raw.sourceLabel,
                       'neighbor_max_radius_um': raw.neighborMaxRadius, 'signal_units': _parse_sig_units(raw.signalUnits), 'has_discrete': raw.hasDiscrete, 'has_continuous_amp': raw.hasContinuousAmp}

        self._df, self._sensor_spec = decode_grpc_message(raw)
        _df_amp = self._df[self._df['chan_type'] == SignalType.AMP]
        _df_ain = self._df[self._df['chan_type'] == SignalType.AIN]
        _df_din = self._df[self._df['chan_type'] == SignalType.DIN]
        _df_dout = self._df[self._df['chan_type'] == SignalType.DOUT]
        self._sig_map = {SignalType.AMP:
                         KeyIdxs(ntv=_df_amp['ntv_key_idx'].to_list(),
                                 dset=_df_amp['dataset_key_idx'].to_list(),
                                 sys=_df_amp['sys_key_idx'].to_list()),
                         SignalType.AIN: KeyIdxs(ntv=_df_ain['ntv_key_idx'].to_list(),
                                                 dset=_df_ain['dataset_key_idx'].to_list(
                         ),
                             sys=_df_ain['sys_key_idx'].to_list()),
                         SignalType.DIN: KeyIdxs(ntv=_df_din['ntv_key_idx'].to_list(),
                                                 dset=_df_din['dataset_key_idx'].to_list(
                         ),
                             sys=_df_din['sys_key_idx'].to_list()),
                         SignalType.DOUT: KeyIdxs(ntv=_df_dout['ntv_key_idx'].to_list(),
                                                  dset=_df_dout['dataset_key_idx'].to_list(
                         ),
                             sys=_df_dout['sys_key_idx'].to_list()),
                         }
        self._sel_sig_map = {SignalType.AMP:
                             KeyIdxs(ntv=_df_amp[_df_amp['selected'] == True]['ntv_key_idx'].to_list(),
                                     dset=_df_amp[_df_amp['selected'] ==
                                                  True]['dataset_key_idx'].to_list(),
                                     sys=_df_amp[_df_amp['selected'] == True]['sys_key_idx'].to_list()),
                             SignalType.AIN: KeyIdxs(ntv=_df_ain[_df_ain['selected'] == True]['ntv_key_idx'].to_list(),
                                                     dset=_df_ain[_df_ain['selected'] == True]['dataset_key_idx'].to_list(
                             ),
                                 sys=_df_ain[_df_ain['selected'] == True]['sys_key_idx'].to_list()),
                             SignalType.DIN: KeyIdxs(ntv=_df_din[_df_din['selected'] == True]['ntv_key_idx'].to_list(),
                                                     dset=_df_din[_df_din['selected'] == True]['dataset_key_idx'].to_list(
                             ),
                                 sys=_df_din[_df_din['selected'] == True]['sys_key_idx'].to_list()),
                             SignalType.DOUT: KeyIdxs(ntv=_df_dout[_df_dout['selected'] == True]['ntv_key_idx'].to_list(),
                                                      dset=_df_dout[_df_dout['selected'] == True]['dataset_key_idx'].to_list(
                             ),
                                 sys=_df_dout[_df_dout['selected'] == True]['sys_key_idx'].to_list()),
                             }
        self._num_sigs = {}
        self._sel_num_sigs = {}
        for stype in SignalType.all():
            self._num_sigs[stype] = len(self._sig_map[stype].ntv)
            self._sel_num_sigs[stype] = len(self._sel_sig_map[stype].ntv)

    def __repr__(self) -> str:
        return self.table.__repr__()

    @property
    def table(self) -> pd.DataFrame:
        """
        Table containing per-channel metadata, with one row per channel.
 
        Returns
        -------
        pd.DataFrame
            Each row describes one channel. Column identifiers are as follows:
 
            - port (:obj:`str`)  
                - Port label from acquisition hardware
 
            - chan_name (:obj:`str`)  
                - Channel name
 
            - chan_type (:class:`~radiens.utils.enums.SignalType`)  
                - Signal type
 
            - sys_key_idx (:obj:`int`)  
                - Immutable absolute index of channel assigned at time of recording
 
            - ntv_key_idx (:obj:`int`)  
                - Immutable relative (to signal type) channel index of the channel assigned at time of recording
 
            - dataset_key_idx (:obj:`int`)  
                - Dataset channel index relative to signal type
 
            - dataset_key_idx_abs (:obj:`int`)  
                - Absolute channel index 
 
            - site_num (:obj:`int`)  
                - Site identifier on the probe
 
            - color_group_idx (:obj:`int`)  
                - Internal color group index used for visualization
 
            - selected (:obj:`bool`)  
                - Whether the channel is selected
 
            - audio (:obj:`list[bool]`)  
                - List of two booleans indicating left and right audio channels ([is_audio_left, is_audio_right])
 
            - site_shape (:obj:`str`)  
                - Geometric descriptor of the site
 
            - site_ctr_x/y/z (:obj:`float`)  
                - Coordinates of the site center relative to the sensor
 
            - site_lim_x/y/z_[min/max] (:obj:`float`)  
                - Site bounding box limits
 
            - site_ctr_tcs_x/y/z (:obj:`float`)  
                - Site center in tissue coordinate system (TCS)
 
            - sensor_units (:class:`~radiens.utils.enums.SignalUnits`)  
                - Physical units of the signal
 
            - site_area_um2 (:obj:`float`)  
                - Area of the site in µm²
 
            - scs_to_tcs (:obj:`float`)  
                - Offset from sensor to tissue coordinate system
 
            - sensor_id (:obj:`str`)  
                - Full sensor identifier
 
            - probe_id (:obj:`str`)  
                - Identifier for the probe
 
            - headstage_id (:obj:`str`)  
                - Identifier for the headstage
 
            - ntv_chan_name (:obj:`str`)  
                - Native channel name from hardware
 
            - sensor_uid (:obj:`str`)  
                - Unique sensor identifier
        """
        return self._df

    @ property
    def attributes(self) -> dict:
        """
        Dictionary of attributes
        """
        return self._d

    def site_positions(self, stype: SignalType) -> dict:
        self._d['']

    def index(self, stype: SignalType) -> KeyIdxs:
        """
        Signal indices by signal type and index type. All indices are zero-indexed.

        Parameters:
            stype (~radiens.utils.enums.SignalType): Signal type

        Returns:
            KeyIdxs (~radiens.utils.constants.KeyIdxs): Key index object with keys `ntv`, `dset`, `sys`

        See Also:
            :py:class:`~radiens.utils.enums.KeyIndex`


        Examples:
            >>> meta.index(SignalType.AMP)
            >>> KeyIdxs(ntv=[5,1,23,46], dset=[0,1,2,3], sys=[5,1,23,46])
            >>> meta.index(SignalType.AIN)
            >>> KeyIdxs(ntv=[3,2,0,1], dset=[0,1,2,3], sys=[35,34,32,33])  # signal has 32 AMP channels

        See Also:
            :py:class:`~radiens.utils.enums.KeyIndex`
            :py:class:`~radiens.utils.enums.SignalType`
        """
        if stype not in self._sig_map:
            raise ValueError('stype not in signal map')
        return self._sig_map[stype]

    def sel_index(self, stype: SignalType) -> KeyIdxs:
        """
        Selected signal indices by signal type and index type.

        Parameters:
            stype (~radiens.utils.enums.SignalType): Signal type


       See Also:
            :py:class:`~radiens.utils.enums.KeyIndex`
        """
        if stype not in self._sig_map:
            raise ValueError('stype not in signal map')
        return self._sel_sig_map[stype]

    def num_sigs(self, stype: SignalType) -> int:
        """
        Number of signals for the requested signal type.  
        """
        if stype not in self._num_sigs:
            raise ValueError('stype not in signal map')
        return self._num_sigs[stype]

    def sel_num_sigs(self, stype: SignalType) -> int:
        """
        Number of selected signals for the requested signal type.  
        """
        if stype not in self._num_sigs:
            raise ValueError('stype not in signal map')
        return self._sel_num_sigs[stype]

    def num_sigs_total(self) -> int:
        """
        Total number of signals 
        """
        n = 0
        for stype in SignalType.all():
            n = n + self._num_sigs[stype]
        return n

    @ property
    def num_selected_sigs_total(self) -> int:
        """
        Total number of signals 
        """
        n = 0
        for stype in SignalType.all():
            n = n + self._sel_num_sigs[stype]
        return n

    @property
    def sig_units(self) -> dict[SignalType, SignalUnits]:
        """
        Dictionary of signal units
        """
        return self._d['signal_units']

    @ property
    def sensor_spec(self) -> dict:
        """
        Dict with ports (str) as keys mapping to dicts describing headstage, site, and probe wireframe metadata
        """
        return self._sensor_spec


def decode_grpc_message(raw_grpc):
    chan_name = []
    chan_type = []
    ntv_key_idx = []
    dataset_key_idx = []
    site_num = []
    color_group_idx = []
    selected = []
    audio = []
    port = []
    site_shape = []
    site_ctr_x = []
    site_ctr_y = []
    site_ctr_z = []
    site_lim_x_min = []
    site_lim_y_min = []
    site_lim_z_min = []
    site_lim_x_max = []
    site_lim_y_max = []
    site_lim_z_max = []
    site_ctr_tcs_x = []
    site_ctr_tcs_y = []
    site_ctr_tcs_z = []
    sensor_units = []
    sys_key_idx = []
    site_area_um2 = []
    scs_to_tcs = []
    sensor_id = []
    probe_id = []
    headstage_id = []
    dataset_key_idx_abs = []
    ntv_chan_name = []
    sensor_uid = []
    if raw_grpc is not None:
        for row in raw_grpc.channels:
            chan_name.append(row.chanName)
            chan_type.append(SignalType(row.chanType))
            ntv_key_idx.append(row.ntvChanIdx)

            dataset_key_idx.append(row.datasetRidx)

            site_num.append(row.siteNum)
            color_group_idx.append(row.colorGroupIdx)
            selected.append(row.isSelected)
            audio.append([row.isAudioLeft, row.isAudioRight])
            port.append(Port._from_enum(row.port).name)
            site_shape.append(row.siteShape)
            site_ctr_x.append(row.siteCtrX)
            site_ctr_y.append(row.siteCtrY)
            site_ctr_z.append(row.siteCtrZ)
            site_lim_x_min.append(row.siteLimXMin)
            site_lim_y_min.append(row.siteLimYMin)
            site_lim_z_min.append(row.siteLimZMin)
            site_lim_x_max.append(row.siteLimXMax)
            site_lim_y_max.append(row.siteLimYMax)
            site_lim_z_max.append(row.siteLimZMax)
            site_ctr_tcs_x.append(row.siteCtrTcsX)
            site_ctr_tcs_y.append(row.siteCtrTcsY)
            site_ctr_tcs_z.append(row.siteCtrTcsZ)
            sensor_units.append(row.sensorUnits)
            sys_key_idx.append(row.absIdx)

            site_area_um2.append(row.siteAreaMicron2)
            scs_to_tcs.append([row.scsToTcsX, row.scsToTcsY, row.scsToTcsZ])
            sensor_id.append(row.sensorID)
            probe_id.append(row.probeID)
            headstage_id.append(row.headstageID)
            dataset_key_idx_abs.append(row.datasetAidx)
            ntv_chan_name.append(row.ntvChanName)
            sensor_uid.append(row.sensorUID)

    _df = pd.DataFrame({'port': port,
                        'chan_name': chan_name,
                        'chan_type': chan_type,
                        'ntv_key_idx': ntv_key_idx,
                        'site_num': site_num,
                        'color_group_idx': color_group_idx,
                        'selected': selected,
                        'audio': audio,
                        'site_shape': site_shape,
                        'site_ctr_x': site_ctr_x,
                        'site_ctr_y': site_ctr_y,
                        'site_ctr_z': site_ctr_z,
                        'site_lim_x_min': site_lim_x_min,
                        'site_lim_y_min': site_lim_y_min,
                        'site_lim_z_min': site_lim_z_min,
                        'site_lim_x_max': site_lim_x_max,
                        'site_lim_y_max': site_lim_y_max,
                        'site_lim_z_max': site_lim_z_max,
                        'site_ctr_tcs_x': site_ctr_tcs_x,
                        'site_ctr_tcs_y': site_ctr_tcs_y,
                        'site_ctr_tcs_z': site_ctr_tcs_z,
                        'sensor_units': sensor_units,
                        'sys_key_idx': sys_key_idx,
                        'site_area_um2': site_area_um2,
                        'scs_to_tcs': scs_to_tcs,
                        'sensor_id': sensor_id,
                        'probe_id': probe_id,
                        'headstage_id': headstage_id,
                        'ntv_chan_name': ntv_chan_name,
                        'sensor_uid': sensor_uid,
                        'dataset_key_idx': dataset_key_idx,
                        'dataset_key_idx_abs': dataset_key_idx_abs,
                        }).reset_index(drop=True)
    _df.index.name = 'dyn_sort_idx'

    sensor_port_spec = {}
    for port in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
        sensor_port_spec[port] = []
    if raw_grpc is not None:
        for m, _ in enumerate(raw_grpc.sensorPortSpec.sensorA):
            sensor_port_spec['A'].append(decode_grpc_sensor_port_spec(
                raw_grpc.sensorPortSpec.sensorA[m]))
        for m, _ in enumerate(raw_grpc.sensorPortSpec.sensorB):
            sensor_port_spec['B'].append(decode_grpc_sensor_port_spec(
                raw_grpc.sensorPortSpec.sensorB[m]))
        for m, _ in enumerate(raw_grpc.sensorPortSpec.sensorC):
            sensor_port_spec['C'].append(decode_grpc_sensor_port_spec(
                raw_grpc.sensorPortSpec.sensorC[m]))
        for m, _ in enumerate(raw_grpc.sensorPortSpec.sensorD):
            sensor_port_spec['D'].append(decode_grpc_sensor_port_spec(
                raw_grpc.sensorPortSpec.sensorD[m]))
        for m, _ in enumerate(raw_grpc.sensorPortSpec.sensorE):
            sensor_port_spec['E'].append(decode_grpc_sensor_port_spec(
                raw_grpc.sensorPortSpec.sensorE[m]))
        for m, _ in enumerate(raw_grpc.sensorPortSpec.sensorF):
            sensor_port_spec['F'].append(decode_grpc_sensor_port_spec(
                raw_grpc.sensorPortSpec.sensorF[m]))
        for m, _ in enumerate(raw_grpc.sensorPortSpec.sensorG):
            sensor_port_spec['G'].append(decode_grpc_sensor_port_spec(
                raw_grpc.sensorPortSpec.sensorG[m]))
        for m, _ in enumerate(raw_grpc.sensorPortSpec.sensorH):
            sensor_port_spec['H'].append(decode_grpc_sensor_port_spec(
                raw_grpc.sensorPortSpec.sensorH[m]))

    return _df, sensor_port_spec


def decode_grpc_sensor_port_spec(grpc_sensor):
    d = {'probe_id': grpc_sensor.probeId,
         'headstage_id': grpc_sensor.headstageId,
         'sensor_uid': '',
         'x_min': grpc_sensor.xMin,
         'x_max': grpc_sensor.xMax,
         'y_min': grpc_sensor.yMin,
         'y_max': grpc_sensor.yMax,
         'wireframe_x': [],
         'wireframe_y': [],
         'wireframe_vtx_x_lim': 0,
         'wireframe_vtx_y_lim': 0,
         'sensor_pos': {'x': 0, 'y': 0, 'z': 0, 'ring_angle': 0, 'axial_angle': 0, 'arc_angle': 0}}
    for pt in grpc_sensor.wireframe.vtx:
        d['wireframe_x'].append(pt.x)
        d['wireframe_y'].append(pt.y)
    d['sensor_uid'] = grpc_sensor.sensorUID if grpc_sensor.sensorUID is not None else d['sensor_uid']
    d['wireframe_vtx_x_lim'] = grpc_sensor.wireframe.vtxXlim if grpc_sensor.wireframe.vtxXlim is not None else d['wireframe_vtx_x_lim']
    d['wireframe_vtx_y_lim'] = grpc_sensor.wireframe.vtxYlim if grpc_sensor.wireframe.vtxYlim is not None else d['wireframe_vtx_y_lim']

    if grpc_sensor.position is not None:
        d['sensor_pos']['x'] = grpc_sensor.position.X
        d['sensor_pos']['y'] = grpc_sensor.position.Y
        d['sensor_pos']['z'] = grpc_sensor.position.Z
        d['sensor_pos']['ring_angle'] = grpc_sensor.position.RingAngle
        d['sensor_pos']['axial_angle'] = grpc_sensor.position.AxialAngle
        d['sensor_pos']['arc_angle'] = grpc_sensor.position.ArcAngle
    return d

