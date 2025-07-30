"""This module contains the provider for weather data."""

import logging
from datetime import timedelta, timezone

import numpy as np
import pandas as pd
from midas.util.dateformat import GER

from ..meta import (
    AVG_T_AIR,
    BI,
    CLOUDINESS,
    DI,
    GHI,
    PRESSURE,
    SUN_HOURS,
    T_AIR,
    WIND,
    WINDDIR,
)

COLS = {
    T_AIR: [1.42, [-20, 45.0]],
    AVG_T_AIR: [1.36, [-20, 45.0]],
    BI: [1.0, [0, 1368]],
    DI: [1.0, [0, 1368]],
    WIND: [1.0, [0, 150]],
    WINDDIR: [1.0, [0, 360]],
    PRESSURE: [0.0764, [700, 1100]],
    SUN_HOURS: [1.0, [0, 60]],
    CLOUDINESS: [1.0, [0, 100]],
}

LOG = logging.getLogger(__name__)


class WeatherData:
    """A simple weather data provider.

    This class provides weather data from a hdf file. Either a concrete
    datetime can be selected or randomly from a time frame.

    Parameters
    ----------
    filename : str
        Absolute path to the weather database.
    seed : int
        A seed for the randum number generatore. Random values are only
        used in the *select_block* method to pick randomly one value
        from the block. The values itself are unchanged.

    """

    def __init__(self, filename, seed=None):
        try:
            self.wdata = pd.read_csv(filename, index_col=0, date_format=GER)
        except (FileNotFoundError, UnicodeDecodeError):
            if filename.endswith(".hdf5"):
                self.wdata = pd.read_hdf(filename, "weather")
            else:
                LOG.critical(
                    "Weather data not available! Please update your Midas"
                    "runtime config and download the data. Run "
                    "'midasctl configure -u' followed by "
                    "'midasctl download -m weather' (without ')"
                )
                raise

        self.rng = np.random.RandomState(seed)

    def select_hour(self, now_dt, horizon=0):
        """
        Select weather data at given datetime *now_dt*.

        Returns
        -------
        list
            A *list* containing [[t_air], [avg_t_air], [GHI-DI], [DI]]

        """
        start_dt = now_dt.replace(
            minute=0, second=0, microsecond=0
        ).astimezone(timezone.utc)
        dates = [start_dt + timedelta(hours=h) for h in range(horizon + 1)]
        delta = (
            self.wdata.index[0].to_pydatetime()
            - self.wdata.index[-1].to_pydatetime()
            - timedelta(hours=1)
        )
        for idx in range(len(dates)):
            while dates[idx] > self.wdata.index[-1]:
                dates[idx] += delta

            dates[idx] = dates[idx].strftime(GER)

        data = self.wdata.loc[dates].copy()
        data[BI] = data[GHI] - data[DI]  # Direct radiation
        return [data[c].values.tolist() for c in COLS]

    def select_block(self, now_dt, horizon=0, frame=1):
        """Select weather data from a block related to *now_dt*.

        Gather the weather data from *frame* days in the past and in
        the future at exactly the same hour of the day and select
        randomly one of those values for each output. If self.horizon
        has a value > 1, then this is repeated for all hours in the
        horizon.

        Parameters
        ----------
        now_dt : datetime.datetime
            The time for which data is requested.
        horizon : int, optional
            Fetches data from the time steps following the provided
            time. Can be used to simulate weather forecast.
        frame : int, optional
            Specify the number of days which should be considered in
            each direction.

        """
        if frame < 1:
            return self.select_hour(now_dt, horizon)

        raw_data = []
        data = [[] for _ in COLS]

        base_dt = now_dt.replace(minute=0, second=0, microsecond=0).astimezone(
            timezone.utc
        )
        start_dt = base_dt - timedelta(days=frame)
        days = [start_dt + timedelta(days=day) for day in range(frame * 2 + 1)]

        for day in days:
            raw_data.append(self.select_hour(day, horizon))

        raw_data = np.array(raw_data)
        for day in range(frame * 2 + 1):
            for idx in range(len(COLS)):
                data[idx].append(self.rng.choice(raw_data[:, idx, day]))

        return data
