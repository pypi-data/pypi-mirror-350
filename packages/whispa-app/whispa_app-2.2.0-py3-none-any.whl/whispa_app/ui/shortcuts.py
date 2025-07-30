"""Keyboard shortcuts management for Whispa App."""

import sys
from typing import Dict, Callable, Optional
import tkinter as tk

class ShortcutManager:
    """Manages application keyboard shortcuts."""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize shortcut manager.
        
        Args:
            root: The root window to bind shortcuts to
        """
        self.root = root
        self.shortcuts: Dict[str, Callable] = {}
        self._setup_default_shortcuts()
        
    def _setup_default_shortcuts(self) -> None:
        """Set up default keyboard shortcuts."""
        # Platform-specific modifier key
        self.mod_key = "Command" if sys.platform == "darwin" else "Control"
        
        # Default shortcuts
        self.default_shortcuts = {
            f"<{self.mod_key}-o>": ("Open File", None),
            f"<{self.mod_key}-s>": ("Save Transcription", None),
            f"<{self.mod_key}-S>": ("Save Translation", None),
            f"<{self.mod_key}-t>": ("Start Transcription", None),
            f"<{self.mod_key}-l>": ("Start Translation", None),
            f"<{self.mod_key}-q>": ("Quit", None),
            f"<{self.mod_key}-comma>": ("Open Settings", None),
            f"<{self.mod_key}-h>": ("Show Help", None),
            "F5": ("Toggle Theme", None),
            "Escape": ("Cancel Operation", None)
        }
        
    def register_shortcut(
        self,
        key: str,
        callback: Callable,
        description: Optional[str] = None
    ) -> None:
        """
        Register a new keyboard shortcut.
        
        Args:
            key: The key combination (e.g., "<Control-s>")
            callback: The function to call when shortcut is triggered
            description: Optional description of what the shortcut does
        """
        self.shortcuts[key] = callback
        self.root.bind(key, lambda e: callback())
        
    def unregister_shortcut(self, key: str) -> None:
        """
        Remove a keyboard shortcut.
        
        Args:
            key: The key combination to remove
        """
        if key in self.shortcuts:
            self.root.unbind(key)
            del self.shortcuts[key]
            
    def get_shortcuts_help(self) -> str:
        """
        Get help text listing all registered shortcuts.
        
        Returns:
            Formatted string of all shortcuts and their descriptions
        """
        lines = ["Keyboard Shortcuts:", ""]
        
        # Get max lengths for formatting
        max_key = max(len(k) for k in self.default_shortcuts.keys())
        max_desc = max(len(d[0]) for d in self.default_shortcuts.values())
        
        # Format each shortcut
        for key, (desc, _) in sorted(self.default_shortcuts.items()):
            key_str = key.replace("<", "").replace(">", "")
            lines.append(f"{key_str:<{max_key}} : {desc:<{max_desc}}")
            
        return "\n".join(lines)
        
    def show_shortcuts_dialog(self) -> None:
        """Show a dialog with all available shortcuts."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Keyboard Shortcuts")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Make dialog modal
        dialog.focus_set()
        
        # Add shortcuts text
        text = tk.Text(dialog, wrap="word", width=50, height=20)
        text.insert("1.0", self.get_shortcuts_help())
        text.configure(state="disabled")
        text.pack(padx=10, pady=10)
        
        # Add close button
        close_btn = tk.Button(
            dialog,
            text="Close",
            command=dialog.destroy
        )
        close_btn.pack(pady=(0, 10))
        
        # Center dialog on parent window
        dialog.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 50,
            self.root.winfo_rooty() + 50
        )) 