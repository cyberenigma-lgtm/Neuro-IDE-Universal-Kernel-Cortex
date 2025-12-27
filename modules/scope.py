import tkinter as tk
from modules.base import NeuroModule
from theme import COLORS, FONTS
from locale_engine import engine
from scope.visualizer import TimelineCanvas
from scope.parser import SerialLogParser

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="Neuro-Scope", icon="📡", lang_key="tab_scope")
        
    def build_ui(self, parent):
        self.parent = parent
        
        # Dashboard Header
        header = tk.Frame(parent, bg=COLORS["bg_panel"], height=40)
        header.pack(fill="x", side="top")
        
        self.lbl_info = tk.Label(header, text="TEMPORAL CHRONICLE STREAM", bg=COLORS["bg_panel"], fg=COLORS["accent_primary"], font=FONTS["code"])
        self.lbl_info.pack(side="left", padx=20, pady=10)
        
        self.lbl_scope_zoom = tk.Label(header, text="ZOOM", bg=COLORS["bg_panel"], fg=COLORS["text_secondary"], font=FONTS["small"])
        self.lbl_scope_zoom.pack(side="left", padx=10)
        
        self.slider_zoom = tk.Scale(header, from_=50, to=500, orient="horizontal", bg=COLORS["bg_panel"], fg=COLORS["accent_primary"], highlightthickness=0, command=self.update_zoom, length=200)
        self.slider_zoom.set(100)
        self.slider_zoom.pack(side="left", padx=5)

        # Split Container (Timeline + Details)
        self.split = tk.PanedWindow(parent, orient="vertical", bg=COLORS["bg_dark"], sashwidth=2, sashrelief="flat")
        self.split.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Visualizer
        self.scope_viz = TimelineCanvas(self.split, on_event_click=self.show_event_details)
        self.split.add(self.scope_viz, minsize=300)
        
        # Detail Panel
        detail_frame = tk.Frame(self.split, bg=COLORS["bg_medium"], highlightthickness=1, highlightbackground=COLORS["border"] if "border" in COLORS else "#30363D")
        self.split.add(detail_frame, minsize=150)
        
        self.lbl_scope_details = tk.Label(detail_frame, text="EVENT DIAGNOSTICS", font=FONTS["subheading"], bg=COLORS["bg_medium"], fg=COLORS["accent_secondary"])
        self.lbl_scope_details.pack(anchor="w", padx=20, pady=10)
        
        # Action Bar in Details
        det_toolbar = tk.Frame(detail_frame, bg=COLORS["bg_medium"])
        det_toolbar.pack(fill="x", padx=20)
        
        self.txt_details = tk.Text(detail_frame, bg="#050505", fg=COLORS["text_secondary"], font=FONTS["code"], height=8, borderwidth=0, padx=10, pady=10)
        self.txt_details.pack(fill="both", expand=True, padx=20, pady=10)
        self.txt_details.insert(tk.END, "SELECT A NEURAL EVENT FOR ANALYSIS...")

        self.load_demo_data()

    def on_file_loaded(self, data):
        """Scope can attempt to parse raw serial logs from a binary doc if present"""
        try:
            raw_text = data.decode('utf-8', errors='ignore')
            parser = SerialLogParser()
            events = parser.parse(raw_text)
            if events:
                self.scope_viz.load_events(events)
                self.lbl_info.config(text=f"CHRONICLE SYNC: {len(events)} EVENTS", fg=COLORS["accent_success"])
        except:
            pass

    def refresh_ui(self):
        # Update localizations if labels exist
        if hasattr(self, 'lbl_info'):
            self.lbl_info.config(text="TEMPORAL CHRONICLE STREAM")
        self.lbl_scope_zoom.config(text="ZOOM")
        self.lbl_scope_details.config(text="EVENT DIAGNOSTICS")

    def update_zoom(self, val):
        self.scope_viz.set_zoom(val)

    def show_event_details(self, ev):
        self.txt_details.delete("1.0", tk.END)
        self.txt_details.insert(tk.END, f"{engine.get_string('scope_time')}   {ev['time']:.4f}s\n")
        self.txt_details.insert(tk.END, f"{engine.get_string('scope_type')}   {ev['type'].upper()} ({ev['level']})\n")
        self.txt_details.insert(tk.END, f"{engine.get_string('scope_content')} {ev['content']}\n")
        if "description" in ev:
             self.txt_details.insert(tk.END, f"{engine.get_string('scope_desc')}    {ev['description']}\n")

    def load_demo_data(self):
        demo_log = """
[Initialization...]
Memory Map: Valid
{Physical Allocator Ready}
!IDT Loaded Successfully
?SSE Enabled
Searching for boot drive...
Found ATA Primary Master
[Loading Kernel...]
Kernel size: 64KB
Jump to higher half...
]PIC Masked...
!Interrupts Enabled
#EXCEPTION TEST (Recovered)
KERNEL PANIC AVOIDED.
System Ready.
"""
        parser = SerialLogParser()
        events = parser.parse(demo_log)
        self.scope_viz.load_events(events)
