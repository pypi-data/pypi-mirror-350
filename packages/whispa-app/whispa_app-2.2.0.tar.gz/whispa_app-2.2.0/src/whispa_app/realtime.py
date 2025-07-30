"""Real-time audio transcription module."""

import queue
import threading
import wave
import logging
from typing import Optional, Callable, Generator
from pathlib import Path
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

class AudioBuffer:
    """Circular buffer for audio data."""
    
    def __init__(self, max_size: int = 30 * 16000):  # 30 seconds at 16kHz
        """Initialize audio buffer."""
        self.buffer = np.zeros(max_size, dtype=np.float32)
        self.max_size = max_size
        self.size = 0
        self.write_pos = 0
        self.lock = threading.Lock()
        
    def write(self, data: np.ndarray) -> None:
        """Write audio data to buffer."""
        with self.lock:
            n = len(data)
            if n > self.max_size:
                data = data[-self.max_size:]
                n = self.max_size
                
            # Write data
            space_to_end = self.max_size - self.write_pos
            if n <= space_to_end:
                self.buffer[self.write_pos:self.write_pos + n] = data
                self.write_pos += n
            else:
                self.buffer[self.write_pos:] = data[:space_to_end]
                self.buffer[:n - space_to_end] = data[space_to_end:]
                self.write_pos = n - space_to_end
                
            self.size = min(self.size + n, self.max_size)
            
    def read(self, n: Optional[int] = None) -> np.ndarray:
        """Read audio data from buffer."""
        with self.lock:
            if n is None:
                n = self.size
            n = min(n, self.size)
            
            # Calculate read position
            read_pos = (self.write_pos - self.size) % self.max_size
            
            # Read data
            if read_pos + n <= self.max_size:
                data = self.buffer[read_pos:read_pos + n].copy()
            else:
                # Handle wrap-around
                first_part = self.buffer[read_pos:].copy()
                second_part = self.buffer[:n - len(first_part)].copy()
                data = np.concatenate([first_part, second_part])
                
            return data
            
    def clear(self) -> None:
        """Clear the buffer."""
        with self.lock:
            self.size = 0
            self.write_pos = 0
            self.buffer.fill(0)

class RealtimeTranscriber:
    """Real-time audio transcription using Whisper."""
    
    def __init__(
        self,
        model_size: str = "small",
        device: str = "auto",
        compute_type: str = "float16",
        language: Optional[str] = None,
        sample_rate: int = 16000,
        chunk_duration: float = 30.0
    ):
        """
        Initialize real-time transcriber.
        
        Args:
            model_size: Whisper model size
            device: Device to run model on ("cpu" or "cuda")
            compute_type: Model computation type
            language: Optional language code
            sample_rate: Audio sample rate
            chunk_duration: Duration of audio chunks in seconds
        """
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type
        )
        self.language = language
        self.sample_rate = sample_rate
        self.chunk_samples = int(chunk_duration * sample_rate)
        
        # Audio handling
        self.audio_buffer = AudioBuffer(max_size=self.chunk_samples)
        self.stream: Optional[sd.InputStream] = None
        self.is_recording = False
        
        # Transcription
        self.transcription_queue = queue.Queue()
        self.transcription_thread: Optional[threading.Thread] = None
        
    def start(
        self,
        callback: Optional[Callable[[str], None]] = None
    ) -> None:
        """
        Start real-time transcription.
        
        Args:
            callback: Optional callback for transcription results
        """
        if self.is_recording:
            return
            
        def audio_callback(indata, frames, time, status):
            if status:
                logging.warning(f"Audio callback status: {status}")
            self.audio_buffer.write(indata[:, 0])
            
        # Start audio stream
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.float32,
            callback=audio_callback
        )
        self.stream.start()
        self.is_recording = True
        
        # Start transcription thread
        def transcribe_loop():
            while self.is_recording:
                # Get audio chunk
                audio = self.audio_buffer.read()
                if len(audio) < self.chunk_samples:
                    continue
                    
                # Transcribe
                segments, _ = self.model.transcribe(
                    audio,
                    language=self.language,
                    beam_size=5
                )
                
                # Process results
                text = " ".join(segment.text for segment in segments)
                if text.strip():
                    if callback:
                        callback(text)
                    self.transcription_queue.put(text)
                    
        self.transcription_thread = threading.Thread(
            target=transcribe_loop,
            daemon=True
        )
        self.transcription_thread.start()
        
    def stop(self) -> None:
        """Stop real-time transcription."""
        self.is_recording = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        if self.transcription_thread:
            self.transcription_thread.join()
            self.transcription_thread = None
        self.audio_buffer.clear()
        
    def get_transcription(self) -> Generator[str, None, None]:
        """
        Get transcription results.
        
        Yields:
            Transcribed text segments
        """
        while True:
            try:
                text = self.transcription_queue.get_nowait()
                yield text
            except queue.Empty:
                break
                
    def save_audio(self, filepath: Path) -> None:
        """
        Save recorded audio to file.
        
        Args:
            filepath: Path to save audio file
        """
        audio = self.audio_buffer.read()
        with wave.open(str(filepath), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(self.sample_rate)
            wf.writeframes((audio * 32767).astype(np.int16).tobytes()) 