"""Test for the current-weather model."""

import os
import unittest
from datetime import datetime, timedelta, timezone
from os.path import abspath, join

from midas.util.runtime_config import RuntimeConfig

from midas_weather.download import download_weather
from midas_weather.model.current import WeatherCurrent
from midas_weather.model.provider import WeatherData


class TestWeatherCurrent(unittest.TestCase):
    """Test class for the current-weather model."""

    def setUp(self):
        data_path = RuntimeConfig().paths["data_path"]
        tmp_path = os.path.abspath(os.path.join(data_path, "tmp"))
        os.makedirs(tmp_path, exist_ok=True)

        download_weather(data_path, tmp_path, False)

        self.datapath = abspath(
            join(data_path, RuntimeConfig().data["weather"][0]["name"])
        )
        wdata = WeatherData(filename=self.datapath, seed=0)

        self.now_dt = datetime(
            year=2018,
            month=5,
            day=19,
            hour=13,
            minute=0,
            second=0,
            tzinfo=timezone.utc,
        )

        self.weather = WeatherCurrent(
            wdata=wdata, start_date=self.now_dt, seed=0
        )

    def test_init(self):
        """Test the init function."""
        # weather = WeatherCurrent(
        #     wdata=WeatherData(filename=self.datapath), start_date=self.now_dt
        # )
        self.assertIsInstance(self.weather.wdata, WeatherData)
        self.assertIsInstance(self.weather.now_dt, datetime)

    def test_step(self):
        """Test the step function."""
        self.weather.step()

        self.assertIsInstance(self.weather.t_air_deg_celsius, float)
        self.assertIsInstance(self.weather.day_avg_t_air_deg_celsius, float)
        self.assertIsInstance(self.weather.bh_w_per_m2, float)
        self.assertIsInstance(self.weather.dh_w_per_m2, float)
        self.assertIsInstance(self.weather.wind_v_m_per_s, float)
        self.assertIsInstance(self.weather.wind_dir_deg, float)
        self.assertIsInstance(self.weather.air_pressure_hpa, float)

        self.assertAlmostEqual(self.weather.t_air_deg_celsius, 17.2)
        self.assertAlmostEqual(
            self.weather.day_avg_t_air_deg_celsius, 12.316, places=2
        )
        self.assertAlmostEqual(self.weather.bh_w_per_m2, 33.334, places=2)
        self.assertAlmostEqual(self.weather.dh_w_per_m2, 416.667, places=2)
        self.assertAlmostEqual(self.weather.wind_v_m_per_s, 1.5)
        self.assertAlmostEqual(self.weather.wind_dir_deg, 120.0)
        self.assertAlmostEqual(self.weather.air_pressure_hpa, 1023.0)
        self.assertAlmostEqual(self.weather.sun_hours_min_per_h, 9.0)
        self.assertAlmostEqual(self.weather.cloud_percent, 75.0)

    def test_three_steps(self):
        """Test three calls of the step function.

        The first and second steps are 900s and, therefore, lower than
        the resolution of the dataset. The result will be the same.
        The third step a higher step size and the result will finally
        be differnt.
        """
        # First step
        self.weather.step()
        bh_w_per_m2 = self.weather.bh_w_per_m2
        dh_w_per_m2 = self.weather.dh_w_per_m2
        t_air_deg_celsius = self.weather.t_air_deg_celsius
        day_avg_t_air_deg_celsius = self.weather.day_avg_t_air_deg_celsius

        # Second step, no changes due to resolution
        self.weather.now_dt += timedelta(seconds=900)
        self.weather.step()
        self.assertEqual(t_air_deg_celsius, self.weather.t_air_deg_celsius)
        self.assertEqual(
            day_avg_t_air_deg_celsius, self.weather.day_avg_t_air_deg_celsius
        )
        self.assertEqual(bh_w_per_m2, self.weather.bh_w_per_m2)
        self.assertEqual(dh_w_per_m2, self.weather.dh_w_per_m2)

        self.weather.now_dt += timedelta(seconds=3600)
        self.weather.step()
        self.assertNotEqual(bh_w_per_m2, self.weather.bh_w_per_m2)
        self.assertNotEqual(dh_w_per_m2, self.weather.dh_w_per_m2)
        self.assertNotEqual(t_air_deg_celsius, self.weather.t_air_deg_celsius)
        self.assertEqual(
            day_avg_t_air_deg_celsius, self.weather.day_avg_t_air_deg_celsius
        )

    def test_interpolate(self):
        """Test interpolation of weather data."""
        self.weather.interpolate = True
        self.weather.auto_incr_time = True
        self.weather.step_size = 900

        t_airs = []
        self.weather.step()
        t_airs.append(self.weather.t_air_deg_celsius)
        self.weather.step()
        t_airs.append(self.weather.t_air_deg_celsius)
        self.weather.step()
        t_airs.append(self.weather.t_air_deg_celsius)
        self.weather.step()
        t_airs.append(self.weather.t_air_deg_celsius)
        self.weather.step()
        t_airs.append(self.weather.t_air_deg_celsius)

        for idx in range(1, len(t_airs)):
            self.assertGreater(t_airs[idx], t_airs[idx - 1])

    def test_seed(self):
        """Test randomization of weather data."""
        self.weather.interpolate = True
        self.weather.auto_incr_time = True
        self.weather.step_size = 900

        t_airs = []
        self.weather.step()
        t_airs.append(self.weather.t_air_deg_celsius)
        self.weather.step()
        t_airs.append(self.weather.t_air_deg_celsius)
        self.weather.step()
        t_airs.append(self.weather.t_air_deg_celsius)
        self.weather.step()
        t_airs.append(self.weather.t_air_deg_celsius)

        for idx in range(1, len(t_airs)):
            self.assertNotEqual(t_airs[idx], t_airs[idx - 1])


if __name__ == "__main__":
    unittest.main()
