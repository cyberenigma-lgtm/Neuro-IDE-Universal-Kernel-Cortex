import tkinter as tk
from modules.base import NeuroModule
from theme import COLORS, FONTS

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="Bootloader Visualizer", icon="🖼️", lang_key="tab_bootviz")
        
    def build_ui(self, parent):
        # Split: Left (Canvas), Right (Controls)
        split = tk.PanedWindow(parent, orient="horizontal", bg=COLORS["bg_dark"], sashwidth=4, sashrelief="flat")
        split.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Canvas
        self.canvas = tk.Canvas(split, bg=COLORS["tl_track_bg"], highlightthickness=0)
        split.add(self.canvas, minsize=500)
        
        # Controls
        ctrl = tk.Frame(split, bg=COLORS["bg_panel"])
        split.add(ctrl, minsize=200)
        
        tk.Label(ctrl, text="Boot Stage", font=FONTS["heading"], bg=COLORS["bg_panel"], fg="white").pack(pady=10)
        
        # Stage Buttons
        bg = COLORS["accent_secondary"]
        tk.Button(ctrl, text="1. Real Mode (16-bit)", bg=bg, fg="white", relief="flat", command=lambda: self.draw_stage(1)).pack(fill="x", padx=20, pady=5)
        tk.Button(ctrl, text="2. Protected Mode (32-bit)", bg=bg, fg="white", relief="flat", command=lambda: self.draw_stage(2)).pack(fill="x", padx=20, pady=5)
        tk.Button(ctrl, text="3. Long Mode (64-bit)", bg=bg, fg="white", relief="flat", command=lambda: self.draw_stage(3)).pack(fill="x", padx=20, pady=5)
        
        # Initial Draw
        self.draw_stage(1)
        
    def draw_stage(self, stage):
        c = self.canvas
        c.delete("all")
        w = c.winfo_reqwidth()
        
        # Draw Memory Map Simulation
        
        # Base Memory
        self.draw_block(50, 400, "0x0000 - IVT (Interrupt Vector Table)", "#444444")
        self.draw_block(50, 350, "0x0400 - BDA (BIOS Data Area)", "#555555")
        self.draw_block(50, 300, "0x7C00 - Bootloader (512b)", COLORS["accent_primary"])
        
        if stage >= 1:
            c.create_text(300, 325, text="<-- CS:IP starts here", fill="white", anchor="w")
            
        if stage >= 2:
            self.draw_block(50, 200, "0x100000 - Kernel Space (High Mem)", COLORS["accent_success"])
            self.draw_block(50, 250, "GDT / IDT Tables", COLORS["accent_warning"])
            c.create_text(300, 225, text="<-- Protected Mode Entry", fill="white", anchor="w")
            
        if stage >= 3:
             self.draw_block(50, 100, "0x200000 - Paging Tables (PML4)", COLORS["accent_danger"])
             c.create_text(300, 125, text="<-- Long Mode Enabled (64-bit)", fill="white", anchor="w")

    def draw_block(self, x, y, text, color):
        self.canvas.create_rectangle(x, y, x+200, y+40, fill=color, outline="white")
        self.canvas.create_text(x+100, y+20, text=text, fill="white", font=FONTS["small"])