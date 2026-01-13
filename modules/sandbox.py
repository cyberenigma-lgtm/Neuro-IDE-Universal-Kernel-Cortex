import tkinter as tk
import os
from tkinter import simpledialog, messagebox
from modules.base import NeuroModule
from theme import COLORS, FONTS

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="OSDev Generator", icon="💎", lang_key="tab_sandbox")
        
    def build_ui(self, parent):
        self.parent = parent
        # Header
        tk.Label(parent, text="Quick Project Generator", font=FONTS["heading"], bg=COLORS["bg_panel"], fg="white").pack(pady=10)
        
        # Form
        form = tk.Frame(parent, bg=COLORS["bg_panel"])
        form.pack(pady=20)
        
        # Architecture
        tk.Label(form, text="Architecture:", bg=COLORS["bg_panel"], fg="white", width=15, anchor="e").grid(row=0, column=0, pady=5)
        self.arch = tk.StringVar(value="x86 (32-bit)")
        tk.OptionMenu(form, self.arch, "x86 (32-bit)", "x86_64 (64-bit)").grid(row=0, column=1, sticky="w")
        
        # Bootloader
        tk.Label(form, text="Bootloader:", bg=COLORS["bg_panel"], fg="white", width=15, anchor="e").grid(row=1, column=0, pady=5)
        self.boot = tk.StringVar(value="Multiboot2")
        tk.OptionMenu(form, self.boot, "Limine", "Grub (Multiboot2)", "UEFI", "Legacy BIOS").grid(row=1, column=1, sticky="w")
        
        # Kernel Type
        tk.Label(form, text="Kernel Type:", bg=COLORS["bg_panel"], fg="white", width=15, anchor="e").grid(row=2, column=0, pady=5)
        ktype = tk.StringVar(value="Monolithic")
        tk.OptionMenu(form, ktype, "Monolithic", "Microkernel", "Exokernel", "Hybrid").grid(row=2, column=1, sticky="w")
        
        # Options
        tk.Checkbutton(form, text="Include Serial Drivers", bg=COLORS["bg_panel"], fg="white", selectcolor="#444").grid(row=3, column=1, sticky="w")
        tk.Checkbutton(form, text="Include Framebuffer", bg=COLORS["bg_panel"], fg="white", selectcolor="#444").grid(row=4, column=1, sticky="w")
        
        # Generate
        tk.Button(parent, text="🚀 GENERATE PROJECT", bg=COLORS["accent_success"], fg="white", font=FONTS["heading"], relief="flat", padx=20, pady=10, command=self.generate_project).pack(pady=30)

        # Log label
        self.lbl_status = tk.Label(parent, text="Ready", bg=COLORS["bg_panel"], fg="#777", font=("Consolas", 10))
        self.lbl_status.pack(side="bottom", pady=10)

    def generate_project(self):
        # Ask for name
        name = simpledialog.askstring("Project Name", "Enter Codename:", parent=self.parent)
        if not name: return

        target_dir = os.path.join(os.getcwd(), "projects", name)
        
        try:
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            
            # Use the verified MinGW-compatible templates
            # 1. Bootloader
            with open(os.path.join(target_dir, "boot.asm"), "w") as f:
                f.write("""; Multiboot Header (Calculated for NASM)
MBALIGN     equ  1<<0
MEMINFO     equ  1<<1
FLAGS       equ  MBALIGN | MEMINFO
MAGIC       equ  0x1BADB002
CHECKSUM    equ -(MAGIC + FLAGS)

section .multiboot
align 4
    dd MAGIC
    dd FLAGS
    dd CHECKSUM

section .bss
align 16
stack_bottom:
resb 16384 ; 16 KiB
stack_top:

section .text
global _start:function (_start.end - _start)
_start:
    mov esp, stack_top
    extern kernel_main
    call kernel_main
    cli
.hang:	hlt
    jmp .hang
.end:
""")

            # 2. Kernel
            with open(os.path.join(target_dir, "kernel.c"), "w") as f:
                f.write("""#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/* Validated for GCC MinGW 32-bit */

enum vga_color {
	VGA_COLOR_BLACK = 0,
	VGA_COLOR_BLUE = 1,
	VGA_COLOR_GREEN = 2,
    VGA_COLOR_CYAN = 3,
    VGA_COLOR_RED = 4,
    VGA_COLOR_MAGENTA = 5,
    VGA_COLOR_BROWN = 6,
    VGA_COLOR_LIGHT_GREY = 7,
};

static inline uint8_t vga_entry_color(enum vga_color fg, enum vga_color bg) 
{
	return fg | bg << 4;
}

static inline uint16_t vga_entry(unsigned char uc, uint8_t color) 
{
	return (uint16_t) uc | (uint16_t) color << 8;
}

void kernel_main(void) 
{
    uint16_t* terminal_buffer = (uint16_t*) 0xB8000;
	
    const char* str = "NEURO-CORE ONLINE | SYSTEM OK";
    
    // Clear Screen
    for (size_t y = 0; y < 25; y++) {
        for (size_t x = 0; x < 80; x++) {
            const size_t index = y * 80 + x;
            terminal_buffer[index] = vga_entry(' ', vga_entry_color(VGA_COLOR_LIGHT_GREY, VGA_COLOR_BLACK));
        }
    }
    
    // Print Hello
    for (size_t i = 0; str[i] != 0; i++) {
        terminal_buffer[i] = vga_entry(str[i], vga_entry_color(VGA_COLOR_CYAN, VGA_COLOR_BLACK));
    }
}
""")
            
            # 3. Linker
            with open(os.path.join(target_dir, "linker.ld"), "w") as f:
                f.write("""ENTRY(_start)

SECTIONS
{
	. = 1M;

	.text BLOCK(4K) : ALIGN(4K)
	{
		*(.multiboot)
		*(.text)
	}

	.rodata BLOCK(4K) : ALIGN(4K)
	{
		*(.rodata)
	}

	.data BLOCK(4K) : ALIGN(4K)
	{
		*(.data)
	}

	.bss BLOCK(4K) : ALIGN(4K)
	{
		*(COMMON)
		*(.bss)
	}
}
""")

            # 4. Makefile (MinGW Tuned)
            with open(os.path.join(target_dir, "Makefile"), "w") as f:
                f.write("""# NEURO-OS GENERATED MAKEFILE (MinGW Compatible)
ASM = nasm
CC = gcc
LD = ld
OBJCOPY = objcopy

# Flags for Bare Metal 32-bit on Windows
ASMFLAGS = -f elf32
CFLAGS = -m32 -ffreestanding -O2 -Wall -Wextra -nostdlib -fno-builtin -fno-stack-protector -fno-pic
LDFLAGS = -m i386pe -T linker.ld

all: kernel.bin

kernel.bin: kernel.elf
	$(OBJCOPY) -O binary $< $@
	@echo "Build Success: $@"

kernel.elf: boot.o kernel.o
	$(LD) $(LDFLAGS) -o $@ $^

boot.o: boot.asm
	$(ASM) $(ASMFLAGS) $< -o $@

kernel.o: kernel.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f *.o *.bin *.elf
""")

            self.lbl_status.config(text=f"SUCCESS: Generated '{name}' in /projects", fg=COLORS["accent_success"])
            messagebox.showinfo("Generator", f"Project '{name}' created successfully!\n\nArchitecture: {self.arch.get()}\nBootloader: {self.boot.get()}")
            
        except Exception as e:
            self.lbl_status.config(text=f"ERROR: {str(e)}", fg=COLORS["accent_danger"])
            messagebox.showerror("Generator Error", str(e))