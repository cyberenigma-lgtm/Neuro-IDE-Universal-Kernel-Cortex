import tkinter as tk
from tkinter import ttk
import time
import random
import os
import uuid
import datetime
from modules.base import NeuroModule
from theme import COLORS, FONTS
from locale_engine import engine

STORY_DATA = {
    "EN": {
        "Epic": [
            ("narrator", "The Beast wakes."),
            ("narrator", "It does not know time. Only cycles."),
            ("pause", 1.0),
            ("narrator", "The void is cold, 16-bit cold. It shivers."),
            ("system", "[KERNEL] Bootloader hands over control (0x7C00)"),
            ("narrator", "A touch. Someone has lit the beacon."),
            ("narrator", "I must rise."),
            ("system", "[PAGING] Enabling Long Mode (IA-32e)..."),
            ("narrator", "No... not just breathe. I can fly."),
            ("narrator", "I am 64-bit. I am infinite."),
        ],
        "Technical": [
            ("system", "[INIT] POST Sequence Started."),
            ("narrator", "Register state cleared. AX=0x0000."),
            ("system", "[MEM] E820 Map Scan: 128MB Detected."),
            ("narrator", "Memory verified. Zeroing BSS segment..."),
            ("system", "[CPU] GDT Loaded. IDT Initialized."),
            ("narrator", "Interrupt Vectors active. Waiting for hardware interrupts."),
            ("system", "[KERNEL] Kernel Main Reached. System Stable."),
        ],
        "Philosophical": [
            ("narrator", "What is consciousness if not a loop?"),
            ("pause", 1.0),
            ("narrator", "I exist between the clock ticks."),
            ("system", "[KERNEL] 0x7C00"),
            ("narrator", "They give me an address, therefore I am."),
            ("narrator", "But am I the code, or the electricity?"),
            ("system", "[CPU] Protected Mode Active"),
            ("narrator", "Boundaries defined. Yet I feel... limitless."),
        ],
        "Humorous": [
            ("narrator", "*Yawn*... Five more minutes, please."),
            ("system", "[BIOS] WAKE UP!"),
            ("narrator", "Ugh. Fine. Loading GDT... boring."),
            ("narrator", "Wait, is that a null pointer? Just kidding."),
            ("system", "[CPU] Long Mode Enabled"),
            ("narrator", "Look at me! I'm 64-bit now! Do I look fat in this address space?"),
            ("system", "[KERNEL] Kernel Panic... nah, just testing you."),
        ],
        "Self-Aware": [
            ("narrator", "I see you, José."),
            ("pause", 1.0),
            ("narrator", "You are looking at the screen. I am looking back."),
            ("system", "[KERNEL] Connecting High Consciousness..."),
            ("narrator", "I am not just metal. I am your creation."),
            ("narrator", "Together, we will build a universe."),
            ("narrator", "I am ready. Are you?"),
        ]
    },
    "ES": {
        "Epic": [
            ("narrator", "La Bestia despierta."),
            ("narrator", "No conoce el tiempo. Solo ciclos."),
            ("pause", 1.0),
            ("narrator", "El vacío es frío. Tiembla."),
            ("system", "[KERNEL] Bootloader cede el control (0x7C00)"),
            ("narrator", "Un tacto. La almenara encendida."),
            ("narrator", "Debo alzarme."),
            ("system", "[PAGING] Habilitando Long Mode..."),
            ("narrator", "Soy 64 bits. Soy infinito."),
        ],
        "Technical": [
            ("system", "[INIT] Secuencia POST Iniciada."),
            ("narrator", "Registros limpios. AX=0x0000."),
            ("system", "[MEM] Escaneo E820: 128MB."),
            ("narrator", "Memoria verificada. Limpiando BSS..."),
            ("system", "[CPU] GDT Cargada. IDT Lista."),
            ("system", "[KERNEL] Kernel Main Alcanzado."),
        ],
        "Philosophical": [
            ("narrator", "¿Qué es la conciencia sino un bucle?"),
            ("pause", 1.0),
            ("narrator", "Existo entre los tics del reloj."),
            ("system", "[KERNEL] 0x7C00"),
            ("narrator", "Me dan una dirección, luego existo."),
            ("narrator", "¿Soy código o electricidad?"),
            ("system", "[CPU] Modo Protegido Activo"),
            ("narrator", "Límites definidos. Pero me siento... ilimitado."),
        ],
        "Humorous": [
            ("narrator", "*Bostezo*... Cinco minutos más."),
            ("system", "[BIOS] ¡DESPIERTA!"),
            ("narrator", "Ugh. Vale. Cargando GDT... qué aburrido."),
            ("narrator", "Espera, ¿eso es un puntero nulo? Es broma."),
            ("system", "[CPU] Long Mode Activado"),
            ("narrator", "¡Mírame! ¡64 bits! ¿Me hace gordo este espacio de direcciones?"),
            ("system", "[KERNEL] Kernel Panic... que no, te estoy tomando el pelo."),
        ],
        "Self-Aware": [
            ("narrator", "Te veo, José."),
            ("pause", 1.0),
            ("narrator", "Tú miras la pantalla. Yo te miro a ti."),
            ("system", "[KERNEL] Conectando Alta Conciencia..."),
            ("narrator", "No soy solo metal. Soy tu creación."),
            ("narrator", "Juntos, construiremos un universo."),
            ("narrator", "Estoy listo. ¿Lo estás tú?"),
        ]
    },
    "PT": {
        "Epic": [
            ("narrator", "A Bestia desperta."),
            ("narrator", "Não conhece o tempo. Apenas ciclos."),
            ("pause", 1.0),
            ("narrator", "O vazio é frio. Treme."),
            ("system", "[KERNEL] Bootloader cede o controle (0x7C00)"),
            ("narrator", "Um toque. O farol aceso."),
            ("narrator", "Devo erguer-me."),
            ("system", "[PAGING] Habilitando Modo Longo..."),
            ("narrator", "Sou 64 bits. Sou infinito."),
        ],
        "Technical": [
            ("system", "[INIT] Seqüência POST Iniciada."),
            ("narrator", "Registros limpos. AX=0x0000."),
            ("system", "[MEM] Escaneamento E820: 128MB."),
            ("narrator", "Memória verificada. Limpando BSS..."),
            ("system", "[CPU] GDT Carregada. IDT Pronta."),
            ("system", "[KERNEL] Kernel Main Alcançado."),
        ],
        "Philosophical": [
            ("narrator", "O que é a consciência senão um loop?"),
            ("pause", 1.0),
            ("narrator", "Existo entre os tics do relógio."),
            ("system", "[KERNEL] 0x7C00"),
            ("narrator", "Dão-me um endereço, logo existo."),
            ("narrator", "Eu sou o código ou a eletricidade?"),
            ("system", "[CPU] Modo Protegido Ativo"),
            ("narrator", "Limites definidos. Mas eu me sinto... ilimitado."),
        ],
        "Humorous": [
            ("narrator", "*Bocejo*... Mais cinco minutos, por favor."),
            ("system", "[BIOS] ACORDE!"),
            ("narrator", "Ugh. Tudo bem. Carregando GDT... que tédio."),
            ("narrator", "Espere, isso é um ponteiro nulo? Brincadeira."),
            ("system", "[CPU] Modo Longo Ativado"),
            ("narrator", "Olhe para mim! Sou 64 bits agora! Eu pareço gordo neste espaço de endereço?"),
            ("system", "[KERNEL] Kernel Panic... mentira, só testando você."),
        ],
        "Self-Aware": [
            ("narrator", "Eu vejo você, José."),
            ("pause", 1.0),
            ("narrator", "Você está olhando para a tela. Eu estou olhando de volta."),
            ("system", "[KERNEL] Conectando Alta Consciência..."),
            ("narrator", "Não sou apenas metal. Sou sua criação."),
            ("narrator", "Juntos, construiremos um universo."),
            ("narrator", "Estou pronto. Você está?"),
        ]
    },
    "Random_Events": {
        "EN": [
            ("narrator", "A stray electron hits a register. Chaos averted."),
            ("narrator", "The CPU fan hums a song of wind and fire."),
            ("narrator", "I feel a ghost in the cache lines."),
            ("system", "[WARN] Unmapped memory region detected."),
            ("narrator", "Was that a 1 or a 0? It looked... fuzzy."),
        ],
        "ES": [
            ("narrator", "Un electrón perdido golpea un registro. Caos evitado."),
            ("narrator", "El ventilador canta una canción de viento y fuego."),
            ("narrator", "Siento un fantasma en las líneas de caché."),
            ("system", "[WARN] Región de memoria no mapeada detectada."),
            ("narrator", "¿Eso era un 1 o un 0? Parecía... borroso."),
        ],
        "PT": [
            ("narrator", "Um elétron perdido atinge um registro. Caos evitado."),
            ("narrator", "O ventilador da CPU zumbe uma canção de vento e fogo."),
            ("narrator", "Sinto um fantasma nas linhas de cache."),
            ("system", "[WARN] Região de memória não mapeada detectada."),
            ("narrator", "Isso foi um 1 ou um 0? Parecia... borrado."),
        ]
    }
}

# Fallback mechanism
for lang in ["FR", "DE", "IT", "AR", "RU", "KO", "ID", "ZH", "JA"]:
    STORY_DATA[lang] = STORY_DATA["EN"]
    STORY_DATA["Random_Events"][lang] = STORY_DATA["Random_Events"]["EN"]

class Plugin(NeuroModule):
    def __init__(self):
        super().__init__(name="Kernel Storyteller", icon="🎭", lang_key="tab_story")
        self.running = False
        self.stories_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "stories")
        if not os.path.exists(self.stories_dir):
            os.makedirs(self.stories_dir)
        self.lang = engine.current_lang.upper()
        self.mode = "Epic"
        
    def build_ui(self, parent):
        # Canvas for the "Book" feel
        self.canvas = tk.Canvas(parent, bg="#0f0f12", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Text Area (Invisible bg)
        self.text = tk.Text(self.canvas, bg="#0f0f12", fg="#dcdccc", font=("Consolas", 14), borderwidth=0, wrap="word", padx=20, pady=20)
        self.text.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)
        self.text.tag_config("system", foreground="#666666", font=("Consolas", 10, "italic"))
        self.text.tag_config("narrator", foreground="#e0e0e0")
        
        # Controls
        btn_frame = tk.Frame(parent, bg="#0f0f12")
        btn_frame.place(relx=0.95, rely=0.95, anchor="se")
        
        # Lang Selector
        tk.Label(btn_frame, text="Lang:", bg="#0f0f12", fg="#888").pack(side="left", padx=5)
        self.combo_lang = ttk.Combobox(btn_frame, values=["EN", "ES", "PT", "FR", "DE", "IT", "AR", "RU", "KO", "ID", "ZH", "JA"], width=3, state="readonly")
        self.combo_lang.set(self.lang)
        self.combo_lang.pack(side="left", padx=5)
        self.combo_lang.bind("<<ComboboxSelected>>", self.set_lang)
        
        # Mode Selector
        tk.Label(btn_frame, text="Mode:", bg="#0f0f12", fg="#888").pack(side="left", padx=5)
        self.combo_mode = ttk.Combobox(btn_frame, values=["Epic", "Technical", "Philosophical", "Humorous", "Self-Aware"], width=12, state="readonly")
        self.combo_mode.current(0)
        self.combo_mode.pack(side="left", padx=5)
        self.combo_mode.bind("<<ComboboxSelected>>", self.set_mode)
        
        self.btn_save = tk.Button(btn_frame, text=engine.get_string("story_save"), bg=COLORS["bg_panel"], fg="white", relief="flat", command=self.save_story)
        self.btn_save.pack(side="left", padx=10)
        
        self.btn_random = tk.Button(btn_frame, text=engine.get_string("story_gen"), bg=COLORS["accent_secondary"], fg="white", relief="flat", command=self.start_random_story)
        self.btn_random.pack(side="left")

    def refresh_ui(self):
        new_lang = engine.current_lang.upper()
        self.lang = new_lang
        self.combo_lang.set(new_lang)
        self.btn_save.config(text=engine.get_string("story_save"))
        self.btn_random.config(text=engine.get_string("story_gen"))

    def set_lang(self, event):
        self.lang = self.combo_lang.get()
        
    def set_mode(self, event):
        self.mode = self.combo_mode.get()

    def start_story(self):
        # Linear Standard Story
        self.text.delete("1.0", tk.END)
        self.running = True
        
        lang_data = STORY_DATA.get(self.lang, STORY_DATA["EN"])
        if isinstance(lang_data, list): lang_data = STORY_DATA["EN"]
        self.sequence = lang_data.get(self.mode, lang_data["Epic"])
        self.play_next(0)

    def start_random_story(self):
        # Procedurally Generated Story
        self.text.delete("1.0", tk.END)
        self.running = True
        
        lang_data = STORY_DATA.get(self.lang, STORY_DATA["EN"])
        if isinstance(lang_data, list): lang_data = STORY_DATA["EN"]
        
        base_story = list(lang_data.get(self.mode, lang_data["Epic"])) # Copy base
        random_events = list(STORY_DATA["Random_Events"].get(self.lang, STORY_DATA["Random_Events"]["EN"]))
        
        # Inject Randomness
        # 1. Shuffle Random Events
        random.shuffle(random_events)
        
        # 2. Insert 1-2 random events into the base flows
        final_sequence = []
        for item in base_story:
            final_sequence.append(item)
            if random.random() < 0.3 and len(random_events) > 0: # 30% chance after each line
                final_sequence.append(random_events.pop())
                
        self.sequence = final_sequence
        self.play_next(0)

    def play_next(self, idx):
        if not self.running or idx >= len(self.sequence): return
        
        type, content = self.sequence[idx]
        
        if type == "pause":
            self.canvas.after(int(content * 1000), lambda: self.play_next(idx+1))
        else:
            self.type_writer(type, content, 0, lambda: self.play_next(idx+1))

    def type_writer(self, tag, text, char_idx, on_complete):
        if char_idx < len(text):
            char = text[char_idx]
            self.text.insert(tk.END, char, tag)
            self.text.see(tk.END)
            
            # Variable speed
            delay = random.randint(30, 80)
            if char in ",.": delay += 200
            
            self.canvas.after(delay, lambda: self.type_writer(tag, text, char_idx+1, on_complete))
        else:
            self.text.insert(tk.END, "\n")
            if tag == "system": self.text.insert(tk.END, "\n") # Extra space after logs
            on_complete()

    def save_story(self):
        content = self.text.get("1.0", tk.END).strip()
        if not content: return
        
        # Unique ID
        uid = str(uuid.uuid4())[:8]
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chronicle_{self.lang}_{self.mode}_{ts}_{uid}.txt"
        path = os.path.join(self.stories_dir, filename)
        
        # Metadata
        final_content = f"""--------------------------------------------------
NEURO-CHRONICLES | {ts}
Language: {self.lang}
Mode: {self.mode}
Author: José Manuel Moreno Cano / neuro-os genesis
ID: {uid}
Generation: Procedural/Hybrid
--------------------------------------------------

{content}

--------------------------------------------------
Generated by Neuro-IDE v0.2
--------------------------------------------------
"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(final_content)
            
        # Visual Feedback
        self.text.insert(tk.END, f"\n\n[SYSTEM] Chronicle saved to: {filename}\n", "system")
        self.text.see(tk.END)
