import tkinter as tk
import random
from modules.base import NeuroModule
from theme import COLORS, FONTS

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="Kernel Behavior", icon="📊", lang_key="tab_profiler")
        
    def build_ui(self, parent):
        # Header
        tk.Label(parent, text="CPU Usage & Interrupts (Simulated)", font=FONTS["heading"], bg=COLORS["bg_panel"], fg="white").pack(pady=10)
        
        # Main Canvas
        self.canvas = tk.Canvas(parent, bg="#000000", height=300, highlightthickness=1, highlightbackground=COLORS["accent_secondary"])
        self.canvas.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Start Animation
        self.data_cpu = [0] * 50
        self.data_int = [0] * 50
        self.animate()
        
    def animate(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10: w = 400 # Default if not packed yet
        
        # Shift data
        self.data_cpu.pop(0)
        self.data_cpu.append(random.randint(10, 90))
        self.data_int.pop(0)
        self.data_int.append(random.randint(0, 50))
        
        self.canvas.delete("all")
        
        # Grid
        for i in range(0, h, 40):
            self.canvas.create_line(0, i, w, i, fill="#222222", dash=(2,2))
            
        # Draw CPU (Green)
        points_cpu = []
        step = w / 50
        for i, val in enumerate(self.data_cpu):
            x = i * step
            y = h - (val / 100 * h)
            points_cpu.append(x)
            points_cpu.append(y)
        if len(points_cpu) > 4:
            self.canvas.create_line(points_cpu, fill=COLORS["accent_success"], width=2, smooth=True)
            
        # Draw Interrupts (Red/Warning)
        points_int = []
        for i, val in enumerate(self.data_int):
            x = i * step
            y = h - (val / 100 * h)
            points_int.append(x)
            points_int.append(y)
        if len(points_int) > 4:
            self.canvas.create_line(points_int, fill=COLORS["accent_danger"], width=1, dash=(2,2))
            
        self.canvas.create_text(20, 20, text="CPU %", fill=COLORS["accent_success"], anchor="w")
        self.canvas.create_text(20, 40, text="IRQs", fill=COLORS["accent_danger"], anchor="w")
            
        parent_widget = self.canvas.master
        if parent_widget.winfo_exists():
            parent_widget.after(100, self.animate)