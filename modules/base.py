import tkinter as tk
from theme import COLORS, FONTS

class NeuroModule:
    """Base interface for all Neuro-IDE plugins"""
    def __init__(self, name: str, icon: str = "🧩"):
        self.name = name
        self.icon = icon
    
    def get_tab_name(self) -> str:
        return f" {self.icon} {self.name} "
        
    def build_ui(self, parent_frame: tk.Frame):
        """Override this to build your module's UI"""
        lbl = tk.Label(parent_frame, text=f"{self.name}\n(Under Construction)", font=FONTS["heading"], bg=COLORS["bg_panel"], fg=COLORS["text_dim"])
        lbl.pack(expand=True)
