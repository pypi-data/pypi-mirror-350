from __future__ import annotations

import datetime
import warnings
from collections import namedtuple
from pathlib import Path

import numpy as np
import pandas as pd
from radiens.api.api_utils.util import (to_matrix_from_protobuf_dense_matrix,
                                        to_matrix_from_protobuf_radix_matrix)
from radiens.grpc_radiens import common_pb2
from radiens.lib.channel_metadata import ChannelMetadata
from radiens.lib.dataset_metadata import DatasetMetadata
from radiens.utils.constants import SignalArrays, TimeRange
from radiens.utils.enums import FftWindow, PsdScaling, SignalType, SignalUnits
from radiens.utils.util import (equal_key_idxs, generic_repr,
                                is_concatable_trs, make_time_range,
                                time_range_from_protobuf)


class Signals():
    '''
    Container for a multi-channel (multi-trace) dataset for amplifier, GPIO analog in, GPIO digital in, and GPIO digital out signals. 

    All traces for all signal types have the same sampling frequency and start and end times.  Thus, the set of traces of each signal type is a 2-D matrix.  
    '''

    def __init__(self, raw: common_pb2.HDSnapshot2):
        """
        """
        if not isinstance(raw, common_pb2.HDSnapshot2):
            raise TypeError('raw must be common_pb2.HDSnapshot2')
        self._d = {'dsource_id': raw.dsourceID}
        self._sgrp = ChannelMetadata(raw.sigs.sG)
        self._tr = time_range_from_protobuf(raw.sigs.tR)
        self._sigs = SignalArrays(amp=to_matrix_from_protobuf_radix_matrix(raw.sigs.amp),
                                  gpio_ain=to_matrix_from_protobuf_radix_matrix(
            raw.sigs.ain),
            gpio_din=to_matrix_from_protobuf_radix_matrix(
            raw.sigs.din),
            gpio_dout=to_matrix_from_protobuf_radix_matrix(raw.sigs.dout))

    def __repr__(self) -> str:
        return generic_repr(self)

    @ property
    def time_range(self) -> TimeRange:
        """
        dataset time range in seconds
        """
        return self._tr

    @ property
    def TR(self) -> TimeRange:
        """
        Aliases dataset time range.
        """
        return self._tr

    @ property
    def signals(self) -> SignalArrays:
        """
        Time-series signals as a named tuple by signal type.  

        For each signal type, the multi-channel dataset is a 2-D numpy array, with dim 0=trace position and dim 1 is the sample values over the time range. 
        """
        return self._sigs

    @ property
    def attributes(self) -> dict:
        """
        Dataset attributes
        """
        return self._d

    @ property
    def channel_metadata(self) -> ChannelMetadata:
        """
        Dataset channel metadata 
        """
        return self._sgrp

    def concat(self, other: Signals) -> None:
        """
        Concatenate two Signals objects into a single Signals object. 

        Args:
            other: Signals object to concatenate with self. 

        Returns:
            Signals: concatenated Signals object. 
        """

        # check inputs
        if not isinstance(other, Signals):
            raise TypeError('other must be Signals')
        if not is_concatable_trs([self._tr, other._tr]):
            raise ValueError(
                f'time ranges are not able to be concatenated: {self._tr} and {other._tr}')
        for stype in SignalType.all():
            if not equal_key_idxs([self._sgrp.index(stype), other._sgrp.index(stype)]):
                raise ValueError(
                    f'channel metadata for {stype} is not compatible')

        # concatenate signals
        amp = np.concatenate((self._sigs.amp, other._sigs.amp), axis=1)
        gpio_ain = np.concatenate(
            (self._sigs.gpio_ain, other._sigs.gpio_ain), axis=1)
        gpio_din = np.concatenate(
            (self._sigs.gpio_din, other._sigs.gpio_din), axis=1)
        gpio_dout = np.concatenate(
            (self._sigs.gpio_dout, other._sigs.gpio_dout), axis=1)

        # get total time range in samples
        timestamp_range = [self._tr.timestamp[0], other._tr.timestamp[1]]

        # update self with concatenated signals
        self._tr = make_time_range(timestamp=timestamp_range, fs=self._tr.fs)
        self._sigs = SignalArrays(amp=amp, gpio_ain=gpio_ain,
                                  gpio_din=gpio_din, gpio_dout=gpio_dout)


class PSD():
    '''
    Container for a multi-channel (multi-trace) power spectrum density (PSD) dataset. 
    '''

    def __init__(self, raw: common_pb2.PSD | str | Path, dataset_metadata: DatasetMetadata = None):
        """
        """
        if isinstance(raw, common_pb2.PSD):
            self._load_from_raw(raw)
        elif isinstance(raw, (str, Path)):
            if dataset_metadata is None:
                raise ValueError(
                    'videre: dataset_metadata must be provided to load from file')
            self._load_from_file(
                Path(raw).expanduser().resolve(), dataset_metadata)

    def __repr__(self) -> str:
        return generic_repr(self)

    def _load_from_file(self, file: Path, dataset_metadata: DatasetMetadata):
        """
        """
        if file.suffix != '.npz':
            if file.suffix != '':
                warnings.warn(
                    f'file extension {file.suffix} will be replaced with .npz')

            file = file.with_suffix('.npz')
        if not file.exists():
            raise FileNotFoundError(f'file not found: {file}')
        if file.suffix != '.npz':
            raise ValueError(
                f'file must have a .npz extension, found {file.suffix}')
        with np.load(file) as data:
            _id = str(data['dsource_id'])
            _tr = make_time_range(
                timestamp=data['time_range_ts'], fs=dataset_metadata.TR.fs)
            _psd = np.array(data['psd'], dtype=np.float64)
            _freq = np.array(data['freq'], dtype=np.float64)
            _freq_range = np.array(data['freq_range'], dtype=np.float64)
            _freq_bin_width = float(data['freq_bin_width'])

            if _id != dataset_metadata.id:
                raise ValueError(
                    f'dsource_id in file {data["dsource_id"]} does not match dataset_metadata.id {dataset_metadata.id}')
            if _freq.size != _psd.shape[1]:
                raise ValueError(
                    f'freq array size {_freq.size} does not match psd shape {_psd.shape[1]}')
            if _freq_range.size != 2:
                raise ValueError(
                    f'freq_range array size {_freq_range.size} must be 2')
            if _freq_range[0] > _freq[0] or _freq_range[1] < _freq[-1]:
                raise ValueError(
                    f'freq_range {data["freq_range"]} does not match freqs')

            self._d = {
                'dsource_id': _id,
                'wdw_type': FftWindow.parse(int(data['wdw_type'])),
                'scaling': PsdScaling.parse(int(data['scaling'])),
                'freq_bin_width': _freq_bin_width,
            }
            self._sgrp = dataset_metadata.channel_metadata
            self._tr = _tr
            self._psd = _psd
            self._freq = _freq
            self._freq_range = _freq_range

    def _load_from_raw(self, raw: common_pb2.PSD):
        """
        """
        self._d = {'dsource_id': raw.dsourceID, 'wdw_type': FftWindow(raw.wdwType),
                   'scaling': PsdScaling(raw.scaling), 'freq_bin_width': raw.freqBinWidth}
        self._sgrp = ChannelMetadata(raw.sG)
        self._tr = time_range_from_protobuf(raw.tR)
        self._psd = to_matrix_from_protobuf_dense_matrix(raw.psd)
        self._freq = np.array(raw.freq, dtype=np.float64)
        self._freq_range = np.array(raw.freqRange, dtype=np.float64)

    @ property
    def time_range(self) -> TimeRange:
        """
        dataset time range in seconds.
        """
        return self._tr

    @property
    def units(self) -> dict[SignalType, str]:
        """
        Signal units
        """

        out = {}
        for (stype, units) in self._sgrp.sig_units.items():
            out[stype] = _to_psd_units(units, self.scaling)

        return out

    @property
    def TR(self) -> TimeRange:
        """
        Aliases dataset time range.
        """
        return self._tr

    @property
    def psd(self) -> np.ndarray:
        """
        Power spectral density   

        """
        return self._psd

    @property
    def window_type(self) -> FftWindow:
        """
        PSD window type
        """
        return self._d['wdw_type']

    @property
    def scaling(self) -> PsdScaling:
        """
        PSD scaling
        """
        return self._d['scaling']

    @ property
    def frequencies(self) -> np.ndarray:
        """
        PSD frequencies

        """
        return self._freq

    @ property
    def freq_range(self) -> np.ndarray:
        """
        PSD frequency range as [freq start, obj.frequencies[-1]+obj.freq_bin_width) in Hz.

        """
        return self._freq_range

    @ property
    def freq_bin_width(self) -> float:
        """
        PSD frequency bin width in Hz 

        """
        return self._d['freq_bin_width']

    @ property
    def attributes(self) -> dict:
        """
        Dataset attributes
        """
        return self._d

    @ property
    def channel_metadata(self) -> ChannelMetadata:
        """
        Dataset channel metadata 
        """
        return self._sgrp

    @property
    def dsource_id(self) -> str:
        """
        Data source ID
        """
        return self._d['dsource_id']

    def save(self, file: str | Path) -> None:
        """
        Save PSD data to file. 

        Args:
            file: file path to save PSD data. The file will be saved with a .npz extension.
        """

        file = Path(file).expanduser().resolve()

        if file.suffix != '.npz':
            if file.suffix != '':
                warnings.warn(
                    f'file extension {file.suffix} will be replaced with .npz')

            file = file.with_suffix('.npz')

        np.savez(
            file,
            psd=self._psd,
            freq=self._freq,
            freq_range=self._freq_range,
            freq_bin_width=self.freq_bin_width,
            dsource_id=self.dsource_id,
            wdw_type=self.window_type.value,
            scaling=self.scaling.value,
            time_range_sec=np.array(self._tr.sec),
            time_range_ts=np.array(self._tr.timestamp),
        )

    @staticmethod
    def load(file: str | Path, dataset_metadata: DatasetMetadata) -> PSD:
        """
        Load PSD data from file. 

        Args:
            file: file path to load PSD data. The file must have a .npz extension.
            dataset_metadata: dataset metadata for the PSD data. 

        Returns:
            PSD: PSD object
        """

        return PSD(Path(file).expanduser().resolve(), dataset_metadata)


def _to_psd_units(units: SignalUnits, scaling: PsdScaling) -> str:
    if scaling == PsdScaling.ABSOLUTE:
        return str(units) + '²/Hz'
    else:
        raise NotImplementedError(
            'only absolute scaling is supported, found {scaling}'
        )
