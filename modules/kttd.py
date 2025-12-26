import tkinter as tk
import random
from modules.base import NeuroModule
from theme import COLORS, FONTS

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="Time-Travel Debugger", icon="⏳", lang_key="tab_kttd")
        
    def build_ui(self, parent):
        # Top: Controls
        ctrl = tk.Frame(parent, bg=COLORS["bg_medium"], height=60)
        ctrl.pack(fill="x", side="top")
        
        # Slider
        tk.Label(ctrl, text="Timeline:", bg=COLORS["bg_medium"], fg="white").pack(side="left", padx=10)
        self.slider = tk.Scale(ctrl, from_=0, to=1000, orient="horizontal", showvalue=0, bg=COLORS["bg_medium"], fg=COLORS["accent_primary"], command=self.update_state)
        self.slider.pack(side="left", fill="x", expand=True, padx=10)
        self.lbl_time = tk.Label(ctrl, text="T: 0 ticks", bg=COLORS["bg_medium"], fg="white", width=15)
        self.lbl_time.pack(side="left", padx=10)
        
        # Main: Split View (Code | Registers)
        split = tk.PanedWindow(parent, orient="horizontal", bg=COLORS["bg_dark"], sashwidth=4, sashrelief="flat")
        split.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Code View
        self.txt_code = tk.Text(split, bg=COLORS["bg_dark"], fg="#aaaaaa", font=FONTS["mono"], height=20, borderwidth=0)
        split.add(self.txt_code, minsize=400)
        self.load_mock_asm()
        
        # Reg View
        self.frame_regs = tk.Frame(split, bg=COLORS["bg_panel"])
        split.add(self.frame_regs, minsize=200)
        
        tk.Label(self.frame_regs, text="CPU REGISTERS", font=FONTS["heading"], bg=COLORS["bg_panel"], fg="white").pack(padx=10, pady=10)
        
        self.regs = {}
        for r in ["RAX", "RBX", "RCX", "RDX", "RSI", "RDI", "RSP", "RBP", "RIP"]:
            f = tk.Frame(self.frame_regs, bg=COLORS["bg_panel"])
            f.pack(fill="x", padx=10, pady=2)
            tk.Label(f, text=r, width=5, bg=COLORS["bg_panel"], fg=COLORS["accent_secondary"], anchor="w").pack(side="left")
            val = tk.Label(f, text="0x0000000000000000", font=FONTS["mono"], bg=COLORS["bg_panel"], fg="white", anchor="e")
            val.pack(side="right")
            self.regs[r] = val
            
    def load_mock_asm(self):
        asm = """
_start:
    xor rax, rax        ; 0
    mov rbx, 0x10       ; 1
loop_start:
    add rax, rbx        ; 2
    inc rcx             ; 3
    cmp rax, 0x100      ; 4
    jl loop_start       ; 5
    
    mov rdi, rax        ; 6
    call print_hex      ; 7
    hlt                 ; 8
"""
        self.txt_code.insert(tk.END, asm.strip())
        
    def update_state(self, val):
        t = int(val)
        self.lbl_time.config(text=f"T: -{1000-t} ticks")
        
        # Mock Register Changes based on slider
        # Deterministic simulation for demo
        val_rax = (t * 16) % 0xFFFFFF
        val_rbx = 0x10
        val_rcx = t
        val_rip = 0x400000 + (t % 8) * 4
        
        self.regs["RAX"].config(text=f"0x{val_rax:016X}")
        self.regs["RBX"].config(text=f"0x{val_rbx:016X}")
        self.regs["RCX"].config(text=f"0x{val_rcx:016X}")
        self.regs["RIP"].config(text=f"0x{val_rip:016X}", fg=COLORS["accent_warning"])
        
        # Highlight line
        line = (t % 9) + 1
        self.txt_code.tag_remove("current", "1.0", tk.END)
        self.txt_code.tag_add("current", f"{line}.0", f"{line}.end")
        self.txt_code.tag_config("current", background=COLORS["bg_medium"], foreground="white")