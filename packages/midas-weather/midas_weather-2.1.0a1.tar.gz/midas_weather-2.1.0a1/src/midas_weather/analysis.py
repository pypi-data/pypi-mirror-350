import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from midas.util import report_util

from .meta import (
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

ATTR_UNIT_MAP = {
    T_AIR: "temperature [°C]",
    AVG_T_AIR: "temperature [°C]",
    BI: "radiation [W/m²]",
    DI: "radiation [W/m²]",
    WIND: "speed [m/s]",
    WINDDIR: "direction [°]",
    PRESSURE: "pressure [hPA]",
    SUN_HOURS: "[min/h]",
    CLOUDINESS: "percentage [%]",
}


def analyze(
    name: str,
    data: pd.HDFStore,
    output_folder: str,
    start: int,
    end: int,
    step_size: int,
    full: bool,
):
    weather_sim_keys = [
        sim_key for sim_key in data.keys() if "WeatherData" in sim_key
    ]

    for sim_key in weather_sim_keys:
        wdata = data[sim_key]
        if start > 0:
            wdata = wdata.iloc[start:]
        if end > 0:
            wdata = wdata.iloc[:end]

        analyze_weather(
            wdata,
            step_size,
            f"{name}-{sim_key.replace('/', '')}",
            output_folder,
            full,
        )


def analyze_weather(data, step_size, name, output_path, full_report):
    plot_path = os.path.join(
        output_path, name.rsplit("-", 1)[1].replace("__", "_")
    )
    os.makedirs(plot_path, exist_ok=True)

    report_content = []

    report_path = os.path.join(output_path, f"{name}_report.md")
    report_file = open(report_path, "w")
    stats = {}
    for col in data.columns:
        _, attr = col.split("___")
        stats[attr] = {
            "Min": data[col].min(),
            "Max": data[col].max(),
            "Mean": data[col].mean(),
            "Std": data[col].std(),
        }
        stats[attr]["plot"] = _plot_series(data[col], attr, name, plot_path)
    _create_report(stats, report_content)

    for line in report_content:
        report_file.write(f"{line}\n")
    report_file.close()

    report_util.convert_markdown(report_path)


def _plot_series(data, attr, name, output_path):
    series = data.values

    annual = np.sort(series)[::-1]
    _, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
    ax1.plot(series)
    ax1.set_title(f"{attr}")
    ax1.set_ylabel(ATTR_UNIT_MAP[attr])

    ax2.plot(annual)
    ax2.set_title(f"annual curve {attr}")
    ax2.set_ylabel(ATTR_UNIT_MAP[attr])
    ax2.set_xlabel("time [s]")

    filename = os.path.join(output_path, f"{name}_{attr}.png")
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()

    return filename


def _create_report(stats, report):
    report.append("# Analysis of Weather Data\n")

    for attr, keys in stats.items():
        report.append(
            f"## Summary of {attr}\n\n*Quantity [Unit]*: "
            f"{ATTR_UNIT_MAP[attr]}\n"
        )
        for key, val in keys.items():
            if key != "plot":
                report.append(f"- {key}: {val:.3f}")

        report.append(f"\n![{attr}]({keys['plot']})" + "{width=60%}\n")
    report.append("")
