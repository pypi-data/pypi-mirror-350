import time
import unittest
from pathlib import Path

from radiens.allego_client import AllegoClient
from radiens.lib.spikes import SpikesSet
from radiens.utils.enums import SignalType


class base_utest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._dir = Path(__file__).parent

    def setUp(self):
        self.client = AllegoClient()
        self.client.set_streaming('off')
        self.client.spike_sorter().set_sorting('off')
        self.client.set_sampling_freq(30000)
        self.client.spike_sorter().initialize()
        time.sleep(1.0)

    def test_get_status(self):
        status = self.client.get_status()
        self.assertEqual('sim-spikes', status.system_mode)
        self.assertEqual(30000, status.sample_freq)

    def test_set_dio(self):
        self.client.set_digital_out_manual(True, False)
        reg = self.client.get_digital_out_states()
        self.assertEqual('manual', reg['digital_outs_mode'])
        self.assertTrue(reg['states'][0]['state'])
        self.assertEqual(0, reg['states'][0]['chan_idx'])
        self.assertFalse(reg['states'][1]['state'])
        self.assertEqual(1, reg['states'][1]['chan_idx'])

    def test_get_channel_metadata(self):
        meta = self.client.get_channel_metadata()
        self.assertEqual(32, meta.num_sigs(SignalType.AMP))
        self.assertEqual(2, meta.num_sigs(SignalType.AIN))
        self.assertEqual(2, meta.num_sigs(SignalType.DIN))
        self.assertEqual(2, meta.num_sigs(SignalType.DOUT))

    def test_signal_metrics(self):
        resp = self.client.signal_metrics().get_metrics_status()
        self.assertEqual(0.2, resp.attributes['packet_dur_sec'])
        self.client.set_streaming('on')
        time.sleep(2.0)
        resp = self.client.signal_metrics().get_metrics_status()
        self.assertGreater(resp.time_range.sec[1],  0)
        resp.print()
        resp = self.client.signal_metrics().get_metrics(3)
        resp.print()
        print("val = ", resp.val)
        self.client.set_streaming('off')

    def test_streaming_and_spike_sorting(self):
        self.client.spike_sorter().initialize()
        time.sleep(3.0)
        status = self.client.get_status()
        self.assertEqual('S_OFF', status.stream.mode)
        dash = self.client.spike_sorter().get_dashboard()
        self.assertEqual('SYS_OFF', dash.state.loc['mode'][0])
        self.client.set_streaming('on')
        time.sleep(0.5)
        status = self.client.get_status()
        self.assertEqual('S_ON', status.stream.mode)
        resp = self.client.spike_sorter().get_state()
        self.assertEqual('SYS_OFF', resp.state.loc['mode'][0])
        self.assertFalse(resp.state.loc['is_on'][0])
        self.client.spike_sorter().set_sorting('on')
        time.sleep(3.0)
        resp = self.client.spike_sorter().get_state()
        self.assertEqual('SYS_ON', resp.state.loc['mode'][0])
        self.assertTrue(resp.state.loc['is_on'][0])
        dash = self.client.spike_sorter().get_dashboard()
        self.assertEqual('SYS_ON', dash.state.loc['mode'][0])
        self.client.spike_sorter().set_sorting('off')
        time.sleep(2.0)
        resp = self.client.spike_sorter().get_state()
        self.assertEqual('SYS_OFF', resp.state.loc['mode'][0])
        self.assertFalse(resp.state.loc['is_on'][0])
        dash = self.client.spike_sorter().get_dashboard()
        self.assertEqual('SYS_OFF', dash.state.loc['mode'][0])
        self.client.set_streaming('off')
        time.sleep(0.25)
        status = self.client.get_status()
        self.assertEqual('S_OFF', status.stream.mode)

        resp = self.client.spikes().get_recent_spikes()
        self.assertTrue(isinstance(resp, SpikesSet))
        self.assertEqual(67, resp.num_pts_waveform)
        self.assertGreater(resp.num_spikes_total, 0)
        self.assertTrue(resp.has_component('waveforms'))
        self.assertFalse(resp.has_component('timestamps'))

        df_params = self.client.spike_sorter().get_params()
        thr_level = df_params.loc[df_params['ntv_idx'] == 0]['thr'].to_numpy()[
            0]
        self.assertEqual(80, thr_level[0])
        self.assertEqual(120, thr_level[1])

        self.client.spike_sorter().set_threshold_level(neg_thr=523, pos_thr=469)
        df_params = self.client.spike_sorter().get_params()
        thr_level = df_params.loc[df_params['ntv_idx'] == 0]['thr'].to_numpy()[
            0]
        self.assertEqual(523, thr_level[0])
        self.assertEqual(469, thr_level[1])

        self.client.spike_sorter().set_threshold_level(neg_thr=80, pos_thr=120)
        df_params = self.client.spike_sorter().get_params()
        thr_level = df_params.loc[df_params['ntv_idx'] == 0]['thr'].to_numpy()[
            0]
        self.assertEqual(80, thr_level[0])
        self.assertEqual(120, thr_level[1])

        spec = self.client.spikes().get_spikes_metadata()
        self.assertEqual(0, spec.time_range[0][0])
        self.assertGreater(spec.time_range[0][1], 0)
        self.assertEqual(7, len(spec.site_summary_stats))
        self.assertEqual(32, len(spec.sites))
        self.assertGreater(len(spec.neurons), 0)


if __name__ == "__main__":
    unittest.main()
