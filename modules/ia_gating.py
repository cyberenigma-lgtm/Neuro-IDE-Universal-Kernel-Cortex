import tkinter as tk
import math
import random
from modules.base import NeuroModule
from theme import COLORS, FONTS
from locale_engine import engine

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="IA Gating Neuronal", icon="🛡️", lang_key="tab_ia_gating")
        self.ia_states = [0] * 16 # 0: Sleeping, 1: Standby, 2: Active, 3: Critical
        self.nodes = []
        
    def build_ui(self, parent):
        self.parent = parent
        
        # Header
        self.lbl_header = tk.Label(parent, text=engine.get_string("tab_ia_gating"), font=FONTS["heading"], bg=COLORS["bg_panel"], fg="white")
        self.lbl_header.pack(pady=10)
        
        # Description
        self.lbl_desc = tk.Label(parent, text=engine.get_string("ia_gating_desc"), 
                               font=FONTS["main"], bg=COLORS["bg_panel"], fg=COLORS["text_secondary"])
        self.lbl_desc.pack()
        
        # Central Canvas for Brain-like display
        self.canvas = tk.Canvas(parent, bg="#0f0f12", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Controls
        self.btn_frame = tk.Frame(parent, bg=COLORS["bg_panel"])
        self.btn_frame.pack(pady=10)
        
        self.btn_simulate = tk.Button(self.btn_frame, text="Simulate Gating", bg=COLORS["accent_secondary"], fg="white", relief="flat", padx=10, command=self.simulate_gating)
        self.btn_simulate.pack(side="left", padx=5)
        
        self.parent.after(100, self.draw_brain)
        
    def draw_brain(self):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width <= 1: width, height = 600, 400
        
        cx, cy = width // 2, height // 2
        radius = min(cx, cy) - 50
        
        # Brain outline (subtle)
        self.canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius, outline="#1a1a2e", width=2)
        
        self.nodes = []
        for i in range(16):
            angle = math.radians(i * (360 / 16))
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            
            state = self.ia_states[i]
            color = "#333333" # Sleeping
            if state == 1: color = "#555577" # Standby
            elif state == 2: color = COLORS["accent_success"] # Active
            elif state == 3: color = COLORS["accent_danger"] # Critical
            
            # Pulse effect for active nodes
            r = 15
            if state >= 2:
                r += random.randint(-2, 2)
                self.canvas.create_oval(x-r-5, y-r-5, x+r+5, y+r+5, outline=color, width=1)
            
            node_id = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="white", width=1)
            self.canvas.create_text(x, y, text=f"IA-{i+1}", fill="white", font=("Arial", 8, "bold"))
            self.nodes.append((x, y))

        # Connections (Active Gating)
        for i in range(16):
            if self.ia_states[i] >= 2:
                for j in range(i+1, 16):
                    if self.ia_states[j] >= 2:
                        x1, y1 = self.nodes[i]
                        x2, y2 = self.nodes[j]
                        self.canvas.create_line(x1, y1, x2, y2, fill=COLORS["accent_primary"], width=1, dash=(2, 2))
        
        self.parent.after(500, self.draw_brain)

    def simulate_gating(self):
        # Reset
        self.ia_states = [0] * 16
        
        # Pick 5 random IA to be Active
        active_indices = random.sample(range(16), 5)
        for idx in active_indices:
            self.ia_states[idx] = 2
            
        # Standby for neighbors
        for idx in active_indices:
            prev = (idx - 1) % 16
            nxt = (idx + 1) % 16
            if self.ia_states[prev] == 0: self.ia_states[prev] = 1
            if self.ia_states[nxt] == 0: self.ia_states[nxt] = 1
            
        # One Critical for drama
        self.ia_states[random.choice(active_indices)] = 3
        
    def refresh_ui(self):
        self.lbl_header.config(text=engine.get_string("tab_ia_gating"))
        self.lbl_desc.config(text=engine.get_string("ia_gating_desc"))
