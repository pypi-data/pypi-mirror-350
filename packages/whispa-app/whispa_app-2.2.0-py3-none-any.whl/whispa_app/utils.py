import re
from datetime import timedelta

def simplify_text(text: str) -> str:
    """Clean up text by removing extra whitespace and normalizing punctuation."""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Normalize quotes
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace(''', "'").replace(''', "'")
    
    # Fix spacing around punctuation
    text = re.sub(r'\s+([.,!?])', r'\1', text)
    text = re.sub(r'([.,!?])\s+', r'\1 ', text)
    
    return text.strip()

def format_timestamp(seconds: float) -> str:
    """Convert seconds to timestamp format (HH:MM:SS,mmm)."""
    td = timedelta(seconds=seconds)
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    seconds = td.seconds % 60
    milliseconds = td.microseconds // 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def format_duration(seconds: float) -> str:
    """Format duration in a human-readable format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

def format_file_size(size_bytes: int) -> str:
    """Format file size in a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"
