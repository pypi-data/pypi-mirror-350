"""Export functionality for various subtitle formats."""

import json
from typing import List, Dict, Any, Union
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path

@dataclass
class Segment:
    """Represents a transcription/translation segment with timing."""
    
    start: float  # Start time in seconds
    end: float    # End time in seconds
    text: str     # Segment text
    
    def to_srt_timestamp(self, t: float) -> str:
        """Convert seconds to SRT timestamp format."""
        td = timedelta(seconds=t)
        hours = td.seconds // 3600
        minutes = (td.seconds % 3600) // 60
        seconds = td.seconds % 60
        milliseconds = round(td.microseconds / 1000)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
        
    def to_vtt_timestamp(self, t: float) -> str:
        """Convert seconds to WebVTT timestamp format."""
        td = timedelta(seconds=t)
        hours = td.seconds // 3600
        minutes = (td.seconds % 3600) // 60
        seconds = td.seconds % 60
        milliseconds = round(td.microseconds / 1000)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

class SubtitleExporter:
    """Handles exporting transcriptions to various subtitle formats."""
    
    def __init__(self, segments: List[Segment]):
        """
        Initialize subtitle exporter.
        
        Args:
            segments: List of transcription segments
        """
        self.segments = segments
        
    @classmethod
    def from_whisper_segments(
        cls,
        segments: List[Dict[str, Any]]
    ) -> "SubtitleExporter":
        """
        Create exporter from Whisper segments.
        
        Args:
            segments: List of Whisper segment dictionaries
            
        Returns:
            SubtitleExporter instance
        """
        converted = [
            Segment(
                start=seg["start"],
                end=seg["end"],
                text=seg["text"].strip()
            )
            for seg in segments
        ]
        return cls(converted)
        
    def to_srt(self, output_file: Union[str, Path]) -> None:
        """
        Export segments to SubRip (SRT) format.
        
        Args:
            output_file: Path to save SRT file
        """
        with open(output_file, "w", encoding="utf-8") as f:
            for i, segment in enumerate(self.segments, 1):
                # Segment number
                f.write(f"{i}\n")
                
                # Timestamps
                f.write(
                    f"{segment.to_srt_timestamp(segment.start)} --> "
                    f"{segment.to_srt_timestamp(segment.end)}\n"
                )
                
                # Text
                f.write(f"{segment.text}\n\n")
                
    def to_vtt(self, output_file: Union[str, Path]) -> None:
        """
        Export segments to WebVTT format.
        
        Args:
            output_file: Path to save VTT file
        """
        with open(output_file, "w", encoding="utf-8") as f:
            # WebVTT header
            f.write("WEBVTT\n\n")
            
            for i, segment in enumerate(self.segments, 1):
                # Optional cue identifier
                f.write(f"Cue {i}\n")
                
                # Timestamps
                f.write(
                    f"{segment.to_vtt_timestamp(segment.start)} --> "
                    f"{segment.to_vtt_timestamp(segment.end)}\n"
                )
                
                # Text
                f.write(f"{segment.text}\n\n")
                
    def to_json(self, output_file: Union[str, Path]) -> None:
        """
        Export segments to JSON format.
        
        Args:
            output_file: Path to save JSON file
        """
        data = {
            "segments": [
                {
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text
                }
                for segment in self.segments
            ]
        }
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    def to_txt(self, output_file: Union[str, Path]) -> None:
        """
        Export segments to plain text format.
        
        Args:
            output_file: Path to save text file
        """
        with open(output_file, "w", encoding="utf-8") as f:
            for segment in self.segments:
                f.write(f"{segment.text}\n") 