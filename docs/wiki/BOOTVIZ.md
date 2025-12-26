# 🗺️ BootViz: El Mapa de la Memoria física

BootViz proporciona una visualización espacial de cómo se distribuye la memoria RAM de tu máquina durante el arranque.

---

## 🌱 Principiante (La Vecindad de la RAM)
La memoria de tu ordenador es como un vecindario enorme. BootViz te muestra quién vive en cada casa: quién es el kernel, dónde están los dispositivos de vídeo y qué áreas están prohibidas porque el fabricante del ordenador las usa para sí mismo.

---

## ⚙️ Medio (El Mapa E820)
Visualiza las regiones reportadas por el BIOS o el Bootloader.

- **Usable (Verde):** Memoria libre donde puedes cargar programas.
- **Reserved (Rojo):** Zonas prohibidas que no debes tocar.
- **ACPI/MMIO (Naranja):** Puentes de comunicación con el hardware.

Útil para saber si tu kernel cabe en la memoria o si estás intentando escribir en una zona prohibida.

---

## 🧙 Avanzado (Layout en Long Mode)
BootViz te ayuda a planificar tu **Kernel Heap** y tus tablas de paginación.

- **Mapeo de Dispositivos:** Identifica las direcciones físicas para el buffer de vídeo (LFB) para pintar en pantalla.
- **Validación de Límites:** Asegura que los descriptores de memoria no se solapen, evitando errores silenciosos de corrupción de datos que son imposibles de encontrar de otra manera.
