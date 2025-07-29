import warnings
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from radiens.api import api_allego, api_videre
from radiens.grpc_radiens import biointerface_pb2, radiens_dev_pb2
from radiens.lib.channel_metadata import ChannelMetadata
from radiens.utils.constants import (DEFAULT_HUB_ID, NEURONS1_ADDR,
                                     NEURONS_SINK_DSOURCE_ID, TimeRange)
from radiens.utils.enums import RadiensService, SignalType
from radiens.utils.util import make_time_range

# the following lines are to avoid circular imports and are only used for typing hints
# (TYPE_CHECKING always evaluates to false at runtime)
if TYPE_CHECKING:
    from radiens.allego_client import AllegoClient
    from radiens.videre_client import VidereClient


class SpikesClient():
    """
    Spikes object for AllegoClient, VidereClient
    """

    def __init__(self, parent_client):
        """
        """
        self.__parent: VidereClient | AllegoClient = parent_client

    def _is_allego(self) -> bool:
        return self.__parent.type.is_allego()

    def _is_curate(self) -> bool:
        return self.__parent.type.is_curate()

    def _is_videre(self) -> bool:
        return self.__parent.type.is_videre()

    def get_spikes_metadata(self):
        """
        Returns metadata on the spikes processed by the spike sorter

        Returns:
            pandas.DataFrame

        Example:
            >>> client.get_spikes()
            None

        """
        if self._is_allego():
            return api_allego.get_spikes_spec(NEURONS1_ADDR)

    def get_spike_rasters(self, dsource_id=None):
        """
        Returns spike rasters from the spike sorter

        Returns:
            pandas.DataFrame

        Example:
            >>> client.get_spikes()
            None

        """
        msg = biointerface_pb2.SpikeSorterGetRasterDataRequest()
        if self._is_allego():
            return api_allego.sorter_get_raster_data(NEURONS1_ADDR, msg)

    def get_recent_spikes(self, time_wdw_sec=1.0, ntv_chan_idxs=None, max_spikes_per_chan=100, channel_meta=None):
        """
        Returns the most recent spikes for the requested ``ntv_chan_idxs`` over the requested time window. 
        The returned spike data has spike timestamps, spike waveforms, and spike labels. 

        Returns:
            pandas.DataFrame

        Example:
            >>> client.get_spikes()
            None

        """
        if channel_meta in [None]:
            channel_meta = self.__parent.get_channel_metadata()
        if not isinstance(channel_meta, ChannelMetadata):
            raise ValueError(
                'channel metadata must be of type ChannelMetadata')
        ntv_chan_idxs = channel_meta.index(SignalType.AMP).ntv
        msg = biointerface_pb2.SpikesGetSpikesRequest(dsourceID=NEURONS_SINK_DSOURCE_ID,
                                                      mode=biointerface_pb2.Spikes,  # not used
                                                      ntvChanIdx=ntv_chan_idxs,
                                                      timeStart=time_wdw_sec,
                                                      timeStop=np.nan,
                                                      spikeLabels=[],  # not used
                                                      maxSpikesPerChannel=max_spikes_per_chan,
                                                      spikeComp=[],  # not used
                                                      )
        return api_allego.get_spikes(NEURONS1_ADDR, msg)

    def get_spike_waveforms(self, dataset_id: str, time_range: TimeRange | list = None, hub_name=DEFAULT_HUB_ID):
        """
        Gets spike waveforms for specified time range of a spikes file

        Parameters: 
            dataset_id (str): dataset ID 
            time_range (list[float])
            ntv_idxs (list[float])

        Returns:

        """

        if self._is_videre():
            time_range = self.__parent._parse_time_range(
                dataset_id, time_range)
            return api_videre.get_spike_waveforms(self.__parent._server_address(hub_name, RadiensService.CORE), dataset_id, time_range)
        else:
            raise Exception('{} cannot get spike waveforms',
                            self.__parent.type)

    def get_spike_timestamps(self, dataset_id: str, time_range:  TimeRange | list = None, hub_name=DEFAULT_HUB_ID):
        """
        Gets spike timestamps for specified time range of a spikes file

        Parameters: 
            dataset_id (str): dataset ID 
            time_range (list[float])

        Returns:

        """

        if self._is_videre():
            time_range = self.__parent._parse_time_range(
                dataset_id, time_range)
            return api_videre.get_spikes_timestamps(
                self.__parent._server_address(hub_name, RadiensService.CORE),
                dataset_id,
                time_range,
            )
        else:
            raise Exception('{} cannot get spike timestamps',
                            self.__parent.type)

    def get_neuron_timestamps(self, dataset_id: str, time_range: TimeRange, ntv_idxs: list):
        resp = self.get_spike_timestamps(dataset_id, time_range, ntv_idxs)
        neuron_dict = {}
        for chan in resp:
            for i, l in enumerate(chan['labels']):
                unique_label = str(chan['ntv_idx']) + str(l)
                if unique_label not in neuron_dict:
                    neuron_dict[unique_label] = {
                        'timestamps': [],
                        'ntv_idx': chan['ntv_idx']
                    }
                neuron_dict[unique_label]['timestamps'].append(
                    chan['timestamps'][i])

        # rename neurons to be numbers 1-len(neuron_dict)
        neuron_labels_old = list(neuron_dict.keys())
        for i, unique_label in enumerate(neuron_labels_old):
            neuron_dict[i] = neuron_dict.pop(unique_label)
        return neuron_dict

    def get_neurons(self):
        """
        Returns neurons from the spike sorter

        Returns:
            pandas.DataFrame

        Example:
            >>> client.get_spikes()
            None

        """
        msg = biointerface_pb2.BiointerfaceGetNeuronsRequest()
        return api_allego.get_neurons(NEURONS1_ADDR, msg)

    def convert_kilosort_output(self,
                                source_bio_path: str | Path = "",
                                source_bio_basename: str | Path = "",
                                source_vex_path: str | Path = "",
                                source_vex_basename: str | Path = "",
                                sink_bio_path: str | Path = "",
                                sink_bio_basename: str | Path = "",
                                hub_name=DEFAULT_HUB_ID):
        """
         Converts the output of kilosort into a .spikes file that can be loaded into radiens
        """
        spec = radiens_dev_pb2.WrangleMerge(
            vexSpikesView=radiens_dev_pb2.WrangleMergeVexSpikesView(
                sourceVex=radiens_dev_pb2.WrangleFileDesc(
                    path=str(source_vex_path),
                    baseName=str(source_vex_basename),
                ),
                sourceBio=radiens_dev_pb2.WrangleFileDesc(
                    path=str(source_bio_path),
                    baseName=str(source_bio_basename),
                ),
                view=[
                    radiens_dev_pb2.WrangleMergeVexSpikesViewSpec(
                        sinkBio=radiens_dev_pb2.WrangleFileDesc(
                            path=str(sink_bio_path),
                            baseName=str(sink_bio_basename),
                        )
                    )
                ],
            ),
        )

        req = radiens_dev_pb2.WrangleRequest(
            mode=radiens_dev_pb2.WRANGLE_MODE_IMPORT_KILOSORT_SPIKES,
            spec=spec,
        )

        # radiens_dev_pb2.WrangleMode.DESCRIPTOR.
        if not self._is_videre():
            raise Exception(
                '{} cannot convert kilosort output'.format(self.__parent.type))
        return api_videre.convert_kilosort_output(self.__parent._server_address(hub_name, RadiensService.SORTER), req)
