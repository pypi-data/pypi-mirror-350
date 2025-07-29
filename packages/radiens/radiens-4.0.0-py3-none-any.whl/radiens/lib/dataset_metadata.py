import datetime
import json

import pandas as pd
from radiens.api.api_utils.util import ext_to_radiens_file_type, to_file_ext
from radiens.grpc_radiens import allegoserver_pb2, common_pb2, datasource_pb2
from radiens.lib.channel_metadata import ChannelMetadata
from radiens.utils.constants import TimeRange
from radiens.utils.enums import RadiensFileType, SignalType
from radiens.utils.util import generic_repr, make_time_range


class FileSetDescriptor():
    '''
    Radiens data file descriptor.
    '''

    def __init__(self, raw_msg=None):
        """
        """
        self._path = None
        self._base_name = None
        self._file_type = None
        self._file_uid = None
        self._dsource_idx = 0
        self._timestamp = ''
        if not raw_msg is None:
            self._path = raw_msg.path
            self._base_name = raw_msg.baseName
            self._file_type = to_file_ext(raw_msg.fileType)
            self._file_uid = raw_msg.fileNameUID

    @property
    def path(self) -> str:
        """
        Path to Radiens data file set.
        """
        return self._path

    @property
    def base_name(self) -> str:
        """
        Base name of Radiens data file set.
        """
        return self._base_name

    @property
    def file_type(self) -> str:
        """
        File type of Radiens data file set.
        """
        return self._file_type

    @property
    def file_uid(self) -> any:
        """
        File set UID (optional). Returns None if no index will be appended
        """
        return self._file_uid

    @property
    def file_name_index(self) -> any:
        """
        Index appended to the base file name (optional). Returns None if no index will be appended.
        """
        return self._dsource_idx

    @property
    def file_name_timestamp(self) -> any:
        """
        Returns True if timestamp is appended to the file name.
        """
        return self._timestamp

    def set_from_rec_cfg(self, msg: allegoserver_pb2.ConfigRecording):
        self._path = msg.baseFilePath
        self._base_name = msg.baseFileName
        self._file_type = to_file_ext(common_pb2.XDAT)
        self._dsource_idx = msg.dataSourceIdx
        self._timestamp = msg.timeStamp


class FileSetStat():
    '''
    Radiens data file set summary status.
    '''

    def __init__(self, raw_msg: datasource_pb2.DataSourceFileSetStat):
        """
        """
        self._num_files = raw_msg.numFiles
        self._num_bytes_primary_data = raw_msg.numBytesPrimaryData
        self._num_bytes_meta_data = raw_msg.numBytesMetaData
        self._num_bytes_total = raw_msg.numBytes
        self._is_metadata = raw_msg.isMetadataFile
        self._timestamp = raw_msg.timeStamp.ToDatetime()
        self._num_chan = raw_msg.numChannels
        self._dur_sec = raw_msg.durationSec
        self._dset_spec = {'uid': raw_msg.datasetUID,
                           'checksum': raw_msg.datasetChecksum, 'provenance': []}
        for prov in raw_msg.datasetProvenance:
            self._dset_spec['provenance'].append(prov)
        self._fs = raw_msg.sampleRate
        self._background_proc = None
        if raw_msg.backgroundProc is not None:
            self._background_proc = {'id': raw_msg.backgroundProc.uID,
                                     'frac_complete': raw_msg.backgroundProc.fracComplete,
                                     'elapsed_time_sec': raw_msg.backgroundProc.elapsedTimeSec,
                                     'est_time_completion_walltime': raw_msg.backgroundProc.estimatedCompletionWallTime}

    @ property
    def num_files(self) -> int:
        """
        Number of files in the file set.
        """
        return self._num_files

    @ property
    def num_bytes(self) -> dict:
        """
        Number of bytes in file set, keys are "primary_data", "meta_data", and "total"
        """
        return {'primary_data': self._num_bytes_primary_data, 'meta_data': self._num_bytes_meta_data, 'total': self._num_bytes_total}

    @ property
    def has_meta_data_file(self) -> bool:
        """
        Flag for existence of Radiens meta data file.
        """
        return self._is_metadata

    @ property
    def timestamp(self) -> datetime.datetime:
        """
        File set time stamp.
        """
        return self._timestamp

    @ property
    def num_chan(self) -> int:
        '''
        Total number of channels in the data file of all signal types, i.e., all amp, gpio-ain, gpio-din, and gpio-dout channels.
        '''
        return self._num_chan

    @ property
    def dur_sec(self) -> float:
        '''
        Duration of file set in seconds.
        '''
        return self._dur_sec

    @ property
    def dataset_spec(self) -> dict:
        '''
        Dataset specifications, with keys = "uid", "checksum", "provenance"
        '''
        return self._dset_spec

    @ property
    def samp_freq(self) -> float:
        '''
        Dataset sample frequency in samples/sec.
        '''
        return self._fs

    @ property
    def fs(self) -> float:
        '''
        Aliaes `dataset.samp_freq`.
        '''
        return self._fs

    @ property
    def background_proc(self) -> dict:
        '''
        Background processing specifications (system reserved)
        '''
        return self._background_proc


class DatasetFileSet():
    '''
    '''

    def __init__(self, raw_msg: datasource_pb2.CpRmMvLsReply.DataSourceInfo):
        """
        Summary information on the file set of one Radiens dataset.
        """
        self._desc = FileSetDescriptor(raw_msg.desc)
        self._stat = FileSetStat(raw_msg.stat)

    @ property
    def descriptor(self) -> FileSetDescriptor:
        """
        File set descriptor providing path, base name, and file type.
        """
        return self._desc

    @ property
    def stat(self) -> FileSetStat:
        """
        File set summary status including duration, number of channels, etc.
        """
        return self._stat


class DatasetMetadata():
    '''
    '''

    def __init__(self, raw_msg: datasource_pb2.DataSourceSetSaveReply = None):
        """
            Meta data describing one Radiens data file or dataset.
        """
        self._d = {'dsource_id': '',
                   'kpi_dsource_id': '',
                   'TR': make_time_range(time_range=[0, 0], fs=1.0),
                   'channel_metadata': ChannelMetadata(),
                   'dataset_uid': '',
                   'source_type': '',
                   'file_type': '',
                   'source_mode': '',
                   'label': '',
                   'path': '',
                   'base_name': ''}
        if raw_msg is None:
            return

        if len(raw_msg.status.tR.timestamp) == 2 and len(raw_msg.status.tR.timeRangeSec) == 2:
            tr = make_time_range(pbTR=raw_msg.status.tR)
        else:  # deprecated, but for backward compatibility atm
            tr = make_time_range(timestamp=list(raw_msg.status.timestampRange),
                                 time_range=list(raw_msg.status.timeRange),
                                 fs=float(raw_msg.status.sampleFreq))

        self._d = {'dsource_id': raw_msg.dsourceID,
                   'kpi_dsource_id': raw_msg.status.kpiDsourceID,
                   'TR': tr,
                   'channel_metadata': ChannelMetadata(raw_msg.status.signalGroup),
                   'dataset_uid': raw_msg.status.uid,
                   'source_type': raw_msg.status.dataSourceType,
                   'file_type': RadiensFileType.parse(raw_msg.status.fileType),
                   'source_mode': raw_msg.status.mode,
                   'label': raw_msg.status.label,
                   'path': raw_msg.status.path,
                   'base_name': raw_msg.status.baseFileName}

    @ property
    def id(self) -> str:
        """
        Dataset ID of this DataSource the Radiens hub.  `None` indicates that it is not on a hub.
        """
        return self._d['dsource_id']

    @ property
    def time_range(self) -> TimeRange:
        """
        Dataset time range (:py:class:`~radiens.utils.constants.TimeRange`)
        """
        return self._d['TR']

    @ property
    def TR(self) -> TimeRange:
        """
        Alias for `time_range`.
        """
        return self._d['TR']

    @ property
    def channel_metadata(self) -> ChannelMetadata:
        """
        Dataset's ChannelMetadata, which describes the dataset's signals (aka channels), probes, positions, etc.
        """
        return self._d['channel_metadata']

    @ property
    def attributes(self) -> dict:
        """
        Dataset attributes.
        """
        return self._d

    @ property
    def path(self) -> str:
        """
        File system path of the Radiens data file set that backs this DataSource.
        """
        return self._d['path']

    @ property
    def base_name(self) -> str:
        """
        File system base name of the Radiens data file set that backs this DataSource.
        """
        return self._d['base_name']

    @ property
    def file_type(self) -> RadiensFileType:
        """
        File type of the Radiens data file set that backs this DataSource.
        """
        return self._d['file_type']

    @ property
    def table(self) -> pd.DataFrame:
        """
        Dataset attributes as a table.
        """
        return pd.DataFrame({'path': [self.path],
                             'name': [self.base_name],
                             'type': [self._d['file_type'].name],
                             'time range (sec)': ['[{:.3f}, {:.3f}]'.format(*self.time_range.sec)],
                             'duration (sec)': ['{:.3f}'.format(self.time_range.dur_sec)],
                             'channels': [self.channel_metadata.num_sigs(SignalType.AMP)],
                             'gpio': [[self.channel_metadata.num_sigs(SignalType.AIN), self.channel_metadata.num_sigs(SignalType.DIN), self.channel_metadata.num_sigs(SignalType.DOUT)]],
                             'sample freq': ['{:.0f}'.format(self.time_range.fs)],
                             'dataset UID': [self._d['dataset_uid']],
                             'label': [self._d['label']],
                             'hub ID (mutable)': [self.id]}).T.rename({0: 'Value'}, axis='columns')

    def __str__(self) -> str:
        return self.table.__str__()

    def __repr__(self) -> str:
        return self.table.__repr__()

    def clear_dataset_id(self) -> None:
        """
        Clears this DataSource's dataset ID by setting it to None.
        This is a power user function. Best practice is to call it when the dataset has been cleared from the Radiens hub.

        """
        self._d['dataset_id'] = None
