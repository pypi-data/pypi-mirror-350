from pathlib import Path

import pandas as pd
from radiens.grpc_radiens import datasource_pb2
from radiens.lib.dataset_metadata import DatasetFileSet
from radiens.utils.constants import TIME_SPEC


class FileSysResponse():
    '''
    Radiens data file set information.
    '''

    def __init__(self, raw_msg: datasource_pb2.CpRmMvLsReply):
        """
        """

        self._num_files = raw_msg.numFiles
        self._num_dsrc = raw_msg.numDsource
        self._num_bytes = raw_msg.numBytes
        self._msg = raw_msg.msg
        self._dsrc: list[DatasetFileSet] = []
        for dsource in raw_msg.dsource:
            self._dsrc.append(DatasetFileSet(dsource))

    @property
    def total_num_files(self) -> int:
        """
        Number of files touched involved with the OS command. It may be greater than or equal to "num_data_sources". 
        """
        return self._num_files

    @property
    def num_data_sources(self) -> int:
        """
        Number of Radiens data sources involved with the OS command. 
        """
        return self._num_dsrc

    @property
    def num_bytes(self) -> int:
        """
        Number of bytes processed across all files by the OS command
        """
        return self._num_bytes

    @property
    def cmd_msg(self) -> str:
        """
        Result message from the OS command
        """
        return self._msg

    @property
    def datasources(self) -> list[DatasetFileSet]:
        """
        List of data sources (aka data file sets) resulting from the OS command.
        """
        return self._dsrc

    @property
    def datasource_table(self) -> pd.DataFrame:
        """
        Table describing channel metadata (index, position, channel type, units, etc)
        """
        d = {'path': [], 'base_name': [], 'type': [], 'dataset_uid': [], 'num_files': [],
             'bytes_primary_data': [], 'bytes_meta_data': [], 'bytes_total': [],
             'timestamp': [], 'num_chan': [], 'dur_sec': [],
             'samp_freq': [], 'checksum': [], 'provenance': []}
        for dsource in self._dsrc:
            d['path'].append(dsource.descriptor.path)
            d['base_name'].append(dsource.descriptor.base_name)
            d['type'].append(dsource.descriptor.file_type)
            d['dataset_uid'].append(dsource.stat.dataset_spec['uid'])
            d['num_files'].append(dsource.stat.num_files)
            d['bytes_primary_data'].append(
                dsource.stat.num_bytes['primary_data'])
            d['bytes_meta_data'].append(dsource.stat.num_bytes['meta_data'])
            d['bytes_total'].append(dsource.stat.num_bytes['total'])
            d['timestamp'].append(dsource.stat.timestamp.strftime(TIME_SPEC))
            d['num_chan'].append(dsource.stat.num_chan)
            d['dur_sec'].append(dsource.stat.dur_sec)
            d['samp_freq'].append(dsource.stat.samp_freq)
            d['checksum'].append(dsource.stat.dataset_spec['checksum'])
            d['provenance'].append(dsource.stat.dataset_spec['provenance'])
        return pd.DataFrame(d)

    def append(self, resp: any):
        """
        appends a FileSysResponse object to the receiver (system reserved)
        """
        if not isinstance(resp, FileSysResponse):
            raise TypeError('resp must be FileSysResponse')
        if len(resp.data_sources) == 0:
            return
        self._num_files = resp.total_num_files
        self._num_dsrc = resp.num_data_sources
        self._num_bytes = resp.num_bytes
        self._msg += ':{}'.format(resp.cmd_msg)
        for dsource in resp.data_sources:
            self._dsrc.append(dsource)
