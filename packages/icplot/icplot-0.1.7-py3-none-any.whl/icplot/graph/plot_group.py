"""
Module to handle generation of plots
"""

from datetime import date
from dataclasses import dataclass

from pydantic import BaseModel

from iccore.data.units import DateRange
from iccore.data.quantity import Quantity


@dataclass(frozen=True)
class VideoConfig:
    """
    Representation of a video
    """

    fps: int = 5
    format: str = "mp4"
    active: bool = True


@dataclass(frozen=True)
class ContourConfig:
    """
    Representation of a contour plot
    """

    show_grid: bool = True
    colormap: str = "rainbow"
    format: str = "png"


@dataclass(frozen=True)
class LineConfig:
    """
    Representatino of a line plot
    """

    format: str = "png"


class PlotGroup(BaseModel, frozen=True):
    """
    A group of plots to be generated, one per quantity.
    """

    quantities: list[Quantity] = []
    start_date: date | None = None
    end_date: date | None = None
    video: VideoConfig | None = None
    contour: ContourConfig = ContourConfig()
    line: LineConfig = LineConfig()
    formats: tuple[str, ...] = ("mpl", "vtk")
    active: bool = True

    @property
    def date_range(self) -> DateRange | None:
        if not self.start_date:
            return None
        return DateRange(start=self.start_date, end=self.end_date)
