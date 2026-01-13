import tkinter as tk
from modules.base import NeuroModule
from theme import COLORS, FONTS

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="ScreenDiff", icon="📺", lang_key="tab_screendiff")
        
    def build_ui(self, parent):
        # Header
        tk.Label(parent, text="Visual Regression Testing", font=FONTS["heading"], bg=COLORS["bg_panel"], fg="white").pack(pady=10)
        
        # Layout
        frame = tk.Frame(parent, bg=COLORS["bg_dark"])
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left Image
        l = tk.Frame(frame, bg="#000000", width=400, height=300)
        l.pack(side="left", padx=10, fill="both", expand=True)
        l.pack_propagate(False)
        tk.Label(l, text="BASELINE (v1.0)", fg="#888", bg="black").pack(expand=True)
        
        # Right Image
        r = tk.Frame(frame, bg="#000000", width=400, height=300)
        r.pack(side="left", padx=10, fill="both", expand=True)
        r.pack_propagate(False)
        tk.Label(r, text="CURRENT (v1.1)", fg="#888", bg="black").pack(expand=True)
        
        # Controls
        ctrl = tk.Frame(parent, bg=COLORS["bg_panel"], height=50)
        ctrl.pack(fill="x", pady=10)
        
        tk.Label(ctrl, text="Difference Metric: 0.05% (PASS)", fg=COLORS["accent_success"], bg=COLORS["bg_panel"], font=FONTS["heading"]).pack()