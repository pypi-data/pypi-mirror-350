"""Transcription functionality using Whisper models."""

import os
import logging
from typing import Dict, Any, Callable
from pathlib import Path
from faster_whisper import WhisperModel

# Global model cache
_model_cache = {}

def get_supported_audio_formats() -> list:
    """Get list of supported audio formats."""
    return ["wav", "mp3", "m4a", "ogg", "flac"]

def load_model(model_size: str, device: str = "auto") -> WhisperModel:
    """
    Load or get cached Whisper model.
    
    Args:
        model_size: Model size (tiny, base, small, medium, large)
        device: Device to use (cpu, cuda, auto)
        
    Returns:
        Loaded WhisperModel instance
    """
    # Normalize model size
    model_size = model_size.replace("model_", "")
    
    # Create cache key
    key = f"{model_size}_{device}"
    
    # Return cached model if available
    if key in _model_cache:
        return _model_cache[key]
        
    # Determine compute type based on device
    if device == "cpu":
        compute_type = "int8"
    else:
        # Try float16 first, fallback to int8 if not supported
        try:
            import torch
            if torch.cuda.is_available() and torch.cuda.get_device_capability()[0] >= 7:
                compute_type = "float16"
            else:
                compute_type = "int8"
        except:
            compute_type = "int8"
    
    # Check for local model first
    local_model_path = Path(__file__).parent / "models" / model_size
    model_path = str(local_model_path) if local_model_path.exists() else f"Systran/faster-whisper-{model_size}"
    
    try:
        logging.info(f"Loading Whisper model from {'local path' if local_model_path.exists() else 'hub'}: {model_size}")
        logging.info(f"Using device: {device}, compute type: {compute_type}")
        
        _model_cache[key] = WhisperModel(
            model_path,
            device=device,
            compute_type=compute_type,
            download_root=str(Path(__file__).parent / "models")
        )
        return _model_cache[key]
        
    except Exception as e:
        logging.error(f"Failed to load Whisper model '{model_size}': {str(e)}")
        raise RuntimeError(
            "Could not load the Whisper model. Ensure you have an internet connection "
            "for first-run downloads, or place a 'models/{model_size}' folder beside the EXE."
        )

def transcribe_file(
    file_path: str,
    model_size: str = "tiny",
    device: str = "auto",
    progress_callback: Callable[[float], None] = None
) -> Dict[str, Any]:
    """
    Transcribe audio file to text.
    
    Args:
        file_path: Path to audio file
        model_size: Whisper model size to use
        device: Device to run on (cpu, cuda, auto)
        progress_callback: Optional callback for progress updates
        
    Returns:
        Dict containing:
            - text: Full transcription text
            - segments: List of timed segments
            - language: Detected language
    """
    # Validate file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")
        
    # Validate file format
    ext = os.path.splitext(file_path)[1].lower()[1:]
    if ext not in get_supported_audio_formats():
        raise ValueError(f"Unsupported audio format: {ext}")
    
    # Force CPU if no GPU available
    try:
        import torch
        if not torch.cuda.is_available():
            device = "cpu"
            logging.info("No GPU detected, using CPU for transcription")
    except:
        device = "cpu"
        logging.info("PyTorch not available, using CPU for transcription")
    
    # Load model
    model = load_model(model_size, device)
    
    try:
        # Signal start of processing
        if progress_callback:
            progress_callback(0.1)  # Show some initial progress
            
        # Transcribe
        segments, info = model.transcribe(
            file_path,
            beam_size=5,
            word_timestamps=True,
            condition_on_previous_text=True,
            initial_prompt="",
            language=None,
            task="transcribe"
        )
        
        # Format output
        result = {
            "text": " ".join(seg.text for seg in segments),
            "segments": [
                {
                    "start": seg.start,
                    "end": seg.end,
                    "text": seg.text,
                    "id": i
                }
                for i, seg in enumerate(segments)
            ],
            "language": info.language
        }
        
        # Signal completion
        if progress_callback:
            progress_callback(1.0)
            
        return result
        
    except Exception as e:
        logging.error(f"Transcription failed: {str(e)}")
        raise RuntimeError(f"Transcription failed: {str(e)}")
