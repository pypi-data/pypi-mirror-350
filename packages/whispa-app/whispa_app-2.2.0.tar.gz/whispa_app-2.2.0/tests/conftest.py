"""Pytest configuration and shared fixtures."""

import os
import pytest
from pathlib import Path
from unittest.mock import Mock

@pytest.fixture
def test_dir():
    """Get the test directory path."""
    return Path(__file__).parent

@pytest.fixture
def data_dir(test_dir):
    """Create and get the test data directory."""
    data_path = test_dir / "data"
    data_path.mkdir(exist_ok=True)
    return data_path

@pytest.fixture
def mock_progress_callback():
    """Create a mock progress callback."""
    return Mock()

@pytest.fixture
def sample_transcription():
    """Sample transcription result."""
    return {
        "text": "This is a sample transcription.",
        "segments": [
            {
                "start": 0.0,
                "end": 2.0,
                "text": "This is",
                "id": 0
            },
            {
                "start": 2.0,
                "end": 4.0,
                "text": "a sample transcription.",
                "id": 1
            }
        ],
        "language": "en"
    }

@pytest.fixture
def sample_translation():
    """Sample translation result."""
    return {
        "text": "Esto es una transcripción de muestra.",
        "segments": [
            {
                "start": 0.0,
                "end": 2.0,
                "text": "Esto es",
                "id": 0
            },
            {
                "start": 2.0,
                "end": 4.0,
                "text": "una transcripción de muestra.",
                "id": 1
            }
        ],
        "language": "es"
    } 