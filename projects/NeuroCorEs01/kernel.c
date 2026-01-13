#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/* Check if the compiler thinks you are targeting the wrong operating system. */
#if defined(__linux__)
#error "You are not using a cross-compiler, you will most likely run into trouble"
#endif

/* Hardware text mode color constants. */
enum vga_color {
	VGA_COLOR_BLACK = 0,
	VGA_COLOR_BLUE = 1,
	VGA_COLOR_GREEN = 2,
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
    // Minimal VGA Driver
    uint16_t* terminal_buffer = (uint16_t*) 0xB8000;
	
    const char* str = "NEURO-OS GENERATED KERNEL ONLINE!";
    
    for (size_t y = 0; y < 25; y++) {
    for (size_t x = 0; x < 80; x++) {
        const size_t index = y * 80 + x;
        terminal_buffer[index] = vga_entry(' ', vga_entry_color(VGA_COLOR_LIGHT_GREY, VGA_COLOR_BLACK));
    }
    }
    
    for (size_t i = 0; str[i] != 0; i++) {
        terminal_buffer[i] = vga_entry(str[i], vga_entry_color(VGA_COLOR_GREEN, VGA_COLOR_BLACK));
    }
}
