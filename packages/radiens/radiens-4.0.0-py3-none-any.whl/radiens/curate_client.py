import time
import uuid
import warnings
from collections.abc import Iterable
from pathlib import Path

import radiens.api.api_curate as api_curate
import radiens.api.api_videre as api_videre
from grpc import RpcError
from radiens.api.api_utils.protocols import (ProtocolAPI, TransformEdge,
                                             TransformNode)
from radiens.api.api_utils.util import (BaseClient, ext_to_radiens_file_type,
                                        to_file_ext, to_radiens_file_type,
                                        to_suffix)
from radiens.exceptions.grpc_error import RpcException
from radiens.file_sys_client import FileSystemClient
from radiens.grpc_radiens import datasource_pb2
from radiens.lib.dataset_metadata import DatasetMetadata
from radiens.metrics_client import MetricsClient
from radiens.spikes_client import SpikesClient
from radiens.utils.constants import (CONVERTIBLE_RADIENS_FILE_TYPES,
                                     DEFAULT_HUB_ID)
from radiens.utils.enums import ClientType, RadiensFileType, RadiensService
from radiens.utils.interceptors import SessionMetaData
from radiens.utils.util import rm_xdat_file
from tqdm.autonotebook import tqdm


class CurateClient(BaseClient):
    """
    CurateClient implements the radiens API for data curation. It matches and extends the functionality of the Radiens Curate UI app.
    """

    def __init__(self, hub_name=DEFAULT_HUB_ID):
        """ """
        super().__init__()
        self._spikes = SpikesClient(self)
        self._metrics = MetricsClient(self)
        self._fsys = FileSystemClient()
        self._dsp_stream = {}

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
    def id(self) -> str:
        """
        UID of this client session.
        """
        return self._id()

    @property
    def type(self) -> ClientType:
        """
        Returns :py:attr:`~radiens.utils.enums.ClientType.CURATE`
        """
        return ClientType.CURATE

    def signal_metrics(self) -> MetricsClient:
        """
        Signal metrics API
        """
        return self._metrics

    def spikes(self) -> SpikesClient:
        """
        Spikes API
        """
        return self._spikes

    @property
    def dsp_stream(self):
        """
        dict of DSP streams running in the background.
        """
        return self._dsp_stream

    def dsp_clean_up(self):
        """
        Cleans up after any DSP operation that has finished.

        Returns:
            None

        Examples:
            >>> stream_id = client.dsp_low_pass_filter(750, './my_source_file', './my_output_file')
            >>> progress_bar(stream_id)

        See Also:
            :py:meth:`dsp_progress`
            :py:meth:`dsp_low_pass_filter`

        """
        to_del = []
        for stream_id in self.dsp_stream:
            if self.dsp_stream[stream_id]["stream"].done():
                to_del.append(stream_id)
        for stream_id in to_del:
            del self.dsp_stream[stream_id]

    def progress_bar(self, stream_id):
        """
        Displays a progress bar showing the progress of the DSP stream running in the background.
        This function blocks until the background DSP stream is complete.
        This is an optional function that does not effect the DSP operation.

        Parameters:
            stream_id (str): stream ID of the requested DSP stream.

        Returns:
            None

        Examples:
            >>> stream_id = client.dsp_low_pass_filter(750, './my_source_file', './my_output_file')
            >>> progress_bar(stream_id)

        See Also:
            :py:meth:`dsp_progress`
            :py:meth:`dsp_low_pass_filter`

        """
        pbar = tqdm(
            total=self.dsp_stream[stream_id]["data_source"].time_range.dur_sec,
            desc=stream_id,
            smoothing=0.9,
            bar_format="{desc}: {percentage:.1f}%|{bar}| {n:.2f}/{total_fmt} [{elapsed}<{remaining}]",
        )
        for progress in self.dsp_stream[stream_id]["stream"]:
            if progress.incrementSec is None:
                warnings.warn(
                    'stream message not available. Returning immediately')
                pbar.close()
                return
            pbar.update(progress.incrementSec)
            if self.dsp_stream[stream_id]["stream"].done():
                pbar.update(progress.incrementSec)
                break
            time.sleep(0.1)
        pbar.close()

    def dsp_progress(self, stream_id):
        """
        Returns the progress of the 'stream_id' DSP stream running in the background.  It returns 1.0 if the DSP operation has completed.
        It is non-blocking.

        Parameters:
            stream_id (str): stream ID of the requested DSP stream.

        Returns:
            frac_complete (float): fraction complete of the DSP stream.

        Examples:
            >>> stream_id = client.dsp_low_pass_filter(750, './my_source_file', './my_output_file')
            >>> dsp_progress(stream_id)
            >>> 0.5

        See Also:
            :py:meth:`dsp_progress_bar`
            :py:meth:`dsp_low_pass_filter`

        """
        if self.dsp_stream[stream_id]["stream"].done():
            return 1.0
        for progress in self.dsp_stream[stream_id]["stream"]:
            if progress.fracComplete is None:
                warnings.warn(
                    'stream message not available. Returning immediately')
                return
            return progress.fracComplete

    def dsp_low_pass_filter(
        self,
        cutoff_freq: float,
        source_path: any,
        target_path: any,
        force=False,
        hub_name=DEFAULT_HUB_ID,
    ) -> str:
        """
        Applies low-pass filter to source file to result in target file.

        The requested cut-off frequency must be < fs/2, where fs is the sample frequency of the source file.

        Parameters:
            cutoff_freq (float): filter cut-off frequency in samples/sec (Hz)
            source_path (str, pathlib.Path): path to source file
            target_path (str, pathlib.Path): path to target (output) file
            force (bool): flag to force replacing target file if it exists
            hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

        Returns:
            stream_id (str): background DSP stream ID

        Notes:
            The source and target files must be XDAT files.
            This is non-blocking and the requested DSP operation runs in the background.

        Example:
            >>> client.dsp_low_pass_filter(750, './my_source_file', './my_output_file')
            my_stream_id_e4c-jnwq

        See Also:
            :py:meth:`dsp_progress`
            :py:meth:`dsp_progress_bar`
            :py:meth:`dsp_high_pass_filter`
        """
        if force:
            rm_xdat_file(Path(target_path))
        protocol = ProtocolAPI('lp_filter')
        protocol.add_node(TransformNode(
            'src_0').datasource_source(Path(source_path)))
        protocol.add_node(TransformNode('filt_lp').lowpass(cutoff_freq))
        protocol.add_edge(TransformEdge(
            'edge_0', protocol.nodes['src_0'].id, protocol.nodes['filt_lp'].id))
        protocol.add_node(TransformNode(
            'targ_0').datasource_sink(Path(target_path)))
        protocol.add_edge(TransformEdge(
            'edge_1', protocol.nodes['filt_lp'].id, protocol.nodes['targ_0'].id))
        self._dsp_stream[protocol.id] = {
            'data_source': self._link_data_file(
                Path(source_path)),
            'protocol': protocol,
            'stream': self._do_protocol(protocol, hub_name),
        }
        self._clear_dataset(source_path)
        self._dsp_stream[protocol.id]["data_source"].clear_dataset_id()
        return protocol.id

    def dsp_high_pass_filter(
        self,
        cutoff_freq: float,
        source_path: str | Path,
        target_path: str | Path,
        force=False,
        hub_name=DEFAULT_HUB_ID,
    ):
        """
        Applies high-pass filter to source file to result in target file.

        The requested cut-off frequency must be < fs/2, where fs is the sample frequency of the source file.

        Parameters:
            cutoff_freq (float): filter cut-off frequency in samples/sec (Hz)
            source_path (str, pathlib.Path): path to source file
            target_path (str, pathlib.Path): path to target (output) file
            force (bool): flag to force replacing target file if it exists
            hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

        Returns:
            stream_id (str): background DSP stream ID

        Notes:
            The source and target files must be XDAT files.
            This is non-blocking and the requested DSP operation runs in the background.

        Example:
            >>> client.dsp_high_pass_filter(20, './my_source_file', './my_output_file')
            None
        """
        if force:
            rm_xdat_file(Path(target_path))
        protocol = ProtocolAPI('hp_filter')
        protocol.add_node(TransformNode(
            'src_0').datasource_source(Path(source_path)))
        protocol.add_node(TransformNode('filt_hp').highpass(cutoff_freq))
        protocol.add_edge(TransformEdge(
            'edge_0', protocol.nodes['src_0'].id, protocol.nodes['filt_hp'].id))
        protocol.add_node(TransformNode(
            'targ_0').datasource_sink(Path(target_path)))
        protocol.add_edge(TransformEdge(
            'edge_1', protocol.nodes['filt_hp'].id, protocol.nodes['targ_0'].id))
        self._dsp_stream[protocol.id] = {'data_source': self._link_data_file(
            Path(source_path)), 'protocol': protocol, 'stream': self._do_protocol(protocol, hub_name)}
        self._clear_dataset(Path(source_path))
        self._dsp_stream[protocol.id]["data_source"].clear_dataset_id()
        return protocol.id

    def dsp_band_pass_filter(
        self,
        low_cutoff_freq: float,
        high_cutoff_freq,
        source_path: any,
        target_path: any,
        force=False,
        hub_name=DEFAULT_HUB_ID,
    ) -> str:
        """
        Applies band-pass filter to source file to result in target file.

        The requested cut-off frequencies must be < fs/2, where fs is the sample frequency of the source file.
        The low_cutoff_freq must be less than the high_cutoff_freq.

        Parameters:
            low_cutoff_freq (float): filter low cut-off frequency in samples/sec (Hz)
            high_cutoff_freq (float): filter high cut-off frequency in samples/sec (Hz)
            source_path (str, pathlib.Path): path to source file
            target_path (str, pathlib.Path): path to target (output) file
            force (bool): flag to force replacing target file if it exists
            hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

        Returns:
            stream_id (str): background DSP stream ID

        Notes:
            The source and target files must be XDAT files.
            This is non-blocking. The requested DSP operation runs in the background.

        Example:
            >>> client.dsp_band_pass_filter(750,  2000, './my_source_file', './my_output_file')
            my_stream_id_e4c-jtyn4

        See Also:
           :py:meth:`dsp_progress`
           :py:meth:`dsp_progress_bar`
           :py:meth:`dsp_high_pass_filter`
        """
        if force:
            rm_xdat_file(Path(target_path))
        protocol = ProtocolAPI('bp_filter')
        protocol.add_node(TransformNode(
            'src_0').datasource_source(Path(source_path)))
        protocol.add_node(TransformNode('filt_bp').bandpass(
            low_cutoff_freq, high_cutoff_freq))
        protocol.add_edge(TransformEdge(
            'edge_0', protocol.nodes['src_0'].id, protocol.nodes['filt_bp'].id))
        protocol.add_node(TransformNode(
            'targ_0').datasource_sink(Path(target_path)))
        protocol.add_edge(TransformEdge(
            'edge_1', protocol.nodes['filt_bp'].id, protocol.nodes['targ_0'].id))
        self._dsp_stream[protocol.id] = {'data_source': self._link_data_file(
            Path(source_path)), 'protocol': protocol, 'stream': self._do_protocol(protocol, hub_name)}
        self._clear_dataset(source_path)
        self._dsp_stream[protocol.id]["data_source"].clear_dataset_id()
        return protocol.id

    def dsp_band_stop_filter(
        self,
        low_cutoff_freq: float,
        high_cutoff_freq,
        source_path: any,
        target_path: any,
        force=False,
        hub_name=DEFAULT_HUB_ID,
    ) -> str:
        """
        Applies band-stop (aka band reject) filter to source file to result in target file.

        The requested cut-off frequencies must be < fs/2, where fs is the sample frequency of the source file.
        The low_cutoff_freq must be less than the high_cutoff_freq.

        Parameters:
            low_cutoff_freq (float): filter low cut-off frequency in samples/sec (Hz)
            high_cutoff_freq (float): filter high cut-off frequency in samples/sec (Hz)
            source_path (str, pathlib.Path): path to source file
            target_path (str, pathlib.Path): path to target (output) file
            force (bool): flag to force replacing target file if it exists
            hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

        Returns:
            stream_id (str): background DSP stream ID

        Notes:
            The source and target files must be XDAT files.
            This is non-blocking. The requested DSP operation runs in the background.

        Example:
            >>> client.dsp_band_stop_filter(750,  2000, './my_source_file', './my_output_file')
            my_stream_id_e4c-jtyn4

        See Also:
           :py:meth:`dsp_progress`
           :py:meth:`dsp_progress_bar`
           :py:meth:`dsp_high_pass_filter`
        """
        if force:
            rm_xdat_file(Path(target_path))
        protocol = ProtocolAPI('bs_filter')
        protocol.add_node(TransformNode(
            'src_0').datasource_source(Path(source_path)))
        protocol.add_node(TransformNode('filt_bs').bandstop(
            low_cutoff_freq, high_cutoff_freq))
        protocol.add_edge(TransformEdge(
            'edge_0', protocol.nodes['src_0'].id, protocol.nodes['filt_bs'].id))
        protocol.add_node(TransformNode(
            'targ_0').datasource_sink(Path(target_path)))
        protocol.add_edge(TransformEdge(
            'edge_1', protocol.nodes['filt_bs'].id, protocol.nodes['targ_0'].id))
        self._dsp_stream[protocol.id] = {'data_source': self._link_data_file(
            Path(source_path)), 'protocol': protocol, 'stream': self._do_protocol(protocol, hub_name)}
        self._clear_dataset(source_path)
        self._dsp_stream[protocol.id]["data_source"].clear_dataset_id()
        return protocol.id

    def dsp_notch_filter(
        self,
        freq: float,
        bandwidth,
        source_path: any,
        target_path: any,
        force=False,
        hub_name=DEFAULT_HUB_ID,
    ) -> str:
        """
        Applies notch filter to source file to result in target file.

        The requested frequency must be < fs/2, where fs is the sample frequency of the source file.

        Parameters:
            freq (float): notch frequency in samples/sec (Hz)
            bandwidth (float): filter bandwidth in samples/sec (Hz)
            source_path (str, pathlib.Path): path to source file
            target_path (str, pathlib.Path): path to target (output) file
            force (bool): flag to force replacing target file if it exists
            hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

        Returns:
            stream_id (str): background DSP stream ID

        Notes:
            The source and target files must be XDAT files.
            This is non-blocking. The requested DSP operation runs in the background.

        Example:
            >>> client.dsp_notch_filter(50,  2, './my_source_file', './my_output_file')
            my_stream_id_e4c-lkqw

        See Also:
           :py:meth:`dsp_progress`
           :py:meth:`dsp_progress_bar`
           :py:meth:`dsp_high_pass_filter`
        """
        if force:
            rm_xdat_file(Path(target_path))
        protocol = ProtocolAPI('notch_filter')
        protocol.add_node(TransformNode(
            'src_0').datasource_source(Path(source_path)))
        protocol.add_node(TransformNode('filt_notch').notch(freq, bandwidth))
        protocol.add_edge(TransformEdge(
            'edge_0', protocol.nodes['src_0'].id, protocol.nodes['filt_notch'].id))
        protocol.add_node(TransformNode(
            'targ_0').datasource_sink(Path(target_path)))
        protocol.add_edge(TransformEdge(
            'edge_1', protocol.nodes['filt_notch'].id, protocol.nodes['targ_0'].id))
        self._dsp_stream[protocol.id] = {'data_source': self._link_data_file(
            Path(source_path)), 'protocol': protocol, 'stream': self._do_protocol(protocol, hub_name)}
        self._clear_dataset(source_path)
        self._dsp_stream[protocol.id]["data_source"].clear_dataset_id()
        return protocol.id

    def dsp_paired_diff(
        self,
        source_chan: int,
        ref_chan: int,
        source_path: any,
        target_path: any,
        force=False,
        hub_name=DEFAULT_HUB_ID,
    ) -> str:
        """
        Applies paired differential transform to the source file resulting in the target file.

        The source channel is set to the new value = (source-reference) for each time sample.
        The reference signal is zeroed.

        Parameters:
            source_chan (int): source channel index
            ref_chan (int): reference channel index
            source_path (str, pathlib.Path): path to source file
            target_path (str, pathlib.Path): path to target (output) file
            force (bool): flag to force replacing target file if it exists
            hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

        Returns:
            stream_id (str): background DSP stream ID

        Notes:
            The source and target files must be XDAT files.
            This is non-blocking. The requested DSP operation runs in the background.

        Example:
            >>> client.dsp_paired_diff(1,  5, './my_source_file', './my_output_file')
            my_stream_id_e4c-rt4m

        See Also:
           :py:meth:`dsp_progress`
           :py:meth:`dsp_progress_bar`
           :py:meth:`dsp_high_pass_filter`
        """
        if force:
            rm_xdat_file(Path(target_path))
        protocol = ProtocolAPI('paired_diff')
        protocol.add_node(TransformNode(
            'src_0').datasource_source(Path(source_path)))
        protocol.add_node(TransformNode(
            'diff').paired_ref(source_chan, ref_chan))
        protocol.add_edge(TransformEdge(
            'edge_0', protocol.nodes['src_0'].id, protocol.nodes['diff'].id))
        protocol.add_node(TransformNode(
            'targ_0').datasource_sink(Path(target_path)))
        protocol.add_edge(TransformEdge(
            'edge_1', protocol.nodes['diff'].id, protocol.nodes['targ_0'].id))
        self._dsp_stream[protocol.id] = {'data_source': self._link_data_file(
            Path(source_path)), 'protocol': protocol, 'stream': self._do_protocol(protocol, hub_name)}
        self._clear_dataset(source_path)
        self._dsp_stream[protocol.id]["data_source"].clear_dataset_id()
        return protocol.id

    def dsp_virtual_ref(
        self,
        ref_chan: int,
        source_path: any,
        target_path: any,
        force=False,
        hub_name=DEFAULT_HUB_ID,
    ) -> str:
        """
        Applies virtual reference transform to the source file resulting in the target file.

        All channels are set to the new value = (chan-ref_chan) for each time sample.
        The reference channel is zeroed.

        Parameters:
            ref_chan (int): reference channel index
            source_path (str, pathlib.Path): path to source file
            target_path (str, pathlib.Path): path to target (output) file
            force (bool): flag to force replacing target file if it exists
            hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

        Returns:
            stream_id (str): background DSP stream ID

        Notes:
            The source and target files must be XDAT files.
            This is non-blocking. The requested DSP operation runs in the background.

        Example:
            >>> client.dsp_virtual_ref(5, './my_source_file', './my_output_file')
            my_stream_id_e4c-wq5c

        See Also:
           :py:meth:`dsp_progress`
           :py:meth:`dsp_progress_bar`
           :py:meth:`dsp_high_pass_filter`
        """
        if force:
            rm_xdat_file(Path(target_path))
        protocol = ProtocolAPI('virtual_ref')
        protocol.add_node(TransformNode(
            'src_0').datasource_source(Path(source_path)))
        protocol.add_node(TransformNode('vref').virtual_ref(ref_chan))
        protocol.add_edge(TransformEdge(
            'edge_0', protocol.nodes['src_0'].id, protocol.nodes['vref'].id))
        protocol.add_node(TransformNode(
            'targ_0').datasource_sink(Path(target_path)))
        protocol.add_edge(TransformEdge(
            'edge_1', protocol.nodes['vref'].id, protocol.nodes['targ_0'].id))
        self._dsp_stream[protocol.id] = {'data_source': self._link_data_file(
            Path(source_path)), 'protocol': protocol, 'stream': self._do_protocol(protocol, hub_name)}
        self._clear_dataset(source_path)
        self._dsp_stream[protocol.id]["data_source"].clear_dataset_id()
        return protocol.id

    def dsp_car(
        self, source_path: any, target_path: any, force=False, hub_name=DEFAULT_HUB_ID
    ) -> str:
        """
        Applies common average reference transform to the source file resulting in the target file.

        All channels are set to the new value = (chan-v_ref) for each time sample, where v_ref is the sum of all the channels.

        Parameters:
            source_path (str, pathlib.Path): path to source file
            target_path (str, pathlib.Path): path to target (output) file
            force (bool): flag to force replacing target file if it exists
            hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

        Returns:
            stream_id (str): background DSP stream ID

        Notes:
            The source and target files must be XDAT files.
            This is non-blocking. The requested DSP operation runs in the background.

        Example:
            >>> client.dsp_car('./my_source_file', './my_output_file')
            my_stream_id_e4c-wq5c

        See Also:
           :py:meth:`dsp_progress`
           :py:meth:`dsp_progress_bar`
           :py:meth:`dsp_high_pass_filter`
        """
        if force:
            rm_xdat_file(Path(target_path))
        protocol = ProtocolAPI('CAR')
        protocol.add_node(TransformNode(
            'src_0').datasource_source(Path(source_path)))
        protocol.add_node(TransformNode('car').car())
        protocol.add_edge(TransformEdge(
            'edge_0', protocol.nodes['src_0'].id, protocol.nodes['car'].id))
        protocol.add_node(TransformNode(
            'targ_0').datasource_sink(Path(target_path)))
        protocol.add_edge(TransformEdge(
            'edge_1', protocol.nodes['car'].id, protocol.nodes['targ_0'].id))
        self._dsp_stream[protocol.id] = {'data_source': self._link_data_file(
            Path(source_path)), 'protocol': protocol, 'stream': self._do_protocol(protocol, hub_name)}
        self._clear_dataset(source_path)
        self._dsp_stream[protocol.id]["data_source"].clear_dataset_id()
        return protocol.id

    def dsp_time_decimate(
        self,
        decimate: int,
        source_path: Path,
        target_path: Path,
        force=False,
        hub_name=DEFAULT_HUB_ID,
    ) -> str:
        """
        Applies time decimation transform to the source file resulting in the target file.

        All channels are decimated in time by 'decimate'.
        The target file sampling frequency is equal to the source file sampling frequency divided by 'decimate'
        For example, if 'decimate=2' and 'source_sampling_freq=10000', then the target file consists of every two source channel samples
        and 'target_sampling_freq=5000'

        Parameters:
            decimate (int): sample factor
            source_path (str, pathlib.Path): path to source file
            target_path (str, pathlib.Path): path to target (output) file
            force (bool): flag to force replacing target file if it exists
            hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

        Returns:
            stream_id (str): background DSP stream ID

        Notes:
            The source and target files must be XDAT files.
            This is non-blocking. The requested DSP operation runs in the background.

        Example:
            >>> client.dsp_time_decimate(3, './my_source_file', './my_output_file')
            my_stream_id_e4c-wq5c

        See Also:
           :py:meth:`dsp_progress`
           :py:meth:`dsp_progress_bar`
           :py:meth:`dsp_high_pass_filter`
        """
        if force:
            rm_xdat_file(Path(target_path))
        protocol = ProtocolAPI('decimate')
        protocol.add_node(TransformNode(
            'src_0').datasource_source(Path(source_path)))
        protocol.add_node(TransformNode('dec').time_decimate(decimate))
        protocol.add_edge(TransformEdge(
            'edge_0', protocol.nodes['src_0'].id, protocol.nodes['dec'].id))
        protocol.add_node(TransformNode(
            'targ_0').datasource_sink(Path(target_path)))
        protocol.add_edge(TransformEdge(
            'edge_1', protocol.nodes['dec'].id, protocol.nodes['targ_0'].id))
        self._dsp_stream[protocol.id] = {'data_source': self._link_data_file(
            Path(source_path)), 'protocol': protocol, 'stream': self._do_protocol(protocol, hub_name)}
        self._clear_dataset(source_path)
        self._dsp_stream[protocol.id]["data_source"].clear_dataset_id()
        return protocol.id

    def file_convert(
            self,
            source_path: Path,
            dest_path: Path,
            dest_file_type: str,
            force=False,
            hub_name=DEFAULT_HUB_ID,
    ) -> str:
        """
        Converts source file to target file.

        Parameters:
            source_path (str, pathlib.Path): path to source file
            target_path (str, pathlib.Path): path to target (output) file
            force (bool): flag to force replacing target file if it exists
            hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

        Returns:
            stream_id (str): background DSP stream ID

        Notes:
            The source and target files
        """

        source_path = Path(source_path).expanduser().resolve()
        source_path = Path(source_path.parent, source_path.stem)

        dest_path = Path(dest_path).expanduser().resolve()
        dest_path = Path(dest_path.parent, dest_path.stem)

        # load source
        try:
            source_meta = self._link_data_file(Path(source_path))
        except Exception as e:
            raise ValueError("error loading source file", e)

        if dest_path.suffix != "":
            dest_file_type = RadiensFileType.parse(
                ext_to_radiens_file_type(dest_path.suffix))
        elif Path('file.'+dest_file_type).suffix != "":
            dest_file_type = RadiensFileType.parse(
                ext_to_radiens_file_type(Path('file.'+dest_file_type).suffix))
        else:
            warnings.warn(
                'no file extension provided for target file. Assuming XDAT')
            dest_file_type = RadiensFileType.XDAT

        source_file_type = source_meta.file_type
        if source_file_type == dest_file_type and dest_path.parent == source_path.parent and dest_path.stem == source_path.stem:
            raise ValueError("source and target files are the same")

        if source_file_type not in CONVERTIBLE_RADIENS_FILE_TYPES or dest_file_type not in CONVERTIBLE_RADIENS_FILE_TYPES:
            raise ValueError(
                f"file conversion between {source_file_type} and {dest_file_type} is not supported")

        source_path = Path(str(source_path)+to_suffix(source_file_type))
        dest_path = Path(str(dest_path)+to_suffix(dest_file_type))

        if force:
            try:
                self._fsys.delete_files(dest_path)
            except RpcException as e:
                if "datasource does not exist" in map(
                        lambda x: x.strip(), e.message.split(':')):
                    pass
                else:
                    raise e

        source_path = str(source_path)
        protocol = ProtocolAPI('file_convert')
        protocol.add_node(TransformNode(
            'src_0').datasource_source(Path(source_path)))
        protocol.add_node(TransformNode(
            'targ_0').datasource_sink(Path(dest_path)))
        protocol.add_edge(TransformEdge(
            'edge_0', protocol.nodes['src_0'].id, protocol.nodes['targ_0'].id))
        self._dsp_stream[protocol.id] = {'data_source': self._link_data_file(
            Path(source_path)), 'protocol': protocol, 'stream': self._do_protocol(protocol, hub_name)}
        self._clear_dataset(source_path)
        self._dsp_stream[protocol.id]["data_source"].clear_dataset_id()
        return protocol.id

    def dsp_slice_time(
        self,
        time_start: float,
        time_end: float,
        source_path: Path,
        target_path: Path,
        force=False,
        hub_name=DEFAULT_HUB_ID,
    ):
        """
        Slices the source data file in time to result in the target file.

        Parameters:
            time_start (float): slice start time in seconds
            time_end (float): slice end time in seconds
            source_path (str, pathlib.Path): path to source file
            target_path (str, pathlib.Path): path to target (output) file
            force (bool): flag to force replacing target file if it exists
            hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

        Returns:
            stream_id (str): background DSP stream ID

        Notes:
            "time_start" and "time_end" are the absolute time in the source file.
            The source and target files must be XDAT files.
            This is non-blocking and the requested DSP operation runs in the background.

        Example:
            >>> client.dsp_slice_time(0.5, 10, './my_source_file', './my_output_file')
            None

        See Also:
            :py:meth:`dsp_progress`
            :py:meth:`dsp_progress_bar`
            :py:meth:`dsp_slice_channels`
        """
        if force:
            rm_xdat_file(Path(target_path))
        protocol = ProtocolAPI('slice_time_0')
        protocol.add_node(TransformNode(
            'src_0').datasource_source(source_path))
        protocol.add_node(TransformNode(
            'slice_time').slice_time(time_start, time_end))
        protocol.add_edge(TransformEdge(
            'edge_0', protocol.nodes['src_0'].id, protocol.nodes['slice_time'].id))
        protocol.add_node(TransformNode('targ_0').datasource_sink(target_path))
        protocol.add_edge(TransformEdge(
            'edge_1', protocol.nodes['slice_time'].id, protocol.nodes['targ_0'].id))
        self._dsp_stream[protocol.id] = {'data_source': self._link_data_file(
            Path(source_path)), 'protocol': protocol, 'stream': self._do_protocol(protocol, hub_name)}
        self._clear_dataset(source_path)
        self._dsp_stream[protocol.id]["data_source"].clear_dataset_id()
        return protocol.id

    def dsp_slice_channels(
        self,
        target_channels: list,
        source_path: Path,
        target_path: Path,
        force=False,
        hub_name=DEFAULT_HUB_ID,
    ):
        """
        Slices out (removes) the target channels from source data file to result in the target file.

        Parameters:
            target_channels (list): channel indices of channels to slice from the source
            source_path (str, pathlib.Path): path to source file
            target_path (str, pathlib.Path): path to target (output) file
            force (bool): flag to force replacing target file if it exists
            hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

        Returns:
            stream_id (str): background DSP stream ID

        Notes:
            "target_channels" are the absolute channel indices of the source file, including GPIO signals.
            The source and target files must be XDAT files.
            This is non-blocking and the requested DSP operation runs in the background.

        Example:
            >>> client.dsp_slice_channels([0,2,8,5], './my_source_file', './my_output_file')
            None

        See Also:
           :py:meth:`dsp_progress`
           :py:meth:`dsp_progress_bar`
           :py:meth:`dsp_slice_time`
        """
        if force:
            rm_xdat_file(Path(target_path))
        protocol = ProtocolAPI('slice_chan_0')
        protocol.add_node(TransformNode(
            'src_0').datasource_source(source_path))
        protocol.add_node(TransformNode(
            'slice_chan').slice_channels(target_channels))
        protocol.add_edge(TransformEdge(
            'edge_0', protocol.nodes['src_0'].id, protocol.nodes['slice_chan'].id))
        protocol.add_node(TransformNode('targ_0').datasource_sink(target_path))
        protocol.add_edge(TransformEdge(
            'edge_1', protocol.nodes['slice_chan'].id, protocol.nodes['targ_0'].id))
        self._dsp_stream[protocol.id] = {'data_source': self._link_data_file(Path(source_path)),
                                         'protocol': protocol,
                                         'stream': self._do_protocol(protocol, hub_name)}
        self._clear_dataset(source_path)
        self._dsp_stream[protocol.id]["data_source"].clear_dataset_id()
        return protocol.id

    def _do_protocol(self, protocol: ProtocolAPI, hub_name=DEFAULT_HUB_ID) -> str:
        api_curate.set_protocol(self._server_address(
            hub_name, RadiensService.CORE), protocol)
        return api_curate.apply_protocol(self._server_address(hub_name, RadiensService.CORE),  protocol.id)

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

    def _link_data_file(
        self, source: any, calc_metrics=False, force=False, hub_name=DEFAULT_HUB_ID
    ) -> DatasetMetadata:
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
            isForce=force,
        )
        return api_videre.set_datasource(
            self._server_address(hub_name, RadiensService.CORE), req
        )
