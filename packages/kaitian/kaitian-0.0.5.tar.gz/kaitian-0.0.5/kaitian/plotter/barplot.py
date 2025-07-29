"""Bar and Bar-line plot."""

from __future__ import annotations

import logging
from typing import Literal

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import polars as pl

from .theme import Theme


def plot_bar(
    data: pl.DataFrame,
    ax: plt.Axes,
    bars: list[str] | str,
    lines: list[str] | str | None = None,
    stack: list | None = None,
    overlap: list | None = None,
    theme: Literal["science", "sharp", "nature", "purple"] = "science",
    fontsize: int | None = None,
    title: str | None = None,
) -> plt.Axes:
    logger = logging.getLogger(__name__)
    themer = Theme(theme=theme, fontsize=fontsize)

    if isinstance(bars, str):
        bars = [bars]
    if lines is None:
        lines = []
    elif isinstance(lines, str):
        lines = [lines]
    ...
