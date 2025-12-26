import tkinter as tk
import re
from modules.base import NeuroModule
from theme import COLORS, FONTS
from locale_engine import engine

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="Neuro-Doctor", icon="🧨", lang_key="tab_doctor")
        
    def build_ui(self, parent):
        # Layout: Left (Input), Right (Diagnosis)
        split = tk.PanedWindow(parent, orient="horizontal", bg=COLORS["bg_dark"], sashwidth=4, sashrelief="flat")
        split.pack(fill="both", expand=True, padx=10, pady=10)
        
        # LEFT: Input
        frame_input = tk.Frame(split, bg=COLORS["bg_panel"])
        split.add(frame_input, minsize=400)
        
        tk.Label(frame_input, text="Paste Kernel Log / Panic Dump:", font=FONTS["heading"], bg=COLORS["bg_panel"], fg=COLORS["text_primary"]).pack(anchor="w", padx=10, pady=5)
        self.txt_input = tk.Text(frame_input, bg=COLORS["bg_dark"], fg=COLORS["text_secondary"], font=FONTS["mono"], borderwidth=0)
        self.txt_input.pack(fill="both", expand=True, padx=10, pady=5)
        
        btn_diagnose = tk.Button(frame_input, text="🚑 DIAGNOSE PANIC", bg=COLORS["accent_danger"], fg="white", font=FONTS["heading"], relief="flat", command=self.diagnose)
        btn_diagnose.pack(fill="x", padx=10, pady=10)

        # RIGHT: Diagnosis
        frame_output = tk.Frame(split, bg=COLORS["bg_panel"])
        split.add(frame_output, minsize=300)
        
        self.lbl_header = tk.Label(frame_output, text=engine.get_string("tab_doctor"), font=FONTS["heading"], bg=COLORS["bg_panel"], fg=COLORS["text_primary"])
        self.lbl_header.pack(anchor="w", padx=10, pady=5)
        
        self.txt_output = tk.Text(frame_output, bg=COLORS["bg_medium"], fg=COLORS["accent_warning"], font=FONTS["mono"], borderwidth=0, state="disabled")
        self.txt_output.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh_ui(self):
        self.lbl_header.config(text=engine.get_string("tab_doctor"))

    def diagnose(self):
        log = self.txt_input.get("1.0", tk.END)
        report = []
        confidence = 0
        
        # Heuristics
        if "Triple Fault" in log or "resetting cpu" in log.lower():
            report.append("CRITICAL: Triple Fault detected.")
            report.append(" - Cause: IDT not loaded or invalid GDT.")
            report.append(" - Fix: Check 'lidt' instruction and GDT descriptors.")
            confidence += 90
            
        if "Page Fault" in log or "#PF" in log:
            report.append("ERROR: Page Fault (#PF).")
            report.append(" - Cause: Accessing unmapped memory or permissions violation.")
            report.append(" - Check: CR2 register for the faulting address.")
            confidence += 80

        if "General Protection Fault" in log or "#GP" in log:
            report.append("ERROR: General Protection Fault (#GP).")
            report.append(" - Cause: Privileged instruction in user mode or segment violation.")
            confidence += 75
            
        if "stack" in log.lower() and ("overflow" in log.lower() or "corruption" in log.lower()):
            report.append("WARNING: Stack Corruption suspect.")
            report.append(" - Cause: Infinite recursion or buffer overflow.")
            confidence += 60
            
        if not report:
            report.append("Status: No obvious panic signatures found.")
            report.append("Recommendation: Enable verbose serial logging.")
        else:
            report.insert(0, f"Confidence: {min(confidence, 100)}%\n")
            
        self.txt_output.config(state="normal")
        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, "\n".join(report))
        self.txt_output.config(state="disabled")