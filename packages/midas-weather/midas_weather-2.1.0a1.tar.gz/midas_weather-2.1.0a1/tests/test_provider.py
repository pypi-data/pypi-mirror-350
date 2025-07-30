"""This module contains the test for the weather data provider."""

import os
import unittest
from datetime import datetime, timedelta, timezone
from os.path import abspath, join

from midas.util.dateformat import GER
from midas.util.runtime_config import RuntimeConfig
from pandas.core.frame import DataFrame

from midas_weather.download import download_weather
from midas_weather.meta import (
    AVG_T_AIR,
    CLOUDINESS,
    DI,
    GHI,
    PRESSURE,
    SUN_HOURS,
    T_AIR,
    WIND,
    WINDDIR,
)
from midas_weather.model.provider import WeatherData


class TestWeather(unittest.TestCase):
    """Test the weather data provider."""

    def setUp(self):
        data_path = RuntimeConfig().paths["data_path"]
        tmp_path = os.path.abspath(os.path.join(data_path, "tmp"))
        os.makedirs(tmp_path, exist_ok=True)

        download_weather(data_path, tmp_path, False)

        self.datapath = abspath(
            join(data_path, RuntimeConfig().data["weather"][0]["name"])
        )
        self.wdp = WeatherData(filename=self.datapath, seed=0)

    def test_init(self):
        """Test the init function."""
        self.assertIsInstance(self.wdp.wdata, DataFrame)
        cols = self.wdp.wdata.columns
        self.assertIn(AVG_T_AIR, cols)
        self.assertIn(T_AIR, cols)
        self.assertIn(GHI, cols)
        self.assertIn(DI, cols)
        self.assertIn(WIND, cols)
        self.assertIn(WINDDIR, cols)
        self.assertIn(PRESSURE, cols)
        self.assertIn(SUN_HOURS, cols)
        self.assertIn(CLOUDINESS, cols)

    def test_results(self):
        """Test the results."""

        now_dt = datetime.strptime("2018-05-19 12:00:00+0000", GER)
        data = self.wdp.select_hour(now_dt)

        self.assertEqual(data[0][0], 16.6)  # t_air
        self.assertAlmostEqual(data[1][0], 12.31666667)  # avg_t_air
        self.assertAlmostEqual(data[3][0], 386.1111111)  # diffuse radiation
        self.assertAlmostEqual(
            data[2][0], (411.1111111 - data[3][0])
        )  # direct radiation
        self.assertAlmostEqual(data[4][0], 1.3)  # wind speed
        self.assertAlmostEqual(data[5][0], 250)  # wind direction
        self.assertAlmostEqual(data[6][0], 1023.2)  # air pressure
        self.assertAlmostEqual(data[7][0], 12.0)  # sun hours
        self.assertAlmostEqual(data[8][0], 87.5)  # cloudiness

        data = self.wdp.select_hour(now_dt + timedelta(hours=1))
        self.assertEqual(data[0][0], 17.2)
        self.assertAlmostEqual(data[1][0], 12.316666667)
        self.assertAlmostEqual(data[3][0], 416.6666667)
        self.assertAlmostEqual(data[2][0], 450 - 416.6666667)
        self.assertAlmostEqual(data[4][0], 1.5)
        self.assertAlmostEqual(data[5][0], 120)
        self.assertAlmostEqual(data[6][0], 1023.0)
        self.assertAlmostEqual(data[7][0], 9.0)
        self.assertAlmostEqual(data[8][0], 75.0)

    def test_select_hour(self):
        """Test the select hour function."""
        now_dt = datetime.strptime("2017-12-31 23:00:00+0000", GER)

        data = self.wdp.select_hour(now_dt)

        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 9)
        for datum in data:
            self.assertIsInstance(datum, list)
            self.assertEqual(len(datum), 1)
            for value in datum:
                self.assertIsInstance(value, float)

        # Access with different time zone should yield the same result
        now_dt = datetime.strptime("2018-01-01 00:00:00+0100", GER)
        data2 = self.wdp.select_hour(now_dt)

        for d1, d2 in zip(data, data2):
            self.assertEqual(d1[0], d2[0])

    @unittest.skip
    def test_select_hour_outside_dataset(self):
        """Test the datetime clipping to the dataset.

        Clipping only works into the future, not into the past.
        """
        data1 = self.wdp.select_hour(
            datetime.strptime("2025-01-01 00:00:00+0000", GER)
        )

        data2 = self.wdp.select_hour(
            datetime.strptime("2008-12-31 23:00:00+0000", GER)
        )

        for d1, d2 in zip(data1, data2):
            self.assertEqual(d1[0], d2[0])

        data3 = self.wdp.select_hour(
            datetime.strptime("2024-06-08 16:00:00+0200", GER)
        )
        # 2024 is a leap year, a direct mapping to 2010-06-08 is not
        # possible
        data4 = self.wdp.select_hour(
            datetime.strptime("2010-06-09 14:00:00+0000", GER)
        )

        for d1, d2 in zip(data3, data4):
            self.assertEqual(d1[0], d2[0])

        data5 = self.wdp.select_hour(
            datetime.strptime("2050-06-08 16:00:00+0200", GER)
        )
        data6 = self.wdp.select_hour(
            datetime.strptime("2022-06-09 14:00:00+0000", GER)
        )

        for d1, d2 in zip(data5, data6):
            self.assertEqual(d1[0], d2[0])

    def test_horizon(self):
        """The forecast horizon function.

        With a horizon of 2, the result should have three values.
        The requested current time plus the next two values.
        """
        now_dt = datetime.strptime("2017-12-31 23:00:00+0000", GER)

        data = self.wdp.select_hour(now_dt, horizon=2)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 9)
        for datum in data:
            self.assertIsInstance(datum, list)
            self.assertEqual(len(datum), 3)

    def test_select_block(self):
        """Test the select block function."""
        now_dt = datetime.strptime("2018-01-01 00:00:00+0100", GER)

        data = self.wdp.select_block(now_dt, horizon=2, frame=1)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 9)
        for datum in data:
            self.assertIsInstance(datum, list)
            self.assertEqual(len(datum), 3)

        # Temperature
        # 00:00 on 2017-12-31, 2018-01-01, 2018-01-02
        self.assertIn(data[0][0], [7.8, 9.1, 4.4])
        # 01:00 on 2017-12-31, 2018-01-01, 2018-01-02
        self.assertIn(data[0][1], [6.9, 7.9, 3.4])

    def test_select_block_year_change(self):
        """Test the select block function with a year change."""
        wdp = WeatherData(filename=self.datapath, seed=0)
        now_dt = datetime(
            year=2018,
            month=12,
            day=31,
            hour=23,
            minute=0,
            second=0,
            tzinfo=timezone(offset=timedelta(seconds=3600)),
        )
        for _ in range(10):  # test different random numbers
            data = wdp.select_block(now_dt, horizon=2, frame=1)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 9)
            for datum in data:
                self.assertIsInstance(datum, list)
                self.assertEqual(len(datum), 3)
            self.assertIn(data[0][0], [6.7, 8.2, 4.6])
            self.assertIn(data[0][1], [6.7, 7.8, 5.1])
            self.assertIn(data[0][2], [6.7, 7.9, 6.1])


if __name__ == "__main__":
    unittest.main()
