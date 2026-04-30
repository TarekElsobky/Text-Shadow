import customtkinter as ctk
from core.constants import COLORS
import time


class HoverButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, event=None):
        self.configure(border_color=COLORS["cyan"], border_width=2)
    
    def _on_leave(self, event=None):
        self.configure(border_color=COLORS["border"], border_width=1)


class LogBox(ctk.CTkTextbox):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("fg_color", "#050b14")
        kwargs.setdefault("border_color", COLORS["border"])
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("height", 120)
        kwargs.setdefault("font", ctk.CTkFont(family="Consolas", size=11))
        super().__init__(master, **kwargs)
        self.configure(state="disabled")
        self.tag_config("timestamp", foreground=COLORS["text_dim"])
        self.tag_config("info", foreground=COLORS["cyan_dim"])
        self.tag_config("success", foreground=COLORS["green"])
        self.tag_config("error", foreground=COLORS["red"])
        self.tag_config("warning", foreground=COLORS["yellow"])
        self.tag_config("message", foreground=COLORS["text_main"])
    
    def log(self, message: str, level: str = "INFO"):
        self.configure(state="normal")
        timestamp = time.strftime("%H:%M:%S")
        level_lower = level.lower()
        if level_lower not in ["info", "success", "error", "warning"]:
            level_lower = "info"
        self.insert("end", f"[{timestamp}] ", "timestamp")
        self.insert("end", f"[{level}] ", level_lower)
        self.insert("end", f"{message}\n", "message")
        self.configure(state="disabled")
        self.see("end")
    
    def clear(self):
        self.configure(state="normal")
        self.delete("1.0", "end")
        self.configure(state="disabled")
