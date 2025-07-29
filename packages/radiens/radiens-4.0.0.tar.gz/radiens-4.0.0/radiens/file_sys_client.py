from collections.abc import Iterable
from pathlib import Path

import pandas as pd
from radiens.api import api_curate, api_videre
from radiens.api.api_utils.util import BaseClient, to_radiens_file_type
from radiens.grpc_radiens import common_pb2, datasource_pb2
from radiens.lib.dataset_metadata import DatasetMetadata
from radiens.lib.fsys import FileSysResponse
from radiens.utils.constants import DEFAULT_HUB_ID
from radiens.utils.enums import RadiensService
from radiens.utils.interceptors import SessionMetaData


class FileSystemClient(BaseClient):
    """
    Container for Radiens file system commands.
    """

    def __init__(self, hub_name=DEFAULT_HUB_ID):
        """ """
        super().__init__()
        core_addr = self._server_address(hub_name, RadiensService.CORE)
        SessionMetaData(core_addr=core_addr)

    @property
    def hubs(self) -> dict:
        """
        dict of active radiens hubs, with hub ID as key.
        """
        return self._hubs()

    @property
    def id(self) -> str:
        """
        UID of this client session.
        """
        return self._id()

    def ls(self, req_dir: str | Path, sort_by="date", hub_name=DEFAULT_HUB_ID) -> FileSysResponse:
        """
        Aliases client.list_dir() to list Radiens recording and/or spikes files that are in the requested directory.

        See Also:
            :py:meth:`list_dir()`
        """
        pArgs = []
        try:
            pArgs = [str(Path(req_dir).expanduser().resolve())]
        except TypeError:
            try:
                for x in req_dir:
                    pArgs.append(str(Path(x).expanduser().resolve()))
            except TypeError:
                raise TypeError(
                    "req_dir must be a str or Path or a list of them")

        return api_curate.dsrc_list_dir(self._server_address(hub_name, RadiensService.CORE), pArgs, sort_by)

    def list_dir(
        self, req_dir: str | Path | Iterable[str | Path] = "", sort_by="date", include="all", hub_name=DEFAULT_HUB_ID
    ) -> pd.DataFrame:
        """
        Lists Radiens recording and/or spikes files that are in the requested directory.

        Parameters:
            req_dir (str, pathlib.Path): requested directory; if empty, `$HOME/radix/data` is used
            sort_by (str): flag to specify the ordering of the returned file list, 'date', 'name', 'size', 'type' (default='date)
            include (str): flag to specify file types, 'recording', 'time-series', 'spikes', 'all' (default='all')
            hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

        Returns:
            file_type (pandas.DataFrame): table of files in the requested directory

        Example:
            >>> client.list_dir("./")
            pandas.DataFrame

        Notes:
            Directory name wildcards are allowed, but must resolve to only one directory.

        See Also:
            :py:meth:`ls`
        """
        if len(req_dir) == 0:
            req_dir = [""]
        elif isinstance(req_dir, (Path, str)):
            req_dir = [req_dir]
        for i, x in enumerate(req_dir):
            if x == "":
                x = Path("~/radix/data").expanduser().resolve()
            req_dir[i] = Path(x).expanduser().resolve()
            if not req_dir[i].is_dir():
                raise ValueError(f"{req_dir[i]} is not a directory")

        dsrc_table = self.ls(req_dir, sort_by, hub_name).datasource_table
        if include != "all":
            dsrc_table = dsrc_table[dsrc_table.type == include]
        return dsrc_table

    def copy_files(
        self, source: any, dest: any, force=False, hub_name=DEFAULT_HUB_ID
    ) -> FileSysResponse:
        """
        Copies one or more Radiens files.

        Parameters:
            source (str, pathlib.Path, list): path to source file(s)
            dest (str, pathlib.Path): path to destination file(s)
            force (bool): flag to force copy if destination file already exists (default=False)
            hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

        Returns:
            file_desc (FileSysResponse): details of the command result

        Example:
            >>> client.copy_files("./my_rec_file.xdat", './targ_dir/new_file')
            FileSysResponse

        Notes:
            The destination file type is always the same as the source file type.
            File name wildcards are allowed, but must resolve to only one file.

        See Also:
            :py:meth:`cp`
        """
        return self.cp(source, dest, force, hub_name)

    def cp(
        self, source: any, dest: any, force=False, hub_name=DEFAULT_HUB_ID
    ) -> FileSysResponse:
        """
        Aliases client.copy_files() to copy one or more Radiens files.

        See Also:
            :py:meth:`copy_files`
        """
        src_one = None
        src_many = None
        if isinstance(source, (Path, str)):
            src_one = Path(source).expanduser().resolve()
        elif isinstance(source, (list, Iterable)):
            src_many = []
            for file in source:
                src_many.append(Path(file).expanduser().resolve())
        else:
            raise ValueError("source must be string, Path, or list")

        if not isinstance(dest, (Path, str)):
            raise ValueError("dest must be string or Path")

        dest = Path(dest).expanduser().resolve()
        if src_one is not None:
            src_desc = common_pb2.FileDescriptor(
                path=str(src_one.parent),
                baseName=src_one.stem,
                fileType=to_radiens_file_type(src_one).value,
            )
            if dest.is_dir():
                dest = Path(dest, src_one.name)
            dest_desc = common_pb2.FileDescriptor(
                path=str(dest.parent), baseName=dest.stem, fileType=to_radiens_file_type(src_one).value)
            req_one = datasource_pb2.CopyRemoveDataSourceFileRequest.OneFile(
                src=src_desc, dest=dest_desc)
            req = datasource_pb2.CopyRemoveDataSourceFileRequest(
                isForce=bool(force), one=req_one)
            return api_curate.dsrc_copy(self._server_address(hub_name, RadiensService.CORE), req)

        # many files
        if not dest.is_dir():
            raise ValueError("dest must be a path when copying multiple files")
        src_desc = []
        for file in src_many:
            src_desc.append(
                common_pb2.FileDescriptor(
                    path=str(file.parent),
                    baseName=file.stem,
                    fileType=to_radiens_file_type(file).value,
                )
            )
        req_many = datasource_pb2.CopyRemoveDataSourceFileRequest.MultipleFiles(
            src=src_desc, destPath=str(dest), destFileType=to_radiens_file_type(Path(file)).value)
        req = datasource_pb2.CopyRemoveDataSourceFileRequest(
            isForce=bool(force), many=req_many)
        return api_curate.dsrc_copy(self._server_address(hub_name, RadiensService.CORE), req)

    def delete_files(self, source: any, hub_name=DEFAULT_HUB_ID) -> FileSysResponse:
        """
        Deletes (aka removes) one or more Radiens files.

        Parameters:
            source (str, pathlib.Path, list): path to source file(s)
            dry_run (bool): flag to list the requested files without deleting them (default=False)
            hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

        Returns:
            file_type (pandas.DataFrame): table of copied files.

        Example:
            >>> client.delete_files("./my_rec_file.xdat")
            pandas.DataFrame

        Notes:
            The requested files are permanently deleted from the file system.
            File name wildcards are allowed, but must resolve to only one file.

        See Also:
            :py:meth:`rm`
        """
        return self.rm(source, hub_name)

    def rm(self, source: any, hub_name=DEFAULT_HUB_ID) -> FileSysResponse:
        """
        Aliases client.delete_files() to delete (aka remove) one or more Radiens files.

        See Also:
            :py:meth:`delete_files`
        """
        src_many = []
        if isinstance(source, (Path, str)):
            src_many = [Path(source).expanduser().resolve()]
        elif isinstance(source, (list, Iterable)):
            for file in source:
                src_many.append(Path(file).expanduser().resolve())
        else:
            raise ValueError("source type must be string, Path, or list")

        src_desc = []
        for file in src_many:
            src_desc.append(common_pb2.FileDescriptor(
                path=str(file.parent), baseName=file.stem, fileType=to_radiens_file_type(file).value))
        req_many = datasource_pb2.CopyRemoveDataSourceFileRequest.MultipleFiles(
            src=src_desc)
        req = datasource_pb2.CopyRemoveDataSourceFileRequest(
            isForce=True, many=req_many)
        return api_curate.dsrc_remove(self._server_address(hub_name, RadiensService.CORE), req)

    def rename_file(
        self, source: any, dest=any, force=False, validate=True, hub_name=DEFAULT_HUB_ID
    ) -> FileSysResponse:
        """
        Renames (aka moves) one Radiens file.

        Parameters:
            source (str, pathlib.Path): path to source file
            dest (str, pathlib.Path): path to destination file
            dry_run (bool): flag to list the requested files without deleting them (default=False)
            force (bool): flag to force renaming if the destination file exists (default=False)
            hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

        Returns:
            file_type (pandas.DataFrame): table of renamed file.

        Example:
            >>> client.rename_files("./my_rec_file.xdat", "./targ_dir/my_rec_file")
            pandas.DataFrame

        Notes:
            The destination file type is the same as the source file type.
            File name wildcards are allowed, but must resolve to only one file.

        See Also:
            :py:meth:`mv`
        """
        return self.mv(source, dest, force, validate, hub_name)

    def mv(
        self, source: any, dest=any, force=True, validate=True, hub_name=DEFAULT_HUB_ID
    ) -> FileSysResponse:
        """
        Aliases client.rename_file() to rename (aka move) one Radiens file.

        See Also:
            :py:meth:`rename_file`
        """
        if isinstance(source, (Path, str)):
            src = Path(source).expanduser().resolve()
        else:
            raise ValueError("source must be string or Path")
        if isinstance(dest, (Path, str)):
            dest = Path(dest).expanduser().resolve()
        else:
            raise ValueError("dest must be string or Path")

        src_desc = common_pb2.FileDescriptor(
            path=str(src.parent), baseName=src.stem, fileType=to_radiens_file_type(src).value
        )
        dest_desc = common_pb2.FileDescriptor(
            path=str(dest.parent), baseName=dest.stem, fileType=to_radiens_file_type(dest).value)
        req = datasource_pb2.MoveDataSourceFileRequest(
            isForce=force, isValidate=validate, src=src_desc, dest=dest_desc)
        return api_curate.dsrc_move(self._server_address(hub_name, RadiensService.CORE), req)

    def link_data_file(
        self, source: any, calc_metrics=False, hub_name=DEFAULT_HUB_ID
    ) -> DatasetMetadata:
        """
        Links a Radiens data file to the Radiens hub as a new dataset.

        Parameters:
            source (str, pathlib.Path): path to source file
            calc_metrics (bool) optional: set True to calculate signal metrics (default=False)
            hub_name (str) optional: radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

        Returns:
            data_source (DatasetMetadata): data file metadata

        See Also:
            :py:meth:`rename_file`
            :py:meth:`_clear_dataset()`
            :py:meth:`get_dataset_ids()`
        """
        if isinstance(source, (Path, str)):
            source = Path(source).expanduser().resolve()
        else:
            raise ValueError("source must be string or Path")
        req = datasource_pb2.DataSourceSetSaveRequest(
            path=str(source.parent),
            baseName=source.stem,
            fileType=to_radiens_file_type(source).value,
            dsourceID=source.stem + self.id,
            isBackgroundKPI=calc_metrics,
        )
        return api_videre.set_datasource(
            self._server_address(hub_name, RadiensService.CORE), req
        )

    def get_data_file_metadata(
        self, source: any, hub_name=DEFAULT_HUB_ID
    ) -> DatasetMetadata:
        """
        Returns the meta data for a Radiens data file.

        Parameters:
            source (str, pathlib.Path): path to source file
            hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

        Returns:
            data_source (DatasetMetadata): data file metadata

        See Also:
            :py:meth:`rename_file`
            :py:meth:`_clear_dataset()`
            :py:meth:`get_dataset_ids()`
        """
        if isinstance(source, (Path, str)):
            source = Path(source).expanduser().resolve()
        else:
            raise ValueError('source must be string or Path')
        req = datasource_pb2.DataSourceSetSaveRequest(path=str(source.parent), baseName=source.stem, fileType=to_radiens_file_type(
            source).value, dsourceID=source.stem+self.id, isBackgroundKPI=False)
        dsrc = api_videre.set_datasource(
            self._server_address(hub_name, RadiensService.CORE), req)
        self._clear_dataset(dsrc.id)
        dsrc.clear_dataset_id()
        return dsrc

    def _clear_dataset(self, source=[], dataset_id=[], hub_name=DEFAULT_HUB_ID) -> str:
        if not isinstance(dataset_id, (list, str, Iterable)):
            raise ValueError("dataset_id must be string or list of strings")
        if isinstance(dataset_id, str):
            dataset_id = [dataset_id]
        if isinstance(source, (str, Path)):
            source = [Path(source)]
        _get_ids = []
        for _id in self._get_dataset_ids(hub_name):
            if len(dataset_id) > 0 and dataset_id[0] == "all" and _id.find(self.id) > 0:
                _get_ids.append(_id)
            else:
                for req_id in dataset_id:
                    if req_id == _id:
                        _get_ids.append(_id)
            for src in source:
                if _id.find(Path(src).stem) > 0 and _id.find(self.id) > 0:
                    _get_ids.append(_id)
        return api_videre.unlink_datasource(
            self._server_address(hub_name, RadiensService.CORE), _get_ids
        )

    def _get_dataset_ids(self, hub_name=DEFAULT_HUB_ID) -> list:
        return api_videre.list_datasource_ids(
            self._server_address(hub_name, RadiensService.CORE)
        )
