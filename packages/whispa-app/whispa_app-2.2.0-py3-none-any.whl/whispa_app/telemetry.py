"""Anonymous telemetry collection for Whispa App."""

import os
import json
import uuid
import logging
import platform
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class Telemetry:
    """Handles anonymous telemetry collection."""
    
    def __init__(self, opt_out: bool = False):
        """Initialize telemetry system."""
        self.opt_out = opt_out
        self.session_id = str(uuid.uuid4())
        self.data_dir = self._get_metrics_dir()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_session = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_file = self.data_dir / f"session_{self.session_id}.json"
        
        # Initialize session data
        self.session_data = {
            "session_id": self.session_id,
            "system_info": {
                "os": platform.system(),
                "os_version": platform.version(),
                "python_version": platform.python_version(),
                "cpu_count": os.cpu_count(),
                "has_gpu": bool(os.environ.get("CUDA_VISIBLE_DEVICES")),
            },
            "transcriptions": [],
            "translations": [],
            "operations": [],
            "errors": []
        }
        
        if not self.opt_out:
            self._save_session()
    
    def _get_metrics_dir(self) -> Path:
        """Get the metrics directory path."""
        if platform.system() == "Windows":
            base = Path(os.getenv("LOCALAPPDATA", "")) / "WhispaApp"
        else:
            base = Path.home() / ".whispa"
        return base / "metrics"
        
    def _save_session(self):
        """Save current session data to file."""
        if self.opt_out:
            return
            
        try:
            with open(self.session_file, 'w') as f:
                json.dump(self.session_data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save telemetry data: {e}")
    
    def record_transcription(self, model_size: str, file_type: str, file_size: int,
                           duration_ms: int, success: bool = True, error: Optional[str] = None):
        """Record a transcription operation."""
        if self.opt_out:
            return
            
        data = {
            "event_type": "transcription",
            "timestamp": datetime.now().isoformat(),
            "model_size": model_size,
            "file_type": file_type,
            "file_size_bytes": file_size,
            "duration_ms": duration_ms,
            "success": success
        }
        if error:
            data["error"] = error
            
        self.session_data["transcriptions"].append(data)
        
        # Save to individual file for easier querying
        file_path = self.data_dir / f"transcription_{self.session_id}_{len(self.session_data['transcriptions'])}.json"
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save transcription data: {e}")
            
        self._save_session()
        
    def record_translation(self, target_lang: str, text_length: int, duration_ms: int,
                         success: bool = True, error: Optional[str] = None):
        """Record a translation operation."""
        if self.opt_out:
            return
            
        data = {
            "event_type": "translation",
            "timestamp": datetime.now().isoformat(),
            "target_language": target_lang,
            "text_length": text_length,
            "duration_ms": duration_ms,
            "success": success
        }
        if error:
            data["error"] = error
            
        self.session_data["translations"].append(data)
        self._save_session()
        
    def record_operation(self, operation: str, duration_ms: int, success: bool = True,
                        context: Optional[Dict[str, Any]] = None):
        """Record completion of a long-running operation."""
        if self.opt_out:
            return
            
        data = {
            "event_type": "operation",
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "duration_ms": duration_ms,
            "success": success
        }
        if context:
            data["context"] = context
        
        self.session_data["operations"].append(data)
        self._save_session()
        
    def record_error(self, error_type: str, error_message: str, context: Dict[str, Any]):
        """Record an error event."""
        if self.opt_out:
            return
            
        data = {
            "event_type": "error",
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "error_message": error_message,
            "context": context
        }
        
        self.session_data["errors"].append(data)
        self._save_session()
        
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics for the current session."""
        stats = {
            "transcriptions": {
                "total": len(self.session_data["transcriptions"]),
                "successful": sum(1 for t in self.session_data["transcriptions"] if t["success"]),
                "failed": sum(1 for t in self.session_data["transcriptions"] if not t["success"]),
                "avg_duration_ms": 0
            },
            "translations": {
                "total": len(self.session_data["translations"]),
                "successful": sum(1 for t in self.session_data["translations"] if t["success"]),
                "failed": sum(1 for t in self.session_data["translations"] if not t["success"]),
                "avg_duration_ms": 0
            }
        }
        
        # Calculate averages
        if stats["transcriptions"]["total"] > 0:
            stats["transcriptions"]["avg_duration_ms"] = sum(
                t["duration_ms"] for t in self.session_data["transcriptions"]
            ) / stats["transcriptions"]["total"]
            
        if stats["translations"]["total"] > 0:
            stats["translations"]["avg_duration_ms"] = sum(
                t["duration_ms"] for t in self.session_data["translations"]
            ) / stats["translations"]["total"]
            
        return stats 