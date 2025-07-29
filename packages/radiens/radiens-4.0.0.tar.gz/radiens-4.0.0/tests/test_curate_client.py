import time
import unittest
from datetime import datetime
from pathlib import Path
from pprint import pprint

from radiens.curate_client import CurateClient
from radiens.file_sys_client import FileSystemClient
from radiens.utils.enums import SignalType
from radiens.videre_client import VidereClient
from tqdm import tqdm


class base_utest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._dir = Path(__file__).parent

    def setUp(self):
        self.client = CurateClient()
        self.videre_client = VidereClient()
        self.fsys_client = FileSystemClient()
        self.radix_data = '~/radix/data'
        self.data_path = '~/radix/data/radiens_test_data'
        self.dataset_0 = '64chan_1s'
        self.tmp_data_path = '~/radix/data/radiens_test_data/tmp'
        self.tmp_dataset_1 = 'tmp_0'

    def tearDown(self) -> None:
        if Path(self.tmp_data_path, self.tmp_dataset_1+'_data.xdat').expanduser().resolve().exists():
            Path(self.tmp_data_path, self.tmp_dataset_1 +
                 '_data.xdat').expanduser().resolve().unlink()
            Path(self.tmp_data_path, self.tmp_dataset_1 +
                 '_timestamp.xdat').expanduser().resolve().unlink()
            Path(self.tmp_data_path, self.tmp_dataset_1 +
                 '.xdat.json').expanduser().resolve().unlink()

    def _has_test_data(self):
        if not Path(self.data_path).expanduser().resolve().exists() or not Path(self.data_path, self.dataset_0+'_data.xdat').expanduser().resolve().exists():
            return False
        return True

    def _dsp_block_until_done(self, stream_id, msg):
        start_time = datetime.now()
        while True:
            elapsed = datetime.now() - start_time
            if elapsed.total_seconds() > 5:
                self.assertFalse(True, 'dsp timed out: {}'.format(msg))
            if self.client.dsp_progress(stream_id) == 1.0:
                break
            time.sleep(0.1)

    def test_apply_filters(self):
        if not self._has_test_data():
            self.skipTest('~/radix/data/radiens_test_data is not set up')

        self.videre_client.clear_dataset(dataset_id='all')
        self.client.dsp_clean_up()

        stream_id = self.client.dsp_low_pass_filter(200.0, Path(self.data_path, self.dataset_0),
                                                    Path(self.tmp_data_path, self.tmp_dataset_1), force=True)
        self._dsp_block_until_done(stream_id, 'low pass filter')
        self.client.dsp_clean_up()

        stream_id = self.client.dsp_high_pass_filter(1000.0, Path(self.data_path, self.dataset_0),
                                                     Path(self.tmp_data_path, self.tmp_dataset_1), force=True)
        self._dsp_block_until_done(stream_id, 'high pass filter')
        self.client.dsp_clean_up()

        stream_id = self.client.dsp_band_pass_filter(200, 1000.0, Path(self.data_path, self.dataset_0),
                                                     Path(self.tmp_data_path, self.tmp_dataset_1), force=True)
        self._dsp_block_until_done(stream_id, 'band pass filter')
        self.client.dsp_clean_up()

        stream_id = self.client.dsp_band_stop_filter(250, 750.0, Path(self.data_path, self.dataset_0),
                                                     Path(self.tmp_data_path, self.tmp_dataset_1), force=True)
        self._dsp_block_until_done(stream_id, 'band stop filter')
        self.client.dsp_clean_up()

        stream_id = self.client.dsp_notch_filter(60, 1.0, Path(self.data_path, self.dataset_0),
                                                 Path(self.tmp_data_path, self.tmp_dataset_1), force=True)
        self._dsp_block_until_done(stream_id, 'notch filter')

        stream_id = self.client.dsp_paired_diff(4, 6, Path(self.data_path, self.dataset_0),
                                                Path(self.tmp_data_path, self.tmp_dataset_1), force=True)
        self._dsp_block_until_done(stream_id, 'paired differential')

        stream_id = self.client.dsp_virtual_ref(23, Path(self.data_path, self.dataset_0),
                                                Path(self.tmp_data_path, self.tmp_dataset_1), force=True)
        self._dsp_block_until_done(stream_id, 'virtual reference')

        stream_id = self.client.dsp_car(Path(self.data_path, self.dataset_0),
                                        Path(self.tmp_data_path, self.tmp_dataset_1), force=True)
        self._dsp_block_until_done(stream_id, 'CAR')

        stream_id = self.client.dsp_time_decimate(2, Path(self.data_path, self.dataset_0),
                                                  Path(self.tmp_data_path, self.tmp_dataset_1+'.xdat'), force=True)
        self._dsp_block_until_done(stream_id, 'time decimate')
        self.assertEqual(20000/2, self.fsys_client.get_data_file_metadata(
            Path(self.tmp_data_path, self.tmp_dataset_1)).time_range.fs)

        stream_id = self.client.dsp_slice_time(16, 17, Path(self.data_path, self.dataset_0),
                                               Path(self.tmp_data_path, self.tmp_dataset_1+'.xdat'), force=True)
        self._dsp_block_until_done(stream_id, 'slice time')
        self.assertEqual(1.0, self.fsys_client.link_data_file(
            Path(self.tmp_data_path, self.tmp_dataset_1)).time_range.dur_sec)

        stream_id = self.client.dsp_slice_channels([4, 6, 23], Path(self.data_path, self.dataset_0),
                                                   Path(self.tmp_data_path, self.tmp_dataset_1+'.xdat'), force=True)
        self._dsp_block_until_done(stream_id, 'slice channels')
        self.assertEqual(32, self.fsys_client.get_data_file_metadata(
            Path(self.data_path, self.dataset_0)).channel_metadata.num_sigs(SignalType.AMP))
        self.assertEqual(3, self.fsys_client.get_data_file_metadata(
            Path(self.tmp_data_path, self.tmp_dataset_1)).channel_metadata.num_sigs(SignalType.AMP))

    def test_slice_time(self):
        if not self._has_test_data():
            self.skipTest('~/radix/data/radiens_test_data is not set up')


if __name__ == "__main__":
    unittest.main()
