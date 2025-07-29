"""
A data series in a plot
"""

import typing

from pydantic import BaseModel

from icplot.color import Color


class PlotSeries(BaseModel, frozen=True):
    """
    A data series in a plot, such as a single line in a line-plot

    :param position_right: allows the series to be plotted on the right y-axis.
    :type position_right: bool, optional
    """

    label: str
    color: Color = Color()
    series_type: str = ""
    highlight: bool = False
    position_right: bool = False


class ImageSeries(PlotSeries, frozen=True):
    """
    A plot data series where the elements are images
    """

    data: typing.Any
    transform: typing.Any
    series_type: str = "image"


class LinePlotSeries(PlotSeries, frozen=True):
    """
    A plot series for line plots

    :param drawstyle: Naming comes from matplotlib API, allows for various square plots,
               default is a normal point to point line plot.
    :type drawstyle: str, optional
    """

    x: list
    y: list
    x_err: float | list[float] | list[list[float]] | None = None
    y_err: float | list[float] | list[list[float]] | None = None
    err_capsize: float = 2.0
    marker: str = "o"
    series_type: str = "line"
    drawstyle: str = "default"
    linestyle: str = "-"


class ScatterPlotSeries(PlotSeries, frozen=True):
    """
    Scatter type plot series
    """

    data: typing.Any
    series_type: str = "scatter"
