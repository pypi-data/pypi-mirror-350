"""Tests for transcription functionality."""

import os
import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from whispa_app.transcription import transcribe_file, get_supported_audio_formats

@pytest.fixture
def sample_audio_path(tmp_path):
    """Create a dummy audio file for testing."""
    audio_file = tmp_path / "test.wav"
    audio_file.write_bytes(b"dummy audio content")
    return str(audio_file)

@pytest.fixture
def mock_whisper_model():
    """Mock Whisper model for testing."""
    model = Mock()
    model.transcribe.return_value = (
        [
            Mock(start=0.0, end=2.0, text="Hello,"),
            Mock(start=2.0, end=4.0, text="this is a test transcription.")
        ],
        Mock(language="en")
    )
    return model

def test_get_supported_audio_formats():
    """Test getting supported audio formats."""
    formats = get_supported_audio_formats()
    assert isinstance(formats, list)
    assert len(formats) > 0
    assert all(isinstance(fmt, str) for fmt in formats)
    assert "wav" in formats
    assert "mp3" in formats

@patch("whispa_app.transcription.load_model")
def test_transcribe_file_success(mock_load_model, sample_audio_path, mock_whisper_model):
    """Test successful transcription."""
    mock_load_model.return_value = mock_whisper_model
    
    result = transcribe_file(
        file_path=sample_audio_path,
        model_size="tiny",
        device="cpu",
        progress_callback=lambda x: None
    )
    
    assert isinstance(result, dict)
    assert "text" in result
    assert "segments" in result
    assert len(result["segments"]) > 0
    assert result["text"] == "Hello, this is a test transcription."

@patch("whispa_app.transcription.load_model")
def test_transcribe_file_progress(mock_load_model, sample_audio_path, mock_whisper_model):
    """Test transcription progress callback."""
    mock_load_model.return_value = mock_whisper_model
    progress_values = []
    
    def progress_callback(value):
        progress_values.append(value)
    
    transcribe_file(
        file_path=sample_audio_path,
        model_size="tiny",
        device="cpu",
        progress_callback=progress_callback
    )
    
    assert len(progress_values) > 0
    assert min(progress_values) >= 0
    assert max(progress_values) <= 100

def test_transcribe_file_invalid_path():
    """Test transcription with invalid file path."""
    with pytest.raises(FileNotFoundError):
        transcribe_file(
            file_path="nonexistent.wav",
            model_size="tiny",
            device="cpu",
            progress_callback=lambda x: None
        )

def test_transcribe_file_invalid_format(tmp_path):
    """Test transcription with unsupported file format."""
    invalid_file = tmp_path / "test.xyz"
    invalid_file.write_text("dummy content")
    
    with pytest.raises(ValueError, match="Unsupported audio format"):
        transcribe_file(
            file_path=str(invalid_file),
            model_size="tiny",
            device="cpu",
            progress_callback=lambda x: None
        ) 