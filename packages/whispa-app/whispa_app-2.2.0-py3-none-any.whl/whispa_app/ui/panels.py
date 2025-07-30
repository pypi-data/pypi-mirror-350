# src/whispa_app/ui/panels.py

import customtkinter as ctk
from typing import Dict, Callable, Any

def build_panels(
    root: ctk.CTk,
    on_transcribe: Callable[[], None],
    on_translate: Callable[[], None],
    on_export: Callable[[], None],
    on_model_change: Callable[[str], None],
    on_language_change: Callable[[str], None],
    font_size: int = 16
) -> Dict[str, Any]:
    """
    Build the main UI panels.
    
    Args:
        root: Root window
        on_transcribe: Callback when transcribe button clicked
        on_translate: Callback when translate button clicked
        on_export: Callback when export button clicked
        on_model_change: Callback when model selection changes
        on_language_change: Callback when language selection changes
        font_size: Font size for text and buttons
        
    Returns:
        Dict containing:
            - input: Input panel frame
            - output: Output panel frame
            - controls: Controls panel frame
            - input_text: Input text box
            - output_text: Output text box
            - model_var: Model selection variable
            - lang_var: Language selection variable
    """
    # Input panel (left side)
    input_frame = ctk.CTkFrame(root)
    input_frame.grid(row=0, column=0, sticky="nsew", padx=(10,5), pady=10)
    input_frame.grid_columnconfigure(0, weight=1)
    input_frame.grid_rowconfigure(1, weight=1)
    
    # Input title
    ctk.CTkLabel(
        input_frame,
        text="Input",
        font=("Segoe UI", font_size + 2, "bold")
    ).grid(row=0, column=0, sticky="w", padx=10, pady=(10,5))
    
    # Input text box
    input_text = ctk.CTkTextbox(
        input_frame,
        font=("Segoe UI", font_size),
        wrap="word"
    )
    input_text.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
    
    # Input buttons
    input_buttons = ctk.CTkFrame(input_frame, fg_color="transparent")
    input_buttons.grid(row=2, column=0, sticky="ew", padx=10, pady=(5,10))
    
    transcribe_btn = ctk.CTkButton(
        input_buttons,
        text="Transcribe",
        command=on_transcribe,
        font=("Segoe UI", font_size)
    )
    transcribe_btn.pack(side="left", padx=5)
    
    # Output panel (right side)
    output_frame = ctk.CTkFrame(root)
    output_frame.grid(row=0, column=1, sticky="nsew", padx=(5,10), pady=10)
    output_frame.grid_columnconfigure(0, weight=1)
    output_frame.grid_rowconfigure(1, weight=1)
    
    # Output title
    ctk.CTkLabel(
        output_frame,
        text="Output",
        font=("Segoe UI", font_size + 2, "bold")
    ).grid(row=0, column=0, sticky="w", padx=10, pady=(10,5))
    
    # Output text box
    output_text = ctk.CTkTextbox(
        output_frame,
        font=("Segoe UI", font_size),
        wrap="word"
    )
    output_text.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
    
    # Output buttons
    output_buttons = ctk.CTkFrame(output_frame, fg_color="transparent")
    output_buttons.grid(row=2, column=0, sticky="ew", padx=10, pady=(5,10))
    
    translate_btn = ctk.CTkButton(
        output_buttons,
        text="Translate",
        command=on_translate,
        font=("Segoe UI", font_size)
    )
    translate_btn.pack(side="left", padx=5)
    
    export_btn = ctk.CTkButton(
        output_buttons,
        text="Export",
        command=on_export,
        font=("Segoe UI", font_size)
    )
    export_btn.pack(side="left", padx=5)
    
    # Controls panel (bottom)
    controls_frame = ctk.CTkFrame(root)
    controls_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0,10))
    controls_frame.grid_columnconfigure((0,1), weight=1)
    
    # Model selection
    model_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
    model_frame.grid(row=0, column=0, sticky="w", padx=10, pady=10)
    
    ctk.CTkLabel(
        model_frame,
        text="Model:",
        font=("Segoe UI", font_size)
    ).pack(side="left", padx=(0,5))
    
    model_var = ctk.StringVar(value="small")
    model_dropdown = ctk.CTkComboBox(
        model_frame,
        values=["model_tiny", "model_base", "model_small", "model_medium", "model_large"],
        variable=model_var,
        command=on_model_change,
        font=("Segoe UI", font_size)
    )
    model_dropdown.pack(side="left")
    
    # Language selection
    lang_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
    lang_frame.grid(row=0, column=1, sticky="e", padx=10, pady=10)
    
    ctk.CTkLabel(
        lang_frame,
        text="Language:",
        font=("Segoe UI", font_size)
    ).pack(side="left", padx=(0,5))
    
    lang_var = ctk.StringVar(value="English")
    lang_dropdown = ctk.CTkComboBox(
        lang_frame,
        values=["language_English", "language_Spanish", "language_French", "language_German", "language_Chinese", "language_Japanese"],
        variable=lang_var,
        command=on_language_change,
        font=("Segoe UI", font_size)
    )
    lang_dropdown.pack(side="left")
    
    # Configure grid weights
    root.grid_columnconfigure((0,1), weight=1)
    root.grid_rowconfigure(0, weight=1)
    
    return {
        "input": input_frame,
        "output": output_frame,
        "controls": controls_frame,
        "input_text": input_text,
        "output_text": output_text,
        "model_var": model_var,
        "lang_var": lang_var,
        "transcribe_btn": transcribe_btn,
        "translate_btn": translate_btn,
        "export_btn": export_btn,
        "model_dropdown": model_dropdown,
        "lang_dropdown": lang_dropdown
    }
