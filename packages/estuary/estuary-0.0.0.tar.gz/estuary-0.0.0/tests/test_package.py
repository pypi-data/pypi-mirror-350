from __future__ import annotations

import importlib.metadata

import estuary as m


def test_version():
    assert importlib.metadata.version("estuary") == m.__version__
