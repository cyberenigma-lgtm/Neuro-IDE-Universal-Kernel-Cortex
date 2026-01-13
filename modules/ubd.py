import tkinter as tk
from tkinter import filedialog
from modules.base import NeuroModule
from theme import COLORS, FONTS
from locale_engine import engine

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="Universal Binary Diff", icon="⚖️", lang_key="tab_ubd")
        self.file1_data = None
        self.file2_data = None
        
    def build_ui(self, parent):
        self.parent = parent
        
    def build_ui(self, parent):
        self.parent = parent
        
        # Dashboard Header
        header = tk.Frame(parent, bg=COLORS["bg_panel"], height=50)
        header.pack(fill="x", side="top")
        
        tk.Button(header, text="📂 LOAD BINARY A", bg=COLORS["accent_secondary"], fg="white", relief="flat", font=FONTS["small"], command=lambda: self.load_file(1)).pack(side="left", padx=10, pady=10)
        self.lbl_f1 = tk.Label(header, text="EMPTY SLOT", bg=COLORS["bg_panel"], fg=COLORS["text_dim"], font=FONTS["code"])
        self.lbl_f1.pack(side="left", padx=5)
        
        tk.Label(header, text=" VS ", bg=COLORS["bg_panel"], fg=COLORS["accent_primary"], font=FONTS["subheading"]).pack(side="left", padx=10)
        
        tk.Button(header, text="📂 LOAD BINARY B", bg=COLORS["accent_secondary"], fg="white", relief="flat", font=FONTS["small"], command=lambda: self.load_file(2)).pack(side="left", padx=10, pady=10)
        self.lbl_f2 = tk.Label(header, text="EMPTY SLOT", bg=COLORS["bg_panel"], fg=COLORS["text_dim"], font=FONTS["code"])
        self.lbl_f2.pack(side="left", padx=5)
        
        self.btn_diff = tk.Button(header, text="⚡ COMPARE BITWISE", bg=COLORS["accent_danger"], fg="white", relief="flat", font=FONTS["small"], command=self.run_diff)
        self.btn_diff.pack(side="right", padx=20, pady=10)

        # Main Diff Layout (Side by Side)
        self.diff_container = tk.Frame(parent, bg=COLORS["bg_dark"])
        self.diff_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.common_scroll = tk.Scrollbar(self.diff_container, orient="vertical", command=self.sync_scroll, bg=COLORS["bg_medium"])
        self.common_scroll.pack(side="right", fill="y")
        
        # Hex view frames
        f1 = tk.Frame(self.diff_container, bg=COLORS["bg_panel"], highlightthickness=1, highlightbackground=COLORS["border"] if "border" in COLORS else "#30363D")
        f1.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        f2 = tk.Frame(self.diff_container, bg=COLORS["bg_panel"], highlightthickness=1, highlightbackground=COLORS["border"] if "border" in COLORS else "#30363D")
        f2.pack(side="left", fill="both", expand=True, padx=(5, 0))
        
        self.txt_a = tk.Text(f1, bg="#050505", fg=COLORS["text_secondary"], font=FONTS["code"], wrap="none", borderwidth=0, yscrollcommand=self.common_scroll.set, padx=10, pady=10)
        self.txt_a.pack(fill="both", expand=True)
        
        self.txt_b = tk.Text(f2, bg="#050505", fg=COLORS["text_secondary"], font=FONTS["code"], wrap="none", borderwidth=0, yscrollcommand=self.common_scroll.set, padx=10, pady=10)
        self.txt_b.pack(fill="both", expand=True)
        
        # Tags for diffs (Neuro-IDE Skin)
        for t in [self.txt_a, self.txt_b]:
            t.tag_config("diff", background="#4a0000", foreground=COLORS["accent_danger"])
            t.tag_config("offset", foreground=COLORS["accent_secondary"])

    def on_file_loaded(self, data):
        """Sync Binary A with the global file"""
        self.file1_data = data
        if hasattr(self, 'lbl_f1'):
            self.lbl_f1.config(text="GLOBAL SYNC ACTIVE", fg=COLORS["accent_primary"])
            if self.file2_data:
                self.run_diff()

    def refresh_ui(self):
        pass

    def sync_scroll(self, *args):
        self.txt_a.yview(*args)
        self.txt_b.yview(*args)

    def load_file(self, num):
        path = filedialog.askopenfilename(filetypes=[("Binary Files", "*.bin;*.img;*.dat"), ("All Files", "*.*")])
        if not path: return
        try:
            with open(path, "rb") as f:
                data = f.read()
            if num == 1:
                self.file1_data = data
                self.lbl_f1.config(text=path[-15:])
            else:
                self.file2_data = data
                self.lbl_f2.config(text=path[-15:])
        except Exception as e:
            print(f"Error loading side {num}: {e}")

    def run_diff(self):
        if self.file1_data is None or self.file2_data is None: return
        
        self.txt_a.delete("1.0", tk.END)
        self.txt_b.delete("1.0", tk.END)
        
        length = min(len(self.file1_data), len(self.file2_data), 1024) # Limit for proto
        
        for i in range(0, length, 8):
            chunk1 = self.file1_data[i:i+8]
            chunk2 = self.file2_data[i:i+8]
            
            offset_str = f"{i:04X} | "
            self.txt_a.insert(tk.END, offset_str, "offset")
            self.txt_b.insert(tk.END, offset_str, "offset")
            
            for j in range(8):
                b1 = chunk1[j] if j < len(chunk1) else None
                b2 = chunk2[j] if j < len(chunk2) else None
                
                tag = "diff" if b1 != b2 else ""
                
                self.txt_a.insert(tk.END, f"{b1:02X} " if b1 is not None else "   ", tag)
                self.txt_b.insert(tk.END, f"{b2:02X} " if b2 is not None else "   ", tag)
                
            self.txt_a.insert(tk.END, "\n")
            self.txt_b.insert(tk.END, "\n")

        self.txt_a.insert(tk.END, f"\n... [END OF SCAN] ...", "offset")
        self.txt_b.insert(tk.END, f"\n... [END OF SCAN] ...", "offset")