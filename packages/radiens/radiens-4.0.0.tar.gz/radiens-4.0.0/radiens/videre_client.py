from collections.abc import Iterable
from pathlib import Path

import numpy as np
import pandas as pd
from radiens.api import api_videre
from radiens.api.api_utils.util import (BaseClient, get_dataset_id,
                                        to_radiens_file_type)
from radiens.file_sys_client import FileSystemClient
from radiens.grpc_radiens import common_pb2, datasource_pb2, radiensserver_pb2
from radiens.lib.dataset_metadata import DatasetMetadata
from radiens.lib.summa import SummaAnalysis, SummaStatus
from radiens.metrics_client import MetricsClient
from radiens.signals_client import SignalsClient
from radiens.spike_sorter_client import SpikeSorterClient
from radiens.spikes_client import SpikesClient
from radiens.utils.constants import DEFAULT_HUB_ID, TimeRange
from radiens.utils.enums import ClientType, RadiensFileType, RadiensService
from radiens.utils.interceptors import SessionMetaData
from radiens.utils.util import make_time_range


class VidereClient(BaseClient):
    """
    VidereClient implements the radiens API for offline analysis and visualization.
    It matches and extends the functionality of the Radiens Videre UI app.
    """

    def __init__(self, hub_name=DEFAULT_HUB_ID):
        """
        """
        super().__init__()
        self._default_hub = hub_name
        self._sorter = SpikeSorterClient(self)
        self._spikes = SpikesClient(self)
        self._metrics = MetricsClient(self)
        self._signals = SignalsClient(self)
        self._file_system = FileSystemClient()
        self._meta_cache = {}

        # initialize session metadata
        core_addr = self._server_address(hub_name, RadiensService.CORE)
        SessionMetaData(core_addr=core_addr)

    @property
    def hubs(self) -> dict:
        """
        dict of active radiens hubs, with hub ID as key.
        """
        return self._hubs()

    @property
    def hub(self) -> str:
        """
        Radiens hub for this instance of VidereClient.
        """
        return self._default_hub

    @property
    def id(self) -> str:
        """
        UID of this client session.
        """
        return self._id()

    @property
    def type(self) -> ClientType:
        """
        Returns :py:attr:`~radiens.utils.enums.ClientType.VIDERE`
        """
        return ClientType.VIDERE

    def signal_metrics(self) -> MetricsClient:
        """
        Videre signal metrics API
        """
        return self._metrics

    def spike_sorter(self) -> SpikeSorterClient:
        """
        Videre spike sorter API
        """
        return self._sorter

    def spikes(self) -> SpikesClient:
        """
        Videre spikes API
        """
        return self._spikes

    def signals(self) -> SignalsClient:
        """
        Signals API
        """
        return self._signals

    def _cache_file_meta(self, meta: DatasetMetadata):
        self._meta_cache[meta.id] = meta

    def _uncache_file_meta(self, id: str | DatasetMetadata):
        if isinstance(id, DatasetMetadata):
            id = id.id
        self._meta_cache.pop(id, None)

    def list_dir(self, req_dir: str | Path | Iterable[str | Path] = "", sort_by="date", include="all", hub_name=DEFAULT_HUB_ID) -> pd.DataFrame:
        """
            Lists Radiens recording and/or spikes files that are in the requested directory. This function is a wrapper around the file system client. See :py:meth:`FileSystemClient.list_dir` for more details.
        """
        return self._file_system.list_dir(req_dir, sort_by=sort_by, include=include, hub_name=hub_name)

    def link_data_file(self, path:  str | Path, ftype: str | RadiensFileType = None, calc_metrics: bool = True, force: bool = False, hub_name=DEFAULT_HUB_ID, link_spikes: bool = True) -> DatasetMetadata:
        """
            Links a Radiens data file to the Radiens hub and returns the data set meta data.
            If force=False (default) and the 'path' is already linked then nothing is done and existing data set meta data is returned.
            Use force=True to always link the source as a new dataset. All instances of a linked data set are backed by the same data files.

            Parameters:
                path (str, pathlib.Path): path to source file
                ftype (str, RadiensFileType) optional: file type (default=None, inferred from file extension)
                calc_metrics (bool) optional: use True to calculate signal metrics (default=True)
                force (bool) optional: use True to force the source to be linked to the hub (default=False)
                hub_name (str) optional: radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

            Returns:
                data_source (DatasetMetadata): data file metadata

            See Also:
                :py:meth:`rename_file`
                :py:meth:`clear_dataset()`
                :py:meth:`get_dataset_ids()`
        """
        path = Path(path).expanduser().resolve()
        if ftype is None or ftype == "":
            if path.suffix == '':
                raise ValueError(
                    'File type must be specified if path has no extension')
            ftype = path.suffix
        req = datasource_pb2.DataSourceSetSaveRequest(
            path=str(path.parent),
            baseName=path.stem,
            fileType=RadiensFileType.parse(ftype).value,
            dsourceID=path.stem + self.id,
            isBackgroundKPI=calc_metrics,
            isForce=force,
            forceNoSorter=True,
        )
        dataset_meta, associated_spikes = api_videre.set_datasource(
            self._server_address(hub_name, RadiensService.CORE), req)
        self._cache_file_meta(dataset_meta)

        if link_spikes:
            for spike_path in associated_spikes:
                req = datasource_pb2.DataSourceSetSaveRequest(
                    path=str(spike_path.parent),
                    baseName=spike_path.stem,
                    fileType=to_radiens_file_type(spike_path).value,
                    dsourceID=spike_path.stem,
                    isBackgroundKPI=False,
                    isForce=force,
                )
                spike_meta, _ = api_videre.set_datasource(
                    self._server_address(hub_name, RadiensService.CORE), req)
                self._cache_file_meta(spike_meta)
        return dataset_meta

    def _parse_time_range(self, dataset_id: str, time_range: TimeRange | list = None) -> TimeRange:
        if isinstance(time_range, TimeRange):
            return time_range
        else:
            meta = self._get_file_meta_from_id(dataset_id)
            if not isinstance(time_range, list):
                return meta.time_range
            else:
                return make_time_range(time_range, fs=meta.time_range.fs)

    def get_data_file_metadata(self, dataset_idx: int = None, dataset_id: str = None, path: str | Path = None, hub_name=DEFAULT_HUB_ID, fail_hard=False) -> DatasetMetadata:
        """
            Returns meta data for one Radiens dataset or file.  The dataset can be requested by index, ID or full path, in that order of preference.

            Parameters:
                dataset_idx (int): index of dataset in table returned by :py:meth:`get_dataset_ids`
                dataset_id (str): dataset ID as listed in table returned by :py:meth:`get_dataset_ids` 
                path (str, pathlib.Path): full path to data file set in form of `path/base_name.ext`.
                hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)
                fail_hard (bool): if True, then an exception is raised if the requested dataset is not available.

            Returns:
                dataset_meta (DatasetMetadata): data set metadata

            Side Effects:
                If the requested dataset is specified by `path`, then it is linked to the hub and remains linked.

            See Also:
                :py:meth:`rename_file`
                :py:meth:`_clear_dataset`
                :py:meth:`get_dataset_ids`
        """
        dataset_id, path = get_dataset_id(self.get_dataset_ids(), self.id, hub_name, dataset_idx=dataset_idx,
                                          dataset_id=dataset_id, path=path, fail_hard=fail_hard)
        if dataset_id is not None:
            if path is None:
                return self._get_file_meta_from_id(dataset_id, force_refresh=True, hub_name=hub_name)
            else:
                req = datasource_pb2.DataSourceSetSaveRequest(path=str(path.expanduser().resolve().parent), baseName=path.stem, fileType=to_radiens_file_type(
                    path).value, isBackgroundKPI=False, isForce=False)
                return api_videre.set_datasource(self._server_address(hub_name, RadiensService.CORE), req)
        raise ValueError('No dataset found')

    def _get_file_meta_from_id(self, dataset_id: str, force_refresh=False, hub_name=DEFAULT_HUB_ID) -> DatasetMetadata:
        if not force_refresh and dataset_id in self._meta_cache:
            return self._meta_cache[dataset_id]
        else:
            req = datasource_pb2.DataSourceSetSaveRequest(
                dsourceID=dataset_id,
                isBackgroundKPI=False,
                isForce=False,
            )
            meta, _ = api_videre.set_datasource(
                self._server_address(hub_name, RadiensService.CORE), req)
            self._cache_file_meta(meta)
            return meta

    def clear_dataset(self, dataset_idx: int = None, dataset_id: str = None, path: str | Path = None, hub_name=DEFAULT_HUB_ID, fail_hard=False) -> any:
        """
            Clears one or more datasets of this Curate session from the Radiens hub.
            Use dataset_id='all' to clear all session datasets.
            This is a power user function.

            Parameters:
                source (str, list) optional: data source file or list of data source files.
                dataset_id (str, list) optional: dataset ID or list of dataset IDs (default=[], 'all' clears all datasets for the Curate session)
                hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

            Returns:
                num_unlinked (int): number of unlinked datasets
                dataset_ids (pandas.DataFrame): linked dataset IDs on the Radiens hub.

            See Also:
                :py:meth:`link_data_file()`
                :py:meth:`get_dataset_ids()`
        """
        available_dataset_ids = self.get_dataset_ids()
        if dataset_id == 'all' or dataset_idx == 'all':
            dataset_id = available_dataset_ids['dataset ID'].values
            api_videre.unlink_datasource(self._server_address(
                hub_name, RadiensService.CORE), dataset_id)
            for dset_id in dataset_id:
                self._uncache_file_meta(dset_id)
        else:
            dataset_id, _ = get_dataset_id(available_dataset_ids, self.id, hub_name, dataset_idx=dataset_idx,
                                           dataset_id=dataset_id, path=path, fail_hard=fail_hard)
            if dataset_id is not None:
                api_videre.unlink_datasource(self._server_address(
                    hub_name, RadiensService.CORE), [dataset_id])
                self._uncache_file_meta(dataset_id)
        new_avail = self.get_dataset_ids(hub_name=hub_name)
        return len(available_dataset_ids)-len(new_avail), new_avail

    def get_dataset_ids(self, hub_name=DEFAULT_HUB_ID) -> pd.DataFrame:
        """
            Returns sorted list of linked dataset IDs on the Radiens hub.

            Returns:
                dataset_ids (pandas.DataFrame): linked dataset IDs on the Radiens hub.

            See Also:
                :py:meth:`link_data_file()`
                :py:meth:`clear_dataset()`
        """
        resp = api_videre.list_datasource_ids(
            self._server_address(hub_name, RadiensService.CORE))
        df = pd.DataFrame({'dataset ID': resp, 'base name': [x[:x.find('_-_')]
                                                             for x in resp]}).sort_values(by='dataset ID', axis=0).reset_index(drop=True)
        df.index.name = 'index'
        return df

    def dashboard(self, close: bool = False, hub_name=DEFAULT_HUB_ID) -> None:
        """
            Launches a dashboard for the Radiens Hub

            Returns:
                None
        """
        args = common_pb2.DashboardCommandRequest.Args(
            cmd=common_pb2.DASH_CMD_CLOSE) if close else common_pb2.DashboardCommandRequest.Args(cmd=common_pb2.DASH_CMD_OPEN)
        req = common_pb2.DashboardCommandRequest(
            args=args, dashType=common_pb2.DASH_1)
        api_videre.command_dashboard(
            self._server_address(hub_name, RadiensService.DASH), req)

    def summa_list_sessions(self, hub_name=DEFAULT_HUB_ID) -> None:
        """
            Lists the current Summa analysis sessions for the Radiens Hub

            Returns:
                None
        """
        return api_videre.summa_list_sessions(self._server_address(hub_name, RadiensService.DASH), common_pb2.StandardRequest())

    def summa_clear_sessions(self, hub_name=DEFAULT_HUB_ID) -> None:
        """
            Lists the current Summa analysis sessions for the Radiens Hub

            Returns:
                None
        """
        return api_videre.summa_clear_sessions(self._server_address(hub_name, RadiensService.DASH), common_pb2.StandardRequest())

    def summa_launch_session_analysis(self, summa_id: str = None, dataset_ids: list = None, bin_dur_sec: float = 1.0,  hub_name=DEFAULT_HUB_ID) -> None:
        """
            Launches a new Summa analysis session.

            Returns:
                status (SummaStatus): Summa analysis status.
        """
        if not isinstance(dataset_ids, list):
            raise ValueError('dataset_ids must be a list')
        req = radiensserver_pb2.SummaAnalysisRequest(
            summaID='default' if summa_id is None else summa_id,
            dsourceIDs=dataset_ids,
            pktDurSec=bin_dur_sec,
        )
        return SummaAnalysis(api_videre.summa_launch_session_analysis(self._server_address(hub_name, RadiensService.DASH), req)).status

    def summa_session_status(self, summa_id: str = None, hub_name=DEFAULT_HUB_ID) -> None:
        """
            Launches a dashboard for the Radiens Hub

            Returns:
                None
        """
        req = radiensserver_pb2.SummaAnalysisRequest(
            summaID='default' if summa_id is None else summa_id,
            reqPart='',
        )
        resp = api_videre.summa_get_session_analysis(
            self._server_address(hub_name, RadiensService.DASH), req)
        return SummaStatus(resp.state)

    def summa_get_session_aggregate_statistics(self, summa_id: str = None, hub_name=DEFAULT_HUB_ID) -> None:
        """
            Launches a dashboard for the Radiens Hub

            Returns:
                None
        """
        req = radiensserver_pb2.SummaAnalysisRequest(
            summaID='default' if summa_id is None else summa_id,
            reqPart='agg',
        )
        return SummaAnalysis(api_videre.summa_get_session_analysis(self._server_address(hub_name, RadiensService.DASH), req))

    def summa_get_session_datasource_statistics(self, summa_id: str = None, dataset_ids: list = None, hub_name=DEFAULT_HUB_ID) -> None:
        """
            Launches a dashboard for the Radiens Hub

            Returns:
                None
        """
        dsrc_part = 'dsource:'
        if dataset_ids is None or len(dataset_ids) == 0:
            dsrc_part += 'all'
        else:
            for dset_id in dataset_ids:
                dsrc_part += '{},'.format(dset_id)
        req = radiensserver_pb2.SummaAnalysisRequest(
            summaID='default' if summa_id is None else summa_id,
            reqPart=dsrc_part,
        )
        return SummaAnalysis(api_videre.summa_get_session_analysis(self._server_address(hub_name, RadiensService.DASH), req))
