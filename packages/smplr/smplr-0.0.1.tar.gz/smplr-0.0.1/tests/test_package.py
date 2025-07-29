from __future__ import annotations

import importlib.metadata

import smplr as m


def test_version():
    assert importlib.metadata.version("smplr") == m.__version__
