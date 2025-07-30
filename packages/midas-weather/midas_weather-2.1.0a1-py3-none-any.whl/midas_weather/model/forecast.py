"""This module contains the forecast-weather model."""

import math
from datetime import timedelta

import numpy as np
import pandas as pd

from ..meta import (
    AVG_T_AIR,
    BI,
    CLOUDINESS,
    DI,
    PRESSURE,
    SUN_HOURS,
    T_AIR,
    WIND,
    WINDDIR,
)
from .current import WeatherCurrent
from .provider import COLS


class WeatherForecast(WeatherCurrent):
    """Weather forecast model.

    Uses the real data from future steps and applies a random error
    to the values.

    An internal start date is used and updated each step. This model
    provides weather information read from a weather time series.
    Additional functionality can be activated.

    Parameters
    ----------
    wdata : midas.core.weather.model.provider.WeatherData
        A reference to the class storing the actual data.
    start_date : datetime.datime
        The point of time in the year which should be started with.
    step_size : int, optional
        *step_size is an input and needs to be set in each step.*
        Used to step the internal datetime object. Does not reset
        after a step, so it can also be provided once during
        initialization.
    interpolate : bool, optional
        If set to *True*, data is interpolated if the internal datetime
        points to a time within two hours.
    seed : int, optional
        A seed for the random number generator.
    randomize : bool, optional
        If set to *True*, a normally distributed random noise is
        applied to the data.
    block_mode : bool, optional
        If set to *True*, the *select_block* function is used instead
        of the *select_hour* function. See the *WeatherData* to learn
        about the differences
    frame : int, optional
        If *block_mode* is True, this value is passed to the
        *select_block* function. Defaults to 1.
    forecast_horizon_hours : float, optional
        Specify for how many hours in the future a forecast should be
        generated.
    forecast_error : float, optional
        Specify how large the forecast error should be. Defaults to 0
        for a perfect forecast.

    Attributes
    ----------
    t_air_deg_celsius : float
        The current air temperature in degree celsius.
    day_avg_t_air_deg_celsius : float
        The current day's average air temperatur in degree celsius.
    bh_w_per_m2:
        Beam horizontal or direct solar radiation on the horizontal
        plane in Watt per square meter of the current step.
    dh_w_per_m2:
        Diffuse horizontal or diffuse solar radiation on the horizontal
        plane in Watt per square meter of the current step.

    """

    def __init__(
        self,
        wdata,
        start_date,
        step_size=None,
        forecast_horizon_hours=0.25,
        forecast_error=0,
        seed=None,
        interpolate=False,
        block_mode=False,
        randomize=False,
    ):
        super().__init__(
            wdata, start_date, step_size, randomize, interpolate, seed
        )

        self.forecast_horizon_hours = forecast_horizon_hours
        self.forecast_error = forecast_error
        self.forecast = None

        if block_mode:
            self.select_data = self.wdata.select_block
        else:
            self.select_data = self.wdata.select_hour

    def step(self):
        """Perform a simulation step."""

        pred_start = self.now_dt + timedelta(seconds=self.step_size)

        self.forecast = pd.DataFrame(
            columns=list(COLS.keys()),
            index=pd.date_range(
                pred_start,
                self.now_dt + timedelta(hours=self.forecast_horizon_hours),
                freq=f"{self.step_size}s",
            ),
        )
        horizon = int(math.ceil(self.forecast_horizon_hours)) + 2

        results = self.select_data(pred_start, horizon)

        steps = int(self.forecast_horizon_hours * 3_600 / self.step_size)

        if self.interpolate:
            val_idx = np.arange(0, (horizon + 1) * 3_600, 3_600)

            # start_hour = pred_start.hour
            start_sec = pred_start.minute * 60 + pred_start.second
            sel_idxs = []
            for _ in range(steps):
                sel_idxs.append(start_sec)
                start_sec += self.step_size

            results = [
                [np.interp(h, val_idx, results[idx]) for h in sel_idxs]
                for idx, _ in enumerate(COLS)
            ]

        else:
            sel_idxs = []
            start_hour = pred_start.hour
            for _ in range(steps):
                sel_idxs.append(pred_start.hour - start_hour)
                pred_start += timedelta(hours=self.step_size / 3_600)
                if pred_start.hour < start_hour:
                    start_hour = pred_start.hour - 1

            results = [
                [results[idx][h] for h in sel_idxs]
                for idx, _ in enumerate(COLS)
            ]

        if self.randomize:
            results = [
                [
                    v
                    * self.rng.normal(
                        scale=self.forecast_error * info[0], loc=1.0
                    )
                    for v in results[idx]
                ]
                for idx, info in enumerate(COLS.values())
            ]

        for idx, (col, info) in enumerate(COLS.items()):
            results[idx] = np.clip(
                results[idx], info[1][0], info[1][1]
            ).tolist()
            self.forecast[col] = results[idx]
            setattr(self, col, results[idx])

        return results

    @property
    def forecast_bh_w_per_m2(self):
        """Handle forecast_ - prefix."""
        return self.forecast.loc[:, [BI]]

    @property
    def forecast_dh_w_per_m2(self):
        """Handle forecast_ - prefix."""
        return self.forecast.loc[:, [DI]]

    @property
    def forecast_t_air_deg_celsius(self):
        """Handle forecast_ - prefix."""
        return self.forecast.loc[:, [T_AIR]]

    @property
    def forecast_day_avg_t_air_deg_celsius(self):
        """Handle forecast_ - prefix."""
        return self.forecast.loc[:, [AVG_T_AIR]]

    @property
    def forecast_wind_v_m_per_s(self):
        """Handle forecast_ - prefix."""
        return self.forecast.loc[:, [WIND]]

    @property
    def forecast_wind_dir_degree(self):
        """Handle forecast_ - prefix."""
        return self.forecast.loc[:, [WINDDIR]]

    @property
    def forecast_air_pressure_hpa(self):
        """Handle forecast_ - prefix."""
        return self.forecast.loc[:, [PRESSURE]]

    @property
    def forecast_sun_hours_min_per_h(self):
        """Handle forecast_ - prefix."""
        return self.forecast.loc[:, [SUN_HOURS]]

    @property
    def forecast_cloud_percent(self):
        """Handle forecast_ - prefix."""
        return self.forecast.loc[:, [CLOUDINESS]]
