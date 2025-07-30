"""Batch processing for multiple audio files."""

import os
import json
import logging
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from .transcription import transcribe_file
from .translation import translate
from .telemetry import Telemetry

@dataclass
class BatchJob:
    """Represents a single file in a batch processing job."""
    input_file: Path
    output_dir: Path
    model_size: str
    target_language: Optional[str] = None
    status: str = "pending"
    error: Optional[str] = None
    transcription: Optional[str] = None
    translation: Optional[str] = None

class BatchProcessor:
    """Handles batch processing of multiple audio files."""
    
    SUPPORTED_FORMATS = {".wav", ".mp3", ".m4a", ".flac", ".ogg", ".aac"}
    
    def __init__(
        self,
        output_dir: Optional[Path] = None,
        max_workers: int = 4,
        telemetry: Optional[Telemetry] = None
    ):
        """
        Initialize batch processor.
        
        Args:
            output_dir: Directory to save output files
            max_workers: Maximum number of concurrent jobs
            telemetry: Optional telemetry instance
        """
        self.output_dir = output_dir or Path.cwd() / "output"
        self.max_workers = max_workers
        self.telemetry = telemetry
        self.jobs: List[BatchJob] = []
        
    def add_files(
        self,
        files: List[str],
        model_size: str,
        target_language: Optional[str] = None
    ) -> None:
        """
        Add files to the batch processing queue.
        
        Args:
            files: List of file paths
            model_size: Whisper model size to use
            target_language: Optional target language for translation
        """
        for file in files:
            path = Path(file)
            if path.suffix.lower() in self.SUPPORTED_FORMATS:
                self.jobs.append(BatchJob(
                    input_file=path,
                    output_dir=self.output_dir / path.stem,
                    model_size=model_size,
                    target_language=target_language
                ))
            else:
                logging.warning(f"Unsupported file format: {file}")
                
    def process_all(
        self,
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> None:
        """
        Process all jobs in the queue.
        
        Args:
            progress_callback: Optional callback for progress updates
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)
        total_jobs = len(self.jobs)
        completed = 0
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all jobs
            future_to_job = {
                executor.submit(self._process_job, job): job
                for job in self.jobs
            }
            
            # Process completed jobs
            for future in as_completed(future_to_job):
                job = future_to_job[future]
                completed += 1
                
                try:
                    future.result()  # This will raise any exceptions from the job
                except Exception as e:
                    job.status = "error"
                    job.error = str(e)
                    logging.error(f"Failed to process {job.input_file}: {e}")
                
                if progress_callback:
                    progress_callback(
                        completed,
                        total_jobs,
                        f"Processing {job.input_file.name}"
                    )
                    
    def _process_job(self, job: BatchJob) -> None:
        """
        Process a single batch job.
        
        Args:
            job: The job to process
        """
        try:
            # Create output directory
            job.output_dir.mkdir(parents=True, exist_ok=True)
            
            # Transcribe
            job.status = "transcribing"
            job.transcription = transcribe_file(
                str(job.input_file),
                job.model_size
            )
            
            # Save transcription
            trans_file = job.output_dir / f"{job.input_file.stem}_transcription.txt"
            with open(trans_file, "w", encoding="utf-8") as f:
                f.write(job.transcription)
                
            # Translate if requested
            if job.target_language:
                job.status = "translating"
                job.translation = translate(
                    job.transcription,
                    job.target_language
                )
                
                # Save translation
                trans_file = job.output_dir / f"{job.input_file.stem}_translation.txt"
                with open(trans_file, "w", encoding="utf-8") as f:
                    f.write(job.translation)
                    
            # Save job metadata
            meta_file = job.output_dir / "metadata.json"
            with open(meta_file, "w") as f:
                json.dump({
                    "input_file": str(job.input_file),
                    "model_size": job.model_size,
                    "target_language": job.target_language,
                    "status": "completed",
                    "error": None
                }, f, indent=2)
                
            job.status = "completed"
            
        except Exception as e:
            job.status = "error"
            job.error = str(e)
            raise
            
    def get_status(self) -> Dict[str, Any]:
        """
        Get current batch processing status.
        
        Returns:
            Dictionary with status information
        """
        status = {
            "total": len(self.jobs),
            "completed": sum(1 for j in self.jobs if j.status == "completed"),
            "failed": sum(1 for j in self.jobs if j.status == "error"),
            "pending": sum(1 for j in self.jobs if j.status == "pending"),
            "in_progress": sum(1 for j in self.jobs if j.status in ("transcribing", "translating")),
            "jobs": []
        }
        
        for job in self.jobs:
            status["jobs"].append({
                "file": str(job.input_file),
                "status": job.status,
                "error": job.error
            })
            
        return status 