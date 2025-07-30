import customtkinter as ctk
from tkinter import filedialog

def build_file_input(parent, browse_cmd, start_cmd):
    frame = ctk.CTkFrame(parent)
    frame.pack(fill="x", pady=10)
    entry = ctk.CTkEntry(frame, placeholder_text="Select audio file...")
    entry.pack(side="left", fill="x", expand=True, padx=5)
    ctk.CTkButton(frame, text="Browse", command=lambda: browse_cmd(entry)).pack(side="left", padx=5)
    btn = ctk.CTkButton(frame, text="Transcribe", state="disabled", command=lambda: start_cmd(entry.get()))
    btn.pack(side="left", padx=5)
    return frame, entry, btn