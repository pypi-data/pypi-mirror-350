from __future__ import annotations

from itertools import product

import matplotlib.pyplot as plt
import numpy as np

# With pytest-mpl
import pytest

import smplr


def create_plot(
    grid: bool | None = None,
    logx: bool | None = None,
    logy: bool | None = None,
    legend: bool | None = None,
    tight: bool | None = None,
) -> plt.Figure:
    plt.close("all")  # Clear any existing figures
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    fig, ax = plt.subplots()
    ax.plot(x, y, label="sin(x)")
    if grid:
        ax.grid(True)
    if logx:
        ax.set_xscale("log")
    if logy:
        ax.set_yscale("log")
    if legend:
        ax.legend()
    if tight:
        plt.tight_layout()
    return fig


@pytest.mark.parametrize(
    ("param", "start", "end"),
    product(
        ["tight", "legend", "grid", "logx", "logy"],
        [None, True, False],
        [None, True, False],
    ),
)
@pytest.mark.mpl_image_compare(baseline_dir="baseline", remove_text=True)
def test_bool(param, start, end):
    fig = create_plot(**{param: start})
    smplr.style_plot1d(fig=fig, **{param: end})
    return fig
