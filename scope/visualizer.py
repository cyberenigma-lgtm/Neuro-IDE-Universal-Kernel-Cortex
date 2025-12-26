"""
Neuro-Scope: Timeline Canvas
Visualizes events on a scrolling timeline.
"""

import tkinter as tk
from theme import COLORS, FONTS

class TimelineCanvas(tk.Frame):
    def __init__(self, parent, events=None, on_event_click=None):
        super().__init__(parent, bg=COLORS["bg_dark"])
        self.events = events if events else []
        self.on_event_click = on_event_click
        
        self.zoom_level = 100 # Pixels per second
        self.offset_x = 20
        self.height = 250
        
        # Canvas
        self.canvas = tk.Canvas(self, bg=COLORS["tl_track_bg"], height=self.height, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Scrollbar
        self.h_scroll = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.h_scroll.pack(fill="x", side="bottom")
        self.canvas.configure(xscrollcommand=self.h_scroll.set)
        
        self.bind_events()
        self.redraw()
        
    def bind_events(self):
        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<MouseWheel>", self.on_wheel) # Windows
        self.canvas.bind("<Button-4>", self.on_wheel)   # Linux
        self.canvas.bind("<Button-5>", self.on_wheel)   # Linux

    def set_zoom(self, level):
        self.zoom_level = float(level)
        self.redraw()

    def on_click(self, event):
        self.canvas.scan_mark(event.x, event.y)
        # Hit detection
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Simple hit test (check items closest)
        item = self.canvas.find_closest(canvas_x, canvas_y)
        tags = self.canvas.gettags(item)
        for tag in tags:
            if tag.startswith("evt_"):
                idx = int(tag.split("_")[1])
                if 0 <= idx < len(self.events):
                    if self.on_event_click:
                        self.on_event_click(self.events[idx])
                    
                    # Highlight selection
                    self.canvas.delete("highlight")
                    x = self.offset_x + (self.events[idx]["time"] * self.zoom_level)
                    self.canvas.create_oval(x-15, 85, x+15, 115, outline=COLORS["tl_cursor"], width=2, tags="highlight")
                    return

    def on_drag(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        
    def on_wheel(self, event):
        self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        
    def load_events(self, events):
        self.events = events
        self.redraw()
        
    def redraw(self):
        self.canvas.delete("all")
        if not self.events:
            return

        y_center = 100
        max_time = self.events[-1]["time"] + 0.5
        
        # 1. Background Grid & Time Labels
        # Adaptive grid step based on zoom
        step = 0.1
        if self.zoom_level < 50: step = 1.0 # coarse grid for zoomed out
        elif self.zoom_level > 200: step = 0.05 # fine grid for zoomed in
        
        for t in range(int(max_time / step) + 1):
            sec = t * step
            x = self.offset_x + (sec * self.zoom_level)
            
            # Line
            self.canvas.create_line(x, 20, x, 220, fill="#2a2a2a", dash=(1, 4))
            # Text
            self.canvas.create_text(x, 230, text=f"{sec:.2f}s", fill=COLORS["text_dim"], font=FONTS["small"])

        # 2. Draw Events
        for i, ev in enumerate(self.events):
            x = self.offset_x + (ev["time"] * self.zoom_level)
            tag = f"evt_{i}"
            
            if ev["type"] == "marker":
                color = COLORS["tl_event_diamond"]
                if ev["level"] == "error": color = COLORS["accent_danger"]
                elif ev["level"] == "critical": color = COLORS["accent_danger"]
                elif ev["level"] == "warning": color = COLORS["accent_warning"]
                
                # Diamond
                sz = 8
                self.canvas.create_polygon(
                    x, y_center - sz,
                    x + sz, y_center,
                    x, y_center + sz,
                    x - sz, y_center,
                    fill=color, outline="black", tags=tag
                )
                
                # Label (Clean)
                self.canvas.create_text(x, y_center - 20, text=ev["content"], fill=COLORS["text_primary"], font=FONTS["heading"], tags=tag)
                
            elif ev["type"] == "log":
                color = COLORS["tl_log_bar"]
                if ev["level"] == "error": color = COLORS["accent_danger"]
                elif ev["level"] == "warning": color = COLORS["accent_warning"]
                elif ev["level"] == "critical": color = "#ff00ff" # Panic purple
                
                # Bar
                h = 20
                if "PANIC" in ev["content"]: h = 40
                
                self.canvas.create_rectangle(x, y_center + 30, x + 4, y_center + 30 + h, fill=color, outline="", tags=tag)
                
                # Text visibility depends on zoom
                if self.zoom_level > 50:
                    text_content = ev["content"]
                    if len(text_content) > 30: text_content = text_content[:27] + "..."
                    self.canvas.create_text(x, y_center + 35 + h, text=text_content, fill=COLORS["text_dim"], font=FONTS["small"], anchor="nw", angle=45, tags=tag)

        # Update Scroll Region
        total_width = self.offset_x + (max_time * self.zoom_level) + 100
        self.canvas.configure(scrollregion=(0, 0, total_width, self.height))
