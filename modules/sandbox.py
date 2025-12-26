import tkinter as tk
from modules.base import NeuroModule
from theme import COLORS, FONTS

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="OSDev Generator", icon="🏗️", lang_key="tab_sandbox")
        
    def build_ui(self, parent):
        # Header
        tk.Label(parent, text="Quick Project Generator", font=FONTS["heading"], bg=COLORS["bg_panel"], fg="white").pack(pady=10)
        
        # Form
        form = tk.Frame(parent, bg=COLORS["bg_panel"])
        form.pack(pady=20)
        
        # Architecture
        tk.Label(form, text="Architecture:", bg=COLORS["bg_panel"], fg="white", width=15, anchor="e").grid(row=0, column=0, pady=5)
        arch = tk.StringVar(value="x86_64")
        tk.OptionMenu(form, arch, "x86", "x86_64", "ARM64", "RISC-V").grid(row=0, column=1, sticky="w")
        
        # Bootloader
        tk.Label(form, text="Bootloader:", bg=COLORS["bg_panel"], fg="white", width=15, anchor="e").grid(row=1, column=0, pady=5)
        boot = tk.StringVar(value="Multiboot2")
        tk.OptionMenu(form, boot, "Limine", "Grub (Multiboot2)", "UEFI", "Legacy BIOS").grid(row=1, column=1, sticky="w")
        
        # Kernel Type
        tk.Label(form, text="Kernel Type:", bg=COLORS["bg_panel"], fg="white", width=15, anchor="e").grid(row=2, column=0, pady=5)
        ktype = tk.StringVar(value="Monolithic")
        tk.OptionMenu(form, ktype, "Monolithic", "Microkernel", "Exokernel", "Hybrid").grid(row=2, column=1, sticky="w")
        
        # Options
        tk.Checkbutton(form, text="Include Serial Drivers", bg=COLORS["bg_panel"], fg="white", selectcolor="#444").grid(row=3, column=1, sticky="w")
        tk.Checkbutton(form, text="Include Framebuffer", bg=COLORS["bg_panel"], fg="white", selectcolor="#444").grid(row=4, column=1, sticky="w")
        
        # Generate
        tk.Button(parent, text="🚀 GENERATE PROJECT", bg=COLORS["accent_success"], fg="white", font=FONTS["heading"], relief="flat", padx=20, pady=10).pack(pady=30)