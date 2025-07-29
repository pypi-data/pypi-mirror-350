import datetime
from collections import namedtuple
from enum import Enum
from pathlib import Path

import numpy as np
import pandas as pd
from radiens.api.api_utils.util import to_file_ext
from radiens.grpc_radiens import (allegoserver_pb2, biointerface_pb2,
                                  common_pb2, datasource_pb2)
from radiens.lib.channel_metadata import ChannelMetadata
from radiens.utils.constants import TimeRange
from radiens.utils.util import (make_neighbors_desc, make_neuron_desc,
                                make_time_range)

# SPIKE_ENSEMBLE = namedtuple("SpikeWaveforms", ['time_range', 'n_pts_waveform', 'num_total_spikes', 'channel'])
SITE_STATS = namedtuple("SiteStats", ['spike_count', 'spike_count_labeled', 'spike_count_unlabeled',
                                      'spike_rate', 'spike_rate_labeled', 'spike_rate_unlabeled',
                                      'noise', 'snr', 'neurons'])
SPK_LABEL = Enum(
    'SpikeLabel', ['LABELED', 'UNLABELED', 'BAD', 'TOTAL'], start=0)
SPIKE_COMP_SHAPE = namedtuple("SpikeComponentShape", [
    'waveform', 'feature', 'feature2', 'zscore'])


class SpikesSet():
    '''
    Radiens container for spike datasets
    '''

    def __init__(self, msg):
        """
        """
        self._time_range = np.array([], dtype=np.float64)
        self._n_pts_wfm = 0
        self._n_spikes_total = 0
        self._chan = {}
        if isinstance(msg, biointerface_pb2.SpikesSpikeDataDenseReply):
            self._time_range = np.array(msg.timeRange, dtype=np.float64)
            self._n_pts_wfm = msg.waveformNPoints
            self._n_spikes_total = msg.totalNSpikes
            _data = np.frombuffer(msg.data, dtype=np.float32)
            offset0 = 0
            for desc in msg.channelDescriptors:
                self._chan[desc.ntvChanIdx] = {'labels': [str(elem) for elem in desc.labels],
                                               'waveform_max': desc.waveformMaxValue,
                                               'waveform_min': desc.waveformMinValue,
                                               'num_spikes': len(desc.labels),
                                               'comp': {
                                               'timestamps': np.array([], np.int64),
                                               'waveforms': np.array([[]], np.float64),
                                               'ftrs': np.array([[]], np.float64),
                                               'ftrs2': np.array([[]], np.float64)},
                                               'neighbors': {'waveforms': np.array([[[]]], np.float64),
                                                             'ntv_chan_idx': np.array([[[]]], np.float64)}
                                               }
                if len(desc.labels) > 0:
                    self._chan[desc.ntvChanIdx]['waveforms'] = np.reshape(
                        _data[offset0:offset0+(self._n_pts_wfm*len(desc.labels))], (self._n_pts_wfm, len(desc.labels)))
                offset0 = offset0 + self._n_pts_wfm*len(desc.labels)

    @ property
    def envelope_time_range(self) -> np.ndarray:
        """
        Envelope time range in sec
        """
        return self._time_range

    @ property
    def num_pts_waveform(self) -> int:
        """
        Number of points per waveform
        """
        return self._n_pts_wfm

    @ property
    def num_spikes_total(self) -> int:
        """
        Number of total spikes in the spikes set.
        """
        return self._n_spikes_total

    @ property
    def num_channels(self) -> int:
        """
        Number of channels in the spikes set.
        """
        return len(self._chan)

    def channels(self) -> dict:
        """
        Channel data
        """
        return self._chan

    def has_component(self, comp: str) -> bool:
        """
        Returns true if the object has the requested component
        """
        if comp not in ['timestamps', 'waveforms']:
            raise ValueError('comp not valid, use `timestamps` | `waveforms`')
        return self._reserved_has_component(comp)

    def component_len(self, comp: str) -> bool:
        """
        Returns true if the object has the requested component
        """
        if comp not in ['timestamps', 'waveforms']:
            raise ValueError('comp not valid, use `timestamps` | `waveforms`')
        return self._reserved_has_component(comp)

    def _reserved_has_component(self, comp: str) -> bool:
        if comp not in ['timestamps', 'waveforms', 'ftrs', 'ftrs2']:
            raise ValueError(
                'comp not valid, use [`timestamps`|`waveforms` | `ftrs` | `ftrs2`')
        for _, chan in self.channels().items():
            if chan['num_spikes'] > 0:
                return len(chan['comp'][comp]) > 0
        return False

    def _reserved_component_len(self, comp: str) -> int:
        if comp not in ['timestamps', 'waveforms', 'ftrs', 'ftrs2']:
            raise ValueError(
                'comp not valid, use [`timestamps`|`waveforms` | `ftrs` | `ftrs2`')
        for _, chan in self.channels().items():
            if chan['num_spikes'] > 0:
                return len(chan['comp'][comp])
        return 0


class SpikesMetadata():
    '''
    Radiens container for metadata on spikes datasets
    '''

    def __init__(self, msg):
        """
        """
        if not isinstance(msg, biointerface_pb2.SpikesSpecReply):
            raise ValueError('initialized with wrong data type')
        self._d = {'datasourceID': msg.biointerfaceID, 'datasetUID': msg.datasetUID,
                   'checksum': msg.checksum, 'persist_dur_sec': msg.persistDur,
                   'num_sites': msg.numSites, 'size_bytes': msg.sizeBytes,
                   'enabled_ntv_idxs': msg.enabledSiteNtvChanIdx, 'ni_type': biointerface_pb2.BiointerfaceType.Name(msg.bioType),
                   'req_num_neighbors': msg.reqNumNeighbors, 'nbr_radius': msg.neighborhoodRadiusUm}
        self._tr = make_time_range(pbTR=msg.tR)
        self._sg = ChannelMetadata(msg.sG)

        self._site_stats = SITE_STATS(spike_count=msg.siteStats.spikeCountStats,
                                      spike_count_labeled=msg.siteStats.labeledSpikeCountStats,
                                      spike_count_unlabeled=msg.siteStats.unlabeledSpikeCountStats,
                                      spike_rate=msg.siteStats.spikeRateStats,
                                      spike_rate_labeled=msg.siteStats.labeledSpikeRateStats,
                                      spike_rate_unlabeled=msg.siteStats.unlabeledSpikeRateStats,
                                      noise=msg.siteStats.siteNoiseStats,
                                      snr=msg.siteStats.siteSnrStats,
                                      neurons=msg.siteStats.neuronStats)
        self._sensor_ext_metadata = {
            'instance_UID': msg.sensorExt.sensorInstanceUID}
        self._project_ext_metadata = {'project_UID': msg.project.projectUID, 'case_UID': msg.project.caseUID,
                                      'trial_UID': msg.project.trialUID, 'annotate_UID': msg.project.annotateUID}
        self._site = {'ntv_idx': [], 'neighbor': [], 'enabled': [], 'pos_probe': [], 'pos_tissue': [], 'size_bytes': [],
                      'TR': [], 'spike_TR': [], 'spike_count': [], 'spike_rate': [], 'noise': [], 'snr': [], 'neurons': [],
                      'num_neurons': [], 'spike_comp_len': []}
        for site in msg.site:
            self._site['ntv_idx'].append(site.ntvChanIdx)
            self._site['neighbor'].append(make_neighbors_desc(site.neighbor))
            self._site['enabled'].append(site.isEnabled)
            self._site['pos_probe'].append(site.posProbe)
            self._site['pos_tissue'].append(site.posTissue)
            self._site['size_bytes'].append(site.sizeBytes)
            self._site['TR'].append(make_time_range(pbTR=site.tR))
            self._site['spike_TR'].append(make_time_range(pbTR=site.spikeTR))
            self._site['spike_count'].append(site.spikeCountSite)
            self._site['spike_rate'].append(site.spikeRateSite)
            self._site['noise'].append(site.noiseLevelSd)
            self._site['snr'].append(site.snrSite)
            self._site['neurons'].append(
                [make_neuron_desc(elem) for elem in site.neuron])
            self._site['num_neurons'].append(site.numNeurons)
            self._site['spike_comp_len'].append(SPIKE_COMP_SHAPE(waveform=site.compLen.waveform, feature=site.compLen.feature,
                                                                 feature2=site.compLen.feature2, zscore=site.compLen.zscore))

    @ property
    def time_range(self):
        """
        Envelope time range in sec as a `TimeRange` named tuple.
        """
        return self._tr

    @ property
    def site_metadata(self) -> ChannelMetadata:
        """
        Site metadata
        """
        return self._sg

    @ property
    def site_summary_stats(self) -> pd.DataFrame:
        """
        Table of site summary statistics.  Use the SStat enum in radiens.util.constants for the name of each statistic (row) for each column.  
        """
        return pd.DataFrame({'spike_count': self._site_stats.spike_count[:],
                             'spike_count_labeled': self._site_stats.spike_count_labeled[:],
                             'spike_count_unlabeled': self._site_stats.spike_count_unlabeled[:],
                             'spike_rate': self._site_stats.spike_rate[:],
                             'spike_rate_labeled': self._site_stats.spike_count_labeled[:],
                             'spike_rate_unlabeled': self._site_stats.spike_count_unlabeled[:],
                             'noise': self._site_stats.noise[:],
                             'snr': self._site_stats.snr[:],
                             'neurons': self._site_stats.neurons[:],
                             })

    @ property
    def sensor_ext_metadata(self) -> dict:
        """
        Sensor extended metadata
        """
        return self._sensor_ext_metadata

    @ property
    def project_ext_metadata(self) -> dict:
        """
        Project extended metadata
        """
        return self._project_ext_metadata

    @ property
    def sites(self) -> pd.DataFrame:
        """
        Site data as a pandas DataFrame (i.e. table) where each site is a row. 
        """
        return pd.DataFrame(self._site)

    @ property
    def neurons(self) -> pd.DataFrame:
        """
        Neuron data as a pandas DataFrame where each neuron is a row.
        """
        tidy_rows = []
        for _, row in self.sites.iterrows():
            for neuron in row['neurons']:
                row['neuron'] = neuron
                row['neuron_id'] = neuron[0]
                tidy_rows.append(row)
        return pd.concat(tidy_rows, axis=1).T.reset_index()
