CC=i686-elf-gcc
AS=nasm
LD=i686-elf-gcc

all: my_kernel.bin

my_kernel.bin: boot.o kernel.o
	$(CC) -T linker.ld -o $@ -ffreestanding -O2 -nostdlib $^ -lgcc

boot.o: boot.asm
	$(AS) -felf32 $< -o $@

kernel.o: kernel.c
	$(CC) -c $< -o $@ -std=gnu99 -ffreestanding -O2 -Wall -Wextra

clean:
	rm -f *.o *.bin
