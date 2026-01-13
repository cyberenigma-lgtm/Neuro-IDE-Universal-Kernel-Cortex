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
        
        # Neural Log
        self.log_frame = tk.Frame(self.parent, bg=COLORS["bg_panel"])
        self.log_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.txt_log = tk.Text(self.log_frame, height=6, bg="#050505", fg=COLORS["text_secondary"], font=FONTS["code"], borderwidth=0)
        self.txt_log.pack(fill="both", expand=True)
        self.txt_log.insert(tk.END, "[NEURO-GATING] SYSTEM ONLINE. WAITING FOR SIGNAL...\n")
        
        self.parent.after(100, self.draw_brain)

    def log_neural(self, msg):
        self.txt_log.insert(tk.END, f"[GATING] {msg}\n")
        self.txt_log.see(tk.END)
        
    def simulate_gating(self):
        # Reset
        self.ia_states = [0] * 16
        self.log_neural("RESETTING SYNAPTIC PATHWAYS...")
        
        # Pick 5 random IA to be Active
        active_indices = random.sample(range(16), 5)
        for idx in active_indices:
            self.ia_states[idx] = 2
            self.log_neural(f"NODE IA-{idx+1} ACTIVATED [SIGNAL: {random.randint(80,100)}%]")
            
        # Standby for neighbors
        for idx in active_indices:
            prev = (idx - 1) % 16
            nxt = (idx + 1) % 16
            if self.ia_states[prev] == 0: self.ia_states[prev] = 1
            if self.ia_states[nxt] == 0: self.ia_states[nxt] = 1
            
        # One Critical for drama
        crit = random.choice(active_indices)
        self.ia_states[crit] = 3
        self.log_neural(f"WARNING: NODE IA-{crit+1} OVERLOAD DETECTED!")
        
    def refresh_ui(self):
        self.lbl_header.config(text=engine.get_string("tab_ia_gating"))
        self.lbl_desc.config(text=engine.get_string("ia_gating_desc"))
