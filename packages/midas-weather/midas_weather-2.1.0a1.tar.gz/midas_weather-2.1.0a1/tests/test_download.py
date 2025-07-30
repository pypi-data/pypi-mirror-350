import os
import unittest

from midas.util.runtime_config import RuntimeConfig

from midas_weather.download import download_weather


class TestDownload(unittest.TestCase):
    def setUp(self):
        self.data_path = RuntimeConfig().paths["data_path"]
        self.tmp_path = os.path.join(self.data_path, "tmp")
        os.makedirs(self.tmp_path, exist_ok=True)

    @unittest.skip
    def test_download(self):
        download_weather(self.data_path, self.tmp_path, True)


if __name__ == "__main__":
    unittest.main()
