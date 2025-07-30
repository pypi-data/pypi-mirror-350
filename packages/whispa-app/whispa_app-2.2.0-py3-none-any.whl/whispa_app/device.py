import torch
import logging

def select_device(min_vram_gb: int = 6) -> str:
    if torch.cuda.is_available():
        try:
            vram = torch.cuda.get_device_properties(0).total_memory // (1024**3)
            logging.debug(f"GPU VRAM: {vram} GB")
            if vram >= min_vram_gb:
                return "cuda"
        except Exception as e:
            logging.warning(f"GPU query failed: {e}")
    return "cpu"
