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
    fig: plt.Figure = None,
    axes: plt.Axes = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    xlim: tuple[float, float] | None = None,
    ylim: tuple[float, float] | None = None,
    logx: bool | None = None,
    logy: bool | None = None,
    xscale: str | None = None,
    yscale: str | None = None,
    grid: bool | None = None,
    legend: bool | None = None,
    tight: bool | None = None,
    aspect: Any = None,
    strict: bool | None = None,
    **kwargs: Any,
) -> None:
    """
    Apply common styling to a 1D matplotlib Axes object.

    Parameters:
        fig (matplotlib.figure.Figure): Target figure. If None, uses current figure.
        axes (matplotlib.axes.Axes): Target axes. If None, uses current axes.
        title (str): Plot title.
        xlabel, ylabel (str): Axis labels.
        xlim, ylim (tuple): Axis limits as (min, max).
        logx, logy (bool): Use logarithmic x/y axis.
        xscale (str): Scale for the x-axis (e.g., 'linear', 'log'). Overrides `logx` if both are provided.
        yscale (str): Scale for the y-axis (e.g., 'linear', 'log'). Overrides `logy` if both are provided.
        grid (bool): Show grid.
        legend (bool): Show legend.
        tight (bool): Apply tight layout to the figure.
        aspect (Any): Aspect ratio for the axes.
        strict (bool): Raises errors.
        **kwargs: Placeholder for future extension.
    """
    if strict and kwargs:
        ve = "kwargs should be empty in strict mode."
        raise ValueError(ve)

    if axes is not None:
        ax = axes
    elif fig is not None:
        ax = fig.gca()
    else:
        ax = plt.gca()

    # Title and labels
    if title is not None:
        ax.set_title(title)
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    # Axis limits
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)

    # Log scaling
    if logx is not None:
        if logx:
            # Enable logarithmic x-axis
            ax.set_xscale("log")
        else:
            # Disable logarithmic x-axis
            ax.set_xscale("linear")
    if logy is not None:
        if logy:
            # Enable logarithmic y-axis
            ax.set_yscale("log")
        else:
            # Disable logarithmic y-axis
            ax.set_yscale("linear")

    if xscale is not None:
        ax.set_xscale(xscale)
    if yscale is not None:
        ax.set_yscale(yscale)

    # Grid
    if grid is not None:
        if grid:
            # Enable grid
            ax.grid(True)
        else:
            # Disable grid
            ax.grid(False)

    if aspect is not None:
        ax.set_aspect(aspect)

    # Legend
    if legend is not None:
        if legend:
            # Enable legend
            ax.legend()
        elif ax.get_legend():
            # Disable legend
            ax.get_legend().remove()
        # else no legend to remove

    if tight is not None:
        if tight:
            # Enable tight layout
            ax.figure.tight_layout()
        else:
            # Disable tight layout
            ax.figure.set_layout_engine(None)


def style_plot2d(
    axes: plt.Axes = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    xlim: tuple[float, float] | None = None,
    ylim: tuple[float, float] | None = None,
    aspect: Any = None,
    **kwargs: Any,
) -> None:
    """
    Apply common styling to a 2D matplotlib Axes object.
    Parameters:
        axes (matplotlib.axes.Axes): Target axes. If None, uses current axes.
        title (str): Plot title.
        xlabel, ylabel (str): Axis labels.
        xlim, ylim (tuple): Axis limits as (min, max).
        aspect (Any): Aspect ratio for the axes.
        **kwargs: Placeholder for future extension.
    """
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
