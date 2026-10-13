"""Shared pytest fixtures: make ``src`` importable and load the real dataset."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

RAW_DATASET = ROOT / "data" / "raw" / "penguins.csv"


@pytest.fixture(scope="session")
def project_root() -> Path:
    return ROOT


@pytest.fixture(scope="session")
def raw_dataset():
    """The real Palmer Penguins dataset (skips the test when unavailable)."""
    if not RAW_DATASET.exists():
        pytest.skip("data/raw/penguins.csv not available in this environment")
    from src.data_loader import load_dataset

    return load_dataset(RAW_DATASET, root=ROOT, allow_upload=False)
