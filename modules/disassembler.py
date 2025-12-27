import tkinter as tk
from tkinter import filedialog
import os
import struct
from modules.base import NeuroModule
from theme import COLORS, FONTS
from locale_engine import engine

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="Disassembler", icon="⚙️", lang_key="tab_disasm")
        self.current_file = None
        self.data = bytearray()
        
    def build_ui(self, parent):
        self.parent = parent
        
        # Dashboard Header
        header = tk.Frame(parent, bg=COLORS["bg_panel"], height=40)
        header.pack(fill="x", side="top")
        
        self.lbl_info = tk.Label(header, text="DISASSEMBLY STREAM IDLE", bg=COLORS["bg_panel"], fg=COLORS["accent_secondary"], font=FONTS["code"])
        self.lbl_info.pack(side="left", padx=20, pady=10)

        # Main View
        self.container = tk.Frame(parent, bg=COLORS["bg_dark"])
        self.container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.scrollbar = tk.Scrollbar(self.container, bg=COLORS["bg_medium"], activebackground=COLORS["accent_secondary"])
        self.scrollbar.pack(side="right", fill="y")
        
        self.asm_view = tk.Text(self.container, bg="#050505", fg=COLORS["text_secondary"], 
                                font=FONTS["code"], wrap="none", yscrollcommand=self.scrollbar.set,
                                borderwidth=0, padx=10, pady=10)
        self.asm_view.pack(fill="both", expand=True)
        self.scrollbar.config(command=self.asm_view.yview)
        
        # Tags for ASM (Neuro-IDE Skin)
        self.asm_view.tag_config("addr", foreground=COLORS["text_dim"])
        self.asm_view.tag_config("opcode", foreground=COLORS["accent_primary"])
        self.asm_view.tag_config("mnemonic", foreground=COLORS["accent_secondary"], font=("Cascadia Code", 9, "bold"))
        self.asm_view.tag_config("operands", foreground=COLORS["text_primary"])
        self.asm_view.tag_config("comment", foreground="#484F58")

    def on_file_loaded(self, data):
        """Called by core when a global file is loaded"""
        self.data = bytearray(data)
        self.lbl_info.config(text=f"STREAM SYNC: {len(self.data)} BYTES DISASSEMBLED", fg=COLORS["accent_secondary"])
        self.run_disasm()

    def refresh_ui(self):
        pass

    def load_file(self):
        """Legacy local load"""
        path = filedialog.askopenfilename()
        if not path: return
        with open(path, "rb") as f:
            self.on_file_loaded(f.read())

    def run_disasm(self):
        self.asm_view.delete("1.0", tk.END)
        self.asm_view.insert(tk.END, f"; DISASSEMBLY OF {os.path.basename(self.current_file)}\n", "comment")
        self.asm_view.insert(tk.END, f"; Base: 0x10000 (Neuro-OS Legacy)\n\n", "comment")
        
        # Basic x86_64 Decoder (Mock-Disdisassembler for v1.0 zero-dependency)
        # In a real app we'd use 'capstone' here.
        # For this prototype, we'll decode common kernel patterns.
        
        i = 0
        limit = min(len(self.data), 2048) # Limit rows for UI speed
        
        while i < limit:
            addr = 0x10000 + i
            b = self.data[i]
            
            mnemonic = "db"
            operands = f"0x{b:02X}"
            size = 1
            
            # Simple Pattern Matching (Common Kernel Opcodes)
            if b == 0xFA: mnemonic, size = "cli", 1
            elif b == 0xFB: mnemonic, size = "sti", 1
            elif b == 0xF4: mnemonic, size = "hlt", 1
            elif b == 0x90: mnemonic, size = "nop", 1
            elif b == 0x55: mnemonic, size = "push rbp", 1
            elif b == 0x48 and i+1 < len(self.data) and self.data[i+1] == 0x89:
                mnemonic, operands, size = "mov", "rbp, rsp", 3
            elif b == 0xE8: # CALL rel32
                if i+4 < len(self.data):
                    rel = struct.unpack("<i", self.data[i+1:i+5])[0]
                    mnemonic, operands, size = "call", f"0x{addr + 5 + rel:X}", 5
            elif b == 0xEB: # JMP rel8
                 if i+1 < len(self.data):
                    rel = struct.unpack("<b", self.data[i+1:i+2])[0]
                    mnemonic, operands, size = "jmp", f"0x{addr + 2 + rel:X}", 2
            elif b == 0x48 and i+2 < len(self.data) and self.data[i+1] == 0xB8: # MOV RAX, imm64
                 if i+9 < len(self.data):
                    imm = struct.unpack("<Q", self.data[i+2:i+10])[0]
                    mnemonic, operands, size = "movabs", f"rax, 0x{imm:X}", 10
            
            # Render line
            self.asm_view.insert(tk.END, f"{addr:08X}  ", "addr")
            
            op_hex = "".join([f"{self.data[i+j]:02X}" for j in range(size)])
            self.asm_view.insert(tk.END, f"{op_hex.ljust(20)} ", "opcode")
            
            self.asm_view.insert(tk.END, f"{mnemonic.ljust(8)} ", "mnemonic")
            self.asm_view.insert(tk.END, f"{operands}\n", "operands")
            
            i += size

        if i < len(self.data):
             self.asm_view.insert(tk.END, f"\n; ... Remaining {len(self.data) - i} bytes truncated ...\n", "comment")
