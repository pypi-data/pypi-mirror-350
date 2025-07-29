
from collections import namedtuple

from radiens.utils.enums import RadiensFileType

### constants ##
##
##
REGION = 'us-east-1'
APP_CLIENT_ID_DEV = '1q4ugfpgijro91l1cjdhau60cq'
aPP_CLIENT_ID_PROD = '62hgblnnv0dbfrsqad03ub44td'
SERVER_NAME_WINDOWS = 'radiensserver.exe'

ERROR_COLOR_BG = 'black'
ERROR_COLOR_FG = 'red'


MAX_GRPC_MSG_BYTES = 4 * 1024 * 1024  # 4MB
MSG_OVERHEAD_BYTES = 10 * 1024  # 10 KB for metadata seems to work
BYTES_PER_SAMPLE = 4  # float32 representation on server
MAX_SIG_CHUNK_SIZE_BYTES = MAX_GRPC_MSG_BYTES - MSG_OVERHEAD_BYTES

TIME_SPEC = "%Y-%m-%d %H:%M:%S"

DEFAULT_IP = 'localhost'
DEFAULT_HUB_ID = 'default'


# ports
ALLEGO_CORE_PORT = 50051
PCACHE_PORT = 50052
KPI_PORT = 50053
NEURONS1_PORT = 50054

# default server addresses
ALLEGO_CORE_ADDR = '{}:{}'.format(DEFAULT_IP, ALLEGO_CORE_PORT)
PCACHE_ADDR = '{}:{}'.format(DEFAULT_IP, PCACHE_PORT)
KPI_ADDR = '{}:{}'.format(DEFAULT_IP, KPI_PORT)
NEURONS1_ADDR = '{}:{}'.format(DEFAULT_IP, NEURONS1_PORT)

MAX_PB_MSG_SIZE_BYTES = 60e6  # actually limit is 64MB


# only allego stream group
PRIMARY_CACHE_STREAM_GROUP_ID = 'Live Signals'
NEURONS_SINK_DSOURCE_ID = 'sorter-sink:primary_cache'
SPIKE_SORTER_ID = PRIMARY_CACHE_STREAM_GROUP_ID

# sensors
HEADSTAGE_ALIAS = {'smart-16': 'acute_smartlink_A16', 'smart-32': 'chronic_smartlink_CM32',
                   'pass-32': 'passthrough_32',  'pass-64': 'passthrough_64', 'chronic-64': 'chronic_smartlink_H64'}

PROBE_ALIAS = {'v1x16-16': 'v1x16_edge_10mm200_177', '4x8-32': 'a4x8_5mm100_200_177',
               '8x1tet-32': 'a8x1_tet_7mm_200_121',  'buz-32': 'buz32', 'poly3-32': 'a1x32_poly3_8mm50s_177',
               ' poly5-32': 'a1x32_poly5_6mm35s_100',  '8x8-64': 'a8x8_5mm200_200_413', 'poly3-64': 'v1x64_poly3_10mm25s_177',
               'buz-64': 'buz64'}

DEFAULT_STIM_PARAMS = {'stim_shape': 'BIPHASIC',
                       'stim_polarity': 'CATHODIC_FIRST',
                       'first_phase_duration_us': 100,
                       'second_phase_duration_us': 100,
                       'interphase_delay_us': 100,
                       'first_phase_amplitude_uA': 0,
                       'second_phase_amplitude_uA': 0,
                       'baseline_voltage': 0,
                       'trigger_edge_or_level': 'ST_EDGE',
                       'trigger_high_or_low': 'ST_HIGH',
                       'enabled': False,
                       'post_trigger_delay_us': 0,
                       'pulse_or_train': 'SINGLE_PULSE',
                       'number_of_stim_pulses': 2,
                       'pulse_train_period_us': 10000,
                       'refactory_period_ms': 1,
                       'pre_stim_amp_settle_us': 0,
                       'post_stim_amp_settle_us': 0,
                       'maintain_amp_settle_us': False,
                       'enable_amp_settle': False,
                       'post_stim_charge_recovery_on_us': 0,
                       'post_stim_charge_recovery_off_us': 0,
                       'enable_charge_recovery': False,
                       'trigger_source_is_keypress': False,
                       'trigger_source_idx': 0}


# named tuples

SitePosition = namedtuple("SitePosition", [
    'probe_x', 'probe_y', 'probe_z', 'tissue_x', 'tissue_y', 'tissue_z'])
TimeRange = namedtuple(
    "TimeRange", ['sec', 'timestamp', 'fs', 'dur_sec', 'walltime', 'N'])

NeighborsDesc = namedtuple('NeighborsDescriptor', ['radius_um', 'ntv_idxs', 'distance_um', 'theta_deg',
                                                   'phi_deg', 'N', 'pos'])
NeuronDesc = namedtuple('NeuronDescriptor', ['id', 'ntv_idx', 'label', 'pos', 'spike_count',
                                             'spike_rate', 'mean_abs_peak_waveform', 'snr', 'metadata'])
NeuronExtendedMetadata = namedtuple(
    'NeuronExtendedMetadata', ['neuron_uid', 'ensemble_uid', 'func_assembly_uid', 'dataset_uid', 'probe_uid'])

SignalArrays = namedtuple(
    "SignalArrays", ['amp', 'gpio_ain', 'gpio_din', 'gpio_dout'])

#: Python object with keys of type `ntv`, `dset`, `sys`. See :py:class:`~radiens.utils.enums.KeyIndex` for more details
KeyIdxs = namedtuple("KeyIdxs", ['ntv', 'dset', 'sys', ])

SigSelect = namedtuple(
    "SigSelect", ['amp', 'gpio_ain', 'gpio_din', 'gpio_dout', 'key_idx'])
''' SigSelect is used for selecting signals by the given key index type, `key_idx`. The elements are numpy arrays '''

CONVERTIBLE_RADIENS_FILE_TYPES = [
    RadiensFileType.CSV,
    RadiensFileType.XDAT,
    RadiensFileType.KILOSORT2,
    RadiensFileType.NWB,
    RadiensFileType.NEX5,
]

ALL_SITES = -2
SELECTED_SITES = -3
