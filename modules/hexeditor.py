import tkinter as tk
from tkinter import filedialog
import os
from modules.base import NeuroModule
from theme import COLORS, FONTS
from locale_engine import engine

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="Hex Editor", icon="💾", lang_key="tab_hex")
        self.current_file = None
        self.data = bytearray()
        self.bytes_per_row = 16
        
    def build_ui(self, parent):
        self.parent = parent
        
        # Dashboard Header (Minimalist)
        header = tk.Frame(parent, bg=COLORS["bg_panel"], height=40)
        header.pack(fill="x", side="top")
        
        self.lbl_info = tk.Label(header, text="READY FOR DATA STREAM", bg=COLORS["bg_panel"], fg=COLORS["accent_primary"], font=FONTS["code"])
        self.lbl_info.pack(side="left", padx=20, pady=10)

        # Main View (Scrollable)
        self.container = tk.Frame(parent, bg=COLORS["bg_dark"])
        self.container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.scrollbar = tk.Scrollbar(self.container, bg=COLORS["bg_medium"], activebackground=COLORS["accent_primary"])
        self.scrollbar.pack(side="right", fill="y")
        
        self.hex_view = tk.Text(self.container, bg="#050505", fg=COLORS["text_secondary"], 
                                font=FONTS["code"], wrap="none", yscrollcommand=self.scrollbar.set,
                                borderwidth=0, padx=10, pady=10)
        self.hex_view.pack(fill="both", expand=True)
        self.scrollbar.config(command=self.hex_view.yview)
        
        # Tags for highlighting (Neuro-IDE Palette)
        self.hex_view.tag_config("offset", foreground=COLORS["accent_secondary"])
        self.hex_view.tag_config("binary", foreground=COLORS["text_primary"])
        self.hex_view.tag_config("ascii", foreground=COLORS["accent_warning"])
        self.hex_view.tag_config("header", foreground=COLORS["accent_primary"], font=("Cascadia Code", 9, "bold"))
        
        self.refresh_ui()

    def on_file_loaded(self, data):
        """Called by core when a global file is loaded"""
        self.data = bytearray(data)
        self.lbl_info.config(text=f"BUFFER SYNC: {len(self.data)} BYTES", fg=COLORS["accent_primary"])
        self.render_hex()

    def refresh_ui(self):
        pass

    def open_file(self):
        """Legacy local open - redirected to core soon"""
        path = filedialog.askopenfilename(title="Select Binary File")
        if not path: return
        with open(path, "rb") as f:
            self.on_file_loaded(f.read())

    def save_file(self):
        if not self.current_file: return
        try:
            # In a real surgical editor, we'd read back changes from the text widget
            # or have an interactive overlay. For v1.0, we'll implement the "Read-Only + View"
            # as a safety measure, then add "Surgical Edit" in the next patch.
            with open(self.current_file, "wb") as f:
                f.write(self.data)
            self.lbl_info.config(text=f"SAVED: {os.path.basename(self.current_file)}", fg=COLORS["accent_success"])
        except Exception as e:
             self.lbl_info.config(text=f"Save Error: {e}", fg=COLORS["accent_danger"])

    def render_hex(self):
        self.hex_view.delete("1.0", tk.END)
        
        # Header line
        header = "OFFSET   | 00 01 02 03 04 05 06 07  08 09 0A 0B 0C 0D 0E 0F | ASCII\n"
        self.hex_view.insert(tk.END, header, "header")
        self.hex_view.insert(tk.END, "-" * len(header) + "\n", "header")
        
        rows_to_render = min(len(self.data) // 16 + 1, 500) # Limit for UI performance in v1.0
        
        for row in range(rows_to_render):
            offset = row * 16
            chunk = self.data[offset:offset+16]
            if not chunk: break
            
            # Offset
            self.hex_view.insert(tk.END, f"{offset:08X} | ", "offset")
            
            # Hex values
            hex_part = ""
            for i, b in enumerate(chunk):
                hex_part += f"{b:02X} "
                if i == 7: hex_part += " " # Space in the middle
            
            self.hex_view.insert(tk.END, hex_part.ljust(49), "binary")
            self.hex_view.insert(tk.END, " | ", "header")
            
            # ASCII values
            ascii_part = ""
            for b in chunk:
                if 32 <= b <= 126:
                    ascii_part += chr(b)
                else:
                    ascii_part += "."
            
            self.hex_view.insert(tk.END, ascii_part + "\n", "ascii")

        if len(self.data) > (rows_to_render * 16):
            self.hex_view.insert(tk.END, f"\n... [{len(self.data) - rows_to_render*16} more bytes truncated for performance] ...", "header")
