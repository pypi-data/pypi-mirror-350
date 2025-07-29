import time
import unittest
from pathlib import Path
from pprint import pprint

from radiens.utils.enums import SignalType, TrsMode
from radiens.utils.util import make_time_range
from radiens.videre_client import VidereClient


class base_utest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._dir = Path(__file__).parent

    def setUp(self):
        self.client = VidereClient()
        self.radix_data = '~/radix/data'
        self.data_path = '~/radix/data/radiens_test_data'
        self.dataset_0 = '64chan_1s'
        self.tmp_data_path = '~/radix/data/radiens_test_data/tmp'
        self.tmp_dataset_1 = 'tmp_0'

    def tearDown(self) -> None:
        self.client.clear_dataset(dataset_id='all')

    def test_get_signals(self):
        dsource = self.client.link_data_file(
            Path(self.data_path, '64chan_1s.xdat'))
        chunk = 0.01
        TR = make_time_range(time_range=[
                             dsource.time_range.sec[0], dsource.time_range.sec[0] + chunk], fs=dsource.time_range.fs)
        sig = self.client.signals().get_signals(
            TR, TrsMode.SUBSET, sig_sel=None, dataset_metadata=dsource)
        self.assertEqual(
            sig.signals.amp.shape[0], dsource.channel_metadata.num_sigs(SignalType.AMP))
        self.assertEqual(
            sig.signals.gpio_ain.shape[0], dsource.channel_metadata.num_sigs(SignalType.AIN))
        self.assertEqual(2, sig.signals.gpio_ain.shape[0])
        self.assertEqual(sig.signals.amp.shape[1], TR.N)
        self.assertEqual(sig.signals.amp.shape[1], sig.time_range.N)
        self.assertEqual(sig.signals.amp.shape[1], TR.fs * chunk)
        self.assertEqual(dsource.time_range.sec[0], sig.time_range.sec[0])
        self.assertEqual(
            dsource.time_range.sec[0]+chunk, sig.time_range.sec[1])
        self.assertEqual(dsource.time_range.fs, sig.time_range.fs)

    def test_get_psd(self):
        dsource = self.client.link_data_file(
            Path(self.data_path, '64chan_1s.xdat'))
        chunk = 0.2
        TR = make_time_range(time_range=[
                             dsource.time_range.sec[0], dsource.time_range.sec[0] + chunk], fs=dsource.time_range.fs)
        psd = self.client.signals().get_psd(TR, TrsMode.SUBSET, sig_sel=None,
                                            samp_freq=2000.0, dataset_metadata=dsource)
        self.assertEqual(
            psd.psd.shape[0], dsource.channel_metadata.num_sigs(SignalType.AMP))

    def test_signal_metrics(self):
        if Path(self.data_path, '64chan_1s.kpi').expanduser().absolute().exists():
            Path(self.data_path, '64chan_1s.kpi').expanduser().absolute().unlink()
        self.assertFalse(
            Path(self.data_path, '64chan_1s.kpi').expanduser().absolute().exists())

        dsource = self.client.link_data_file(
            Path(self.data_path, '64chan_1s.xdat'), calc_metrics=False)
        self.assertEqual("64chan", dsource.id[0:6])
        time.sleep(2)
        self.assertFalse(
            Path(self.data_path, '64chan_1s.kpi').expanduser().absolute().exists())

        status = self.client.signal_metrics().get_metrics_status(dsource)
        self.assertEqual([0, 0], status.time_range.sec.tolist())

        self.client.signal_metrics().calculate(dsource)
        time.sleep(2)
        self.assertTrue(
            Path(self.data_path, '64chan_1s.kpi').expanduser().absolute().exists())
        status = self.client.signal_metrics().get_metrics_status(dsource)
        self.assertEqual([16, 17], status.time_range.sec.tolist())

        self.client.signal_metrics().clear(dsource)
        self.assertFalse(
            Path(self.data_path, '64chan_1s.kpi').expanduser().absolute().exists())

        self.client.clear_dataset(dataset_id='all')
        dsource = self.client.link_data_file(
            Path(self.data_path, '64chan_1s.xdat'), calc_metrics=True)
        self.assertEqual("64chan", dsource.id[0:6])
        time.sleep(2)
        self.assertTrue(
            Path(self.data_path, '64chan_1s.kpi').expanduser().absolute().exists())


if __name__ == "__main__":
    unittest.main()
