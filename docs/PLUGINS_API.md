# 🔌 Neuro-IDE Plugin API

Neuro-IDE v0.2 is built on a high-modularity architecture. Every tool you see is a **Lobe** (plugin) that interacts with the **Cortex** (core).

## Creating a New Module

All plugins must be placed in the `modules/` directory and inherit from the `NeuroModule` base class found in `base.py`.

### 1. The Structure
Create a new file (e.g., `my_tool.py`) with the following structure:

```python
import tkinter as tk
from modules.base import NeuroModule
from theme import COLORS, FONTS

class Plugin(NeuroModule):
    def __init__(self):
        # icon: Use an emoji or character
        super().__init__(name="My Tool", icon="🛠️")
        
    def build_ui(self, parent):
        """
        This is where you build your UI.
        'parent' is a tk.Frame already created for your tab.
        """
        label = tk.Label(parent, text="Hello OSDev World!", 
                         bg=COLORS["bg_panel"], fg=COLORS["text_primary"],
                         font=FONTS["heading"])
        label.pack(pady=20)
```

### 2. Available Resources
- **`theme.py`**: Use `COLORS` and `FONTS` to maintain the Cyberpunk aesthetic.
- **`NeuroModule`**: Provides helper methods for tab management.
- **Automatic Loading**: The IDE core scans the `modules/` folder and instantiates any class named `Plugin`.

## UI Best Practices
- **Backgrounds**: Always use `COLORS["bg_panel"]` or `COLORS["bg_dark"]`.
- **Accents**: Use `COLORS["accent_primary"]` (Cyan) for highlights.
- **Portability**: Avoid external libraries. Stick to `tkinter` and the Python Standard Library.
