"""This module contains the mosaik meta for the weather simulator."""

DATE = "Datetime"
T_AIR = "t_air_deg_celsius"
AVG_T_AIR = "day_avg_t_air_deg_celsius"
GHI = "gh_w_per_m2"
BI = "bh_w_per_m2"
DI = "dh_w_per_m2"
WIND = "wind_v_m_per_s"
WINDDIR = "wind_dir_deg"
PRESSURE = "air_pressure_hpa"
CLOUDINESS = "cloud_percent"
SUN_HOURS = "sun_hours_min_per_h"
T_AIR_DELTA = "delta_" + T_AIR
RADIATION_DELTA = "delta_" + GHI
WIND_DELTA = "delta_" + WIND


META = {
    "type": "time-based",
    "models": {
        "WeatherCurrent": {
            "public": True,
            "params": [
                "data_path",
                "start_date",
                "interpolate",
                "randomize",
                "seed",
                "block_mode",
                "frame",
            ],
            "attrs": [
                "now",
                BI,
                DI,
                T_AIR,
                AVG_T_AIR,
                WIND,
                WINDDIR,
                PRESSURE,
                CLOUDINESS,
                SUN_HOURS,
                T_AIR_DELTA,
                RADIATION_DELTA,
                WIND_DELTA,
            ],
        },
        "WeatherForecast": {
            "public": True,
            "params": [
                "data_path",
                "start_date",
                "interpolate",
                "forecast_error",
                "seed",
                "randomize",
                "forecast_horizon_hours",
                "block_mode",
                "frame",
            ],
            "attrs": [
                "now",
                "forecast_horizon_hours",
                f"forecast_{BI}",
                f"forecast_{DI}",
                f"forecast_{T_AIR}",
                f"forecast_{AVG_T_AIR}",
                f"forecast_{WIND}",
                f"forecast_{WINDDIR}",
                f"forecast_{PRESSURE}",
                f"forecast_{CLOUDINESS}",
                f"forecast_{SUN_HOURS}",
            ],
        },
    },
}
