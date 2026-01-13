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
        
        self.slider_zoom.set(100)
        self.slider_zoom.pack(side="left", padx=5)

        # Time Travel Slider
        self.lbl_replay = tk.Label(header, text="TIME TRAVEL", bg=COLORS["bg_panel"], fg=COLORS["accent_warning"], font=FONTS["small"])
        self.lbl_replay.pack(side="left", padx=10)
        
        self.slider_replay = tk.Scale(header, from_=0, to=100, orient="horizontal", bg=COLORS["bg_panel"], fg=COLORS["accent_warning"], highlightthickness=0, command=self.time_travel, length=200)
        self.slider_replay.set(100)
        self.slider_replay.pack(side="left", padx=5)


        # Local Load
        tk.Button(header, text="📂 OPEN LOG", bg=COLORS["accent_secondary"], fg="white", relief="flat", padx=10, command=self.load_log_manual).pack(side="right", padx=10, pady=10)

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

    def start_monitoring(self):
        """Start real-time monitoring of serial logs"""
        self.log_path = os.path.join(os.getcwd(), "serial.log")
        self.last_size = 0
        
        # Initial check
        if os.path.exists(self.log_path):
             self.read_log_update()
        else:
             # Create dummy if not exists so user sees something (or just wait)
             # For 100% functional, we wait. But to show it working, we might warn.
             self.txt_details.insert(tk.END, f"[WAITING FOR STREAM] {self.log_path} ...\n")

        # Poll every 1s
        self.parent.after(1000, self.poll_log)

    def poll_log(self):
        if os.path.exists(self.log_path):
            curr_size = os.path.getsize(self.log_path)
            if curr_size > self.last_size:
                self.read_log_update()
        else:
             # Try looking for other common names
             pass
        self.parent.after(1000, self.poll_log)

    def read_log_update(self):
        try:
            with open(self.log_path, "r", errors="ignore") as f:
                # Seek to last read position (simple tail)
                f.seek(self.last_size)
                new_data = f.read()
                self.last_size = f.tell()
                
                if new_data:
                    parser = SerialLogParser()
                    events = parser.parse(new_data)
                    self.scope_viz.load_events(events) # Append? TimelineCanvas needs append support or reload
                    # For v1, we reload full history if parser supports it, or just add new.
                    # TimelineCanvas.load_events clears list. We should check if we can extend.
                    # Assuming load_events replaces. Ideally we read WHOLE file each time for v1 stability.
                    
            # READ ALL for stability (small logs)
            with open(self.log_path, "r", errors="ignore") as f:
                 full_data = f.read()
                 parser = SerialLogParser()
                 events = parser.parse(full_data)
                 self.scope_viz.load_events(events)
                 if hasattr(self, 'lbl_info'):
                     self.lbl_info.config(text=f"LIVE STREAM: {len(events)} EVENTS", fg=COLORS["accent_success"])
        except Exception as e:
            print(f"Log Read Error: {e}")

    def load_log_manual(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename(filetypes=[("Log Files", "*.log;*.txt"), ("All Files", "*.*")])
        if not path: return
        
        try:
             with open(path, "r", errors="ignore") as f:
                 data = f.read()
                 parser = SerialLogParser()
                 events = parser.parse(data)
                 self.all_events = events # Store full history
                 self.scope_viz.load_events(events)
                 if hasattr(self, 'lbl_info'):
                     self.lbl_info.config(text=f"ARCHIVE LOADED: {os.path.basename(path)} ({len(events)} EVENTS)", fg=COLORS["accent_secondary"])
        except Exception as e:
             print(f"Manual Load Error: {e}")

    def time_travel(self, val):
        """Replay history based on slider percentage"""
        if not hasattr(self, 'all_events') or not self.all_events: return
        
        percent = int(val) / 100.0
        # If 100%, show all
        if percent >= 1.0:
            subset = self.all_events
            status = "LIVE"
        else:
            limit = int(len(self.all_events) * percent)
            if limit < 1: limit = 1
            subset = self.all_events[:limit]
            
            # Find time of last event
            last_time = subset[-1]['time'] if subset else 0
            status = f"T -{last_time:.2f}s"
            
        self.scope_viz.load_events(subset)
        if hasattr(self, 'lbl_replay'):
            self.lbl_replay.config(text=f"TIME TRAVEL [{status}]")
