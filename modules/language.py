import tkinter as tk
from tkinter import ttk
from modules.base import NeuroModule
from theme import COLORS, FONTS
from locale_engine import engine

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="Language", icon="🌐")
        
    def build_ui(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bg=COLORS["bg_panel"])
        self.frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Title
        self.lbl_title = tk.Label(self.frame, text="Universal Localization", font=FONTS["heading"], bg=COLORS["bg_panel"], fg=COLORS["text_primary"])
        self.lbl_title.pack(pady=(0, 20))
        
        # Description
        self.lbl_desc = tk.Label(self.frame, text="Select the interface language / Selecciona el idioma / Escolha o idioma", 
                                font=FONTS["main"], bg=COLORS["bg_panel"], fg=COLORS["text_secondary"], wraplength=500)
        self.lbl_desc.pack(pady=10)
        
        # Selector Container
        self.selector_frame = tk.Frame(self.frame, bg=COLORS["bg_panel"])
        self.selector_frame.pack(pady=20)
        
        languages = [
            ("English", "en", "🇺🇸"),
            ("Español", "es", "🇪🇸"),
            ("Português-BR", "pt", "🇧🇷"),
            ("Français", "fr", "🇫🇷"),
            ("Deutsch", "de", "🇩🇪"),
            ("Italiano", "it", "🇮🇹"),
            ("العربية", "ar", "🇸🇦"),
            ("Русский", "ru", "🇷🇺"),
            ("한국어", "ko", "🇰🇷"),
            ("Indonesian", "id", "🇮🇩"),
            ("中文", "zh", "🇨🇳"),
            ("日本語", "ja", "🇯🇵")
        ]
        
        self.buttons = []
        for name, code, flag in languages:
            btn = tk.Button(self.selector_frame, text=f"{flag} {name}", font=FONTS["main"], 
                           bg=COLORS["bg_medium"], fg="white", relief="flat", padx=20, pady=10,
                           command=lambda c=code: self.change_language(c))
            btn.pack(fill="x", pady=5)
            self.buttons.append(btn)
            
        # Refresh current UI
        self.refresh_labels()
        engine.register_callback(self.refresh_labels)

    def change_language(self, code):
        engine.load_lang(code)
        
    def refresh_labels(self):
        # Update tab name indirectly via NeuroIDE if needed, but here we update local labels
        self.lbl_title.config(text=engine.get_string("tab_lang").strip())
        # description is static in this case as it shows all 3 main ones
