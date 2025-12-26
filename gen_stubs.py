import os

STUB_TEMPLATE = """
import tkinter as tk
from modules.base import NeuroModule
from theme import COLORS, FONTS

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="{NAME}", icon="{ICON}")
        
    def build_ui(self, parent):
        # Header
        header = tk.Frame(parent, bg=COLORS["bg_medium"], height=40)
        header.pack(fill="x", side="top")
        tk.Label(header, text="{NAME}", bg=COLORS["bg_medium"], fg="white", font=FONTS["heading"]).pack(side="left", padx=10, pady=5)
        
        # Placeholder Content
        center = tk.Frame(parent, bg=COLORS["bg_panel"])
        center.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(center, text="🚧 {NAME} 🚧", font=("Segoe UI", 24, "bold"), bg=COLORS["bg_panel"], fg=COLORS["accent_primary"]).pack(pady=20)
        tk.Label(center, text="{DESC}", font=FONTS["main"], bg=COLORS["bg_panel"], fg=COLORS["text_secondary"]).pack()
        
        tk.Button(center, text="Initialize Module", bg=COLORS["accent_secondary"], fg="white", relief="flat", padx=20, pady=10).pack(pady=20)
"""

TOOLS = [
    ("kttd", "Hyper-Debugger", "🧠", "Time-Travel Kernel Debugger"),
    ("ubd", "Binary Diff", "🔍", "Universal Binary Diff Tool"),
    ("bootviz", "Boot Visualizer", "🌀", "Real/Protected/Long Mode Visualizer"),
    ("syscalls", "Syscall Mapper", "🧩", "Auto-Syscall Documentation & Mapper"),
    ("profiler", "Kernel Profiler", "🧪", "Interrupts & Latency Profiler"),
    ("screendiff", "Screen Diff", "🛰", "Multi-Emulator Screenshot Comparator"),
    ("sandbox", "OSDev Sandbox", "🧱", "Project Generator & Sandbox"),
    ("divergence", "Instruct. Div.", "🧬", "Instruction-Level Divergence Analyzer"),
    ("memmap", "Memory Map", "🧭", "Live Memory Map Visualizer"),
    ("neurodoctor", "Neuro-Doctor", "🧨", "Kernel Panic Classifier (AI)"),
    ("boottest", "Boot Tester", "🔧", "Universal Bootloader Tester"),
    ("regression", "Regression Det.", "🧰", "Kernel Regression Detector"),
    ("elf", "ELF Explorer", "🧱", "ELF Structure & Symbol Explorer"),
    ("knowledge", "Knowledge Graph", "🧠", "OSDev Knowledge Graph Generator")
]

base_dir = r"c:\Users\cyber\Documents\NeuroOs\Neuro-OS-Genesis\neuro-ide\modules"

for filename, name, icon, desc in TOOLS:
    content = STUB_TEMPLATE.format(NAME=name, ICON=icon, DESC=desc)
    path = os.path.join(base_dir, f"{filename}.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())

print(f"Generated {len(TOOLS)} stubs.")
