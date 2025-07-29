"""
Module to support plotting with matplotlib
"""

import os
from pathlib import Path
import shutil

import numpy as np
import matplotlib.pyplot as plt

from iccore.data.quantity import Quantity
from iccore.data.units import DateRange, to_date_str
from iccore.data import Series, Array

from .plot_group import PlotGroup
from .video import images_to_video


def get_axis_label_from_quantity(quantity: Quantity) -> str:

    if quantity.name == "time":
        return f"{quantity.long_name} (UTC)"

    if quantity.unit.get_symbol():
        return f"{quantity.long_name} ({quantity.unit.get_symbol()})"

    return quantity.long_name


def get_axis_label(array: Array) -> str:
    return get_axis_label_from_quantity(array.quantity)


def get_grid(series: Series):

    if not series.x or not series.y:
        raise RuntimeError("Series missing expected data")

    return np.meshgrid(series.x.data, series.y.data)


def save_plot(fig, path: Path, filename: str, file_prefix: str = ""):
    plt.tight_layout()
    prefix = f"{file_prefix}_" if file_prefix else ""
    os.makedirs(path, exist_ok=True)
    plt.savefig(path / f"{prefix}{filename}")
    plt.clf()
    plt.close(fig)


def get_date_suffix(dates: DateRange | None) -> str:
    if not dates:
        return ""
    if not dates.start or not dates.end:
        return ""

    return f"_FROM_{to_date_str(dates.start)}_TO_{to_date_str(dates.end)}"


def plot_2d(
    path: Path, config: PlotGroup, series: Series, quantity: str, file_prefix: str = ""
):
    """
    Generate a contour plot for the provided quantity
    """

    if not series.x:
        raise RuntimeError("Expected series with an x quantity")

    if not series.y:
        raise RuntimeError("Expected series with a y quantity.")

    x, y = get_grid(series)

    array = series.get_array(quantity)

    fig, ax = plt.subplots()

    ax.set_ylabel(get_axis_label(series.y))
    ax.set_xlabel(get_axis_label(series.x))

    if config.date_range:
        start, end = config.date_range.as_tuple()
        if start and end:
            ax.set_xlim((start, end))  # type: ignore
    fig.autofmt_xdate()

    if config.contour.show_grid:
        ax.grid(c="k", ls="-", alpha=0.3)

    if False and array.quantity.has_limits:
        cs = ax.contourf(
            x,
            y,
            np.clip(array.data.T, array.quantity.limits[0], array.quantity.limits[1]),
            cmap=config.contour.colormap,
        )
    else:
        cs = ax.contourf(x, y, array.data.T, cmap=config.contour.colormap)

    cbar = fig.colorbar(cs)
    cbar.ax.set_ylabel(get_axis_label(array))

    save_plot(
        fig,
        path,
        f"{quantity}{get_date_suffix(config.date_range)}.{config.contour.format}",
        file_prefix,
    )


def plot_1d(
    path: Path, config: PlotGroup, series: Series, quantity: str, file_prefix: str = ""
):
    """
    Generate a line plot for the provided quantity
    """

    if not series.x:
        raise RuntimeError("Attempted to plot series without x data")

    array = series.get_array(quantity)

    fig, ax = plt.subplots()
    ax.set_xlabel(get_axis_label(series.x))
    ax.set_ylabel(get_axis_label(array))

    if config.date_range:
        ax.set_xlim(config.date_range.as_tuple())  # type: ignore
    fig.autofmt_xdate()

    if array.quantity.has_limits:
        ax.set_ylim(array.quantity.limits)  # type: ignore

    x = array.data.index.to_numpy(dtype="datetime64[ns]")
    y = array.data.values
    ax.plot(x, y)

    save_plot(
        fig,
        path,
        f"{quantity}{get_date_suffix(config.date_range)}.{config.line.format}",
        file_prefix,
    )


def plot_array(path: Path, series: Series, array: Array, file_prefix):
    """
    Plot an array for a single series x value. Useful for
    time series video frames.
    """

    if not series.x or not series.y:
        raise RuntimeError("Attempted to plot series with missing data")

    for idx, (x, values) in enumerate(zip(series.x.data, array.data)):
        fig, ax = plt.subplots()

        ax.set_title(x)
        ax.set_xlabel(get_axis_label(array))
        ax.set_ylabel(get_axis_label(series.y))

        if array.quantity.has_limits:
            ax.set_xlim(array.quantity.limits)  # type: ignore

        ax.plot(values, series.y.data)

        prefix = f"{file_prefix}_" if file_prefix else ""
        save_plot(fig, path / f"{prefix}{array.quantity.name}", f"{idx}.png")


def make_video(
    path: Path, config: PlotGroup, series: Series, quantity: str, file_prefix: str = ""
):
    plot_array(path, series, series.get_array(quantity), file_prefix)

    prefix = f"{file_prefix}_" if file_prefix else ""

    if not config.video:
        return

    images_to_video(
        path / f"{prefix}{quantity}",
        path,
        f"{prefix}{quantity}{get_date_suffix(config.date_range)}",
        fps=config.video.fps,
        video_format=config.video.format,
    )
    shutil.rmtree(path / f"{prefix}{quantity}")


def plot(
    path: Path,
    config: PlotGroup,
    series: Series,
    quantity: Quantity,
    file_prefix: str = "",
):
    """
    Handle plotting 1-d and 2-d time series and videos for the given quantity
    """

    if series.is_compound:
        for c in series.components:
            plot(path, config, c, quantity, c.name)
        return

    if series.y:
        plot_2d(path, config, series, quantity.name, file_prefix)

        if config.video and config.video.active:
            make_video(path, config, series, quantity.name, file_prefix)
        return

    plot_1d(path, config, series, quantity.name, file_prefix)
