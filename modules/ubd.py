import tkinter as tk
from tkinter import filedialog
from modules.base import NeuroModule
from theme import COLORS, FONTS

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="Binary Diff", icon="🔍", lang_key="tab_ubd")
        self.file1_path = None
        self.file2_path = None
        
    def build_ui(self, parent):
        # Top: Controls
        ctrl = tk.Frame(parent, bg=COLORS["bg_medium"], height=50)
        ctrl.pack(fill="x", side="top")
        
        tk.Button(ctrl, text="Select Binary A", command=lambda: self.sel_file(1), bg=COLORS["accent_secondary"], fg="white", relief="flat").pack(side="left", padx=10, pady=10)
        self.lbl_f1 = tk.Label(ctrl, text="None", bg=COLORS["bg_medium"], fg=COLORS["text_dim"])
        self.lbl_f1.pack(side="left")
        
        tk.Label(ctrl, text=" vs ", bg=COLORS["bg_medium"], fg="white").pack(side="left", padx=10)
        
        tk.Button(ctrl, text="Select Binary B", command=lambda: self.sel_file(2), bg=COLORS["accent_secondary"], fg="white", relief="flat").pack(side="left", padx=10, pady=10)
        self.lbl_f2 = tk.Label(ctrl, text="None", bg=COLORS["bg_medium"], fg=COLORS["text_dim"])
        self.lbl_f2.pack(side="left")
        
        tk.Button(ctrl, text="RUN DIFF", command=self.run_diff, bg=COLORS["accent_success"], fg="white", relief="flat").pack(side="right", padx=10, pady=10)

        # Main: Diff View
        self.txt_diff = tk.Text(parent, bg=COLORS["bg_dark"], fg=COLORS["text_primary"], font=FONTS["mono"], borderwidth=0)
        self.txt_diff.pack(fill="both", expand=True, padx=10, pady=10)
        self.txt_diff.tag_config("match", foreground="#666666")
        self.txt_diff.tag_config("diff", foreground=COLORS["accent_danger"], background="#330000")
        
    def sel_file(self, num):
        path = filedialog.askopenfilename()
        if path:
            if num == 1:
                self.file1_path = path
                self.lbl_f1.config(text=path[-20:])
            else:
                self.file2_path = path
                self.lbl_f2.config(text=path[-20:])

    def run_diff(self):
        if not self.file1_path or not self.file2_path:
            self.txt_diff.insert(tk.END, "Please select two files.\n")
            return
            
        self.txt_diff.delete("1.0", tk.END)
        self.txt_diff.insert(tk.END, f"Comparing:\n A: {self.file1_path}\n B: {self.file2_path}\n\n")
        
        try:
            with open(self.file1_path, "rb") as f1, open(self.file2_path, "rb") as f2:
                d1 = f1.read(1024) # Limit to 1KB for prototype
                d2 = f2.read(1024)
                
                length = max(len(d1), len(d2))
                
                # Header
                self.txt_diff.insert(tk.END, "OFFSET | BINARY A | BINARY B | ASCII\n")
                self.txt_diff.insert(tk.END, "-"*60 + "\n")
                
                diffs = 0
                for i in range(0, length, 16):
                    chunk1 = d1[i:i+16]
                    chunk2 = d2[i:i+16]
                    
                    # Manual Hex Dump
                    hex1 = chunk1.hex(" ").upper()
                    hex2 = chunk2.hex(" ").upper()
                    
                    # Highlight diffs line by line logic is complex, 
                    # let's do a simple byte-by-byte visualizer
                    
                    line_hex = ""
                    for j in range(16):
                        b1 = chunk1[j] if j < len(chunk1) else None
                        b2 = chunk2[j] if j < len(chunk2) else None
                        
                        if b1 == b2:
                            line_hex += f"{b1:02X} " if b1 is not None else "   "
                        else:
                            line_hex += f"[{b1:02X}|{b2 if b2 else '??':02X}] "
                            diffs += 1
                            
                    self.txt_diff.insert(tk.END, f"{i:04X} | {line_hex}\n", "diff" if diffs > 0 else "match")
                    diffs = 0 # reset for next line color logic (simplified)
                    
        except Exception as e:
            self.txt_diff.insert(tk.END, f"Error: {e}")