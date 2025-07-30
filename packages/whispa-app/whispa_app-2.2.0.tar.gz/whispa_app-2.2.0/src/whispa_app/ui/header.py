import customtkinter as ctk

def build_header(parent, show_help, show_about, toggle_adv):
    frame = ctk.CTkFrame(parent, height=50)
    frame.pack(fill="x", padx=5, pady=(5,0))
    ctk.CTkLabel(frame, text="Whispa App", font=("Arial",18,"bold")).pack(side="left", padx=5)
    ctk.CTkButton(frame, text="Help", command=show_help).pack(side="right", padx=5)
    ctk.CTkButton(frame, text="About", command=show_about).pack(side="right", padx=5)
    ctk.CTkButton(frame, text="Advanced ▼", command=toggle_adv).pack(side="right", padx=5)
    return frame