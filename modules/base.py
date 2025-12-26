import tkinter as tk
from theme import COLORS, FONTS
from locale_engine import engine

class NeuroModule:
    """Base interface for all Neuro-IDE plugins"""
    def __init__(self, name: str, icon: str = "🧩", lang_key: str = None):
        self.name = name
        self.icon = icon
        self.lang_key = lang_key
    
    def get_tab_name(self) -> str:
        display_name = self.name
        if self.lang_key:
            # Try to get localized name
            localized = engine.get_string(self.lang_key, self.name)
            if localized != f"[{self.lang_key}]":
                display_name = localized
        return f" {self.icon} {display_name} "
        
    def build_ui(self, parent_frame: tk.Frame):
        """Override this to build your module's UI"""
        self.parent_frame = parent_frame
        display_name = self.name
        if self.lang_key:
            display_name = engine.get_string(self.lang_key, self.name)
            
        self.lbl_default = tk.Label(parent_frame, text=f"{display_name}\n(Under Construction)", font=FONTS["heading"], bg=COLORS["bg_panel"], fg=COLORS["text_dim"])
        self.lbl_default.pack(expand=True)
        
    def refresh_ui(self):
        """Override this to update localized labels inside the module"""
        if hasattr(self, "lbl_default") and self.lbl_default.winfo_exists():
            display_name = self.name
            if self.lang_key:
                display_name = engine.get_string(self.lang_key, self.name)
            self.lbl_default.config(text=f"{display_name}\n(Under Construction)")
