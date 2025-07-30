"""Theme management for Whispa App."""

from typing import Dict, Any, Literal
import customtkinter as ctk

ThemeMode = Literal["light", "dark", "system"]

class ThemeManager:
    """Manages application theming."""
    
    LIGHT_THEME = {
        "colors": {
            "primary": "#007AFF",
            "secondary": "#5856D6",
            "success": "#34C759",
            "warning": "#FF9500",
            "error": "#FF3B30",
            "background": "#F2F2F7",
            "surface": "#FFFFFF",
            "text": "#000000",
            "text_secondary": "#3C3C43",
            "border": "#C6C6C8"
        },
        "fonts": {
            "default": ("Arial", 14),
            "heading": ("Arial", 16, "bold"),
            "button": ("Arial", 14),
            "small": ("Arial", 12)
        }
    }
    
    DARK_THEME = {
        "colors": {
            "primary": "#0A84FF",
            "secondary": "#5E5CE6",
            "success": "#30D158",
            "warning": "#FF9F0A",
            "error": "#FF453A",
            "background": "#1C1C1E",
            "surface": "#2C2C2E",
            "text": "#FFFFFF",
            "text_secondary": "#EBEBF5",
            "border": "#38383A"
        },
        "fonts": LIGHT_THEME["fonts"]  # Same fonts for both themes
    }
    
    def __init__(self):
        """Initialize theme manager."""
        self._current_theme = "system"
        self._update_customtkinter_theme()
        
    @property
    def current_theme(self) -> ThemeMode:
        """Get current theme mode."""
        return self._current_theme
        
    @current_theme.setter
    def current_theme(self, mode: ThemeMode) -> None:
        """Set theme mode."""
        if mode not in ("light", "dark", "system"):
            raise ValueError("Invalid theme mode")
        self._current_theme = mode
        self._update_customtkinter_theme()
        
    def _update_customtkinter_theme(self) -> None:
        """Update CustomTkinter appearance mode."""
        ctk.set_appearance_mode(self._current_theme)
        
    def get_color(self, name: str) -> str:
        """Get color value for current theme."""
        theme = self.LIGHT_THEME if self._is_light_mode() else self.DARK_THEME
        return theme["colors"].get(name, self.LIGHT_THEME["colors"][name])
        
    def get_font(self, style: str = "default") -> tuple:
        """Get font tuple for given style."""
        return self.LIGHT_THEME["fonts"].get(style, self.LIGHT_THEME["fonts"]["default"])
        
    def _is_light_mode(self) -> bool:
        """Check if currently in light mode."""
        if self._current_theme == "system":
            # TODO: Detect system theme
            return True
        return self._current_theme == "light"
        
    def apply_widget_theme(self, widget: ctk.CTkBaseClass, **kwargs) -> None:
        """Apply theme to a CustomTkinter widget."""
        if isinstance(widget, (ctk.CTkButton, ctk.CTkLabel, ctk.CTkEntry)):
            widget.configure(
                font=self.get_font("button"),
                text_color=self.get_color("text"),
                **kwargs
            )
        elif isinstance(widget, ctk.CTkFrame):
            widget.configure(
                fg_color=self.get_color("surface"),
                border_color=self.get_color("border"),
                **kwargs
            )
        elif isinstance(widget, ctk.CTkProgressBar):
            widget.configure(
                progress_color=self.get_color("primary"),
                border_color=self.get_color("border"),
                **kwargs
            )
            
    def apply_theme_recursively(self, widget: ctk.CTkBaseClass) -> None:
        """Apply theme to a widget and all its children."""
        self.apply_widget_theme(widget)
        
        # Apply to children if they exist
        if hasattr(widget, "winfo_children"):
            for child in widget.winfo_children():
                if isinstance(child, ctk.CTkBaseClass):
                    self.apply_theme_recursively(child) 