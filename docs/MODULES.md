# 📦 Neuro-IDE Module Inventory (v0.2)

The Mega-Integrated suite contains 17 specialized modules for operating system development.

## Core Modules
These are built directly into the mission control.
- **Cortex**: Dashboard and system overview.
- **Neuro-Probe**: Static and dynamic binary analysis.
- **Neuro-Scope**: Real-time serial log event visualizer.

## Integrated Plugins (Lobes)
Located in `modules/`.

| Module | Description | Logic |
| :--- | :--- | :--- |
| **Neuro-Doctor** | Analyzes #UD and Panics via serial heuristics. | Functional |
| **Storyteller** | Procedural narrative engine for boot events. | Functional |
| **BootViz** | Memory map visualization (E820/Long Mode). | Functional |
| **UBD** | Binary diffing tool for hex/symbolic comparison. | Functional |
| **ELF Ex** | ELF64 header and section explorer. | Functional |
| **Knowledge** | OSDev dependency graph visualizer. | Functional |
| **KTTD** | Simulated Time-Travel Debugging interface. | Mockup |
| **Profiler** | CPU and Interrupt usage simulation. | Functional |
| **MemMap** | Real-time physical memory region map. | Functional |
| **Syscalls** | System call registration and mapping table. | Functional |
| **Sandbox** | Generator for isolated target environments. | Functional |
| **ScreenDiff** | Visual regression testing (Snapshot comparison). | Functional |
| **Regression** | Performance trend analysis for boot times. | Functional |
| **IDT Explorer** | Interrupt Descriptor Table diagnostic tool. | Functional |
| **Divergence** | Multi-emulator trace comparison. | Functional |
| **Binary Map** | Visualization of binary section density. | Functional |
| **Hex Navigator** | Low-level hex editor and viewer. | Functional |

---
*Each module is designed to be standalone and can be removed or added simply by moving the .py file in/out of the `modules/` folder.*
