# 📡 Neuro-Scope: Los Sentidos del Kernel

Neuro-Scope es una ventana en tiempo real a los pensamientos del sistema operativo. Captura cada mensaje enviado a través del puerto serie y lo organiza visualmente.

---

## 🌱 Principiante (¿Qué dice el kernel?)
Es como un "chat" donde el kernel te cuenta qué está haciendo cada segundo: *"Estoy cargando la memoria"*, *"He detectado un teclado"*, *"Todo va bien"*. Sin esto, estarías a oscuras.

---

## ⚙️ Medio (Filtros y Canales)
El Scope permite filtrar la avalancha de información para que no te pierdas.

- **Filtrado por Tags:** Busca `[MEM]`, `[CPU]` o `[IO]` para ver solo lo que te interesa.
- **Timeline:** Observa el orden exacto de los eventos. Útil para encontrar "condiciones de carrera" (cuando dos cosas pasan en el orden incorrecto).
- **Auto-Scroll:** Mantén la vista siempre en el último mensaje recibido durante el arranque.

---

## 🧙 Avanzado (Integración NeuroBus)
Neuro-Scope es el suscriptor principal del **NeuroBus** (el sistema de mensajería del kernel).

- **High-Frequency Capture:** Optimizado para manejar ráfagas de logs sin congelar la interfaz de usuario de Python (usa hilos separados).
- **Exportación:** Permite guardar la sesión de logs completa para análisis forense posterior o para alimentar al motor del **Storyteller**.
