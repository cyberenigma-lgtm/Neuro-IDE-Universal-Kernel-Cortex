# 🏥 Memory Health & Leak Detection

## 🇺🇸 English
### What is it?
This module analyzes the pattern of memory allocations (`malloc`) and deallocations (`free`) inside your kernel to find leaks (memory that is reserved but never returned).

### How to use it?
1. Your kernel must emit log messages during allocation/free events.
2. The **Memory Health** module captures those tags and tracks the "lifetime" of each pointer.
3. If a pointer is lost (is never freed), the module marks it as a "Potential Leak" with its original source location.

---

## 🇪🇸 Español
### ¿Qué es?
Este módulo analiza el patrón de asignaciones de memoria (`malloc`) y liberaciones (`free`) dentro de tu kernel para encontrar fugas (memoria que se reserva pero nunca se devuelve).

### ¿Cómo usarlo?
1. Tu kernel debe emitir mensajes de log durante los eventos de asignación/liberación.
2. El módulo **Memory Health** captura esas etiquetas y rastrea la "vida" de cada puntero.
3. Si un puntero se pierde (nunca se libera), el módulo lo marca como "Fuga Potencial" junto con su ubicación de origen.
