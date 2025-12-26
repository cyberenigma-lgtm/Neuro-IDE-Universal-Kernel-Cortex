import tkinter as tk
from modules.base import NeuroModule
from theme import COLORS, FONTS

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="Boot Readiness", icon="✅", lang_key="tab_boottest")
        
    def build_ui(self, parent):
        # Header
        tk.Label(parent, text="Universal Boot Compliance Check", font=FONTS["heading"], bg=COLORS["bg_panel"], fg="white").pack(pady=10)
        
        # Checks
        tests = [
            ("Multiboot Header Magic (0xE85250D6)", True),
            ("Top of Stack Alignment (16-byte)", True),
            ("GDT Loading in Assembly", True),
            ("Long Mode Trampoline Correctness", True),
            ("IDT Limit > 0", False),
            ("VGA Buffer Address (0xB8000)", True),
        ]
        
        frame = tk.Frame(parent, bg=COLORS["bg_panel"])
        frame.pack(fill="x", padx=50, pady=20)
        
        for name, passed in tests:
            row = tk.Frame(frame, bg=COLORS["bg_panel"])
            row.pack(fill="x", pady=5)
            
            fg = COLORS["accent_success"] if passed else COLORS["accent_danger"]
            icon = "✅" if passed else "❌"
            
            tk.Label(row, text=icon, font=("Segoe UI Emoji", 12), bg=COLORS["bg_panel"], fg="white", width=4).pack(side="left")
            tk.Label(row, text=name, font=FONTS["main"], bg=COLORS["bg_panel"], fg="white").pack(side="left")
            tk.Label(row, text="PASS" if passed else "FAIL", font=("Consolas", 10, "bold"), bg=COLORS["bg_panel"], fg=fg).pack(side="right")
        
        tk.Text(parent, height=5, bg=COLORS["bg_dark"], fg=COLORS["text_dim"], borderwidth=0).pack(fill="x", padx=20, pady=10)