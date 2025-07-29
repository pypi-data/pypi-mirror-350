from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
import radiens.api.api_allego as api_allego
import radiens.api.api_videre as api_videre
from radiens.grpc_radiens import common_pb2
from radiens.lib.dataset_metadata import DatasetMetadata
from radiens.lib.signals_snapshot import PSD, Signals
from radiens.utils.constants import DEFAULT_HUB_ID, SigSelect, TimeRange
from radiens.utils.enums import (FftWindow, KeyIndex, PsdScaling,
                                 RadiensService, SignalType, TrsMode)
from radiens.utils.util import (make_signal_selector, make_time_range,
                                sig_sel_to_protobuf, time_range_to_protobuf)

# the following lines are to avoid circular imports and are only used for typing hints
# (TYPE_CHECKING always evaluates to false at runtime)
if TYPE_CHECKING:
    from radiens.videre_client import VidereClient


class SignalsClient:
    """
    Signals client object for Allego, Curate, and Videre
    """

    def __init__(self, parent_client: VidereClient):
        """
        """
        if not parent_client.type.is_videre():
            raise ValueError(
                "signals_client: parent_client must be a VidereClient")
        self.__parent: VidereClient = parent_client

    def get_signals(self,
                    time_range: TimeRange | list[float] | np.ndarray = None,
                    sel_mode: TrsMode = None,
                    sig_sel: SigSelect = None,
                    sig_type: SignalType | str = None,
                    ntv_idxs: list[int] | str = None,
                    dataset_metadata: DatasetMetadata = None,
                    hub_name=DEFAULT_HUB_ID) -> Signals:
        """
        Gets signals over the specified time range from a linked dataset.

        Parameters:
            time_range (TimeRange): see :py:meth:`~radiens.utils.util.make_time_range`
            dataset_metadata: see :py:meth:`link_data_file` and :py:meth:`get_data_file_metadata`
            sel_mode (TrsMode): time range selection mode (optional, default :py:attr:`TrsMode.SUBSET`)
            sig_sel (SigSelect): see :py:meth:`~radiens.utils.util.make_signal_selector` (optional)
            sig_type: signal type — one of "amp", "ain", "din", "dout" (optional)
            ntv_idxs: channel indices of `sig_type` to return. (optional, default "all")
            hub_name: (optional)


        Returns:
            signals (Signals)
        """
        if dataset_metadata is None:
            raise ValueError('videre: dataset_metadata must be provided')
        if time_range is None:
            warnings.warn(
                f'no requested time range, using dataset time range {dataset_metadata.TR.sec} (s) ')
            time_range = dataset_metadata.TR
        if not isinstance(time_range, TimeRange):
            if not isinstance(time_range, (list, np.ndarray)):
                raise ValueError(
                    'time_range must be a TimeRange, list, or numpy array')
            time_range = make_time_range(
                time_range=time_range, fs=dataset_metadata.TR.fs)
        if sel_mode is None:
            sel_mode = TrsMode.SUBSET
        if sig_sel is None:
            if sig_type is not None:
                sig_sel = make_signal_selector(
                    **{sig_type: "all" if ntv_idxs is None else ntv_idxs})
            else:
                sig_sel = SigSelect(key_idx=KeyIndex.NTV,
                                    amp=np.array(dataset_metadata.channel_metadata.index(
                                        SignalType.AMP).ntv, dtype=np.int64),
                                    gpio_ain=np.array(dataset_metadata.channel_metadata.index(
                                        SignalType.AIN).ntv, dtype=np.int64),
                                    gpio_din=np.array(dataset_metadata.channel_metadata.index(
                                        SignalType.DIN).ntv, dtype=np.int64),
                                    gpio_dout=np.array(dataset_metadata.channel_metadata.index(
                                        SignalType.DOUT).ntv, dtype=np.int64),
                                    )
        elif sig_sel.key_idx != KeyIndex.NTV:
            raise ValueError("sig_sel must use KeyIndex.NTV as the key index")

        sig_sel_proto = sig_sel_to_protobuf(sig_sel)
        req = common_pb2.HDSnapshotRequest2(
            dsourceID=dataset_metadata.id,
            selMode=sel_mode.value,
            sigSel=sig_sel_proto,
            tR=time_range_to_protobuf(time_range)
        )

        return api_videre.get_signals(
            self.__parent._server_address(hub_name, RadiensService.CORE), req)

    def get_psd(
        self,
        time_range: TimeRange | list[float] | np.ndarray = None,
        sel_mode: TrsMode = None,
        sig_sel: SigSelect = None,
        samp_freq: float = 2000.0,
        freq_range: list | np.ndarray = [1, 300],
        collapse_freq: bool = False,
        scaling: PsdScaling = PsdScaling.ABSOLUTE,
        window: FftWindow = FftWindow.HAMMING_p01,
        freq_resolution: float = None,
        file: str = None,
        dataset_metadata: DatasetMetadata = None,
        hub_name=DEFAULT_HUB_ID,
    ) -> PSD:
        """
        Gets the power spectral density (PSD) for the specified signals over the specified time range.

        Parameters:
            time_range (TimeRange) : requested time range in seconds (required)
            sel_mode (TrsMode): time range selection mode (optional, default=TrsMode.SUBSET)
            sig_sel (SigSelect): requested AMP signals (optional, default=all AMP signals)
            samp_freq (float): PSD sample frequency in Hz. (optional, default=dataset_metadata.TR.fs)
            freq_range (list, np.ndarray): requested frequency range.  (optional, default=[1, 300])
            collapse_freq (bool): True collapses `freq_range` into one frequency bin (optional, default=False)
            scaling (PsdScaling): sets the PSD scale (optional, default=PsdScaling.ABSOLUTE)
            window (FftWindow): sets the FFT window(optional, default=FftWindow.HAMMING_p01)
            freq_resolution (float): requested frequency resolution in Hz (optional, default=None)
            file (string): save psd data to file (optional, default=None)
            dataset_metadata (DatasetMetadata): dataset metadata (required for Videre, optional for Allego, default=None)
            hub_name (str): Radiens hub name (optional, default=DEFAULT_HUB)


        Returns:
            psd (PSD): container object for PSD data.
        """
        if dataset_metadata is None:
            raise ValueError('videre: dataset_metadata must be provided')
        if time_range is None:
            warnings.warn(
                f'no requested time range, using dataset time range {dataset_metadata.TR.sec} (s) ')
            time_range = dataset_metadata.TR
        if not isinstance(time_range, TimeRange):
            time_range = make_time_range(
                time_range=time_range, fs=dataset_metadata.TR.fs)
        if sel_mode is None:
            sel_mode = TrsMode.SUBSET
        if sig_sel is None:
            sig_sel = SigSelect(key_idx=KeyIndex.NTV,
                                amp=np.array(dataset_metadata.channel_metadata.index(
                                    SignalType.AMP).ntv, dtype=np.int64),
                                gpio_ain=np.array(dataset_metadata.channel_metadata.index(
                                    SignalType.AIN).ntv, dtype=np.int64),
                                gpio_din=np.array(dataset_metadata.channel_metadata.index(
                                    SignalType.DIN).ntv, dtype=np.int64),
                                gpio_dout=np.array(dataset_metadata.channel_metadata.index(
                                    SignalType.DOUT).ntv, dtype=np.int64),
                                )
        elif sig_sel.key_idx != KeyIndex.NTV:
            raise ValueError("sig_sel must use KeyIndex.NTV as the key index")

        samp_freq = time_range.fs if samp_freq is None else samp_freq

        req = common_pb2.PSDRequest(
            tR=time_range_to_protobuf(time_range),
            selMode=int(sel_mode.value),
            ntvIdxs=sig_sel.amp,
            stype=SignalType.AMP.value,
            resampleFs=samp_freq,
            wdwType=window.value,
            scaling=scaling.value,
            freqRange=freq_range,
            deltaFreq=freq_resolution,
            collapseFreq=collapse_freq,
            path=file,
            isReturnPSD=True,
            dsourceID=dataset_metadata.id,
        )
        out = api_videre.get_psd(
            self.__parent._server_address(
                hub_name, RadiensService.CORE), req
        )
        if file is not None:
            out.save(file)

        return out
