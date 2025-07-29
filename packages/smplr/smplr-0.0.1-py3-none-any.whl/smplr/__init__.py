"""
Copyright (c) 2025 Alexander Puck Neuwirth. All rights reserved.

smplr: Simplified smpl
"""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt

from ._version import version as __version__

__all__ = ["__version__"]


def style_plot1d(
    axes: plt.Axes = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    xlim: tuple[float, float] | None = None,
    ylim: tuple[float, float] | None = None,
    logx: bool = False,
    logy: bool = False,
    grid: bool = False,
    legend: bool = False,
    tight: bool = False,
    aspect: Any = None,
    strict: bool = False,
    **kwargs: Any,
) -> plt.Axes:
    """
    Apply common styling to a 1D matplotlib Axes object.

    Parameters:
        axes (matplotlib.axes.Axes): Target axes. If None, uses current axes.
        title (str): Plot title.
        xlabel, ylabel (str): Axis labels.
        xlim, ylim (tuple): Axis limits as (min, max).
        logx, logy (bool): Use logarithmic x/y axis.
        grid (bool): Show grid.
        legend (bool): Show legend.
        tight (bool): Apply tight layout to the figure.
        aspect (Any): Aspect ratio for the axes.
        strict (bool): Raises errors.
        **kwargs: Placeholder for future extension.

    Returns:
        ax (matplotlib.axes.Axes): The styled axes object.
    """
    if strict and kwargs:
        ve = "kwargs should be empty in strict mode."
        raise ValueError(ve)

    ax = axes if axes is not None else plt.gca()

    # Title and labels
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)

    # Axis limits
    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)

    # Log scaling
    if logx:
        ax.set_xscale("log")
    if logy:
        ax.set_yscale("log")

    # Grid
    if grid:
        ax.grid(True)

    if aspect:
        ax.set_aspect(aspect)

    # Legend
    if legend:
        ax.legend()

    if tight:
        ax.figure.tight_layout()

    return ax


def style_plot2d(
    axes: plt.Axes = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    xlim: tuple[float, float] | None = None,
    ylim: tuple[float, float] | None = None,
    aspect: Any = None,
    **kwargs: Any,
) -> plt.Axes:
    ax = axes if axes is not None else plt.gca()
    style_plot1d(
        axes=ax,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        xlim=xlim,
        ylim=ylim,
        aspect=aspect,
        **kwargs,
    )
    return ax
