"""Prefetch Whisper models for offline use."""

import os
import sys
import logging
from pathlib import Path
from faster_whisper import WhisperModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def download_model(model_size: str, device: str = "cpu") -> None:
    """
    Download and cache a Whisper model.
    
    Args:
        model_size: Model size (tiny, base, small, medium, large)
        device: Device to use (cpu, cuda)
    """
    try:
        # Normalize model size
        model_size = model_size.replace("model_", "")
        
        # Set download path
        if getattr(sys, "frozen", False):
            # Running as compiled EXE
            base_path = Path(sys.executable).parent
        else:
            # Running as script
            base_path = Path(__file__).parent
            
        download_path = base_path / "models"
        download_path.mkdir(exist_ok=True)
        
        logging.info(f"Downloading {model_size} model to {download_path}...")
        
        # Download model
        WhisperModel(
            f"Systran/faster-whisper-{model_size}",
            device=device,
            compute_type="int8" if device == "cpu" else "float16",
            download_root=str(download_path)
        )
        
        logging.info(f"Successfully downloaded {model_size} model")
        
    except Exception as e:
        logging.error(f"Failed to download {model_size} model: {str(e)}")
        raise

def main():
    """Download all Whisper models."""
    models = ["tiny", "base", "small", "medium", "large"]
    device = "cpu"  # Default to CPU for compatibility
    
    logging.info("Starting model downloads...")
    
    for model in models:
        try:
            download_model(model, device)
        except Exception as e:
            logging.error(f"Skipping {model} model due to error: {str(e)}")
            continue
            
    logging.info("Finished downloading models")

if __name__ == "__main__":
    main()
