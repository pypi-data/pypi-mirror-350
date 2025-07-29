import unittest
from pathlib import Path
from pprint import pprint


class base_utest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_discover_server_unix(self):
        pass


if __name__ == "__main__":
    unittest.main()
