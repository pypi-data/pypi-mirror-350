# src/whispa_app/exporters.py

import json
from datetime import timedelta

def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT/VTT timestamp format."""
    td = timedelta(seconds=seconds)
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    seconds = td.seconds % 60
    milliseconds = td.microseconds // 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def save_as_srt(segments, file_path: str):
    """Save transcription segments in SubRip (.srt) format."""
    with open(file_path, 'w', encoding='utf-8') as f:
        for i, seg in enumerate(segments, 1):
            start = format_timestamp(seg['start'])
            end = format_timestamp(seg['end'])
            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{seg['text'].strip()}\n\n")

def save_as_vtt(segments, file_path: str):
    """Save transcription segments in WebVTT (.vtt) format."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("WEBVTT\n\n")
        for i, seg in enumerate(segments, 1):
            start = format_timestamp(seg['start']).replace(',', '.')
            end = format_timestamp(seg['end']).replace(',', '.')
            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{seg['text'].strip()}\n\n")

def save_as_json(segments, file_path: str):
    """Save transcription segments in JSON format."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump({
            'segments': segments,
            'text': ' '.join(seg['text'].strip() for seg in segments)
        }, f, ensure_ascii=False, indent=2) 