import json
import os

class LocaleEngine:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LocaleEngine, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
        
    def __init__(self):
        if self.initialized:
            return
            
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.lang_dir = os.path.join(self.base_dir, "lang")
        self.current_lang = "en"
        self.strings = {}
        self.callbacks = []
        
        self.load_lang(self.current_lang)
        self.initialized = True
        print(f"LocaleEngine: Initialized instance {id(self)} with base_dir={self.base_dir}")
        
    def load_lang(self, lang_code):
        file_path = os.path.join(self.lang_dir, f"{lang_code}.json")
        if not os.path.exists(file_path):
            print(f"LocaleEngine: Language file {lang_code}.json not found. Falling back to 'en'.")
            file_path = os.path.join(self.lang_dir, "en.json")
            lang_code = "en"
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.strings = json.load(f)
            self.current_lang = lang_code
            print(f"LocaleEngine: Loaded {lang_code}.json successfully.")
            self.notify_listeners()
        except Exception as e:
            print(f"LocaleEngine: Error loading language {lang_code}: {e}")
            
    def get_string(self, key, default=None):
        if default is None:
            default = f"[{key}]"
        return self.strings.get(key, default)
        
    def register_callback(self, callback):
        if callback not in self.callbacks:
            self.callbacks.append(callback)
            
    def notify_listeners(self):
        print(f"LocaleEngine: Notifying {len(self.callbacks)} listeners...")
        for cb in self.callbacks:
            try:
                cb()
            except Exception as e:
                print(f"LocaleEngine: Error in callback: {e}")

# Global instance
engine = LocaleEngine()
