import tkinter as tk
import math
from modules.base import NeuroModule
from theme import COLORS, FONTS
from locale_engine import engine

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="OSDev Knowledge Graph", icon="🧠", lang_key="tab_knowledge")
        
    def build_ui(self, parent):
        self.parent = parent
        # Header
        self.lbl_header = tk.Label(parent, text=engine.get_string("tab_knowledge"), font=FONTS["heading"], bg=COLORS["bg_panel"], fg="white")
        self.lbl_header.pack(pady=10)
        
        self.canvas = tk.Canvas(parent, bg="#1a1a2e", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.draw_graph()
        
    def draw_graph(self):
        nodes = {
            "Bootloader": (400, 50),
            "GDT": (300, 150),
            "IDT": (500, 150),
            "Paging": (400, 250),
            "Kernel Entry": (400, 350),
            "Drivers": (250, 450),
            "Filesystem": (550, 450),
            "Shell": (400, 550)
        }
        
        edges = [
            ("Bootloader", "GDT"), ("Bootloader", "IDT"),
            ("GDT", "Paging"), ("IDT", "Paging"),
            ("Paging", "Kernel Entry"),
            ("Kernel Entry", "Drivers"), ("Kernel Entry", "Filesystem"),
            ("Drivers", "Shell"), ("Filesystem", "Shell")
        ]
        
        c = self.canvas
        
        # Edges
        for u, v in edges:
            x1, y1 = nodes[u]
            x2, y2 = nodes[v]
            c.create_line(x1, y1, x2, y2, fill=COLORS["text_dim"], width=2, arrow=tk.LAST)
            
        # Nodes
        for name, pos in nodes.items():
            x, y = pos
            r = 40
            color = COLORS["accent_primary"]
            if name == "Kernel Entry": color = COLORS["accent_secondary"]
            
            c.create_oval(x-r, y-r/2, x+r, y+r/2, fill=color, outline="white")
            c.create_text(x, y, text=name, fill="white", font=FONTS["small"])

    def refresh_ui(self):
        self.lbl_header.config(text=engine.get_string("tab_knowledge"))