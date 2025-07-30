import os
import unittest

import pandas as pd
from midas.util.runtime_config import RuntimeConfig

from midas_weather.analysis import analyze


class TestDownload(unittest.TestCase):
    def setUp(self):
        self.output_path = os.path.join(
            RuntimeConfig().paths["output_path"], "midasmv_der"
        )
        # self.tmp_path = os.path.join(self.data_path, "tmp")
        self.db = pd.HDFStore(
            "/home/sbalduin/Code/Midas/midas-outputs/midasmv_der.hdf5"
        )
        # os.makedirs(self.tmp_path, exist_ok=True)

    @unittest.skip
    def test_analyze(self):
        analyze("Weather", self.db, self.output_path, 0, 0, 900, False)

    def tearDown(self):
        self.db.close()


if __name__ == "__main__":
    unittest.main()
