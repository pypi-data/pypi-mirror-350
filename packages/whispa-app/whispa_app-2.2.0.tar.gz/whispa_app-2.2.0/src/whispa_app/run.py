# run.py
import sys
from whispa_app.transcription import get_whisper_model
from whispa_app.translation import MODEL_MAP, get_translation_model
from whispa_app.device import select_device
from whispa_app.main import launch_app

def prefetch_models():
    """Download all Whisper + translation models into the HF cache."""
    device = select_device(min_vram_gb=0)  # CPU only

    print("=== Prefetching Whisper models ===")
    for size in ["tiny", "base", "small", "medium", "large"]:
        print(f"Downloading Whisper '{size}'...")
        get_whisper_model(size, device)

    print("\n=== Prefetching translation models ===")
    for lang, repo in MODEL_MAP.items():
        print(f"Downloading translation model for {lang}...")
        get_translation_model(repo, device)

    print("\nAll models cached. You can now use the app offline.")
    sys.exit(0)

def main():
    if "--prefetch" in sys.argv:
        prefetch_models()
    else:
        launch_app()

if __name__ == "__main__":
    main()  # For direct execution during development