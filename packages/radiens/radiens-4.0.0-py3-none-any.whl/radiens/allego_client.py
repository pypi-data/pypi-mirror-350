from typing import Tuple

from numpy import ndarray
from radiens.api import api_allego
from radiens.lib.allego_lib import AllegoState
from radiens.lib.channel_metadata import ChannelMetadata
from radiens.metrics_client import MetricsClient
from radiens.spike_sorter_client import SpikeSorterClient
from radiens.spikes_client import SpikesClient
from radiens.utils.constants import (ALLEGO_CORE_ADDR, PCACHE_ADDR,
                                     PRIMARY_CACHE_STREAM_GROUP_ID)
from radiens.utils.enums import (ClientType, Port, RecordMode, StreamMode,
                                 SystemMode)
from radiens.utils.interceptors import SessionMetaData
from radiens.workspace_client import WorkspaceClient


class AllegoClient:
    """
    AllegoClient implements the radiens API for data acquisition and instrument control.
    It matches and extends the functionality of the Radiens Allego UI app.
    """

    def __init__(self):
        """
        """
        self._samp_freq = None
        self._sorter = SpikeSorterClient(self)
        self._workspace = WorkspaceClient()
        self._spikes = SpikesClient(self)
        self._metrics = MetricsClient(self)

        # initialize SessionMetaData
        SessionMetaData(core_addr=ALLEGO_CORE_ADDR)

    @property
    def type(self) -> ClientType:
        """
        Returns :py:attr:`~radiens.utils.enums.ClientType.ALLEGO`
        """
        return ClientType.ALLEGO

    def workspace(self) -> WorkspaceClient:
        """
        Allego workspace API
        """
        return self._workspace

    def spike_sorter(self) -> SpikeSorterClient:
        """
        Allego spike sorter API
        """
        return self._sorter

    def spikes(self) -> SpikesClient:
        """
        Allego spikes API
        """
        return self._spikes

    def signal_metrics(self) -> MetricsClient:
        """
        Allego signal metrics API
        """
        return self._metrics

    def restart(self, mode: SystemMode | str | int) -> None:
        """
        Restarts Allego in the requested mode.  

        Valid modes: 

            - smartbox_pro, 
            - smartbox_pro_sinaps_256
            - smartbox_pro_sinaps_512
            - smartbox_pro_sinaps_1024
            - smartbox_classic
            - smartbox_sim_gen_sine
            - smartbox_sim_gen_sine_mapped
            - smartbox_sim_gen_sine_high_freq
            - smartbox_sim_gen_sine_multi_band
            - smartbox_sim_gen_spikes
            - open_ephys_usb2
            - open_ephys_usb3
            - intan_usb2
            - intan_recording_controller_1024
            - intan_recording_controller_512
            - xdaq_one_req
            - xdaq_one_stim
            - xdaq_core_req
            - xdaq_core_stim

        Returns:
            None

        Side Effect:
            Resets all settings to their initialization values in the requested mode.

        Example:
            >>> client.restart('sim-spikes')
            None
        """
        return api_allego.restart(ALLEGO_CORE_ADDR, SystemMode.parse(mode))

    # ======= getters =======

    def get_available_sensors(self) -> dict:
        """
        Gets dictionary of dictionaries of available Radiens headstage and probe models, with each model of form key=component ID, value=number of channels. 

        Returns:
            sensors (dict): has keys 'headstages' and 'probes' that map to dictionaries of the available headstage models and probe models, respectively.  

        Example: 
            >>> client.get_available_sensors()
            {'sensors': {'headstages': {'hstg__chronic_smartlink_HC16': 16, 'hstg__acute_smartlink_A64': 64, ...}, 
                        'probes': {'a2x16_10mm50_500_177': 32, 'a1x16_5mm150_177': 16, ...}}
        """
        return api_allego.get_sensors(ALLEGO_CORE_ADDR)

    def get_status(self) -> AllegoState:
        """
        Gets the status of Allego.

        Returns:
            status (~radiens.lib.allego_lib.AllegoState)

        Example: 
            >>> client.get_status().print()
            ALLEGO status:
            stream       : S_ON
                time range : [0.000, 2149.197] sec
                HW memory  : 0.0 
            recording         : R_OFF
                duration        : 0.000 sec
                file name       : allego_0__uid0906-13-55-32
                base name       : allego
                path            : /Users/akelly/sapiens/core_packages/radix/radiens_etc
                index           : 0
                file timestamp  : 0906-13-55-32


        """
        s = api_allego.get_cfg_status(ALLEGO_CORE_ADDR)
        self._samp_freq = s.sample_freq
        return s

    def get_stream_loop_dur_ms(self) -> float:
        """
        Returns the stream loop duration in milliseconds

        Notes:
            Make sure to convert this to seconds if you're using it to set the sleep time in a loop.
        """
        return api_allego.get_stream_loop_dur_ms(ALLEGO_CORE_ADDR)

    def get_channel_metadata(self) -> ChannelMetadata:
        """
        Gets the channel metadata for all connected ports

        Notes:
            All ports are scanned to detect the connected ports. 

        """
        return api_allego.get_signal_group(ALLEGO_CORE_ADDR, PRIMARY_CACHE_STREAM_GROUP_ID)

    def get_signals(self) -> Tuple[ndarray, list]:
        """
        Gets the the most recent signals since last call of itself or :py:meth:`set_time_to_cache_head`.

        Returns:
            sigarray (ndarray[numpy.float32]): raw signal data; the mapping contained in signal_group (see :py:meth:`get_channel_metadata`)
            time_range (list[float]): time range (in seconds) of sigarray

        Notes:
                Sets current time to most recent time point in signal cache.

        This should be called before the first call of :py:meth:`get_signals`. The first call of :py:meth:`get_signals` 
        will return the new signals since the last call to :py:meth:`set_time_to_cache_head` 
        """
        if self._samp_freq is None:
            s = api_allego.get_cfg_status(ALLEGO_CORE_ADDR)
            self._samp_freq = s.sample_freq

        # api.set_time_to_cache_head(PCACHE_ADDR, PRIMARY_CACHE_STREAM_GROUP_ID)

        return api_allego.get_signals(PCACHE_ADDR, PRIMARY_CACHE_STREAM_GROUP_ID, self._samp_freq)

    def get_digital_out_states(self) -> dict:
        """
        Gets digital out state.

        Returns:
            dout_state_dict (dict): has keys 'digital_outs_mode' and 'states'.

        Example:
            >>> client.get_digital_out_states()
            {'digital_outs_mode': 'manual',
            'states': [{'chan_idx': 0, 'state': True}, {'chan_idx': 1, 'state': False}]}
        """
        return api_allego.get_digital_out_states(ALLEGO_CORE_ADDR)

    def get_analog_out_settings(self) -> dict:
        """
        Gets analog out settings

        Returns:
            settings (dict): 

        Example:
            >>> client.get_analog_out_settings()
            {'dac': [
                {'amp_ntv_chan_idx': -1, 
                 'aout_ntv_chan_idx': 0, 
                 'stream': 0,
                 'stream_offset_idx': 0},
                {'amp_ntv_chan_idx': -1,
                 'aout_ntv_chan_idx': 1,
                 'stream': 0,
                 'stream_offset_idx': 0}
                 ],
            'gain': 0,
            'high_pass': {'enable': False, 'cutoff_freq': 0.0}}
        """
        return api_allego.get_dac_register(ALLEGO_CORE_ADDR)

    def get_stim_params(self) -> dict:
        """
        returns current stimulation params (see :py:meth:`set_stim_params`)

        Returns:
            stim_params (dict): a dictionary where the keys are the system channel indices and the values are dictionaries containing the stimulation parameters. Each dictionary associated with a channel will have the following key-value pairs:

                - 'enabled': stimulation enabled on channel (`bool`)
                - 'enable_amp_settle': amp settle enabled on channel (`bool`)
                - 'enable_charge_recovery': charge recovery enabled on channel (`bool`)
                - 'first_phase_amplitude_uA': Level of current in µA for the first phase of the stimulation waveform (type)
                - 'first_phase_duration_us': (`float`)
                - 'interphase_delay_us': (`float`)
                - 'maintain_amp_settle_us': (`float`) 
                - 'number_of_stim_pulses': (`int`)
                - 'post_stim_amp_settle_us': (`float`)
                - 'post_stim_charge_recovery_off_us': (`float`)
                - 'post_stim_charge_recovery_on_us': (`float`)
                - 'post_trigger_delay_us': (`float`)
                - 'pre_stim_amp_settle_us': (`float`)
                - 'pulse_or_train': (`int`)
                - 'pulse_train_period_us': (`float`)
                - 'refactory_period_ms': (`float`)
                - 'second_phase_amplitude_uA': Level of current in µA for the second phase of the stimulation waveform (type)
                - 'second_phase_duration_us': (`float`)
                - 'stim_polarity': (`int`)
                - 'stim_shape': (`int`)
                - 'stim_sys_chan_idx': (`int`)
                - 'trigger_edge_or_level': (`int`)
                - 'trigger_high_or_low': (`int`)
                - 'trigger_source_is_keypress': (`bool`)
                - 'trigger_source_idx': (`int`)


        Example:
            >>> get_stim_params()
            {6: # system idx
                {'stim_shape': 0,
                'stim_polarity': 0,
                'first_phase_duration_us': 100.0,
                'second_phase_duration_us': 100.0,
                'interphase_delay_us': 100.0,
                'first_phase_amplitude_uA': 0.0,
                'second_phase_amplitude_uA': 0.0,
                'baseline_voltage': 0.0,
                'trigger_edge_or_level': 0,
                'trigger_high_or_low': 0,
                'enabled': False,
                'post_trigger_delay_us': 0.0,
                'pulse_or_train': 0,
                'number_of_stim_pulses': 2,
                'pulse_train_period_us': 10000.0,
                'refactory_period_ms': 1.0,
                'pre_stim_amp_settle_us': 0.0,
                'post_stim_amp_settle_us': 0.0,
                'maintain_amp_settle_us': False,
                'enable_amp_settle': False,
                'post_stim_charge_recovery_on_us': 0.0,
                'post_stim_charge_recovery_off_us': 0.0,
                'enable_charge_recovery': False,
                'trigger_source_is_keypress': True,
                'trigger_source_idx': 1,
                'stim_sys_chan_idx': 6 # redundant but expected when setting stim params
                },
            {...}
        """
        return api_allego.get_stim_params(ALLEGO_CORE_ADDR)

    # ======= setters =======

    def set_sampling_freq(self, fs: float) -> None:
        """
        Sets sampling frequency.  Valid sampling frequencies: 625, 1000, 1250, 1500, 2000, 2500, 3000, 3333,
        4000, 5000, 6250, 8000, 10000, 12500, 15000, 20000, 25000, 30000

        Parameters: 
            fs (int): requested sampling frequency (samples/sec)

        Returns:
            None

        Example:
            >>> client.set_samp_freq(12500)
            None

        """
        api_allego.set_fs(ALLEGO_CORE_ADDR, fs)

    def set_analog_out_high_pass(self, cutoff_freq: float, enable=True) -> dict:
        """
        Sets the analog out hardware filter

        Parameters: 
            fs (int): requested sampling frequency (samples/sec)

        Returns:
            analog_out_settings (dict)

        Example:
            >>> client.set_dac_high_pass(500, True)
            {...}
        """
        return api_allego.set_dac_high_pass(ALLEGO_CORE_ADDR, enable, cutoff_freq)

    def set_sensor(self, port: Port | str | int, headstage_id: str, probe_id: str) -> None:
        """
        Sets a sensor (headstage paired with probe) to the requested port.

        The `headstage_id` and `probe_id` arguments are: 
          1. the labels listed in the `Allego` and `Videre` `Probe Model` UI tab.
          2. aliases in radiens.utils.HEADSTAGE_ALIAS and radiens.utils.PROBE_ALIAS  

        Parameters: 
            port (str): requested port (must be a currently connected port)
            headstage_id (str): requested headstage alias or headstage ID
            probe_id (str): requested probe alias or probe ID

        Returns:
            None

        Example:
            >>> client.set_sensor('A', 'smart-32', '4x8-32')
            None

        Notes:
            `radiens.utils.HEADSTAGE_ALIAS` and `radiens.utils.PROBE_ALIAS` are 
            an abridged set of headstage and probe aliases provided for convienence.  

        See also:
            :py:meth:`get_available_sensors()`
            :py:meth:`get_connected_ports()`

        """
        return api_allego.set_sensor(ALLEGO_CORE_ADDR, Port.parse(port), headstage_id, probe_id)

    def set_time_to_cache_head(self) -> None:
        """
        Sets current time to most recent time point in signal cache.

        This should be called before the first call of :py:meth:`get_signals`. The first call of :py:meth:`get_signals` 
        will return the new signals since the last call to :py:meth:`set_time_to_cache_head` 
        """
        return api_allego.set_time_to_cache_head(PCACHE_ADDR, PRIMARY_CACHE_STREAM_GROUP_ID)

    def set_manual_stim_trigger(self, trigger: int) -> None:
        """
        """
        api_allego.set_manual_stim_trigger(ALLEGO_CORE_ADDR, trigger)

    def set_stim_params(self, param_dict: dict) -> None:
        """
        Sets stimulation parameters to a stim channel. Any parameter not specified in the parameter `param_dict` will be kept as is, or set to default parameter, if not already set (see :py:meth:`get_stim_params`).

        Parameters: 
            param_dict: has following key-value pairs; comments are defaults:

                - 'enabled': # False
                - 'enable_amp_settle': # False
                - 'enable_charge_recovery': # False
                - 'first_phase_amplitude_uA': # 0
                - 'first_phase_duration_us': # 0
                - 'interphase_delay_us': # 0
                - 'maintain_amp_settle_us': # 0
                - 'number_of_stim_pulses': # 2
                - 'post_stim_amp_settle_us': # 0
                - 'post_stim_charge_recovery_off_us': # 0
                - 'post_stim_charge_recovery_on_us': # 0
                - 'post_trigger_delay_us': # 0
                - 'pre_stim_amp_settle_us': # 0
                - 'pulse_or_train': # 0 
                - 'pulse_train_period_us': # 0
                - 'refactory_period_ms': # 1
                - 'second_phase_amplitude_uA': # 0
                - 'second_phase_duration_us': # 0
                - 'stim_polarity': # 0
                - 'stim_shape': # 0
                - 'stim_sys_chan_idx': # 0
                - 'trigger_edge_or_level': # 0
                - 'trigger_high_or_low': # 0
                - 'trigger_source_is_keypress': # True
                - 'trigger_source_idx': # 0

        """
        return api_allego.set_stim_params(ALLEGO_CORE_ADDR, param_dict)

    def set_stim_step(self, step: int) -> None:
        api_allego.set_stim_step(ALLEGO_CORE_ADDR, step)

    def set_streaming(self, mode: str | int | bool | StreamMode) -> AllegoState:
        """
        Sets signal streaming to 'on' or 'off' 

        Parameters: 
            mode (str): requested mode, ``on`` or ``off``

         Returns:
            None

        Example:
            >>> client.set_streaming('on')
            None
        """
        api_allego.set_stream_state(ALLEGO_CORE_ADDR, StreamMode.parse(mode))

    def set_recording(self, mode: str | int | bool | RecordMode) -> AllegoState:
        """
        Sets signal recording to 'on' or 'off' 

        Parameters: 
            mode (str): requested mode, ``on`` or ``off``

        Returns:
            None

        Side Effect:
            sets streaming on if `mode=``on`` and streaming is off

        Example:
            >>> client.set_recording('on')
            `AllegoState`
        """
        api_allego.set_record_state(ALLEGO_CORE_ADDR, RecordMode.parse(mode))

    def set_recording_config(self, datasource_path: str, datasource_name: str, datasource_idx: int, is_time_stamp: bool = True) -> None:
        """
        Sets recording configuration

        Parameters: 
            datasource_path (str): path to output XDAT file set
            datasource_name (str): base name of XDAT file set
            datasource_idx (int): index number for the composed file name.
            is_time_stamp (bool): `True` to time stamp the composed file name.

        Returns:
            None

        Example:
            >>> client.set_recording_config('~/radix/data', 'my_base_name', 0, True)
            None
        """
        return api_allego.set_recording_config(ALLEGO_CORE_ADDR, datasource_name, datasource_path, datasource_idx, is_time_stamp)

    def set_digital_out_manual(self, dout1_state: bool, dout2_state: bool) -> None:
        """
        Sets digital out state.

        Parameters:
            dout1_state (bool): new dout 1 state
            dout2_state (bool): new dout 2 state

        Returns:
            None

        Example:
            >>> client.set_digital_out_manual(true, false)
            None

        """
        return api_allego.set_digital_out_manual(ALLEGO_CORE_ADDR, dout1_state, dout2_state)
