"""Dist plot."""

from __future__ import annotations

import logging
from typing import Literal

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import polars as pl
from scipy.stats import gaussian_kde

from .theme import Theme


def plot_dist(
    series: list[pl.Series],
    ax: plt.Axes,
    theme: Literal["science", "sharp", "nature", "purple"] = "science",
    fontsize: int | None = None,
    title: str | None = None,
    max_features: int = 5,
) -> plt.Axes:
    logger = logging.getLogger(__name__)
    themer = Theme(theme=theme, fontsize=fontsize)

    series_to_plot = []
    for s in series:
        if s.drop_nans().drop_nulls().len() == 0:
            logger.warning(f"{s.name} all empty, skip")
            continue
        try:
            _s = s.drop_nans().drop_nulls().to_numpy()
            _kde = gaussian_kde(_s)
            _x = np.linspace(_s.min(), _s.max(), 1000)
            _y = _kde(_x)
            series_to_plot.append((s.name, _x, _y))
        except Exception as e:
            logger.error(f"{s.name} error:\n{e}")
            continue

    if len(series_to_plot) == 0:
        logger.error("all series is none")
        return ax

    if len(series_to_plot) > max_features:
        logger.warning(
            f"too much features to plot {len(series_to_plot)} > {max_features}"
        )
        series_to_plot = series_to_plot[:max_features]

    legend_handles = []
    for sname, sx, sy in series_to_plot:
        _color = themer.get_color()
        ax.plot(sx, sy, color=_color, alpha=0.5, linewidth=2, label=sname)
        legend_handles.append(mpatches.Patch(color=_color, label=sname, alpha=0.5))
        ax.fill_between(sx, sy, color=_color, alpha=0.5 * 0.5)

    if title is None:
        if len(series) == 1:
            title = f"Distribution of {series[0].name}"
        else:
            title = "Distribution"

    ax.set_title(title, fontproperties=themer.font)
    ax.set_xlabel("Value", fontproperties=themer.font)
    ax.set_ylabel("Density", fontproperties=themer.font)
    ax.legend(handles=legend_handles)
    return ax
