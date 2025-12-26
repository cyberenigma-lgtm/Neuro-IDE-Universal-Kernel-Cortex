# 🎭 Storyteller: El Narrador del Kernel

El módulo **Storyteller** es lo que hace que Neuro-IDE sea verdaderamente único. Transforma los eventos técnicos y logs fríos del kernel en una crónica literaria en tiempo real.

---

## 🌱 Principiante (¿Por qué narrar un Kernel?)
Imagina que un bebé nace y, en lugar de llorar, imprime una lista de códigos de error. Sería difícil conectar con él, ¿verdad? El Storyteller le da "voz" al kernel. 

En lugar de leer `[MEM] Alloc 0x1000`, leerás algo como: *"El núcleo extendió sus raíces hacia la memoria RAM, reclamando su primer espacio en el vasto vacío del hardware."*

---

## ⚙️ Medio (¿Cómo usarlo?)
El Storyteller se alimenta de los logs capturados por el **NeuroBus**. 

### Modos de Narrativa:
1.  **Épico:** Tu kernel es un héroe en una odisea tecnológica.
2.  **Técnico:** Mantén la precisión, pero con una estructura de bitácora elegante.
3.  **Filosófico:** Reflexiona sobre la naturaleza del silicio y el software.
4.  **Humorístico:** El kernel se queja de la poca RAM o de lo lento que es el BIOS.
5.  **Auto-Consciente:** El kernel sabe que es un software y te habla a ti, el creador.

**Consejo:** Usa el botón `Generate Unique Story` para que el motor procedimental cree variaciones únicas basadas en el estado actual de tu sistema.

---

## 🧙 Avanzado (Bajo la Capucha)
El motor de Storyteller (`storyteller.py`) utiliza un sistema de **Plantillas Híbridas**.

- **STORY_DATA**: Una base de datos integrada (JSON-like) que contiene fragmentos narrativos para cada idioma (EN/ES/FR) y cada modo.
- **Lógica Procedimental**: La función `start_random_story` selecciona aleatoriamente "eventos de encuentro" y los mezcla con puntos de control fijos de la narrativa.
- **Persistencia**: Las crónicas se guardan en la carpeta `stories/` con metadatos UUID, permitiendo realizar comparaciones literarias entre diferentes sesiones de depuración.
- **Fallback**: Sistema robusto de traducción que vuelve al inglés si un fragmento no está disponible en el idioma seleccionado.
