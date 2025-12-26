import tkinter as tk
from modules.base import NeuroModule
from theme import COLORS, FONTS

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="Memory Visualizer", icon="📑", lang_key="tab_memmap")
        
    def build_ui(self, parent):
        # Header
        tk.Label(parent, text="Physical Memory Layout (E820 Map)", font=FONTS["heading"], bg=COLORS["bg_panel"], fg="white").pack(pady=10)
        
        # Canvas for Memory Bars
        self.canvas = tk.Canvas(parent, bg=COLORS["bg_dark"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.draw_map()
        
    def draw_map(self):
        c = self.canvas
        y = 20
        
        regions = [
            ("0x00000000 - 0x0009FC00", "Base Memory (Usable)", COLORS["accent_success"]),
            ("0x0009FC00 - 0x000A0000", "EBDA (Reserved)", COLORS["accent_danger"]),
            ("0x000A0000 - 0x00100000", "Video RAM & BIOS (Reserved)", COLORS["accent_danger"]),
            ("0x00100000 - 0x00EFFFFF", "High Memory (Kernel Heap)", COLORS["accent_success"]),
            ("0x00F00000 - 0x01000000", "ACPI / MMIO", COLORS["accent_warning"]),
            ("0x01000000 - 0xFFFFFFFF", "Extended RAM (Usable)", COLORS["accent_success"]),
        ]
        
        for range_str, desc, color in regions:
            # Draw block
            c.create_rectangle(50, y, 100, y+40, fill=color, outline="white")
            # Connect line
            c.create_line(100, y+20, 130, y+20, fill="white")
            # Text
            c.create_text(140, y+20, text=desc, fill="white", anchor="w", font=FONTS["main"])
            c.create_text(140, y+35, text=range_str, fill=COLORS["text_dim"], anchor="w", font=FONTS["small"])
            
            y += 60
            
        # Stats
        c.create_text(50, y+20, text="Total Detected RAM: 128 MB", fill=COLORS["accent_primary"], anchor="w", font=FONTS["heading"])