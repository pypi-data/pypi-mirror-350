# src/whispa_app/__init__.py

"""
Whispa App package.

Provides transcription and translation of audio files via Whisper and MarianMT.
"""

__version__ = "2.1.0"

# Expose main application class and launcher
from .main import WhispaApp, launch_app
