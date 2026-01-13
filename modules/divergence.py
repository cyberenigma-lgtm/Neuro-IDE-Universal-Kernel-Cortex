import tkinter as tk
from modules.base import NeuroModule
from theme import COLORS, FONTS

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="Instruction Divergence", icon="📉", lang_key="tab_divergence")
        
    def build_ui(self, parent):
        # Header
        tk.Label(parent, text="Execution Trace Divergence (QEMU vs Bochs)", font=FONTS["heading"], bg=COLORS["bg_panel"], fg="white").pack(pady=10)
        
        paned = tk.PanedWindow(parent, orient="horizontal", bg=COLORS["bg_dark"], sashwidth=4)
        paned.pack(fill="both", expand=True)
        
        # Trace A
        f1 = tk.Frame(paned, bg=COLORS["bg_panel"])
        paned.add(f1, minsize=200)
        tk.Label(f1, text="Trace A (QEMU)", bg=COLORS["bg_medium"], fg="white").pack(fill="x")
        t1 = tk.Text(f1, bg=COLORS["bg_dark"], fg="#aaaaaa", font=FONTS["mono"], height=20, borderwidth=0)
        t1.pack(fill="both", expand=True)
        t1.insert(tk.END, "0x1000: mov eax, 1\n0x1005: int 0x80\n0x1007: jmp 0x1000\n0x1000: mov eax, 1...")
        
        # Trace B
        f2 = tk.Frame(paned, bg=COLORS["bg_panel"])
        paned.add(f2, minsize=200)
        tk.Label(f2, text="Trace B (Bochs)", bg=COLORS["bg_medium"], fg="white").pack(fill="x")
        t2 = tk.Text(f2, bg=COLORS["bg_dark"], fg="#aaaaaa", font=FONTS["mono"], height=20, borderwidth=0)
        t2.pack(fill="both", expand=True)
        t2.insert(tk.END, "0x1000: mov eax, 1\n0x1005: int 0x80\n0x1007: jmp 0x1000\n0x1002: hlt  <-- DIVERGENCE")
        
        # Highlight
        t2.tag_add("div", "4.0", "4.end")
        t2.tag_config("div", background=COLORS["accent_danger"], foreground="white")