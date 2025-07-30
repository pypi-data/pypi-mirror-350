"""MIDAS upgrade module for the weather data simulator."""

import logging
from importlib import import_module

import pandas as pd
from midas.scenario.upgrade_module import UpgradeModule
from midas.util.runtime_config import RuntimeConfig

from .analysis import analyze
from .download import download_weather
from .meta import (
    AVG_T_AIR,
    BI,
    DI,
    PRESSURE,
    RADIATION_DELTA,
    T_AIR,
    T_AIR_DELTA,
    WIND,
    WIND_DELTA,
    WINDDIR,
)

LOG = logging.getLogger(__name__)


class WeatherDataModule(UpgradeModule):
    def __init__(self):
        super().__init__(
            module_name="weather",
            default_scope_name="bremen",
            default_sim_config_name="WeatherData",
            default_import_str=(
                "midas_weather.simulator:WeatherDataSimulator"
            ),
            default_cmd_str=("%(python)s -m midas_weather.simulator %(addr)s"),
            log=LOG,
        )

        self.attrs = {
            T_AIR: [-20, 45],
            AVG_T_AIR: [-20, 45],
            BI: [0, 1368],
            DI: [0, 1368],
            WIND: [0, 150],
            WINDDIR: [0, 360],
            PRESSURE: [700, 1100],
            # wind direction
        }
        self.input_attrs = {
            WIND_DELTA: [-20, 20],
            T_AIR_DELTA: [-20, 20],
            RADIATION_DELTA: [-20, 20],
        }
        self.models = {
            "WeatherCurrent": [attr for attr in self.attrs],
            "WeatherForecast": [f"forecast_{attr}" for attr in self.attrs],
        }
        self._sensors: list = []
        self._actuators: list = []

    def check_module_params(self, module_params):
        """Check the module params and provide default values."""

        module_params.setdefault("start_date", self.scenario.base.start_date)
        module_params.setdefault("data_path", self.scenario.base.data_path)
        module_params.setdefault("interpolate", False)
        module_params.setdefault("noise_factor", 0.05)
        module_params.setdefault(
            "forecast_horizon_hours", self.scenario.base.forecast_horizon_hours
        )
        module_params.setdefault("forecast_error", 0.05)

        if self.scenario.base.no_rng:
            module_params["randomize"] = False
        else:
            module_params.setdefault("randomize", False)

    def check_sim_params(self, module_params):
        """Check the params for a certain simulator instance."""

        self.sim_params.setdefault("start_date", module_params["start_date"])
        self.sim_params.setdefault("data_path", module_params["data_path"])
        self.sim_params.setdefault("interpolate", module_params["interpolate"])
        self.sim_params.setdefault(
            "noise_factor", module_params["noise_factor"]
        )
        self.sim_params.setdefault(
            "forecast_horizon_hours", module_params["forecast_horizon_hours"]
        )
        self.sim_params.setdefault(
            "forecast_error", module_params["forecast_error"]
        )
        self.sim_params.setdefault("randomize", module_params["randomize"])
        self.sim_params.setdefault("seed_max", self.scenario.base.seed_max)
        self.sim_params.setdefault("seed", self.scenario.create_seed())
        self.sim_params.setdefault(
            "filename", RuntimeConfig().data["weather"][0]["name"]
        )
        self.sim_params.setdefault("scripted_events", {})

    def start_models(self):
        """Start models of a certain simulator."""
        mapping_key = "weather_mapping"
        if not self.sim_params.setdefault(
            mapping_key, self.create_default_mapping()
        ):
            # No mapping configured
            return

        if ":" in self.default_import_str:
            mod, clazz = self.default_import_str.split(":")
        else:
            mod, clazz = self.default_import_str.rsplit(".", 1)
        mod = import_module(mod)

        sim_dummy = getattr(mod, clazz)()
        sim_dummy.init(self.sid, **self.sim_params)

        for model, configs in self.sim_params[mapping_key].items():
            model_low = model.lower()

            for idx, config in enumerate(configs):
                model_key = self.scenario.generate_model_key(
                    self, model_low, idx
                )
                self.start_model(model_key, model, config)
                entity = sim_dummy.create(1, model, **config)[0]
                if model == "WeatherForecast":
                    # TODO: add as soon as it is requested
                    continue
                for attr, interval in self.attrs.items():
                    self._sensors.append(
                        {
                            "uid": f"{self.sid}.{entity['eid']}.{attr}",
                            "space": (
                                f"Box(low={interval[0]}, high={interval[1]}, "
                                "shape=(), dtype=np.float32)"
                            ),
                        }
                    )
                for attr, interval in self.input_attrs.items():
                    self._actuators.append(
                        {
                            "uid": f"{self.sid}.{entity['eid']}.{attr}",
                            "space": (
                                f"Box(low={interval[0]}, high={interval[1]}, "
                                "shape=(), dtype=np.float32)"
                            ),
                        }
                    )

    def connect(self):
        if self.sim_params["with_timesim"]:
            for model in self.models:
                if model not in self.sim_params["weather_mapping"]:
                    continue

                timesim, _ = self.scenario.find_first_model("timesim")
                for idx, _ in enumerate(
                    self.sim_params["weather_mapping"][model]
                ):
                    entity = self.scenario.generate_model_key(
                        self, model.lower(), idx
                    )
                    self.connect_entities(
                        timesim, entity, [("local_time", "now")]
                    )

    def connect_to_db(self):
        """Connect models to db."""
        mapping_key = "weather_mapping"
        db_key = self.scenario.find_first_model("store", "database")[0]

        for model, attrs in self.models.items():
            if model == "WeatherForecast":
                # TODO: add as soon as arrays/lists can be stored
                continue

            for idx, _ in enumerate(self.sim_params[mapping_key][model]):
                model_key = self.scenario.generate_model_key(
                    self, model.lower(), idx
                )
                self.connect_entities(model_key, db_key, attrs)

    def create_default_mapping(self):
        default_mapping = {}
        if not self.sim_params["weather_mapping"]:
            self.sim_params["weather_mapping"]["WeatherCurrent"] = [
                {
                    "interpolate": self.sim_params["interpolate"],
                    "randomize": self.sim_params["randomize"],
                }
            ]
        return default_mapping

    def download(self, data_path, tmp_path, force):
        download_weather(data_path, tmp_path, force)

    def analyze(
        self,
        name: str,
        data: pd.HDFStore,
        output_folder: str,
        start: int,
        end: int,
        step_size: int,
        full: bool,
    ):
        analyze(name, data, output_folder, start, end, step_size, full)

    def get_sensors(self):
        for sensor in self._sensors:
            self.scenario.sensors.append(sensor)
            LOG.debug(f"Created sensor entry {sensor}.")

        self._sensors = []

    def get_actuators(self):
        for actuator in self._actuators:
            self.scenario.actuators.append(actuator)
            LOG.debug(f"Created actuator entry {actuator}.")

        self._actuators = []
