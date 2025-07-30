"""Provide global test fixtures."""

from typing import Any

import numpy as np
import pytest


@pytest.fixture()
def tolerance() -> float:
    """Float: Tolerance for testing."""
    return 1e-8


@pytest.fixture()
def loaders() -> dict[str, Any]:
    """Provide object for testing."""
    import json

    import yaml

    return {".json": json.loads, ".yaml": yaml.safe_load}


@pytest.fixture()
def T_list() -> list[float]:
    """Return a list of temperatures for testing."""
    return np.linspace(300, 9999, 100).tolist()  # type: ignore
