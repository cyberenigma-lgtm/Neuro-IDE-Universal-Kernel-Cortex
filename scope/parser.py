"""
Neuro-Scope: Serial Log Parser
Parses raw serial dump into a structured timeline of events.
"""

import re
from typing import List, Dict, Any

class SerialLogParser:
    def __init__(self):
        self.events = []
        self.start_time = 0
        self.estimated_time_per_char = 0.001 # 1ms est per char if no timestamp
    
    def parse(self, raw_data: str) -> List[Dict[str, Any]]:
        """
        Parses raw serial string into events.
        Events:
        - type: 'marker' | 'log'
        - content: str
        - time: float (relative seconds)
        - level: 'info' | 'error' | 'critical'
        """
        self.events = []
        current_time = 0.0
        
        # Split by distinct markers or newlines
        # Markers: [ ] { } ! ? #
        # We need to scan character by character to catch markers buried in text
        
        buffer = ""
        
        for char in raw_data:
            # Check for special single-char markers
            if char in "[]{}!?#":
                # Flush text buffer if exists
                if buffer.strip():
                    self.events.append({
                        "type": "log",
                        "content": buffer.strip(),
                        "time": current_time,
                        "level": "info"
                    })
                    buffer = ""
                
                # Add marker event
                level = "info"
                desc = "Unknown"
                if char == '[': desc = "Kernel Entry"; level="success"
                elif char == ']': desc = "PIC Masked"; level="warning"
                elif char == '{': desc = "Stack Ready"; level="success"
                elif char == '}': desc = "BSS Zeroed"; level="success"
                elif char == '!': desc = "IDT Loaded"; level="critical"
                elif char == '?': desc = "SSE Enabled"; level="info"
                elif char == '#': desc = "Exception Stub"; level="error"
                
                self.events.append({
                    "type": "marker",
                    "content": char,
                    "description": desc,
                    "time": current_time,
                    "level": level
                })
                
                current_time += 0.05 # Marker takes 'time' visually
            
            elif char == '\n':
                # Flush buffer on newline
                if buffer.strip():
                    # Detect Log Level
                    level = "info"
                    if "PANIC" in buffer: level = "critical"
                    elif "ERROR" in buffer: level = "error"
                    elif "WARNING" in buffer: level = "warning"
                    
                    self.events.append({
                        "type": "log",
                        "content": buffer.strip(),
                        "time": current_time,
                        "level": level
                    })
                    buffer = ""
                current_time += 0.01 # Newline small delay
            else:
                buffer += char
                current_time += 0.0005 # Each char slight increment
                
        # Flush remaining
        if buffer.strip():
            self.events.append({
                "type": "log",
                "content": buffer.strip(),
                "time": current_time,
                "level": "info"
            })
            
        return self.events

# Test
if __name__ == "__main__":
    dummy_data = "[Initialization...]{OK}!Starting kernel..."
    parser = SerialLogParser()
    events = parser.parse(dummy_data)
    for e in events:
        print(f"[{e['time']:.4f}s] {e['type'].upper()}: {e['content']}")
