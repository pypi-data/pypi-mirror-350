from typing import TYPE_CHECKING, Union

import pandas as pd
from radiens.api import api_allego
from radiens.grpc_radiens import common_pb2, spikesorter_pb2
from radiens.lib.channel_metadata import ChannelMetadata
from radiens.lib.dataset_metadata import DatasetMetadata
from radiens.utils.constants import NEURONS1_ADDR
from radiens.utils.enums import SignalType

# the following lines are to avoid circular imports and are only used for typing hints
# (TYPE_CHECKING always evaluates to false at runtime)
if TYPE_CHECKING:
    from radiens.allego_client import AllegoClient
    from radiens.videre_client import VidereClient


class SpikeSorterClient:
    """
    Spike sorter client object for AllegoClient, VidereClient
    """

    def __init__(self, parent_client):
        """ """
        self.__parent: Union[AllegoClient, VidereClient] = parent_client

    def _is_allego(self) -> bool:
        return self.__parent.type.is_allego()

    def _is_curate(self) -> bool:
        return self.__parent.type.is_curate()

    def _is_videre(self) -> bool:
        return self.__parent.type.is_videre()

    def initialize(self):
        """
        Stops, clears, and initializes spike sorter to its default parameters.

        Returns:
            None

        Example:
            >>> client.spike_sorter().initialize()
            None

        """
        api_allego.sorter_cmd(NEURONS1_ADDR, spikesorter_pb2.SORTER_CMD_INIT)

    def rebase(self):
        """
        Rebases the spike sorter, which clears all spike data and spike templates.

        Returns:
            None

        Example:
            >>> client.spike_sorter().rebase()
            None

        """
        api_allego.sorter_cmd(NEURONS1_ADDR, spikesorter_pb2.SORTER_CMD_REBASE)

    def clear_spikes(self):
        """
        Clears all spike data from the spike sorter, but does not clear it's sorting settings or spike templates.

        Returns:
            None

        Example:
            >>> client.spike_sorter().clear_spikes()
            None

        """
        api_allego.sorter_cmd(
            NEURONS1_ADDR, spikesorter_pb2.SORTER_CMD_CLEAR_SORT)

    def set_sorting(self, mode: str):
        """
        Sets spike sorting on or off

        Parameters:
            mode (str): mode [``on``, ``off``]

        Returns:
            None

        Example:
            >>> client.spike_sorter().set_sorting('on')
            None

        """
        if mode in ["on"]:
            api_allego.sorter_cmd(NEURONS1_ADDR, spikesorter_pb2.SORTER_CMD_ON)
        elif mode in ["off"]:
            api_allego.sorter_cmd(
                NEURONS1_ADDR, spikesorter_pb2.SORTER_CMD_OFF)
        else:
            raise ValueError("mode must be in ['on', 'off']")

    def launch_offline(self, dsource: DatasetMetadata):
        pass

    def set_threshold_level(
        self,
        neg_thr=None,
        pos_thr=None,
        scale="uV",
        ntv_idxs=None,
        weak_thr=False,
        channel_meta=None,
    ):
        """
        Sets spike detection threshold levels.  This function does not effect the threshold state.

        Parameters:
            neg_thr (str): ``on`` | ``off``
            pos_thr (str): ``on`` | ``off``
            scale (str):  ``uV`` | ``sd``
            ntv_idxs (list): channel native indices (default None=all channels)
            weak_thr (bool): use True to set the weak threshold (default=False)
            channel_meta (ChannelMetadata): Allego connected channels

        Returns:
            msg (str): summary description of threshold levels

        Example:
            >>> client.spike_sorter().set_threshold_level(neg_thr=85)
            '[32 channels] detect: neg thr=85.00 uV, pos thr=n/a uV'

        See Also:
             :py:meth:`set_threshold`
             :py:meth:`get_channel_metadata`

        """
        if neg_thr in [None] and pos_thr in [None]:
            return "no new threshold levels were requested so none were changed"
        if channel_meta in [None]:
            channel_meta = self.__parent.get_channel_metadata()
        if not isinstance(channel_meta, ChannelMetadata):
            raise ValueError(
                "channel metadata must be of type ChannelMetadata")
        ntv_chan_idxs = (
            channel_meta.index(SignalType.AMP).ntv if ntv_idxs in [
                None] else ntv_idxs
        )
        reg_float = [0, 0]
        reg_bool = [False, False]
        if neg_thr not in [None]:
            reg_float[0] = neg_thr
            reg_bool[0] = True
        if pos_thr not in [None]:
            reg_float[1] = pos_thr
            reg_bool[1] = True
        if scale in ["sd"] and weak_thr in [False]:
            arg = common_pb2.SORTER_THR_LEVEL_SD
        elif scale in ["uV"] and weak_thr in [False]:
            arg = common_pb2.SORTER_THR_LEVEL
        elif scale in ["sd"] and weak_thr in [True]:
            arg = common_pb2.SORTER_WEAK_THR_LEVEL_SD
        elif scale in ["uV"] and weak_thr in [True]:
            arg = common_pb2.SORTER_WEAK_THR_LEVEL
        else:
            raise ValueError(
                'scale must be `uV` | `sd` and/or weak_thr must be True | False')
        req = [common_pb2.SpikeSorterSetParamRequest(spikeSorterID='not_used',
                                                     cmd=arg,
                                                     regFloat64=reg_float,
                                                     regBool=reg_bool,
                                                     ntvChanIdx=ntv_chan_idxs)]
        api_allego.sorter_set_params(
            NEURONS1_ADDR, common_pb2.SpikeSorterSetParamsRequest(params=req))
        return '[{} channels] {}: neg thr={} {}, pos_thr={} {}' .format(len(ntv_chan_idxs),
                                                                        'detect' if arg in [common_pb2.SORTER_THR_LEVEL,
                                                                                            common_pb2.SORTER_THR_LEVEL_SD] else 'weak',
                                                                        '{:.2f}'.format(reg_float[0]) if reg_bool[0] in [
            True] else 'n/a',
            scale,
            '{:.2f}'.format(reg_float[1]) if reg_bool[1] in [
            True] else 'n/a',
            scale)

    def set_threshold(self, neg_thr=None, pos_thr=None, ntv_idxs=None, weak_thr=False, channel_meta=None):
        """
        Set threshold 'on' or 'off'

        Parameters:
            neg_thr (str): ``on`` | ``off``
            pos_thr (str): ``on`` | ``off``
            ntv_idxs (list): channel native indices (default None=all channels)
            weak_thr (bool): use True to set the weak threshold (default=False)
            channel_meta (ChannelMetadata): Allego connected channels

        Returns:
            msg (str): summary description of threshold levels

        Example:
            >>> client.spike_sorter().set_threshold(neg_thr='on')
            '[32 channels] detect: neg thr='on', pos thr=n/a'

        See Also:
             :py:meth:`set_threshold_level`
             :py:meth:`get_channel_metadata`

        """
        if neg_thr in [None] and pos_thr in [None]:
            return "no new threshold states were requested so none were changed"
        if channel_meta in [None]:
            channel_meta = self.__parent.get_channel_metadata()
        if not isinstance(channel_meta, ChannelMetadata):
            raise ValueError(
                'channel metadata must be of type ChannelMetadata')
        ntv_idxs = channel_meta.index(SignalType.AMP).ntv
        reg_float = [0, 0]
        reg_bool = [False, False]
        if neg_thr not in [None]:
            if neg_thr not in ["on", "off"]:
                raise ValueError("neg_thr must be ``on`` or ``off``")
            reg_float[0] = 1.0 if neg_thr in ["on"] else 0.0
            reg_bool[0] = True
        if pos_thr not in [None]:
            if pos_thr not in ["on", "off"]:
                raise ValueError("pos_thr must be ``on`` or ``off``")
            reg_float[1] = 1.0 if pos_thr in ["on"] else 0.0
            reg_bool[1] = True
        if weak_thr in [False]:
            arg = common_pb2.SORTER_THR_ACTIVATE
        elif weak_thr in [True]:
            arg = common_pb2.SORTER_WEAK_THR_ACTIVATE
        else:
            raise ValueError('weak_thr must be True | False')
        req = [common_pb2.SpikeSorterSetParamRequest(spikeSorterID='not_used',
                                                     cmd=common_pb2.arg,
                                                     regFloat64=reg_float,
                                                     regBool=reg_bool,
                                                     ntvChanIdx=ntv_idxs)]
        api_allego.sorter_set_params(
            NEURONS1_ADDR, common_pb2.SpikeSorterSetParamsRequest(params=req))
        return '[{} channels] {}: neg thr={}, pos_thr={}' .format(len(ntv_idxs),
                                                                  'detect' if arg in [common_pb2.SORTER_THR_LEVEL,
                                                                                      common_pb2.SORTER_THR_LEVEL_SD] else 'weak',
                                                                  '{}'.format(neg_thr) if reg_bool[0] in [
            True] else 'n/a',
            '{}'.format(pos_thr) if reg_bool[1] in [True] else 'n/a')

    def set_spike_window(self, pre_thr_ms=None, post_thr_ms=None):
        """
        Set spike window.

        Parameters:
            pre_thr_ms (float): pre-threshold window duration in milliseconds (default None=not changed)
            post_thr_ms (float): post-threshold window duration in milliseconds (default None=not changed)

        Returns:
            msg (str): summary description of spike window

        Example:
            >>> client.spike_sorter().set_threshold(neg_thr='on')
            '[32 channels] detect: neg thr='on', pos thr=n/a'

        See Also:
             :py:meth:`set_threshold_level`
             :py:meth:`get_channel_metadata`

        """
        ntv_chan_idxs = self.__parent.get_channel_metadata().index(SignalType.AMP).ntv
        params = self.get_params()
        if len(params) == 0:
            return "no connected channels, spike window was not changed"
        cur_wdw = params.loc[params["ntv_idx"] == 0]["thr_wdw"][0]
        reg_float = [pre_thr_ms, post_thr_ms]
        reg_bool = [True, True]
        if pre_thr_ms in [None]:
            reg_float[0] = cur_wdw[0] * 0.001  # converts to sec
        if post_thr_ms in [None]:
            reg_float[1] = cur_wdw[1] * 0.001  # converts to sec
        req = [common_pb2.SpikeSorterSetParamRequest(spikeSorterID='not_used',
                                                     cmd=common_pb2.SORTER_THR_WDW,
                                                     regFloat64=reg_float,
                                                     regBool=reg_bool,
                                                     ntvChanIdx=ntv_chan_idxs)]
        api_allego.sorter_set_params(
            NEURONS1_ADDR, common_pb2.SpikeSorterSetParamsRequest(params=req))
        params = self.get_params()
        cur_wdw = params.loc[params['ntv_idx'] == 0]['thr_wdw'][0]
        cur_pts = params.loc[params['ntv_idx'] == 0]['thr_wdw_pts'][0]
        return '[{} channels] window: pre-thr={:.2f}, post-thr={:.2f}, total={:.2f} ms [{} points]' .format(len(ntv_chan_idxs),
                                                                                                            cur_wdw[0]*1000.0, cur_wdw[1] *
                                                                                                            1000.0, cur_wdw[2] *
                                                                                                            1000.0,
                                                                                                            cur_pts[2])

    def set_spike_shadow(self, shadow_ms=None):
        """
        Sets spike shadow window.  The shadow window is the time skipped after each threshold crossing.

        Parameters:
            shadow_ms (float): shadow window duration in ms (default None=not changed)

        Returns:
            msg (str): summary description of spike shadow window

        Example:
            >>> client.spike_sorter().set_spike_shadow(1.5)
            '[32 channels] shadow window: 1.5 ms [40 points]'

        See Also:
             :py:meth:`set_threshold_level`
             :py:meth:`get_channel_metadata`

        """
        ntv_chan_idxs = self.__parent.get_channel_metadata().index(SignalType.AMP).ntv
        params = self.get_params()
        if len(params) == 0:
            return "no connected channels, spike shadow window was not changed"
        cur_wdw = params.loc[params["ntv_idx"] == 0]["shadow"][0]
        reg_float = [shadow_ms, 0.0]
        reg_bool = [True, True]
        if shadow_ms in [None]:
            reg_float[0] = cur_wdw[0] * 0.001  # converts to sec
        req = [common_pb2.SpikeSorterSetParamRequest(spikeSorterID='not_used',
                                                     cmd=common_pb2.SORTER_SHADOW,
                                                     regFloat64=reg_float,
                                                     regBool=reg_bool,
                                                     ntvChanIdx=ntv_chan_idxs)]
        api_allego.sorter_set_params(
            NEURONS1_ADDR, common_pb2.SpikeSorterSetParamsRequest(params=req))
        params = self.get_params()
        cur_wdw = params.loc[params["ntv_idx"] == 0]["shadow"][0]
        cur_pts = params.loc[params["ntv_idx"] == 0]["shadow_pts"][0]
        return "[{} channels] shadow window: {:.2f}  ms [{} points]".format(
            len(ntv_chan_idxs), cur_wdw * 1000.0, cur_pts
        )

    def get_params(self) -> pd.DataFrame:
        """
        Returns the spike sorter parameters as a table.

        Returns:
            pandas.DataFrame

        Example:
            >>> client.sorter_get_params()
            None

        """
        return api_allego.sorter_get_params(NEURONS1_ADDR)

    def get_state(self) -> pd.DataFrame:
        """
        Returns the spike sorter state as a table.

        Returns:
            pandas.DataFrame

        Example:
            >>> client.sorter_get_state()
            None

        """
        return api_allego.sorter_get_state(NEURONS1_ADDR)

    def get_dashboard(self) -> pd.DataFrame:
        """
        Returns the spike sorter dashboard as a table.

        Returns:
            pandas.DataFrame

        Example:
            >>> client.sorter_get_dashboard()
            None

        """
        return api_allego.sorter_get_dashboard(NEURONS1_ADDR)
