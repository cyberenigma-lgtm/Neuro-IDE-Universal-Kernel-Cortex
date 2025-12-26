# 🔍 ELF Explorer: Anatomía del Binario

Esta herramienta te permite "abrir" el archivo de tu kernel para ver cómo está organizado antes de que se ejecute.

---

## 🌱 Principiante (El Mapa del Tesoro)
Imagina que tu kernel es un edificio. El ELF Explorer es el plano que muestra dónde está la cocina (los datos), dónde están los dormitorios (el stack) y dónde están las oficinas de comando (el código).

---

## ⚙️ Medio (Secciones y Cabeceras)
Crucial para verificar que tu compilador está haciendo lo que tú quieres.

- **.text:** Aquí vive el código ejecutable.
- **.data / .rodata:** Aquí están tus variables y textos permanentes.
- **.bss:** El espacio vacío reservado para el futuro.
- **Entry Point:** La dirección exacta donde el ordenador empezará a leer tu código. Si esto está mal, el kernel nunca arrancará.

---

## 🧙 Avanzado (Estructura de 64 bits)
Específicamente diseñado para kernels **x86_64**.

- **Program Headers:** Analiza los segmentos `LOAD` y sus permisos (R/W/X). Verifica que el stack no sea ejecutable por seguridad.
- **Symbol Table:** Permite localizar funciones específicas en el binario sin necesidad de depuradores externos pesados como GDB.
- **Validación de Alineación:** Comprueba que las secciones estén alineadas a 4KB (páginas), vital para la paginación en Long Mode.
