from __future__ import annotations

import importlib.metadata

import thames as m


def test_version():
    assert importlib.metadata.version("thames") == m.__version__
