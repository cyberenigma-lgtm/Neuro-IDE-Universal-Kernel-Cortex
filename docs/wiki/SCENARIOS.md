# 🚀 Escenarios del Mundo Real: Resolviendo Crisis en OSDev

Neuro-IDE no es solo teoría. Aquí tienes tres historias de cómo usar las herramientas para salvar tu kernel de la ruina.

---

## 🌩️ Escenario A: "El Triple Fault Infinito"
**Situación:** Tu kernel arranca, pero antes de mostrar nada, el ordenador se reinicia en bucle.

1.  **Abre Neuro-Scope:** Observa los últimos mensajes. Si ves `[GDT] Loading...` y luego nada, el problema está en la transición a 32/64 bits.
2.  **Consulta Neuro-Doctor:** El Doctor te dirá: *"Parece que tu IDT no está alineada o el stack ha colapsado el código"*.
3.  **Solución:** Revisa tu `kernel_entry.asm`. Según el Doctor, el stack debe estar alineado a 16 bytes para llamadas a C.

---

## 🩺 Escenario B: "El Salto al Vacío (#UD)"
**Situación:** Añades una función nueva y el kernel muere con un error de `Invalid Opcode`.

1.  **Abre ELF Explorer:** Mira la dirección de tu función nueva.
2.  **Abre Neuro-Doctor:** El Doctor detecta que el procesador intentó ejecutar código en una dirección que pertenece a la sección `.data`.
3.  **Análisis:** Te das cuenta de que pasaste un puntero de función mal. El Doctor te sugiere: *"Verifica que no estés saltando a una variable en lugar de a una función"*.

---

## 🗺️ Escenario C: "¿Dónde está mi memoria?"
**Situación:** Tu kernel funciona en QEMU pero falla en hardware real (Intel i9).

1.  **Abre BootViz:** Compara el mapa de memoria de QEMU con el de tu máquina real.
2.  **Observación:** En hardware real, hay una zona `Reserved` justo donde tú pensabas cargar tu kernel heap.
3.  **Solución:** Ajustas tu `linker.ld` para mover el heap un poco más arriba, evitando la zona reservada del BIOS. ¡Kernel salvado!

---
**Neuro-IDE** | *Herramientas para los que construyen el futuro desde el bit cero.*
