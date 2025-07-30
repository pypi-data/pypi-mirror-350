"""Tests for the telemetry module."""

import os
import json
from pathlib import Path
import pytest
from whispa_app.telemetry import Telemetry

def test_telemetry_initialization():
    """Test basic telemetry initialization."""
    telemetry = Telemetry()
    assert not telemetry.opt_out
    assert telemetry.session_id is not None

def test_telemetry_opt_out():
    """Test telemetry opt-out functionality."""
    telemetry = Telemetry(opt_out=True)
    assert telemetry.opt_out
    
    # Record should not create any files when opted out
    telemetry.record_transcription(
        model_size="small",
        file_type="wav",
        file_size=1000,
        duration_ms=5000,
        success=True
    )
    
    metrics_dir = telemetry._get_metrics_dir()
    assert not any(metrics_dir.glob("*.json"))

def test_record_transcription():
    """Test recording transcription metrics."""
    telemetry = Telemetry()
    
    # Record a transcription
    telemetry.record_transcription(
        model_size="small",
        file_type="wav",
        file_size=1000,
        duration_ms=5000,
        success=True
    )
    
    # Check if metrics file was created
    metrics_dir = telemetry._get_metrics_dir()
    json_files = list(metrics_dir.glob("transcription_*.json"))
    assert len(json_files) > 0
    
    # Verify metrics content
    with open(json_files[0]) as f:
        metrics = json.load(f)
        assert metrics["event_type"] == "transcription"
        assert metrics["model_size"] == "small"
        assert metrics["file_type"] == "wav"
        assert metrics["success"] is True

@pytest.fixture(autouse=True)
def cleanup():
    """Clean up test metrics files."""
    yield
    telemetry = Telemetry()
    metrics_dir = telemetry._get_metrics_dir()
    if metrics_dir.exists():
        for f in metrics_dir.glob("*.json"):
            f.unlink()
        metrics_dir.rmdir() 