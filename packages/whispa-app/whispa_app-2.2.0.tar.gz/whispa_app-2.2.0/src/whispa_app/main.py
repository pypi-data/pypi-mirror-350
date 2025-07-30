# src/whispa_app/main.py

import sys
import os
import threading
import logging
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import timedelta
from pathlib import Path
import time

import customtkinter as ctk
import psutil
import torch

from whispa_app.device import select_device
from whispa_app.transcription import transcribe_file, get_supported_audio_formats
from whispa_app.translation import translate, TranslationError
from whispa_app.utils import simplify_text, format_timestamp, format_duration, format_file_size
from whispa_app.ui.panels import build_panels
from whispa_app.exporters import save_as_srt, save_as_vtt, save_as_json
from whispa_app.telemetry import Telemetry

def resource_path(rel: str) -> str:
    """
    Resolve a path to a resource, working both in development and when bundled by PyInstaller.
    """
    if getattr(sys, "_MEIPASS", False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(__file__)
    return os.path.join(base, rel)

# Update version
VERSION = "2.2.0"

# Available model sizes and languages
MODELS    = ["tiny", "base", "small", "medium", "large"]
LANGUAGES = ["English", "Spanish", "French", "German", "Chinese", "Japanese"]
SAVE_FORMATS = ["Text (.txt)", "SubRip (.srt)", "WebVTT (.vtt)", "JSON (.json)"]
SUPPORTED_AUDIO = get_supported_audio_formats()

# Icon paths
ICON_ICO = resource_path("assets/icon.ico")
ICON_PNG = resource_path("assets/icon.png")

# Update color scheme with Cursor website style
COLORS = {
    # Primary colors
    "primary": "#1E1E1E",        # Cursor dark
    "primary_light": "#2D2D2D",  # Cursor dark light
    "primary_dark": "#171717",   # Cursor dark darker
    
    # Background colors
    "background_light": "#FFFFFF",  # Pure white background
    "background_dark": "#1E1E1E",   # Dark mode background
    "surface_light": "#F5F5F5",     # Light surface
    "surface_dark": "#2D2D2D",      # Dark surface
    
    # Text colors
    "text_light": "#1E1E1E",     # Dark text
    "text_dark": "#FFFFFF",      # Light text
    "text_secondary_light": "#666666",  # Secondary text light
    "text_secondary_dark": "#A0A0A0",   # Secondary text dark
    
    # Accent colors
    "accent": "#0078D4",         # Azure blue
    "accent_hover": "#106EBE",   # Darker Azure blue
    
    # Status colors
    "success": "#107C10",        # Success green
    "warning": "#797673",        # Warning neutral
    "error": "#E81123",          # Error red
    "info": "#0078D4",          # Info blue
    
    # Border colors
    "border_light": "#E0E0E0",   # Light border
    "border_dark": "#404040"     # Dark border
}

# Font sizes - Match GitHub style
FONT_SIZES = {
    "small": {
        "title": 18,
        "heading": 16,
        "normal": 14,
        "small": 12
    },
    "medium": {
        "title": 20,
        "heading": 18,
        "normal": 16,
        "small": 14
    },
    "large": {
        "title": 22,
        "heading": 20,
        "normal": 18,
        "small": 16
    }
}

# Default settings
DEFAULT_SETTINGS = {
    "theme": "dark",
    "save_format": "Text (.txt)",
    "show_advanced": True,
    "show_system_stats": True,
    "sample_rate": 16000,
    "audio_channels": 1,
    "font_size": "medium"  # small, medium, large
}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('whispa.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ToolTip:
    """
    Simple tooltip that appears on hover for any widget.
    """
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwin = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, _=None):
        if self.tipwin:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tipwin = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tk.Label(
            tw,
            text=self.text,
            justify="left",
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("Arial", 10)
        ).pack(ipadx=1)

    def hide(self, _=None):
        if self.tipwin:
            self.tipwin.destroy()
            self.tipwin = None

class WhispaApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Initialize telemetry
        self.telemetry = Telemetry()
        
        # Initialize progress tracking
        self.current_operation = None
        self.operation_start_time = None

        # Load or create settings
        self.settings_file = Path.home() / ".whispa_settings.json"
        self.settings = self._load_settings()
        self.fonts = FONT_SIZES[self.settings["font_size"]]

        # Set initial theme
        ctk.set_appearance_mode(self.settings["theme"])
        self.configure(fg_color=COLORS[f"background_{self.settings['theme']}"])

        # ----------------------------
        # Load application icon
        # ----------------------------
        for ico in ("assets/icon.ico", "assets/icon.png"):
            path = resource_path(ico)
            if not os.path.isfile(path):
                continue
            try:
                if ico.endswith(".ico"):
                    self.iconbitmap(path)
                else:
                    self._icon_img = tk.PhotoImage(file=path)
                    self.iconphoto(True, self._icon_img)
                break
            except Exception:
                continue

        # ----------------------------
        # Window configuration
        # ----------------------------
        self.title("Whispa App")
        
        # Handle window icon (important for taskbar)
        if sys.platform == "win32":
            if os.path.exists(ICON_ICO):
                try:
                    # Use both methods for Windows
                    self.after(100, lambda: self.iconbitmap(default=ICON_ICO))
                    self.after(100, lambda: self.wm_iconbitmap(ICON_ICO))
                except Exception as e:
                    print(f"Error setting icon: {e}")
        else:
            # For non-Windows platforms
            if os.path.exists(ICON_PNG):
                try:
                    icon_img = tk.PhotoImage(file=ICON_PNG)
                    self.iconphoto(True, icon_img)
                    self._icon_img = icon_img  # Keep reference
                except Exception as e:
                    print(f"Error setting icon: {e}")

        # ----------------------------
        # Window configuration
        # ----------------------------
        self.minsize(1000, 700)  # Reduced minimum size
        
        # Configure grid weights for responsiveness
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # Main content
        self.grid_rowconfigure(2, weight=0)  # Stats footer
        
        # Set default window size to 80% of screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # ----------------------------
        # Advanced settings variables
        # ----------------------------
        self.adv_vram           = tk.IntVar(value=6)
        self.adv_tbeam          = tk.IntVar(value=5)
        self.adv_vad            = tk.BooleanVar(value=True)
        self.adv_num_beams      = tk.IntVar(value=8)
        self.adv_length_penalty = tk.DoubleVar(value=0.8)
        self.adv_temperature    = tk.DoubleVar(value=0.3)
        self.adv_sample_rate    = tk.IntVar(value=self.settings["sample_rate"])
        self.adv_channels       = tk.IntVar(value=self.settings["audio_channels"])

        # Batch processing variables
        self.batch_files = []
        self.is_batch_mode = False
        self.current_batch_file = 0
        self.batch_progress = 0

        # ----------------------------
        # Build the menu bar
        # ----------------------------
        self._create_menubar()

        # ----------------------------
        # Header with theme toggle and title
        # ----------------------------
        self._build_header()

        # ----------------------------
        # Main content container
        # ----------------------------
        self._build_main_content()

        # Start stats updates if enabled
        if self.settings["show_system_stats"]:
            self._build_stats_footer()
            self._update_stats()

    def _build_header(self):
        """Build the application header with title and theme toggle."""
        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        header.grid_columnconfigure(1, weight=1)

        # App title
        title = ctk.CTkLabel(
            header,
            text="Whispa App",
            font=("Segoe UI", self.fonts["heading"], "bold"),
            text_color=COLORS["text_light"] if self.settings["theme"] == "light" else COLORS["text_dark"]
        )
        title.grid(row=0, column=0, padx=10)

        # Theme toggle
        theme_container = ctk.CTkFrame(header, fg_color="transparent")
        theme_container.grid(row=0, column=2, padx=10)
        
        sun_icon = "☀"
        moon_icon = "☾"
        
        ctk.CTkLabel(
            theme_container,
            text=sun_icon,
            font=("Segoe UI", self.fonts["small"]),
            text_color=COLORS["text_light"] if self.settings["theme"] == "light" else COLORS["text_dark"]
        ).pack(side="left", padx=5)

        theme_switch = ctk.CTkSwitch(
            theme_container,
            text="",
            command=self.toggle_theme,
            variable=ctk.StringVar(value="on" if self.settings["theme"] == "dark" else "off"),
            progress_color=COLORS["accent"],
            button_color=COLORS["accent_hover"],
            button_hover_color=COLORS["primary_dark"],
            width=40,
            height=20
        )
        theme_switch.pack(side="left", padx=5)

        ctk.CTkLabel(
            theme_container,
            text=moon_icon,
            font=("Segoe UI", self.fonts["small"]),
            text_color=COLORS["text_light"] if self.settings["theme"] == "light" else COLORS["text_dark"]
        ).pack(side="left", padx=5)

    def _build_main_content(self):
        """Build the main application content."""
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        # Configure grid weights for content
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(2, weight=1)  # Transcription box
        content.grid_rowconfigure(4, weight=1)  # Translation box

        # File selection row
        file_frame = ctk.CTkFrame(content, fg_color="transparent")
        file_frame.grid(row=0, column=0, sticky="ew")
        file_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            file_frame,
            text="Audio File:",
            font=("Segoe UI", self.fonts["normal"]),
            text_color=COLORS["text_light"] if self.settings["theme"] == "light" else COLORS["text_dark"]
        ).grid(row=0, column=0, padx=(0,10), pady=5)

        self.file_entry = ctk.CTkEntry(
            file_frame,
            font=("Segoe UI", self.fonts["normal"]),
            height=28,
            fg_color=COLORS["background_light"] if self.settings["theme"] == "light" else COLORS["primary_light"],
            text_color=COLORS["text_light"] if self.settings["theme"] == "light" else COLORS["text_dark"],
            border_color=COLORS["border_light"] if self.settings["theme"] == "light" else COLORS["border_dark"],
            border_width=1
        )
        self.file_entry.grid(row=0, column=1, sticky="ew", padx=10)

        browse_btn = ctk.CTkButton(
            file_frame,
            text="Browse",
            font=("Segoe UI", self.fonts["small"]),
            command=self._on_browse,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            height=28
        )
        browse_btn.grid(row=0, column=2, padx=(0,5))

        batch_btn = ctk.CTkButton(
            file_frame,
            text="Batch",
            font=("Segoe UI", self.fonts["small"]),
            command=self._on_batch,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            height=28
        )
        batch_btn.grid(row=0, column=3, padx=(0,5))

        # Model selection row
        model_frame = ctk.CTkFrame(content, fg_color="transparent")
        model_frame.grid(row=1, column=0, sticky="ew", pady=10)
        model_frame.grid_columnconfigure(2, weight=1)  # Space between model and transcribe

        ctk.CTkLabel(
            model_frame,
            text="Model:",
            font=("Segoe UI", self.fonts["normal"]),
            text_color=COLORS["text_light"] if self.settings["theme"] == "light" else COLORS["text_dark"]
        ).grid(row=0, column=0, padx=(0,5))

        self.model_menu = ctk.CTkOptionMenu(
            model_frame,
            values=MODELS,
            variable=ctk.StringVar(value=MODELS[2]),
            font=("Segoe UI", self.fonts["small"]),
            fg_color=COLORS["accent"],
            button_color=COLORS["accent_hover"],
            button_hover_color=COLORS["primary_dark"],
            height=28
        )
        self.model_menu.grid(row=0, column=1, padx=5)

        self.transcribe_btn = ctk.CTkButton(
            model_frame,
            text="▶ Transcribe",
            font=("Segoe UI", self.fonts["small"]),
            command=self._on_transcribe,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            height=28
        )
        self.transcribe_btn.grid(row=0, column=3, padx=5)

        # Transcription section
        trans_frame = ctk.CTkFrame(content, fg_color="transparent")
        trans_frame.grid(row=2, column=0, sticky="nsew", pady=10)
        trans_frame.grid_columnconfigure(0, weight=1)
        trans_frame.grid_rowconfigure(0, weight=1)

        self.transcription_box = ctk.CTkTextbox(
            trans_frame,
            font=("Segoe UI", self.fonts["normal"]),
            wrap="word",
            fg_color=COLORS["background_light"] if self.settings["theme"] == "light" else COLORS["primary_light"],
            text_color=COLORS["text_light"] if self.settings["theme"] == "light" else COLORS["text_dark"],
            border_color=COLORS["border_light"] if self.settings["theme"] == "light" else COLORS["border_dark"],
            border_width=1
        )
        self.transcription_box.grid(row=0, column=0, sticky="nsew")

        # Transcription save controls
        trans_save_frame = ctk.CTkFrame(trans_frame, fg_color="transparent")
        trans_save_frame.grid(row=1, column=0, sticky="e", pady=(5,0))

        self.trans_save_menu = ctk.CTkOptionMenu(
            trans_save_frame,
            values=SAVE_FORMATS,
            variable=ctk.StringVar(value=SAVE_FORMATS[0]),
            font=("Segoe UI", self.fonts["small"]),
            fg_color=COLORS["accent"],
            button_color=COLORS["accent_hover"],
            button_hover_color=COLORS["primary_dark"],
            height=28
        )
        self.trans_save_menu.pack(side="left", padx=5)

        trans_save_btn = ctk.CTkButton(
            trans_save_frame,
            text="Save",
            font=("Segoe UI", self.fonts["small"]),
            command=lambda: self._save_transcription(self.transcription_box.get("1.0", "end")),
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            height=28
        )
        trans_save_btn.pack(side="left", padx=5)

        # Translation section
        trans_frame = ctk.CTkFrame(content, fg_color="transparent")
        trans_frame.grid(row=4, column=0, sticky="nsew", pady=10)
        trans_frame.grid_columnconfigure(0, weight=1)
        trans_frame.grid_rowconfigure(0, weight=1)

        self.translation_box = ctk.CTkTextbox(
            trans_frame,
            font=("Segoe UI", self.fonts["normal"]),
            wrap="word",
            fg_color=COLORS["background_light"] if self.settings["theme"] == "light" else COLORS["primary_light"],
            text_color=COLORS["text_light"] if self.settings["theme"] == "light" else COLORS["text_dark"],
            border_color=COLORS["border_light"] if self.settings["theme"] == "light" else COLORS["border_dark"],
            border_width=1
        )
        self.translation_box.grid(row=0, column=0, sticky="nsew")

        # Translation controls
        trans_controls = ctk.CTkFrame(trans_frame, fg_color="transparent")
        trans_controls.grid(row=1, column=0, sticky="e", pady=(5,0))

        ctk.CTkLabel(
            trans_controls,
            text="Translation:",
            font=("Segoe UI", self.fonts["small"]),
            text_color=COLORS["text_light"] if self.settings["theme"] == "light" else COLORS["text_dark"]
        ).pack(side="left", padx=5)

        self.lang_menu = ctk.CTkOptionMenu(
            trans_controls,
            values=LANGUAGES,
            variable=ctk.StringVar(value=LANGUAGES[0]),
            font=("Segoe UI", self.fonts["small"]),
            fg_color=COLORS["accent"],
            button_color=COLORS["accent_hover"],
            button_hover_color=COLORS["primary_dark"],
            height=28
        )
        self.lang_menu.pack(side="left", padx=5)

        self.format_menu = ctk.CTkOptionMenu(
            trans_controls,
            values=SAVE_FORMATS,
            variable=ctk.StringVar(value=self.settings["save_format"]),
            font=("Segoe UI", self.fonts["small"]),
            fg_color=COLORS["accent"],
            button_color=COLORS["accent_hover"],
            button_hover_color=COLORS["primary_dark"],
            height=28
        )
        self.format_menu.pack(side="left", padx=5)

        save_btn = ctk.CTkButton(
            trans_controls,
            text="Save",
            font=("Segoe UI", self.fonts["small"]),
            command=lambda: self._save_translation(self.translation_box.get("1.0", "end")),
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            height=28
        )
        save_btn.pack(side="left", padx=5)

        self.translate_btn = ctk.CTkButton(
            trans_controls,
            text="▶ Translate",
            font=("Segoe UI", self.fonts["small"]),
            command=self._on_translate,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            height=28
        )
        self.translate_btn.pack(side="left", padx=5)

        # Progress section
        progress_frame = ctk.CTkFrame(content, fg_color="transparent")
        progress_frame.grid(row=5, column=0, sticky="ew", pady=10)
        progress_frame.grid_columnconfigure(0, weight=1)

        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            progress_color=COLORS["accent"],
            height=6
        )
        self.progress_bar.grid(row=0, column=0, sticky="ew", padx=100)  # Added padding for centering
        self.progress_bar.set(0)

        # Stats footer
        stats_frame = ctk.CTkFrame(self, fg_color="transparent", height=30)
        stats_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_propagate(False)

        self.stats_lbl = ctk.CTkLabel(
            stats_frame,
            text="System Stats: Initializing...",
            font=("Segoe UI", self.fonts["small"]),
            text_color=COLORS["text_secondary_light"] if self.settings["theme"] == "light" else COLORS["text_secondary_dark"],
            anchor="center"
        )
        self.stats_lbl.grid(row=0, column=0)

        # Bind keyboard shortcuts
        self.bind('<Control-t>', lambda e: self._on_transcribe())
        self.bind('<Control-r>', lambda e: self._on_translate())
        self.bind('<Control-b>', lambda e: self._on_batch())
        self.bind('<Control-s>', lambda e: self._save_transcription(self.transcription_box.get("1.0", "end")))
        self.bind('<Control-Alt-s>', lambda e: self._save_translation(self.translation_box.get("1.0", "end")))

    def _build_stats_footer(self):
        """Build the system stats footer."""
        footer = ctk.CTkFrame(
            self,
            fg_color=COLORS["surface_light"] if self.settings["theme"] == "light" else COLORS["surface_dark"],
            corner_radius=8,
            height=40
        )
        footer.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        footer.grid_columnconfigure(0, weight=1)
        footer.grid_propagate(False)  # Prevent frame from shrinking

        self.stats_lbl = ctk.CTkLabel(
            footer,
            text="System Stats: Initializing...",
            font=("Segoe UI", self.fonts["small"]),
            text_color=COLORS["text_secondary_light"] if self.settings["theme"] == "light" else COLORS["text_secondary_dark"],
            anchor="center"
        )
        self.stats_lbl.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

    def _create_menubar(self):
        """Create the application menu bar with advanced settings."""
        menubar = tk.Menu(self)
        self.configure(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, font=("Segoe UI", 11))
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open File...", command=self._on_browse)
        file_menu.add_command(label="Open Batch...", command=self._on_batch)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0, font=("Segoe UI", 11))
        menubar.add_cascade(label="Settings", menu=settings_menu)
        
        # Advanced Settings submenu
        adv_menu = tk.Menu(settings_menu, tearoff=0, font=("Segoe UI", 11))
        settings_menu.add_cascade(label="Advanced Settings", menu=adv_menu)
        
        # Whisper Settings
        whisper_menu = tk.Menu(adv_menu, tearoff=0, font=("Segoe UI", 11))
        adv_menu.add_cascade(label="Whisper Settings", menu=whisper_menu)
        
        # VRAM limit
        whisper_menu.add_command(
            label="VRAM Limit (GB): " + str(self.adv_vram.get()),
            command=lambda: self._show_number_dialog(
                "VRAM Limit (GB)",
                "Enter maximum GPU memory to use (in GB):",
                self.adv_vram,
                1, 24
            )
        )
        
        # Beam size
        whisper_menu.add_command(
            label="Beam Size: " + str(self.adv_tbeam.get()),
            command=lambda: self._show_number_dialog(
                "Beam Size",
                "Enter beam size (higher = better accuracy but slower):",
                self.adv_tbeam,
                1, 10
            )
        )
        
        # VAD filter
        whisper_menu.add_checkbutton(
            label="VAD Filter",
            variable=self.adv_vad
        )
        
        # Audio Settings
        audio_menu = tk.Menu(adv_menu, tearoff=0, font=("Segoe UI", 11))
        adv_menu.add_cascade(label="Audio Settings", menu=audio_menu)
        
        # Sample rate
        audio_menu.add_command(
            label="Sample Rate: " + str(self.adv_sample_rate.get()),
            command=lambda: self._show_number_dialog(
                "Sample Rate",
                "Enter audio sample rate (Hz):",
                self.adv_sample_rate,
                8000, 48000
            )
        )
        
        # Channels
        audio_menu.add_command(
            label="Audio Channels: " + str(self.adv_channels.get()),
            command=lambda: self._show_number_dialog(
                "Audio Channels",
                "Enter number of audio channels (1=mono, 2=stereo):",
                self.adv_channels,
                1, 2
            )
        )
        
        # Temperature
        audio_menu.add_command(
            label="Temperature: " + str(self.adv_temperature.get()),
            command=lambda: self._show_number_dialog(
                "Temperature",
                "Enter temperature value (0.0 to 1.0):",
                self.adv_temperature,
                0.0, 1.0,
                is_float=True
            )
        )
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0, font=("Segoe UI", 11))
        menubar.add_cascade(label="View", menu=view_menu)
        
        # Font size submenu
        font_menu = tk.Menu(view_menu, tearoff=0, font=("Segoe UI", 11))
        view_menu.add_cascade(label="Font Size", menu=font_menu)
        font_var = tk.StringVar(value=self.settings["font_size"])
        for size in ["small", "medium", "large"]:
            font_menu.add_radiobutton(
                label=size.capitalize(),
                variable=font_var,
                value=size,
                command=lambda s=size: self._change_font_size(s)
            )
        
        # Theme toggle
        view_menu.add_checkbutton(
            label="Dark Theme",
            variable=tk.BooleanVar(value=self.settings["theme"] == "dark"),
            command=self.toggle_theme
        )
        
        # Show/Hide options
        view_menu.add_checkbutton(
            label="Show System Stats",
            variable=tk.BooleanVar(value=self.settings["show_system_stats"]),
            command=self._toggle_stats_visibility
        )

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, font=("Segoe UI", 11))
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="View Help", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)

    def _show_number_dialog(self, title, prompt, variable, min_val, max_val, is_float=False):
        """Show a dialog for entering numeric values."""
        dialog = ctk.CTkInputDialog(
            title=title,
            text=prompt
        )
        dialog.geometry("400x150")  # Make dialog wider
        
        result = dialog.get_input()
        if result:
            try:
                value = float(result) if is_float else int(result)
                if min_val <= value <= max_val:
                    variable.set(value)
                else:
                    messagebox.showerror(
                        "Invalid Value",
                        f"Please enter a value between {min_val} and {max_val}"
                    )
            except ValueError:
                messagebox.showerror(
                    "Invalid Input",
                    "Please enter a valid number"
                )

    def _change_font_size(self, size):
        """Change the application font size."""
        self.settings["font_size"] = size
        self.fonts = FONT_SIZES[size]
        self._save_settings()
        messagebox.showinfo(
            "Font Size Changed",
            "Please restart the application for the font size change to take effect."
        )

    def _toggle_stats_visibility(self):
        """Toggle visibility of system stats."""
        self.settings["show_system_stats"] = not self.settings["show_system_stats"]
        self._save_settings()
        messagebox.showinfo(
            "Settings Changed",
            "Please restart the application for this change to take effect."
        )

    def _update_stats(self):
        """Update system statistics."""
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            stats = [f"CPU: {cpu:.1f}%", f"RAM: {ram:.1f}%"]
            
            if torch.cuda.is_available():
                gpu = torch.cuda.get_device_properties(0)
                used = torch.cuda.memory_reserved(0)
                stats.append(f"GPU: {used/gpu.total_memory*100:.1f}%")
                stats.append(f"VRAM: {format_file_size(used)}/{format_file_size(gpu.total_memory)}")
            
            self.stats_lbl.configure(text="System Stats:  " + "  |  ".join(stats))
        except Exception as e:
            self.stats_lbl.configure(text=f"System Stats: Error ({str(e)})")
        
        if self.settings["show_system_stats"]:
            self.after(2000, self._update_stats)

    def _load_settings(self):
        """Load settings from file or use defaults."""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, "r") as f:
                    settings = json.load(f)
                    # Merge with defaults to handle new settings
                    return {**DEFAULT_SETTINGS, **settings}
            except:
                return DEFAULT_SETTINGS
        return DEFAULT_SETTINGS

    def _save_settings(self):
        """Save current settings to file."""
        with open(self.settings_file, "w") as f:
            json.dump(self.settings, f, indent=2)

    def toggle_theme(self):
        """Toggle between dark and light theme."""
        new_theme = "light" if self.settings["theme"] == "dark" else "dark"
        self.settings["theme"] = new_theme
        ctk.set_appearance_mode(new_theme)
        self.configure(fg_color=COLORS[f"background_{new_theme}"])
        self._save_settings()

    def show_help(self):
        """Show help dialog."""
        help_text = """Whispa App Help

1. Transcription
   - Select an audio file (WAV, MP3, M4A supported)
   - Choose model size (larger = more accurate but slower)
   - Click 'Transcribe' and wait for results
   
2. Translation
   - After transcription, select target language
   - Click 'Translate' to convert text
   
3. Export
   - Use 'Export' to save as TXT file
   - Or copy text directly from output panel
   
4. Tips
   - Models are downloaded on first use
   - Models are cached locally in 'models' folder
   - Use smaller models for faster results
   - Use larger models for better accuracy

Support:
- Report issues: https://github.com/damoojeje/whispa_app/issues
- Documentation: https://whispa-app.readthedocs.io/
- Contact: damilareeniolabi@gmail.com
- Website: www.eniolabi.com"""

        dialog = ctk.CTkToplevel(self)
        dialog.title("Whispa App Help")
        dialog.geometry("500x600")
        dialog.resizable(False, False)
        
        text = ctk.CTkTextbox(
            dialog,
            font=("Segoe UI", 12),
            wrap="word"
        )
        text.pack(fill="both", expand=True, padx=20, pady=20)
        text.insert("1.0", help_text)
        text.configure(state="disabled")

    def show_about(self):
        """Show about dialog."""
        about_text = """Whispa App 2.2.0
        
Audio Transcription & Translation Tool
Powered by OpenAI's Whisper and MarianMT

Developer: Damilare Eniolabi
Email: damilareeniolabi@gmail.com
Website: www.eniolabi.com
GitHub: https://github.com/damoojeje/Whispa_App

© 2025 Damilare Eniolabi
Licensed under MIT License"""

        dialog = ctk.CTkToplevel(self)
        dialog.title("About Whispa App")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        label = ctk.CTkLabel(
            dialog,
            text=about_text,
            justify="left",
            font=("Segoe UI", 12)
        )
        label.pack(padx=20, pady=20)

    def _on_browse(self):
        """Handle the Browse button click."""
        path = filedialog.askopenfilename(filetypes=[("Audio","*.wav *.mp3")])
        if path:
            self.file_entry.delete(0, "end")
            self.file_entry.insert(0, path)

    def _on_transcribe(self):
        """Start transcription in a background thread."""
        audio = self.file_entry.get().strip()
        if not audio:
            return messagebox.showerror("Error", "Select a file first.")
            
        self.transcribe_btn.configure(state="disabled")
        self.transcription_box.delete("1.0","end")
        self.translation_box.delete("1.0","end")
        self.progress_bar.set(0)

        def progress_callback(progress):
            self._update_progress(progress, "transcription")

        start_time = time.time()
        model_size = self.model_menu.get()

        args = (
            audio,
            model_size,
            self.adv_vram.get(),
            progress_callback,
            self.adv_tbeam.get(),
            self.adv_vad.get(),
            self.adv_sample_rate.get(),
            self.adv_channels.get()
        )
        
        threading.Thread(target=self._run_transcribe, args=(args, start_time, model_size), daemon=True).start()

    def _run_transcribe(self, args, start_time, model_size):
        """Run transcription in a background thread."""
        try:
            audio_file = args[0]  # Get just the audio file path
            
            # Update UI to show processing
            self.after(0, lambda: self.transcription_box.delete("1.0", "end"))
            self.after(0, lambda: self.transcription_box.insert("1.0", "Transcribing... Please wait..."))
            self.after(0, lambda: self.progress_bar.set(0))
            
            def progress_callback(progress: float):
                self.after(0, lambda p=progress: self.progress_bar.set(p))
            
            # Run transcription
            text = transcribe_file(
                file_path=audio_file,
                model_size=model_size,
                device="auto",  # Let transcribe_file handle device selection
                progress_callback=progress_callback
            )
            
            # Calculate duration in milliseconds
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Log success with correct parameters
            self.telemetry.record_transcription(
                model_size=model_size,
                file_type=os.path.splitext(audio_file)[1][1:],  # Get extension without dot
                file_size=os.path.getsize(audio_file),
                duration_ms=duration_ms,
                success=True
            )
            
            # Update UI with result
            self.after(0, lambda: self.transcription_box.delete("1.0", "end"))
            self.after(0, lambda: self.transcription_box.insert("1.0", text["text"]))
            self.after(0, lambda: self.transcribe_btn.configure(state="normal"))
            self.after(0, lambda: self.progress_bar.set(0))  # Reset progress bar
            
        except Exception as e:
            logging.error(f"Transcription error: {str(e)}")
            # Log failure with correct parameters
            self.telemetry.record_transcription(
                model_size=model_size,
                file_type=os.path.splitext(audio_file)[1][1:] if 'audio_file' in locals() else "unknown",
                file_size=os.path.getsize(audio_file) if 'audio_file' in locals() else 0,
                duration_ms=int((time.time() - start_time) * 1000),
                success=False,
                error=str(e)
            )
            self.after(0, lambda: self.transcription_box.delete("1.0", "end"))
            self.after(0, lambda: messagebox.showerror("Error", f"Transcription failed: {str(e)}"))
            self.after(0, lambda: self.transcribe_btn.configure(state="normal"))
            self.after(0, lambda: self.progress_bar.set(0))  # Reset progress bar

    def _on_translate(self):
        """Start translation in a background thread."""
        src = self.transcription_box.get("1.0","end").strip()
        if not src:
            return messagebox.showerror("Error","Nothing to translate.")
            
        self.translate_btn.configure(state="disabled")
        self.progress_bar.set(0)
        
        start_time = time.time()
        target_lang = self.lang_menu.get()

        def progress_callback(i, t):
            progress = i / t if t > 0 else 0
            self._update_progress(progress, "translation")

        args = {
            "text": src,
            "target_lang": target_lang,
            "progress_callback": progress_callback
        }
        
        threading.Thread(target=self._run_translate, args=(args, start_time, target_lang), daemon=True).start()

    def _run_translate(self, args, start_time, target_lang):
        """Execute translation in a separate thread"""
        try:
            if not args["text"].strip():
                messagebox.showwarning("Translation Error", "No text to translate!")
                return
                
            translated = translate(**args)
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Log telemetry
            self.telemetry.record_translation(
                target_lang=target_lang,
                text_length=len(args["text"]),
                duration_ms=duration_ms,
                success=True
            )
            
            self.translation_box.configure(state="normal")
            self.translation_box.delete("1.0", "end")
            self.translation_box.insert("1.0", translated)
            self.translation_box.configure(state="disabled")
            
        except TranslationError as e:
            logger.error(f"Translation error: {str(e)}", exc_info=True)
            self.telemetry.record_translation(
                target_lang=target_lang,
                text_length=len(args["text"]),
                duration_ms=int((time.time() - start_time) * 1000),
                success=False,
                error=str(e)
            )
            messagebox.showerror("Translation Error", str(e))
        except Exception as e:
            logger.error(f"Unexpected translation error: {str(e)}", exc_info=True)
            self.telemetry.record_translation(
                target_lang=target_lang,
                text_length=len(args["text"]),
                duration_ms=int((time.time() - start_time) * 1000),
                success=False,
                error=str(e)
            )
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
        finally:
            self.translate_btn.configure(state="normal")
            self.translation_box.configure(state="disabled")
            self._update_progress(0)

    def _save_transcription(self, txt):
        """Save transcription text to a file."""
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(simplify_text(txt))
            messagebox.showinfo("Saved", f"Transcript saved to:\n{path}")

    def _save_translation(self, txt):
        """Save translation text to a file."""
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(simplify_text(txt))
            messagebox.showinfo("Saved", f"Translation saved to:\n{path}")

    def _on_batch(self):
        """Handle the Batch button click."""
        paths = filedialog.askopenfilenames(filetypes=[("Audio","*.wav *.mp3")])
        if paths:
            self.batch_files = paths
            self.is_batch_mode = True
            self.current_batch_file = 0
            self.batch_progress = 0
            self.progress_bar.set(0)
            self.progress_bar.grid()
            threading.Thread(target=self._run_batch, daemon=True).start()

    def _run_batch(self):
        """Worker thread for batch processing."""
        while self.current_batch_file < len(self.batch_files):
            audio = self.batch_files[self.current_batch_file]
            self.progress_bar.set(self.current_batch_file / len(self.batch_files))
            try:
                def progress_callback(progress):
                    self.progress_bar.set(progress)

                text = transcribe_file(
                    audio,
                    self.model_menu.get(),
                    self.adv_vram.get(),
                    progress_callback,
                    self.adv_tbeam.get(),
                    self.adv_vad.get(),
                    self.adv_sample_rate.get(),
                    self.adv_channels.get()
                )
                self.transcription_box.insert("1.0", text)
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Error", str(e)))
            finally:
                self.current_batch_file += 1
        self.progress_bar.set(1)
        self.progress_bar.grid_remove()
        self.is_batch_mode = False

    def _update_progress(self, progress: float, operation: str = None):
        """Update progress bar and track operation metrics."""
        if operation and operation != self.current_operation:
            if self.current_operation:
                # Log completion of previous operation
                duration = time.time() - self.operation_start_time
                self.telemetry.log_operation_complete(
                    operation=self.current_operation,
                    duration=duration,
                    success=True
                )
            self.current_operation = operation
            self.operation_start_time = time.time()
            
        self.progress_bar.set(progress)
        self.update_idletasks()

def launch_app():
    app = WhispaApp()
    app.mainloop()

if __name__ == "__main__":
    launch_app()
