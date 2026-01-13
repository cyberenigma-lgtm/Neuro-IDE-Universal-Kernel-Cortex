# NEURO-OS GENERATED MAKEFILE (MinGW Compatible)
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
