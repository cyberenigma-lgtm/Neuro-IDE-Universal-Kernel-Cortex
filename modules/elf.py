import tkinter as tk
from tkinter import ttk
from modules.base import NeuroModule
from theme import COLORS, FONTS

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="ELF Explorer", icon="📂", lang_key="tab_elf")
        
    def build_ui(self, parent):
        # Header
        tk.Label(parent, text="ELF Binary Structure", font=FONTS["heading"], bg=COLORS["bg_panel"], fg="white").pack(pady=10)
        
        paned = tk.PanedWindow(parent, orient="horizontal", bg=COLORS["bg_dark"], sashwidth=4)
        paned.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tree Structure
        tree = ttk.Treeview(paned, show="tree headings", columns=("Size", "Offset"))
        tree.heading("#0", text="Section")
        tree.heading("Size", text="Size")
        tree.heading("Offset", text="Offset")
        paned.add(tree, minsize=300)
        
        # Root
        root = tree.insert("", "end", text="kernel.elf (64-bit LSB)", open=True)
        
        # Headers
        h = tree.insert(root, "end", text="ELF Header", values=("64 bytes", "0x00"))
        
        # Program Headers
        ph = tree.insert(root, "end", text="Program Headers (3)", open=True)
        tree.insert(ph, "end", text="LOAD [R E]", values=("0x4000", "0x1000"))
        tree.insert(ph, "end", text="LOAD [RW]", values=("0x2000", "0x5000"))
        
        # Sections
        sh = tree.insert(root, "end", text="Sections", open=True)
        tree.insert(sh, "end", text=".text", values=("14.2 KB", "0x1000"))
        tree.insert(sh, "end", text=".rodata", values=("2.1 KB", "0x4500"))
        tree.insert(sh, "end", text=".data", values=("400 B", "0x5000"))
        tree.insert(sh, "end", text=".bss", values=("8 KB", "0x5200"))
        tree.insert(sh, "end", text=".symtab", values=("12 KB", "0x8000"))
        
        # Details View
        details = tk.Frame(paned, bg=COLORS["bg_panel"])
        paned.add(details, minsize=300)
        tk.Label(details, text="Hex / Info", bg=COLORS["bg_panel"], fg=COLORS["text_dim"]).pack(pady=20)