import tkinter as tk
import random
from modules.base import NeuroModule
from theme import COLORS, FONTS

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="Regression", icon="📉", lang_key="tab_regression")
        
    def build_ui(self, parent):
        # Header
        tk.Label(parent, text="Kernel Boot Time Trend", font=FONTS["heading"], bg=COLORS["bg_panel"], fg="white").pack(pady=10)
        
        # Canvas
        canvas = tk.Canvas(parent, bg="#111", highlightthickness=0, height=300)
        canvas.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Draw Trend
        w = 800
        h = 300
        data = [500, 490, 485, 480, 475, 470, 460, 455, 600, 550, 450]
        
        # Axes
        canvas.create_line(50, 250, 750, 250, fill="#444") # X
        canvas.create_line(50, 50, 50, 250, fill="#444")   # Y
        
        # Plot
        step = 700 / len(data)
        prev_x, prev_y = 50, 250 - (data[0]/1000 * 200)
        
        for i, val in enumerate(data):
            x = 50 + i * step
            y = 250 - (val/1000 * 200)
            
            color = COLORS["accent_success"]
            # REGRESSION SPIKE
            if i > 0 and val > data[i-1] + 50: 
                color = COLORS["accent_danger"]
                canvas.create_text(x, y-15, text=f"+{val-data[i-1]}ms", fill=COLORS["accent_danger"])
            
            canvas.create_oval(x-4, y-4, x+4, y+4, fill=color, outline="white")
            if i > 0:
                canvas.create_line(prev_x, prev_y, x, y, fill=COLORS["accent_primary"], width=2)
            
            prev_x, prev_y = x, y
            
            canvas.create_text(x, 270, text=f"v0.{i}", fill="#666")
            
        canvas.create_text(50, 30, text="Boot Time (ms)", fill="white", anchor="w")