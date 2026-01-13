"""
NEURO-IDE: Mission Control Center
Main Entry Point (Surgical Gold v0.2.1)
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Ensure we can import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from theme import COLORS, FONTS
from locale_engine import engine

class NeuroIDE(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Neuro-IDE v0.2.3 (Surgical Suite)")
        self.geometry("1400x900")
        self.configure(bg=COLORS["bg_dark"])
        
        # Internal State
        self.current_file_path = None
        self.current_data = None
        
        # Paths
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.probe_script = os.path.join(self.base_dir, "..", "neuro-tools", "neuro-probe", "probe.py")
        self.kernel_image = os.path.join(self.base_dir, "..", "kernel", "build", "neuro-os.img")
        self.modules_dir = os.path.join(self.base_dir, "modules")
        
        self.plugins = [] 
        
        self.setup_style()
        self.setup_menu()
        self.create_layout()
        
        # Defer module loading until after UI is fully created
        self.after(100, self.load_modules)

        engine.register_callback(self.refresh_ui)
        self.after(200, self.refresh_ui)

    def setup_menu(self):
        self.menubar = tk.Menu(self, bg=COLORS["bg_medium"], fg=COLORS["text_primary"], activebackground=COLORS["accent_primary"])
        
        # FILE MENU
        file_menu = tk.Menu(self.menubar, tearoff=0, bg=COLORS["bg_medium"], fg=COLORS["text_primary"])
        file_menu.add_command(label="Open Document", command=self.action_open_file)
        file_menu.add_command(label="Save", command=self.action_save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=file_menu)
        
        # MODULES MENU
        self.modules_menu = tk.Menu(self.menubar, tearoff=0, bg=COLORS["bg_medium"], fg=COLORS["text_primary"])
        self.menubar.add_cascade(label="Modules", menu=self.modules_menu)
        
        # VIEW MENU
        view_menu = tk.Menu(self.menubar, tearoff=0, bg=COLORS["bg_medium"], fg=COLORS["text_primary"])
        view_menu.add_command(label="Dashboard Mode", command=lambda: self.show_dashboard(self.pane_primary))
        self.menubar.add_cascade(label="View", menu=view_menu)
        
        self.config(menu=self.menubar)

    def action_open_file(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename(filetypes=[
            ("Neuro-OS Images", "*.img;*.bin"),
            ("Source Code", "*.asm;*.c;*.py;*.h"),
            ("Logs", "*.log;*.txt"),
            ("All Files", "*.*")
        ])
        if path:
            self.current_file_path = path
            with open(path, "rb") as f:
                self.current_data = f.read()
            self.status.config(text=f"Loaded: {os.path.basename(path)}")
            self.notify_plugins_of_file()

    def action_save_file(self):
        if not self.current_file_path: return
        
        # Delegate save to all capable plugins
        saved_count = 0
        for plugin, frame in self.plugins:
            if hasattr(plugin, "save_file"):
                try:
                    plugin.save_file()
                    saved_count += 1
                except Exception as e:
                    print(f"Error saving plugin {plugin.name}: {e}")
                    
        if saved_count > 0:
            self.status.config(text=f"Saved: {os.path.basename(self.current_file_path)} ({saved_count} modules synced)")
        else:
            self.status.config(text="No active module handled the save operation.")

    def notify_plugins_of_file(self):
        """Sync all plugins with the newly loaded file"""
        for plugin, frame in self.plugins:
            # Inject filename if supported
            if hasattr(plugin, "set_file_path"):
                 plugin.set_file_path(self.current_file_path)
            # Or manually set it if the attribute exists
            elif hasattr(plugin, "current_file"):
                 plugin.current_file = self.current_file_path
                 
            if hasattr(plugin, "on_file_loaded"):
                plugin.on_file_loaded(self.current_data)
        
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
        # 🟢 ROOT (Mission Control)
        self.main_container = tk.Frame(self, bg=COLORS["bg_dark"])
        self.main_container.pack(fill="both", expand=True)

        # 1️⃣ LEFT SIDEBAR (The Activity Bar)
        self.sidebar = tk.Frame(self.main_container, bg=COLORS["sidebar_bg"], width=65)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Activity Logo
        self.lbl_logo = tk.Label(self.sidebar, text="💎", font=("Segoe UI Emoji", 22), bg=COLORS["sidebar_bg"], fg=COLORS["accent_primary"], pady=20)
        self.lbl_logo.pack()
        
        self.sidebar_scroll = tk.Frame(self.sidebar, bg=COLORS["sidebar_bg"])
        self.sidebar_scroll.pack(fill="both", expand=True)
        self.sidebar_btns = {}

        # 2️⃣ TOP MISSION STRIP (The HUD)
        self.hud = tk.Frame(self.main_container, bg=COLORS["bg_medium"], height=45)
        self.hud.pack(side="top", fill="x")
        
        self.hud_left = tk.Frame(self.hud, bg=COLORS["bg_medium"])
        self.hud_left.pack(side="left", fill="y", padx=20)
        
        self.lbl_mission = tk.Label(self.hud_left, text="MISSION: IDLE", font=FONTS["code"], bg=COLORS["bg_medium"], fg=COLORS["accent_primary"])
        self.lbl_mission.pack(side="left")
        
        self.hud_right = tk.Frame(self.hud, bg=COLORS["bg_medium"])
        self.hud_right.pack(side="right", fill="y", padx=20)
        
        self.lbl_target = tk.Label(self.hud_right, text="TARGET: UNSET", font=FONTS["code"], bg=COLORS["bg_medium"], fg=COLORS["text_secondary"])
        self.lbl_target.pack(side="right")
        
        # HUD Buttons
        self.btn_hud_dual = tk.Button(self.hud_right, text="🪟 DUAL", font=FONTS["small"], bg=COLORS["bg_medium"], fg=COLORS["text_dim"], relief="flat", padx=10, command=self.toggle_dual_view)
        self.btn_hud_dual.pack(side="right", padx=10)

        # 3️⃣ MAIN WORKSPACE (No Explorer)
        self.v_split = tk.PanedWindow(self.main_container, orient="horizontal", bg=COLORS["bg_dark"], sashwidth=2, sashrelief="flat")
        self.v_split.pack(fill="both", expand=True)

        # 4️⃣ HORIZONTAL SPLIT (Editor | Console)
        self.h_split = tk.PanedWindow(self.v_split, orient="vertical", bg=COLORS["bg_dark"], sashwidth=2, sashrelief="flat")
        self.v_split.add(self.h_split)

        # The Operating Table (Workspace)
        self.workspace = tk.PanedWindow(self.h_split, orient="horizontal", bg=COLORS["bg_dark"], sashwidth=2, sashrelief="flat")
        self.h_split.add(self.workspace, minsize=400)
        
        # Primary Pane
        self.pane_primary = tk.Frame(self.workspace, bg=COLORS["bg_dark"])
        self.workspace.add(self.pane_primary)
        
        # Secondary Pane
        self.pane_secondary = tk.Frame(self.workspace, bg=COLORS["bg_dark"])
        self.dual_view_active = False

        # 5️⃣ SURGICAL CONSOLE (Bottom Output)
        self.console_frame = tk.Frame(self.h_split, bg=COLORS["bg_panel"], height=200)
        self.h_split.add(self.console_frame, minsize=50)
        
        tk.Label(self.console_frame, text="SURGICAL LOG", font=FONTS["small"], bg=COLORS["bg_panel"], fg=COLORS["accent_primary"], padx=10).pack(anchor="w")
        self.console_output = tk.Text(self.console_frame, bg="#050505", fg=COLORS["text_secondary"], font=FONTS["code"], borderwidth=0, height=8, padx=10, pady=5)
        self.console_output.pack(fill="both", expand=True)

        # Footer Status (must be created BEFORE show_dashboard)
        self.status = tk.Label(self, text="Neuro-IDE Surgical Lab Online.", bg=COLORS["accent_primary"], fg="black", font=FONTS["small"], anchor="w", padx=10)
        self.status.pack(side="bottom", fill="x")

        # Initial View: Dashboard
        self.show_dashboard(self.pane_primary)

    def toggle_dual_view(self):
        if not self.dual_view_active:
            self.workspace.add(self.pane_secondary)
            self.btn_hud_dual.config(fg=COLORS["accent_primary"], text="🪟 SINGLE VIEW")
            self.dual_view_active = True
            self.status.config(text="Split Screen Engaged.")
        else:
            self.workspace.forget(self.pane_secondary)
            self.btn_hud_dual.config(fg=COLORS["text_dim"], text="🪟 DUAL VIEW")
            self.dual_view_active = False
            self.status.config(text="Single Screen Restored.")

    def dock_module(self, plugin, target_pane=None):
        """Docks a module into the specified pane (defaults to primary)"""
        pane = target_pane if target_pane else self.pane_primary
        
        # Clear pane
        for widget in pane.winfo_children():
            widget.pack_forget()
            
        # If docking into primary, update global mission status
        if pane == self.pane_primary:
            self.status.config(text=f"Engaged: {plugin.name}")
            self.lbl_mission.config(text=f"MISSION STATUS: ANALYZING {plugin.name.upper()}", fg=COLORS["accent_secondary"])

        # Create container
        container = tk.Frame(pane, bg=COLORS["bg_dark"], highlightthickness=1, highlightbackground=COLORS["border"])
        container.pack(fill="both", expand=True, padx=2, pady=2)
        
        mod_header = tk.Frame(container, bg=COLORS["bg_panel"], height=25)
        mod_header.pack(fill="x")
        
        tk.Label(mod_header, text=plugin.name.upper(), font=FONTS["small"], bg=COLORS["bg_panel"], fg=COLORS["accent_primary"], padx=10).pack(side="left")
        
        # Close button for the pane? No, sidebar handles it.
        # But we might want a "Move to Secondary" button here if dual view is on
        if self.dual_view_active and pane == self.pane_primary:
            tk.Button(mod_header, text="➡️", font=("Segoe UI", 8), bg=COLORS["bg_panel"], fg="white", relief="flat", command=lambda p=plugin: self.dock_module(p, self.pane_secondary)).pack(side="right")

        # Build UI in the container
        plugin.build_ui(container)

    def load_modules(self):
        """Dynamically load plugins from modules/ directory"""
        if not os.path.exists(self.modules_dir):
            return

        import importlib.util
        
        # Dashboard Button First
        dash_plugin = type('Dash', (object,), {'icon': '📊', 'name': 'Cortex', 'build_ui': self.show_dashboard})()
        self.build_sidebar_btn(dash_plugin)

        # List .py files
        modules = [f for f in os.listdir(self.modules_dir) if f.endswith(".py") and f != "base.py" and f != "__init__.py"]
        
        # Priority sort
        priority = ["hexeditor.py", "disassembler.py", "scope.py"]
        modules.sort(key=lambda x: priority.index(x) if x in priority else 99)

        loaded_count = 0
        for mod_file in modules:
            try:
                mod_name = mod_file[:-3]
                path = os.path.join(self.modules_dir, mod_file)
                
                spec = importlib.util.spec_from_file_location(f"modules.{mod_name}", path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[f"modules.{mod_name}"] = module
                spec.loader.exec_module(module)
                
                if hasattr(module, "Plugin"):
                    plugin_instance = module.Plugin()
                    
                    # Add to Sidebar only
                    self.build_sidebar_btn(plugin_instance)

                    # Add to Menu (for accessibility)
                    self.modules_menu.add_command(label=f"{plugin_instance.icon} {plugin_instance.name}", 
                                                 command=lambda p=plugin_instance: self.dock_module(p))

                    self.plugins.append((plugin_instance, None))
                    loaded_count += 1
            except Exception as e:
                print(f"Failed to load module {mod_file}: {e}")
                
        self.status.config(text=f"Loaded {loaded_count} external modules.")

    def build_sidebar_btn(self, plugin):
        """Create a sidebar button for a plugin"""
        btn = tk.Button(
            self.sidebar_scroll,
            text=plugin.icon,
            font=("Segoe UI Emoji", 18),
            bg=COLORS["sidebar_bg"],
            fg=COLORS["text_dim"],
            relief="flat",
            width=3,
            height=1,
            command=lambda p=plugin: self.dock_module(p)
        )
        btn.pack(pady=5)
        self.sidebar_btns[plugin.name] = btn
        return btn

    def build_explorer_icon(self, plugin):
        """Create an icon button in the explorer"""
        btn = tk.Button(
            self.explorer_scroll,
            text=plugin.icon,
            font=("Segoe UI Emoji", 16),
            bg=COLORS["bg_medium"],
            fg=COLORS["text_dim"],
            relief="flat",
            width=3,
            height=1,
            command=lambda p=plugin: self.dock_module(p)
        )
        btn.pack(pady=3)
        self.explorer_icons[plugin.name] = btn
        return btn

    def show_dashboard(self, parent):
        """Helper to restore dashboard in docking system"""
        self.dashboard_frame = tk.Frame(parent, bg=COLORS["bg_panel"])
        self.dashboard_frame.pack(fill="both", expand=True)
        self.build_dashboard(self.dashboard_frame)
        self.status.config(text="Cortex Overview Active.")
        self.lbl_mission.config(text="MISSION STATUS: READY", fg=COLORS["accent_primary"])

    def build_dashboard(self, parent):
        # NEURO-IDE MISSION OVERVIEW
        main_grid = tk.Frame(parent, bg=COLORS["bg_panel"])
        main_grid.pack(fill="both", expand=True, padx=40, pady=40)
        
        # TOP BANNER
        banner = tk.Frame(main_grid, bg=COLORS["bg_panel"])
        banner.pack(fill="x", pady=(0, 30))
        
        self.lbl_dash_title = tk.Label(banner, text="NEURO-CORTEX: SURGICAL SUITE", font=FONTS["heading"], bg=COLORS["bg_panel"], fg=COLORS["accent_primary"])
        self.lbl_dash_title.pack(side="left")
        
        # CORE GRID (2x2)
        grid_frame = tk.Frame(main_grid, bg=COLORS["bg_panel"])
        grid_frame.pack(fill="both", expand=True)
        
        def create_card(p, title, icon, info, color):
            card = tk.Frame(p, bg=COLORS["bg_medium"], highlightthickness=1, highlightbackground=COLORS.get("border", "#30363D"), padx=20, pady=20)
            tk.Label(card, text=f"{icon} {title}", font=FONTS.get("subheading", FONTS["heading"]), bg=COLORS["bg_medium"], fg=color).pack(anchor="w")
            tk.Label(card, text=info, font=FONTS.get("body", FONTS["main"]), bg=COLORS["bg_medium"], fg=COLORS["text_secondary"], justify="left").pack(anchor="w", pady=10)
            return card

        self.card_mem = create_card(grid_frame, "SYSTEM BIOMETRICS", "🏥", "Integrity: STABLE\nLeaks: 0 Detected\nDefrag: OPTIMIZED", COLORS["accent_primary"])
        self.card_mem.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.card_surg = create_card(grid_frame, "SURGICAL AUDIT", "🔪", "Ready for intervention.\nActive Session: IDLE\nSecurity: LOCKED", COLORS["accent_secondary"])
        self.card_surg.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.card_probe = create_card(grid_frame, "NEURO-PROBE", "🔍", "Target: neuro-os.img\nArch: x86_64\nMode: Surgical Gold", COLORS["accent_warning"])
        self.card_probe.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        self.card_disc = create_card(grid_frame, "CHRONICLE", "🎲", "Last Save: Never\nEvents Captured: 0\nState: Genesis", COLORS["accent_danger"])
        self.card_disc.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)
        grid_frame.rowconfigure(0, weight=1)
        grid_frame.rowconfigure(1, weight=1)

    def build_probe_ui(self, parent):
        # Header
        header = tk.Frame(parent, bg=COLORS["bg_panel"], height=60)
        header.pack(fill="x", side="top")
        
        self.lbl_probe_header = tk.Label(header, text="NEURO-PROBE: SYSTEM TARGETING", bg=COLORS["bg_panel"], fg=COLORS["accent_primary"], font=FONTS["heading"])
        self.lbl_probe_header.pack(side="left", padx=20, pady=10)
        
        self.btn_run_probe = tk.Button(header, text="▶ EXECUTE ANALYSIS", bg=COLORS["accent_success"], fg="black", font=FONTS["main"], relief="flat", padx=20, command=self.run_probe_analysis)
        self.btn_run_probe.pack(side="right", padx=20, pady=10)
        
        # Output Area
        self.container_probe = tk.Frame(parent, bg=COLORS["bg_dark"])
        self.container_probe.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.probe_output = tk.Text(self.container_probe, bg="#050505", fg=COLORS["text_secondary"], font=FONTS["code"], borderwidth=0, padx=10, pady=10)
        self.probe_output.pack(fill="both", expand=True)
        
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
                    
                    # LOAD INTO SCOPE (Search for scope plugin)
                    for plugin, frame in self.plugins:
                        if plugin.name == "Neuro-Scope":
                            if os.path.exists(json_out):
                                with open(json_out, 'r') as f:
                                    data = json.load(f)
                                    if "qemu" in data and "serial_output" in data["qemu"]:
                                        raw_log = data["qemu"]["serial_output"]
                                        from scope.parser import SerialLogParser
                                        events = SerialLogParser().parse(raw_log)
                                        plugin.scope_viz.load_events(events)
                                        self.status.config(text=f"Analysis Complete. {len(events)} events processed.")
                            break
                else:
                    self.probe_output.insert(tk.END, engine.get_string("probe_error").format(process.returncode))
                    self.status.config(text=engine.get_string("probe_failed"))
                    
            except Exception as e:
                self.probe_output.insert(tk.END, f"\n>> Exception: {e}\n")
            
            finally:
                self.btn_run_probe.config(state="normal")
                
        threading.Thread(target=run, daemon=True).start()



    def refresh_ui(self):
        """Global UI Update on Language Change"""
        print(f"NeuroIDE: Refreshing UI for language '{engine.current_lang}'...")
        self.title(engine.get_string("app_title"))
        self.status.config(text=engine.get_string("status_ready"))
        
        # Plugins (Only refresh those that are actively docked or have built their structure)
        for plugin, frame in self.plugins:
            try:
                # Check if plugin has a set of widgets that need refreshing
                # We can check for a common attribute like 'parent' or just use try/except
                plugin.refresh_ui()
            except AttributeError:
                pass # UI not built yet, skip refresh
            except Exception as e:
                print(f"NeuroIDE: Error updating plugin {plugin.name}: {e}")

        # Dashboard (Update static labels if they exist)
        if hasattr(self, 'lbl_dash_title'):
            try:
                self.lbl_dash_title.config(text=engine.get_string("dash_title"))
            except:
                pass

if __name__ == "__main__":
    app = NeuroIDE()
    app.mainloop()
