"""Pytest configuration and shared fixtures."""
import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Generator


@pytest.fixture
def temp_output_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test outputs."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_cut_pieces():
    """Provide sample cut pieces for testing."""
    from src.generate_bom import CutPiece
    
    return [
        CutPiece("2x4", 48.0, 4, "Legs"),
        CutPiece("2x4", 57.0, 2, "Long stretchers"),
        CutPiece("2x4", 21.0, 2, "Short stretchers"),
        CutPiece("2x6", 60.0, 5, "Top boards"),
    ]


@pytest.fixture
def mock_lumber_prices():
    """Provide mock lumber prices for testing."""
    return {
        "2x4": {"price_per_foot": 0.70},
        "2x6": {"price_per_foot": 1.10},
        "1x4": {"price_per_foot": 0.50},
        "1x6": {"price_per_foot": 0.80},
        "1x10": {"price_per_foot": 1.50},
        "1x12": {"price_per_foot": 2.00},
        "4x4": {"price_per_foot": 2.50},
    }