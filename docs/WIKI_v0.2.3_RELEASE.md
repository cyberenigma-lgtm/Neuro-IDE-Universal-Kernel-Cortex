# 🏥 Neuro-IDE: The Surgical Cockpit
> **Version:** v0.2.3 (Surgical Suite)
> **Status:** Operational (Gold)
> **License:** MIT

## 📡 Overview
**Neuro-IDE** is a specialized "Surgical Cockpit" designed for low-level Operating System development. Unlike generic text editors, Neuro-IDE treats binary files, kernels, and bootloaders as "patients" on an operating table, providing deep-dive visualization and surgical modification tools.

---

## 🚀 Release v0.2.3: "Singularity" Features

### 1. 🏗️ Kernel Generator (New)
*   **Module:** `Kernel Generator`
*   **Function:** Creates a complete, compilable OS skeleton in seconds.
*   **Specs:** 
    *   Generates `boot.asm` (Multiboot 1/2 Compliant).
    *   Generates `kernel.c` (VGA Driver pre-installed).
    *   Generates `Makefile` (Tuned for MinGW/MSYS2 & Linux).
    *   Generates `linker.ld` (1MB Higher Half setup).
*   **Usage:** Go to the tab, name your project ("MyOS"), and click **Initialize**.

### 2. 🕰️ Time Travel Debugger (New)
*   **Module:** `Neuro-Scope`
*   **Function:** Visual timeline replay of serial logs.
*   **Usage:** 
    *   Load a `.log` file or connect real-time.
    *   Use the **"TIME TRAVEL"** slider to rewind execution history.
    *   Filter events to pinpoint exactly when a crash occurred.

### 3. 📂 Universal Loading (Upgrade)
*   **Modules Affected:** Hex Editor, Disassembler, UBD, Neuro-Scope.
*   **Change:** Each module now operates independently.
*   **Usage:** Click the local `📂 OPEN` button inside each tool to load specific files (`.bin`, `.img`, `.log`) without affecting the rest of the workspace.

### 4. 🧬 IO/APIC & Synaptic Simulation (Upgrade)
*   **Module:** `IA Gating` & `IOAPIC`
*   **Change:** Added textual telemetry. The simulator now reports active interrupts and neural node activation in a dedicated log window.

---

## � Bug Fixes & Stability

### 🛑 Critical Fixes
*   **Hex Editor Race Condition:** Solved an issue where the editor attempted to load before the UI hierarchy was built, causing a hard crash.
*   **UBD Cascade Failure:** Fixed a silent error in `ubd.py` that would block the loading of subsequent modules like the Disassembler.
*   **View Menu Crash:** Resolved an `AttributeError` caused by a deprecated reference to `self.notebook` in the global menu.

### 🔌 Connectivity Fixes
*   **Generator Freeze:** Implemented threading/UI updates (`update_idletasks`) in the Kernel Generator to prevent the window from freezing during project creation.
*   **Disconnected Buttons:** Wired up previously "dummy" buttons in the Dashboard and `ia_gating.py` to actual logic.

---

## �🛠️ Module Arsenal (Full List)

| Module | Icon | Role | Description |
| :--- | :---: | :--- | :--- |
| **Dashboard** | 💎 | Hub | Central telemetry and quick access. |
| **Hex Editor** | 💾 | Surgery | Edit bytes directly (.bin/.img). **Double-click to edit.** |
| **Disassembler** | ⚙️ | Analysis | View x86/x64 assembly from raw binary. |
| **Neuro-Scope** | 📡 | Debug | Real-time serial log visualizer with **Time Travel**. |
| **UBD (Diff)** | ⚖️ | Forensics | Compare two kernel binaries bit-by-bit. |
| **MemHealth** | 🏥 | Diagnosis | Heap allocation heatmap (malloc/free tracker). |
| **BootViz** | 🖼️ | Visual | E820 Memory Map visualizer. |
| **Kernel Gen** | 🏗️ | Creation | One-click OS project scaffolder. |
| **IA Gating** | 🛡️ | Sim | Neural Network / Interrupt routing simulator. |
| **ScreenDiff** | 👁️ | QA | Pixel-perfect UI regression testing. |

---

## ⌨️ Shortcuts & Tips
*   **F5 (Refresh):** Reloads the current view.
*   **Double-Click (Hex):** Opens the byte editor dialog.
*   **Time Travel Slider:** Drag left to see past events.
*   **Debug Log:** `debug_session.log` contains internal IDE diagnostics.

---

## 🔧 Installation & Build
```bash
# Clone the repository
git clone https://github.com/cyberenigma-lgtm/Neuro-IDE-Universal-Kernel-Cortex.git

# Enter directory
cd Neuro-IDE-Universal-Kernel-Cortex

# Run (Requires Python 3.x + Tkinter)
python neuro_ide.py
```
