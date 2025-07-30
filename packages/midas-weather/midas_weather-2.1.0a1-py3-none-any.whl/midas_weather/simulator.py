"""This module contains the Weather simulator."""

import json
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import mosaik_api_v3
import numpy as np
import pandas as pd
from midas.util.dateformat import GER
from midas.util.logging import set_and_init_logger
from midas.util.print_format import mformat
from midas.util.runtime_config import RuntimeConfig

from .meta import META
from .model.current import WeatherCurrent
from .model.forecast import WeatherForecast
from .model.provider import WeatherData
from .module import WeatherDataModule

LOG = logging.getLogger("midas_weather.simulator")


class WeatherDataSimulator(mosaik_api_v3.Simulator):
    """The Weather simulator."""

    def __init__(self):
        super().__init__(META)
        self.sid: str
        self.models: Dict[str, Any] = dict()
        self.step_size: int
        self.now_dt: datetime
        self.rng: np.random.RandomState
        self.randomize: bool
        self.interpolate: bool
        self.forecast_horizon_hours: float
        self.forecast_error: float
        self.seed_max: int
        self._time_synced: bool = False
        self._sim_time: int = 0
        self.scripted_events = {}
        self.active_events = {}

    def init(
        self,
        sid: str,
        start_date: str,
        step_size: int = 900,
        data_path: str = RuntimeConfig().paths["data_path"],
        filename: str = RuntimeConfig().data["weather"][0]["name"],
        interpolate: bool = False,
        seed: Optional[int] = None,
        seed_max: int = 2**32 - 1,
        randomize: bool = False,
        forecast_horizon_hours: Optional[float] = None,
        forecast_error: float = 0.05,
        key_value_logs: Optional[bool] = None,
        scripted_events: Optional[dict] = None,
        **kwargs,
    ):
        """Called exactly ones after the simulator has been started.

        Parameters
        ----------
        sid : str
            Simulator ID for this simulator.
        start_date : str
            Start date as UTC ISO 8601 timestring such as
            '2019-01-01 00:00:00+0100'.
        step_size : int, optional
            Step size for this simulator. Defaults to 900.
        data_path : str, optional
            Path to the data folder. Defaults to the data folder in the
            midas root folder.
        filename : str, optional
            Name of the weather database. Defaults to
            *weather_bre2009-2019.hdf5*, the file that is created by
            the *midas.tools.weather_data.build_weather_data* function.
        interpolate : bool, optional
            If set to *True*, interpolation is enabled. Can be
            overwritten by model specific configuration.
        seed : int, optional
            A seed for the random number generator.
        randomize : bool, optional
            If set to *True*, randomization of data will be enabled.
            Otherwise, the data from the database is return unchanged.
            Can be overwritten by model specific configuration.

        Returns
        -------
        dict
            The meta dict (set by *mosaik_api.Simulator*).
        """

        self.sid = sid
        self.step_size = step_size
        self.now_dt = datetime.strptime(start_date, GER).astimezone(
            timezone.utc
        )
        self.rng = np.random.RandomState(seed)
        self.seed_max = seed_max
        self.interpolate = interpolate
        self.randomize = randomize
        if forecast_horizon_hours is None:
            self.forecast_horizon_hours = self.step_size * 2 / 3_600

        self.forecast_error = forecast_error

        self.wdata = self._load_data(data_path, filename)

        if scripted_events is None:
            scripted_events = {}

        for date_string, event in scripted_events.items():
            event_dt = datetime.strptime(date_string, GER).astimezone(
                timezone.utc
            )
            self.scripted_events[event_dt] = event

        self.key_value_logs = key_value_logs
        if self.key_value_logs is None:
            self.key_value_logs = RuntimeConfig().misc.get(
                "key_value_logs", False
            )
        return self.meta

    def create(self, num, model, **model_params):
        """Initialize the simulation model instance (entity).

        Parameters
        ----------
        num : int
            The number of models to create.
        model : str
            The name of the models to create. Must be present inside
            the simulator's meta.

        Returns
        -------
        list
            A list with information on the created entity.
        """
        entities = list()

        for _ in range(num):
            eid = f"{model}-{len(self.models)}"
            seed = self.rng.randint(self.seed_max)

            if model == "WeatherCurrent":
                self.models[eid] = WeatherCurrent(
                    wdata=self.wdata,
                    start_date=self.now_dt,
                    step_size=self.step_size,
                    interpolate=model_params.get("interpolate", False),
                    randomize=model_params.get("randomize", False),
                    seed=model_params.get("seed", seed),
                )

            elif model == "WeatherForecast":
                self.models[eid] = WeatherForecast(
                    wdata=self.wdata,
                    start_date=self.now_dt,
                    step_size=self.step_size,
                    interpolate=model_params.get("interpolate", False),
                    randomize=model_params.get("randomize", False),
                    seed=model_params.get("seed", seed),
                    forecast_horizon_hours=model_params.get(
                        "forecast_horizon_hours", self.forecast_horizon_hours
                    ),
                    forecast_error=model_params.get(
                        "forecast_error", self.forecast_error
                    ),
                )
            entities.append({"eid": eid, "type": model})

        return entities

    def step(self, time: int, inputs: Dict[str, Any], max_advance: int = 0):
        """Perform a simulation step.

        Parameters
        ----------
        time : int
            The current simulation step (by convention in seconds since
            simulation start.
        inputs : dict
            A *dict* containing inputs for entities of this simulator.

        Returns
        -------
        int
            The next step this simulator wants to be stepped.

        """
        self._time_synced = False
        self._sim_time = time

        # Default inputs
        for model in self.models.values():
            model.step_size = self.step_size
            model.now_dt = self.now_dt

        # Inputs from other simulators
        for eid, attrs in inputs.items():
            log_msg = {
                "id": f"{self.sid}.{eid}",
                "name": eid,
                "type": eid.split("-")[1],
                "sim_time": self._sim_time,
                "msg_type": "input",
                "src_eids": [],
            }

            for attr, src_ids in attrs.items():
                setpoint = 0.0
                all_none = True
                for src_id, value in src_ids.items():
                    if value is not None:
                        all_none = False
                        if attr == "now":
                            attr = "now_dt"
                            setpoint = datetime.strptime(value, GER)
                            log_msg["src_eids"].append(src_id)
                            if not self._time_synced:
                                self.now_dt = setpoint
                                self._time_synced = True
                            break
                        setpoint += float(value)
                        log_msg["src_eids"].append(src_id)
                if not all_none:
                    log_msg[attr] = setpoint
                    setattr(self.models[eid], attr, setpoint)
            log_msg["src_eids"] = list(set(log_msg["src_eids"]))
            LOG.info(json.dumps(log_msg, indent=4, default=str))

        # if inputs:
        #     if not self.key_value_logs:
        #         LOG.debug(
        #             "At step %d received inputs %s", time, mformat(inputs)
        #         )
        #     for eid, attrs in inputs.items():
        #         if self._time_synced:
        #             break
        #         for attr, src_ids in attrs.items():
        #             if self.key_value_logs:
        #                 self._log_input(eid, attr, src_ids)
        #             if attr != "now":
        #                 continue
        #             for val in src_ids.values():
        #                 self.now_dt = datetime.strptime(val, GER)
        #                 self._time_synced = True
        #                 break

        for model in self.models.values():
            # model.step_size = self.step_size
            # model.now_dt = self.now_dt
            model.step()

        if self.now_dt in self.scripted_events:
            self.active_events = self.scripted_events[self.now_dt]

        if not self._time_synced:
            self.now_dt += timedelta(seconds=self.step_size)

        return time + self.step_size

    def get_data(self, outputs):
        """Return the requested output (if feasible).

        Parameters
        ----------
        outputs : dict
            A *dict* containing requested outputs of each entity.

        Returns
        -------
        dict
            A *dict* containing the values of the requested outputs.

        """

        data = dict()
        for eid, attrs in outputs.items():
            data[eid] = dict()
            model = eid.split("-")[0]
            for attr in attrs:
                if attr not in self.meta["models"][model]["attrs"]:
                    raise ValueError(f"Unknown output attribute {attr}")

                value = getattr(self.models[eid], attr)
                if isinstance(value, pd.DataFrame):
                    value = value.to_json()
                if not isinstance(value, str):
                    value = float(value)
                # Evaluate scripted event
                # print(self.active_events)
                if attr in self.active_events:
                    value *= self.active_events[attr]
                data[eid][attr] = value
                if self.key_value_logs:
                    self._log_output(eid, attr, value)
        if not self.key_value_logs:
            LOG.debug(
                "At step %d gathered ouputs %s", self._sim_time, mformat(data)
            )
        return data

    def _load_data(self, data_path, filename):
        filepath = os.path.join(data_path, filename)
        if not os.path.isfile(filepath):
            LOG.error(
                "File at '%s' does not exist. Will try to fix this...",
                filepath,
            )
            filepath = os.path.join(
                RuntimeConfig().paths["data_path"],
                RuntimeConfig().data["weather"][0]["name"],
            )
            if not os.path.isfile(filepath):
                try:
                    tmp_path = os.path.join(
                        RuntimeConfig().paths["data_path"], "tmp"
                    )
                    os.makedirs(tmp_path, exist_ok=True)
                    WeatherDataModule().download(
                        RuntimeConfig().paths["data_path"],
                        tmp_path,
                        True,
                        False,
                    )
                    assert os.path.isfile(filepath)

                except Exception:
                    LOG.exception(
                        "Unable to find data set at '%s'. Will die now!",
                        filepath,
                    )
        wdata = WeatherData(filepath, self.rng.randint(self.seed_max))
        return wdata

    def _log_input(self, eid: str, attr: str, src_ids: Dict[str, Any]):
        for src_id, val in src_ids.items():
            if isinstance(val, np.ndarray):
                val = val.tolist()
            elif isinstance(val, np.integer):
                val = int(val)
            elif isinstance(val, (np.float32, np.floating)):
                val = float(val)

            LOG.debug(
                json.dumps(
                    {
                        "id": f"{self.sid}_{eid}",
                        "name": eid,
                        "type": eid.split("-")[0],
                        "msg_type": "input",
                        "attribute": attr,
                        "source": src_id,
                        "value": val,
                    }
                )
            )

    def _log_output(self, eid: str, attr: str, value: Any):
        LOG.debug(
            json.dumps(
                {
                    "id": f"{self.sid}_{eid}",
                    "name": eid,
                    "model": eid.split("-")[0],
                    "type": "output",
                    "attribute": attr,
                    "value": value,
                }
            )
        )


if __name__ == "__main__":
    set_and_init_logger(
        0, "weather-logfile", "midas-weather.log", replace=True
    )
    LOG.info("Starting mosaik simulation...")
    mosaik_api_v3.start_simulation(WeatherDataSimulator())
