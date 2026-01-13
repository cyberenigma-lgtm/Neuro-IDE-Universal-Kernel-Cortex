#include <stdbool.h>
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
