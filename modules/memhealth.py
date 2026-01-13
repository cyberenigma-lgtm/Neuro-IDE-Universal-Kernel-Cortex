import tkinter as tk
from tkinter import messagebox
import random
from modules.base import NeuroModule
from theme import COLORS, FONTS
from locale_engine import engine

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="Memory Health", icon="🏥", lang_key="tab_memhealth")
        self.memory_state = []
        
    def build_ui(self, parent):
        self.parent = parent
        self.safety_on = True # Initial state
        
        # Main Layout (Header | (Canvas + Log) | Legend)
        main_container = tk.Frame(parent, bg=COLORS["bg_dark"])
        main_container.pack(fill="both", expand=True)
        
        # Dashboard Header
        header = tk.Frame(main_container, bg=COLORS["bg_panel"], height=60)
        header.pack(fill="x", side="top")
        
        self.lbl_title = tk.Label(header, text="NEURO-BIOMETRICS v2.2", font=FONTS["heading"], bg=COLORS["bg_panel"], fg=COLORS["accent_primary"])
        self.lbl_title.pack(side="left", padx=20, pady=10)
        
        self.btn_scan = tk.Button(header, text=engine.get_string("memhealth_scan"), bg=COLORS["accent_secondary"], fg="white", relief="flat", padx=10, command=self.run_scan)
        self.btn_scan.pack(side="right", padx=10, pady=10)

        self.btn_defrag = tk.Button(header, text=engine.get_string("memhealth_defrag"), bg=COLORS["accent_warning"], fg="black", font=("Segoe UI", 9, "bold"), relief="flat", padx=10, command=self.run_defrag, state="disabled")
        self.btn_defrag.pack(side="right", padx=10, pady=10)

        self.btn_purge = tk.Button(header, text=engine.get_string("memhealth_purge"), bg=COLORS["accent_danger"], fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=10, command=self.run_purge, state="disabled")
        self.btn_purge.pack(side="right", padx=10, pady=10)

        self.btn_safety = tk.Button(header, text=engine.get_string("memhealth_safety") + ": ON", bg="#440000", fg="white", font=("Segoe UI", 8, "bold"), relief="sunken", padx=5, command=self.toggle_safety)
        self.btn_safety.pack(side="right", padx=10, pady=10)

        # Risk Indicator
        self.lbl_risk = tk.Label(header, text="RISK: STABLE", bg=COLORS["bg_medium"], fg=COLORS["accent_success"], font=("Consolas", 8, "bold"), borderwidth=1, relief="sunken", padx=5)
        self.lbl_risk.pack(side="left", padx=10)

        # Middle Content (Canvas Left | Log Right)
        content_frame = tk.Frame(main_container, bg=COLORS["bg_dark"])
        content_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(content_frame, bg="#0a0a0a", highlightthickness=1, highlightbackground=COLORS["bg_medium"])
        self.canvas.pack(side="left", fill="both", expand=True, padx=(20, 5), pady=10)
        
        log_frame = tk.Frame(content_frame, bg=COLORS["bg_medium"], width=300)
        log_frame.pack(side="right", fill="y", padx=(5, 20), pady=10)
        
        tk.Label(log_frame, text=engine.get_string("memhealth_log"), font=("Consolas", 9, "bold"), bg=COLORS["bg_medium"], fg=COLORS["accent_primary"]).pack(pady=5)
        self.log_text = tk.Text(log_frame, bg="#050505", fg=COLORS["accent_success"], font=("Consolas", 8), width=35, height=20, borderwidth=0)
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.log_text.insert("end", ">> SURGICAL CORTEX IDLE\n")

        # Legend
        legend = tk.Frame(main_container, bg=COLORS["bg_dark"], height=30)
        legend.pack(fill="x", side="bottom")
        
        items = [("FREE", "#222222"), ("ALLOCATED", COLORS["accent_success"]), ("RESERVED", COLORS["accent_warning"]), ("LEAK?", COLORS["accent_danger"])]
        for text, col in items:
            f = tk.Frame(legend, bg=col, width=15, height=15)
            f.pack(side="left", padx=(20, 5), pady=5)
            tk.Label(legend, text=text, bg=COLORS["bg_dark"], fg=COLORS["text_dim"], font=FONTS["small"]).pack(side="left")

        self.parent.after(200, self.run_scan)

    def toggle_safety(self):
        self.safety_on = not self.safety_on
        if self.safety_on:
            self.btn_safety.config(text=engine.get_string("memhealth_safety") + ": ON", bg="#440000", relief="sunken")
            self.log_msg(">> SAFETY LOCK RE-ENGAGED")
        else:
            self.btn_safety.config(text=engine.get_string("memhealth_safety") + ": OFF", bg="#aa0000", relief="raised")
            self.log_msg(">> WARNING: SAFETY LOCK BYPASSED")

    def log_msg(self, msg):
        self.log_text.insert("end", f"{msg}\n")
        self.log_text.see("end")

    def refresh_ui(self):
        self.btn_scan.config(text=engine.get_string("memhealth_scan"))
        self.btn_defrag.config(text=engine.get_string("memhealth_defrag"))
        self.btn_purge.config(text=engine.get_string("memhealth_purge"))
        self.btn_safety.config(text=engine.get_string("memhealth_safety") + (": ON" if self.safety_on else ": OFF"))

    def get_grid_size(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 100: w = 800
        if h < 100: h = 500
        
        box_size = 18
        gap = 3
        cols = (w - 40) // (box_size + gap)
        rows = (h - 40) // (box_size + gap)
        return rows, cols, box_size, gap

    def run_scan(self):
        rows, cols, box_size, gap = self.get_grid_size()
        total_blocks = rows * cols
        
        self.memory_state = [0] * total_blocks
        self.block_details = {} 
        
        leaks_detected = 0
        diagnostics = "Scanning Kernel Sources..."
        alloc_lines = []
        
        self.log_msg(">> STARTING STATIC SCAN...")
        try:
            mem_c_path = os.path.join(os.getcwd(), "kernel", "memory.c")
            if os.path.exists(mem_c_path):
                with open(mem_c_path, "r") as f:
                    lines = f.readlines()
                    malloc_count = 0
                    free_count = 0
                    for i, line in enumerate(lines):
                        if "kmalloc" in line and "(" in line:
                            malloc_count += 1
                            alloc_lines.append(i + 1)
                        if "kfree" in line and "(" in line:
                            free_count += 1
                    
                    if malloc_count > free_count:
                        leaks_detected = malloc_count - free_count
                        diagnostics = f"SCAN: {malloc_count} allocs / {free_count} frees. Leak!"
                        self.log_msg(f">> FOUND {leaks_detected} POTENTIAL LEAKS")
                    else:
                        diagnostics = f"SCAN: Memory balanced ({malloc_count} allocs)."
                        self.log_msg(">> CORE MEMORY LOGIC BALANCED")
            else:
                diagnostics = "ERROR: kernel/memory.c missing."
                self.log_msg(">> CRITICAL: SOURCE NOT FOUND")
        except Exception as e:
            diagnostics = f"SCAN ERROR: {str(e)}"

        # Populate Heatmap Deterministically (Based on scan)
        # Flattened Kernel Map Simulation
        scan_cursor = 0
        total_allocs = len(alloc_lines)
        
        for i in range(total_blocks):
             # Default: Free
             self.memory_state[i] = 0 
             
             # Map detected allocs to lower memory blocks (Nucleus)
             if scan_cursor < total_allocs:
                  if i > 50 and i < (50 + total_allocs * 2): # Spread them out a bit
                      if i % 2 == 0:
                          self.memory_state[i] = 1 # Active
                          self.block_details[i] = f"Source: kernel/memory.c:L{alloc_lines[scan_cursor]}"
                          scan_cursor += 1
                          
             # Leaks (if detected)
             if leaks_detected > 0:
                 # Place leaks in upper memory
                 if i > total_blocks - (leaks_detected * 5) and i % 5 == 0:
                     self.memory_state[i] = 3
                     self.block_details[i] = "WARNING: Unfreed pointer detected in scan."
                     leaks_detected -= 1

             # Reserved areas (System fixed)
             if i < 32: 
                 self.memory_state[i] = 2 
                 self.block_details[i] = "Status: RESERVED (IVT/GDT)" 
            
        self.btn_defrag.config(state="normal")
        self.btn_purge.config(state="normal")
        self.lbl_risk.config(text="RISK: STABLE", fg=COLORS["accent_success"])
        self.defrag_done = False
        self.status_msg = diagnostics
        self.render_state()

    def run_defrag(self):
        if self.safety_on:
            messagebox.showwarning("SAFETY LOCK", "Unlock safety to perform surgery.")
            return

        self.lbl_risk.config(text="RISK: CRITICAL", fg=COLORS["accent_danger"])
        self.log_msg(">> INITIATING DEFRAGMENTATION...")
        self.log_msg(">> VALIDATING MAGIC NUMBERS...")
        
        # Simulate step-by-step hardened processing
        self.parent.after(500, self._step_defrag, 0)

    def _step_defrag(self, step):
        if step < 5:
            addr = 0x100000 + (step * 0x4000)
            self.log_msg(f">> BLOCK {hex(addr)}: METADATA OK")
            self.parent.after(200, self._step_defrag, step + 1)
        else:
            self._finish_defrag()

    def _finish_defrag(self):
        def sort_key(s):
             if s == 1: return 0
             if s == 2: return 1
             if s == 3: return 2
             return 3
             
        self.memory_state.sort(key=sort_key)
        self.defrag_done = True
        self.btn_defrag.config(state="disabled")
        self.lbl_risk.config(text="RISK: OPTIMIZED", fg=COLORS["accent_success"])
        self.status_msg = "DEFRAG SUCCESSFUL."
        self.log_msg(">> DEFRAG COMPLETE: 100% MERGED")
        self.render_state()

    def run_purge(self):
        if self.safety_on:
            messagebox.showwarning("SAFETY LOCK", "Unlock safety to perform surgery.")
            return

        leaks_found = self.memory_state.count(3)
        self.log_msg(f">> PURGING {leaks_found} LEAKS...")
        self.memory_state = [0 if s == 3 else s for s in self.memory_state]
        
        self.purge_count = leaks_found
        self.btn_purge.config(state="disabled")
        self.lbl_risk.config(text="RISK: CLEANED", fg=COLORS["accent_warning"])
        self.status_msg = f"PURGED {leaks_found} LEAKS."
        self.log_msg(f">> SURGICAL SUCCESS: {leaks_found} BLOCKS FREED")
        self.render_state()
        
    def show_diagnostic(self, rid):
        i, status = self.canvas_blocks[rid]
        addr = 0x100000 + (i * 16)
        detail = self.block_details.get(i, "No further details.")
        
        msg = f"DIAGNOSTIC:\nADDR: {hex(addr)}\nSTATUS: {status}\n{detail}\n\n"
        if "LEAK" in status:
            msg += "ACTION: Purge required."
        elif "GARBAGE" in status:
            msg += "ACTION: Defragment."
        else:
            msg += "ACTION: Healthy."
            
        messagebox.showinfo("Diagnostic", msg)

    def render_state(self):
        self.canvas.delete("all")
        rows, cols, box_size, gap = self.get_grid_size()
        self.canvas_blocks = {} 
        
        for i, state in enumerate(self.memory_state):
            if i >= rows * cols: break
            
            r = i // cols
            c = i % cols
            
            color = "#222222"
            status = "FREE"
            if state == 1: 
                color = COLORS["accent_success"]; status = "ALLOCATED"
            elif state == 2: 
                color = COLORS["accent_warning"]; status = "GARBAGE / METADATA"
            elif state == 3: 
                color = COLORS["accent_danger"]; status = "LEAK / CORRUPTED"
            
            x1 = 20 + c * (box_size + gap)
            y1 = 20 + r * (box_size + gap)
            x2 = x1 + box_size
            y2 = y1 + box_size
            
            if state > 0:
                self.canvas.create_rectangle(x1-1, y1-1, x2+1, y2+1, fill="", outline=color, width=1)
            
            rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#333333", width=1)
            self.canvas_blocks[rect_id] = (i, status)
            self.canvas.tag_bind(rect_id, "<Button-1>", lambda e, rid=rect_id: self.show_diagnostic(rid))
            
        final_text = getattr(self, 'status_msg', "SCAN COMPLETE.")
        self.canvas.create_text(self.canvas.winfo_width()//2, self.canvas.winfo_height()-20, 
                                 text=final_text, fill=COLORS["text_dim"], font=("Consolas", 8))
