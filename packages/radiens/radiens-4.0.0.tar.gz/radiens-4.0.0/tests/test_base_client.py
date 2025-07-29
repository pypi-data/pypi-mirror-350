from pprint import pprint
from tqdm import tqdm
import unittest
import time
from datetime import datetime
from pathlib import Path

from radiens.base_client import BaseClient


class base_utest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._dir = Path(__file__).parent

    def setUp(self):
        self.client = BaseClient()
        self.radix_data = '~/radix/data'
        self.data_path = '~/radix/data/radiens_test_data'
        self.dataset_0 = '64chan_1s'
        self.tmp_data_path = '~/radix/data/radiens_test_data/tmp'
        self.tmp_dataset_1 = 'tmp_0'

    def tearDown(self) -> None:
        if Path(self.tmp_data_path, self.tmp_dataset_1+'_data.xdat').expanduser().resolve().exists():
            Path(self.tmp_data_path, self.tmp_dataset_1+'_data.xdat').expanduser().resolve().unlink()
            Path(self.tmp_data_path, self.tmp_dataset_1+'_timestamp.xdat').expanduser().resolve().unlink()
            Path(self.tmp_data_path, self.tmp_dataset_1+'.xdat.json').expanduser().resolve().unlink()

    def _has_test_data(self):
        if not Path(self.data_path).expanduser().resolve().exists() or not Path(self.data_path, self.dataset_0+'_data.xdat').expanduser().resolve().exists():
            return False
        return True

    def test_list_dir(self):
        resp = self.client.ls(Path(self.radix_data))
        #self.assertEqual(Path(self.radix_data).expanduser().resolve(), resp.dest_path)

    def test_cp(self):
        if not self._has_test_data():
            self.skipTest('~/radix/data/radiens_test_data is not set up')
        resp = self.client.cp(Path(self.data_path, '64chan_1s.xdat'), Path(self.tmp_data_path, self.tmp_dataset_1))
        #self.assertEqual(Path(self.data_path, 'tmp').expanduser().resolve(), resp.dest_path)

    def test_rm(self):
        if not self._has_test_data():
            self.skipTest('~/radix/data/radiens_test_data is not set up')
        resp = self.client.cp(Path(self.data_path, '64chan_1s.xdat'), Path(self.tmp_data_path, self.tmp_dataset_1))
        resp = self.client.rm(Path(self.tmp_data_path, self.tmp_dataset_1))
        #self.assertEqual(Path(self.tmp_data_path).expanduser().resolve(), resp.dest_path)

    def test_mv(self):
        if not self._has_test_data():
            self.skipTest('~/radix/data/radiens_test_data is not set up')
        resp = self.client.cp(Path(self.data_path, '64chan_1s.xdat'), Path(self.tmp_data_path, 'tmp_to_mov'))
        resp = self.client.mv(Path(self.tmp_data_path, 'tmp_to_mov'), Path(self.tmp_data_path, self.tmp_dataset_1))
        #self.assertEqual(Path(self.data_path, 'tmp').expanduser().resolve(), resp.dest_path)

    def test_set_dataset(self):
        self.client.clear_dataset(dataset_id='all')
        dsource = self.client.link_data_file(Path(self.data_path, '64chan_1s.xdat'))
        self.assertEqual('64chan_1s', dsource.base_name)
        self.assertEqual([16, 17], dsource.time_range.sec.tolist())
        self.assertEqual([320000, 340000], dsource.time_range.timestamp.tolist())
        self.assertEqual(1, len(self.client.get_dataset_ids()))
        self.client.clear_dataset(dataset_id=dsource.id)
        self.assertEqual(0, len(self.client.get_dataset_ids()))


if __name__ == "__main__":
    unittest.main()
