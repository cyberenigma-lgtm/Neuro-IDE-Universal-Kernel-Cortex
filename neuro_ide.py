"""
NEURO-IDE: Mission Control Center
Main Entry Point
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Ensure we can import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from theme import COLORS, FONTS
from scope.parser import SerialLogParser
from scope.visualizer import TimelineCanvas
from locale_engine import engine

class NeuroIDE(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Neuro-IDE v0.2 (Mega-Integrated)")
        self.geometry("1400x900") # Bigger for mega tools
        self.configure(bg=COLORS["bg_dark"])
        
        # Determine paths
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.probe_script = os.path.join(self.base_dir, "..", "neuro-tools", "neuro-probe", "probe.py")
        self.kernel_image = os.path.join(self.base_dir, "..", "kernel", "build", "neuro-os.img")
        self.modules_dir = os.path.join(self.base_dir, "modules")
        
        self.plugins = [] # Track loaded plugins
        
        self.setup_style()
        self.create_layout()
        
        # Load Demo Data
        self.load_demo_data()
        
        # DYNAMIC MODULE LOADER
        self.load_modules()

        # Register for translations
        engine.register_callback(self.refresh_ui)
        self.refresh_ui()
        
    def setup_style(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        
        # Notebook (Tabs)
        style.configure("TNotebook", background=COLORS["bg_dark"], borderwidth=0)
        style.configure("TNotebook.Tab", background=COLORS["bg_medium"], foreground=COLORS["text_secondary"], padding=[12, 6], font=FONTS["main"])
        style.map("TNotebook.Tab", background=[("selected", COLORS["bg_panel"])], foreground=[("selected", COLORS["accent_primary"])])
        
        # Frames
        style.configure("TFrame", background=COLORS["bg_dark"])
        
    def create_layout(self):
        # Header
        # self.header = tk.Frame(self, bg=COLORS["bg_panel"], height=30)
        # self.header.pack(fill="x")
        
        # Status Bar
        self.status = tk.Label(self, text="Ready.", bg=COLORS["accent_primary"], fg="white", font=FONTS["small"], anchor="w", padx=5)
        self.status.pack(side="bottom", fill="x")
        
        # Main Tabs
        # Use scrolled notebook if too many tabs? For now standard.
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # -- CORE TABS --
        self.tab_dashboard = tk.Frame(self.notebook, bg=COLORS["bg_panel"])
        self.notebook.add(self.tab_dashboard, text=" Cortex ")
        self.build_dashboard()
        
        self.tab_probe = tk.Frame(self.notebook, bg=COLORS["bg_panel"])
        self.notebook.add(self.tab_probe, text=" Neuro-Probe ")
        self.build_probe_ui()

        self.tab_scope = tk.Frame(self.notebook, bg=COLORS["bg_panel"])
        self.notebook.add(self.tab_scope, text=" Neuro-Scope ")
        self.build_scope()
        
    def load_modules(self):
        """Dynamically load plugins from modules/ directory"""
        if not os.path.exists(self.modules_dir):
            return

        import importlib.util
        
        # List .py files
        modules = [f for f in os.listdir(self.modules_dir) if f.endswith(".py") and f != "base.py" and f != "__init__.py"]
        
        loaded_count = 0
        for mod_file in modules:
            try:
                mod_name = mod_file[:-3]
                path = os.path.join(self.modules_dir, mod_file)
                
                spec = importlib.util.spec_from_file_location(f"modules.{mod_name}", path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[f"modules.{mod_name}"] = module
                spec.loader.exec_module(module)
                
                # Look for Plugin class
                if hasattr(module, "Plugin"):
                    plugin_instance = module.Plugin()
                    
                    # Create Tab
                    tab_frame = tk.Frame(self.notebook, bg=COLORS["bg_panel"])
                    self.notebook.add(tab_frame, text=plugin_instance.get_tab_name())
                    
                    # Build UI
                    plugin_instance.build_ui(tab_frame)
                    self.plugins.append((plugin_instance, tab_frame))
                    loaded_count += 1
            except Exception as e:
                print(f"Failed to load module {mod_file}: {e}")
                
        self.status.config(text=f"Loaded {loaded_count} external modules.")

    def build_dashboard(self):
        self.lbl_dash_title = tk.Label(self.tab_dashboard, text=engine.get_string("dash_title"), font=FONTS["heading"], bg=COLORS["bg_panel"], fg=COLORS["text_primary"])
        self.lbl_dash_title.pack(pady=20)
        
        self.lbl_dash_info = tk.Label(self.tab_dashboard, text=engine.get_string("dash_info"), font=FONTS["mono"], bg=COLORS["bg_panel"], fg=COLORS["text_secondary"])
        self.lbl_dash_info.pack()

        # Quick Actions
        btn_frame = tk.Frame(self.tab_dashboard, bg=COLORS["bg_panel"])
        btn_frame.pack(pady=20)

        self.btn_dash_probe = tk.Button(btn_frame, text=engine.get_string("dash_btn_health"), bg=COLORS["accent_secondary"], fg="white", font=FONTS["main"], relief="flat", padx=15, pady=5, command=lambda: self.notebook.select(self.tab_probe))
        self.btn_dash_probe.pack(side="left", padx=10)
        
    def build_probe_ui(self):
        # Header
        header = tk.Frame(self.tab_probe, bg=COLORS["bg_medium"], height=40)
        header.pack(fill="x", side="top")
        
        self.lbl_probe_header = tk.Label(header, text=engine.get_string("probe_header"), bg=COLORS["bg_medium"], fg="white", font=FONTS["heading"])
        self.lbl_probe_header.pack(side="left", padx=10, pady=5)
        
        self.btn_run_probe = tk.Button(header, text=engine.get_string("probe_btn_run"), bg=COLORS["accent_success"], fg="white", relief="flat", padx=10, command=self.run_probe_analysis)
        self.btn_run_probe.pack(side="right", padx=10, pady=5)
        
        # Output Area
        self.probe_output = tk.Text(self.tab_probe, bg="#1e1e1e", fg="#cccccc", font=FONTS["mono"], borderwidth=0)
        self.probe_output.pack(fill="both", expand=True, padx=10, pady=10)
        
    def build_scope(self):
        # Controls
        ctrl_frame = tk.Frame(self.tab_scope, bg=COLORS["bg_medium"], height=40)
        ctrl_frame.pack(fill="x", side="top")
        
        self.btn_scope_reload = tk.Button(ctrl_frame, text=engine.get_string("scope_reload_demo"), bg=COLORS["accent_secondary"], fg="white", relief="flat", padx=10, command=self.load_demo_data)
        self.btn_scope_reload.pack(side="left", padx=5, pady=5)
        
        self.lbl_scope_zoom = tk.Label(ctrl_frame, text=engine.get_string("scope_zoom"), bg=COLORS["bg_medium"], fg="white")
        self.lbl_scope_zoom.pack(side="left", padx=10)
        
        self.slider_zoom = tk.Scale(ctrl_frame, from_=50, to=500, orient="horizontal", bg=COLORS["bg_medium"], fg="white", highlightthickness=0, command=self.update_zoom)
        self.slider_zoom.set(100)
        self.slider_zoom.pack(side="left", fill="x", expand=True, padx=5)

        # Split Container (Timeline + Details)
        split = tk.PanedWindow(self.tab_scope, orient="vertical", bg=COLORS["bg_dark"], sashwidth=4, sashrelief="flat")
        split.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Visualizer
        self.scope_viz = TimelineCanvas(split, on_event_click=self.show_event_details)
        split.add(self.scope_viz, minsize=300)
        
        # Detail Panel
        detail_frame = tk.Frame(split, bg=COLORS["bg_panel"])
        split.add(detail_frame, minsize=150)
        
        self.lbl_scope_details = tk.Label(detail_frame, text=engine.get_string("scope_event_details"), font=FONTS["heading"], bg=COLORS["bg_panel"], fg=COLORS["text_primary"])
        self.lbl_scope_details.pack(anchor="w", padx=10, pady=5)
        
        self.txt_details = tk.Text(detail_frame, bg=COLORS["bg_dark"], fg=COLORS["text_secondary"], font=FONTS["mono"], height=8, borderwidth=0)
        self.txt_details.pack(fill="both", expand=True, padx=10, pady=5)
        self.txt_details.insert(tk.END, engine.get_string("scope_select_event"))

    def update_zoom(self, val):
        self.scope_viz.set_zoom(val)

    def show_event_details(self, ev):
        self.txt_details.delete("1.0", tk.END)
        self.txt_details.insert(tk.END, f"{engine.get_string('scope_time')}   {ev['time']:.4f}s\n")
        self.txt_details.insert(tk.END, f"{engine.get_string('scope_type')}   {ev['type'].upper()} ({ev['level']})\n")
        self.txt_details.insert(tk.END, f"{engine.get_string('scope_content')} {ev['content']}\n")
        if "description" in ev:
             self.txt_details.insert(tk.END, f"{engine.get_string('scope_desc')}    {ev['description']}\n")


    def run_probe_analysis(self):
        """Execute output logs subprocess for Probe"""
        import subprocess
        import threading
        import json
        
        self.probe_output.delete("1.0", tk.END)
        self.probe_output.insert(tk.END, f"{engine.get_string('probe_launching')}\n")
        self.probe_output.insert(tk.END, f"{engine.get_string('probe_target').format(self.kernel_image)}\n")
        
        def run():
            self.btn_run_probe.config(state="disabled")
            self.status.config(text=engine.get_string("probe_running"))
            
            # Temporary JSON output file
            json_out = "probe_result.json"
            if os.path.exists(json_out):
                os.remove(json_out)
                
            cmd = ["python", self.probe_script, "--image", self.kernel_image, "--timeout", "5", "--output", json_out]
            
            try:
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=os.path.dirname(self.probe_script))
                
                # Stream output
                for line in process.stdout:
                    self.probe_output.insert(tk.END, line)
                    self.probe_output.see(tk.END)
                
                process.wait()
                
                if process.returncode == 0:
                    self.probe_output.insert(tk.END, engine.get_string("probe_success"))
                    self.status.config(text=engine.get_string("probe_complete"))
                    
                    # LOAD INTO SCOPE
                    if os.path.exists(json_out):
                        with open(json_out, 'r') as f:
                            data = json.load(f)
                            # Assume QEMU for timeline
                            if "qemu" in data and "serial_output" in data["qemu"]:
                                raw_log = data["qemu"]["serial_output"]
                                parser = SerialLogParser()
                                events = parser.parse(raw_log)
                                self.scope_viz.load_events(events)
                                self.notebook.select(self.tab_scope) # Switch to scope
                                self.status.config(text=engine.get_string("scope_imported").format(len(events)))
                else:
                    self.probe_output.insert(tk.END, engine.get_string("probe_error").format(process.returncode))
                    self.status.config(text=engine.get_string("probe_failed"))
                    
            except Exception as e:
                self.probe_output.insert(tk.END, f"\n>> Exception: {e}\n")
            
            finally:
                self.btn_run_probe.config(state="normal")
                
        threading.Thread(target=run, daemon=True).start()

    def load_demo_data(self):
        # Simulate a kernel boot log
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
        self.status.config(text=engine.get_string("status_ready"))

    def refresh_ui(self):
        """Global UI Update on Language Change"""
        self.title(engine.get_string("app_title"))
        self.status.config(text=engine.get_string("status_ready"))
        
        # Tabs
        self.notebook.tab(self.tab_dashboard, text=engine.get_string("tab_cortex"))
        self.notebook.tab(self.tab_probe, text=engine.get_string("tab_probe"))
        self.notebook.tab(self.tab_scope, text=engine.get_string("tab_scope"))
        
        # Plugins
        for plugin, frame in self.plugins:
            try:
                self.notebook.tab(frame, text=plugin.get_tab_name())
            except:
                pass

        # Dashboard
        self.lbl_dash_title.config(text=engine.get_string("dash_title"))
        self.lbl_dash_info.config(text=engine.get_string("dash_info"))
        self.btn_dash_probe.config(text=engine.get_string("dash_btn_health"))
        
        # Probe
        self.lbl_probe_header.config(text=engine.get_string("probe_header"))
        self.btn_run_probe.config(text=engine.get_string("probe_btn_run"))
        
        # Scope
        self.btn_scope_reload.config(text=engine.get_string("scope_reload_demo"))
        self.lbl_scope_zoom.config(text=engine.get_string("scope_zoom"))
        self.lbl_scope_details.config(text=engine.get_string("scope_event_details"))

if __name__ == "__main__":
    app = NeuroIDE()
    app.mainloop()
