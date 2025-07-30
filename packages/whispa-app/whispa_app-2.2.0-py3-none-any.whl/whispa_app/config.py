"""Configuration management for Whispa App."""

import os
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path

class Config:
    """Manages application configuration and user preferences."""
    
    DEFAULT_CONFIG = {
        "theme": "system",  # system, light, or dark
        "window": {
            "width": 800,
            "height": 600,
            "maximized": False
        },
        "language": "English",
        "model": "small",
        "advanced": {
            "vram_threshold": 6,
            "beam_size": 5,
            "vad_filter": True,
            "num_beams": 8,
            "length_penalty": 0.8,
            "temperature": 0.3
        },
        "logging": {
            "level": "INFO",
            "file": None
        }
    }
    
    def __init__(self):
        """Initialize configuration manager."""
        self.config_dir = self._get_config_dir()
        self.config_file = self.config_dir / "config.json"
        self.config = self._load_config()
        
    def _get_config_dir(self) -> Path:
        """Get the configuration directory path."""
        if os.name == "nt":  # Windows
            base_dir = Path(os.getenv("APPDATA", ""))
        else:  # Unix/Linux/Mac
            base_dir = Path.home() / ".config"
            
        return base_dir / "whispa_app"
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        try:
            if self.config_file.exists():
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                # Update with any new default keys
                return self._update_config_with_defaults(config)
        except Exception as e:
            logging.warning(f"Failed to load config: {e}")
            
        return self._create_default_config()
        
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration file."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        config = dict(self.DEFAULT_CONFIG)
        self.save(config)
        return config
        
    def _update_config_with_defaults(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing config with any new default values."""
        updated = False
        
        def update_dict(current: Dict[str, Any], default: Dict[str, Any]) -> bool:
            nonlocal updated
            changed = False
            for key, value in default.items():
                if key not in current:
                    current[key] = value
                    changed = True
                elif isinstance(value, dict) and isinstance(current[key], dict):
                    if update_dict(current[key], value):
                        changed = True
            updated = updated or changed
            return changed
            
        update_dict(config, self.DEFAULT_CONFIG)
        if updated:
            self.save(config)
            
        return config
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        try:
            keys = key.split(".")
            value = self.config
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
            
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        keys = key.split(".")
        config = self.config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value
        self.save(self.config)
        
    def save(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Save configuration to file."""
        if config is not None:
            self.config = config
            
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            logging.error(f"Failed to save config: {e}")
            
    def reset(self) -> None:
        """Reset configuration to defaults."""
        self.config = dict(self.DEFAULT_CONFIG)
        self.save(self.config) 