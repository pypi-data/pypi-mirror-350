from collections import namedtuple
from pathlib import Path
from pprint import pprint

import numpy as np
import pandas as pd
from radiens.grpc_radiens import (allegoserver_pb2, common_pb2, datasource_pb2,
                                  spikesorter_pb2)
from radiens.lib.dataset_metadata import FileSetDescriptor

SORTER_STATE = namedtuple("SorterState", ['mode', 'msg', 'time_initialize',
                                          'time_start', 'time_stop', 'launch_time', 'frac_complete', 'is_on',
                                          'kernal_err_msg', 'kernal_warn_msg'])


class SorterState():
    '''
    Radiens container for the spike sorter dashboard
    '''

    def __init__(self, resp):
        """
        """
        if not isinstance(resp, spikesorter_pb2.SpikeSorterDashboardGeneralRec):
            raise ValueError('spike sorter SorterState argument is wrong type')

        self._df_state = pd.DataFrame({'mode': [spikesorter_pb2.SpikeSorterStateSystem.Name(resp.sys)],
                                       'frac_complete': [resp.fracComplete],
                                       'message': [resp.msg],
                                       'init_time': [resp.initializeTime],
                                       'launch_time': [resp.launchTime],
                                       'session_start_time': [resp.sessionStartTime],
                                       'session_stop_time': [resp.sessionStopTime],
                                       'is_on': [resp.isOn],
                                       'kernel_err_message': [resp.kernelErrorMessage],
                                       'kernel_warn_message': [resp.kernelWarnMessage],
                                       }).T

    @ property
    def state(self) -> pd.DataFrame:
        """
        Spike sorter state as a pandas DataFrame

        Access fields via:
            ss.state.loc['mode'][0]
        """
        return self._df_state


class Dashboard():
    '''
    Radiens container for the spike sorter dashboard
    '''

    def __init__(self, resp):
        """
        """
        if not isinstance(resp, spikesorter_pb2.SpikeSorterGetDashboardReply):
            raise ValueError('spike sorter Dashboard argument is wrong type')

        self._df_state = SorterState(resp.general.state)
        self._gen = pd.DataFrame({'ports': [resp.enabledPorts],
                                  'time_range': [np.array(resp.general.timeRange)],
                                  'num_sites_total': [resp.general.numTotalSites],
                                  'num_sites_enabled': [resp.general.numEnabledSites],
                                  'num_sites_active': [resp.general.numActiveSites],
                                  'num_units': [resp.general.numNeurons],
                                  'probe_yield_mean': [resp.general.probeYield],
                                  'site_yield_mean': [resp.general.siteYield],
                                  'num_spikes_processed': [resp.general.numSpikesProcessed],
                                  'num_spikes_labeled': [resp.general.numSpikesLabeled],
                                  'sort_efficiency': [resp.general.sortEfficiency],
                                  'spikes_file_path': [resp.general.sinkDesc.path],
                                  'spikes_file_base_name': [resp.general.sinkDesc.baseName],
                                  }).T
        _sum_stats = []
        _sum_stats.append(pd.DataFrame({'stat': ['probe-snr', 'probe-noise', 'probe-units'],
                                        'port': ['all', 'all', 'all'],
                                        'N': [resp.siteStats.snr[11], resp.siteStats.noise[11], resp.siteStats.neuronYield[11]],
                                        'mean': [resp.siteStats.snr[0], resp.siteStats.noise[0], resp.siteStats.neuronYield[0]],
                                        'sd': [resp.siteStats.snr[1], resp.siteStats.noise[1], resp.siteStats.neuronYield[1]],
                                        'min': [resp.siteStats.snr[3], resp.siteStats.noise[3], resp.siteStats.neuronYield[3]],
                                        'max': [resp.siteStats.snr[4], resp.siteStats.noise[4], resp.siteStats.neuronYield[4]],
                                        'median': [resp.siteStats.snr[6], resp.siteStats.noise[6], resp.siteStats.neuronYield[6]],
                                        'mode': [np.NaN, np.NaN, resp.siteStats.neuronYield[2]],
                                        'mode_cnt': [np.NaN, np.NaN, resp.siteStats.neuronYield[5]],
                                        'q25': [resp.siteStats.snr[7], resp.siteStats.noise[7], resp.siteStats.neuronYield[7]],
                                        'q75': [resp.siteStats.snr[8], resp.siteStats.noise[8], resp.siteStats.neuronYield[8]],
                                        'skew': [resp.siteStats.snr[9], resp.siteStats.noise[9], resp.siteStats.neuronYield[9]],
                                        'kurtosis': [resp.siteStats.snr[10], resp.siteStats.noise[10], resp.siteStats.neuronYield[10]],
                                        }))

        for k in resp.portStats:
            v = resp.portStats[k]
            snr = v.snr
            noise = v.noise
            neuron_yield = v.neuronYield
            if len(snr) != 12:
                snr = [0 for elem in range(0, 12)]
            if len(neuron_yield) != 12:
                neuron_yield = [0 for elem in range(0, 12)]
            if len(noise) != 12:
                noise = [0.01 for elem in range(0, 12)]
            _sum_stats.append(pd.DataFrame({'stat': ['port-snr', 'port-noise', 'port-units'],
                                            'port': [k, k, k],
                                            'N': [snr[11], noise[11], neuron_yield[11]],
                                            'mean': [snr[0], noise[0], neuron_yield[0]],
                                            'sd': [snr[1], noise[1], neuron_yield[1]],
                                            'min': [snr[3], noise[3], neuron_yield[3]],
                                            'max': [snr[4], noise[4], neuron_yield[4]],
                                            'median': [snr[6], noise[6], neuron_yield[6]],
                                            'mode': [np.NaN, np.NaN, neuron_yield[2]],
                                            'mode_cnt': [np.NaN, np.NaN, neuron_yield[5]],
                                            'q25': [snr[7], noise[7], neuron_yield[7]],
                                            'q75': [snr[8], noise[8], neuron_yield[8]],
                                            'skew': [snr[9], noise[9], neuron_yield[9]],
                                            'kurtosis': [snr[10], noise[10], neuron_yield[10]],
                                            }))
        self._df_sum_stats = pd.concat(_sum_stats, axis=0)

    @ property
    def summary_stats(self) -> pd.DataFrame:
        """
        Summary statistics for all ports and probes as a pandas DataFrame
        """
        return self._df_sum_stats

    @ property
    def general(self) -> pd.DataFrame:
        """
        General summary of spike sorter performance
        """
        return self._gen

    @ property
    def state(self) -> pd.DataFrame:
        """
        Spike sorter state as a pandas DataFrame
        """
        return self._df_state.state
