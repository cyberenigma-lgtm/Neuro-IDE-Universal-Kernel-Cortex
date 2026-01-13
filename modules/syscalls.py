import tkinter as tk
from tkinter import ttk
from modules.base import NeuroModule
from theme import COLORS, FONTS

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="Syscall Mapper", icon="🗺️", lang_key="tab_syscalls")
        
    def build_ui(self, parent):
        # Header
        tk.Label(parent, text="Kernel System Calls Registry", font=FONTS["heading"], bg=COLORS["bg_panel"], fg="white").pack(pady=10)
        
        # Search
        f = tk.Frame(parent, bg=COLORS["bg_panel"])
        f.pack(fill="x", padx=20)
        tk.Label(f, text="Search:", bg=COLORS["bg_panel"], fg="white").pack(side="left")
        tk.Entry(f, bg=COLORS["bg_medium"], fg="white", relief="flat").pack(side="left", fill="x", expand=True, padx=10)
        
        # Table
        cols = ("ID", "Name", "Handler", "Privilege")
        tree = ttk.Treeview(parent, columns=cols, show="headings", height=15)
        tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100)
            
        # Mock Data
        data = [
            ("0x00", "sys_print", "k_print", "User"),
            ("0x01", "sys_read", "k_read", "User"),
            ("0x02", "sys_yield", "sched_yield", "User"),
            ("0x10", "sys_alloc", "vmm_alloc", "Kernel"),
            ("0x11", "sys_free", "vmm_free", "Kernel"),
            ("0xFF", "sys_reboot", "power_reset", "Ring0 Only"),
        ]
        
        for item in data:
            tree.insert("", "end", values=item)
            
        tk.Button(parent, text="Generate Documentation", bg=COLORS["accent_secondary"], fg="white", relief="flat").pack(pady=10)