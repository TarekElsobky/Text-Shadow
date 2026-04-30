import customtkinter as ctk
import os
from core.constants import COLORS
from ui.ui_panels import Sidebar, HidePanel, ExtractPanel
from ui.ui_widgets import LogBox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SteganoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Text Shadow - Steganography Tool")
        self.geometry("1300x800")
        self.minsize(1100, 700)
        self.configure(fg_color=COLORS["bg_dark"])
        try:
            self.iconbitmap(os.path.join(os.path.dirname(__file__), "eyes.ico"))
        except:
            pass  # Skip icon if not found
        self._build()
    
    def _build(self):
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        self.sidebar = Sidebar(main_container, self._switch_panel)
        self.sidebar.pack(side="left", fill="y")
        
        divider = ctk.CTkFrame(main_container, width=1, fg_color=COLORS["border"])
        divider.pack(side="left", fill="y")
        
        right_area = ctk.CTkFrame(main_container, fg_color="transparent")
        right_area.pack(side="left", fill="both", expand=True)
        
        self.content_frame = ctk.CTkFrame(right_area, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        self.panels = {
            "hide": HidePanel(self.content_frame),
            "extract": ExtractPanel(self.content_frame)
        }
        
        log_frame = ctk.CTkFrame(right_area, fg_color="transparent")
        log_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            log_frame,
            text="LIVE LOGS",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=COLORS["cyan"]
        ).pack(anchor="w", pady=(0, 5))
        
        self.shared_log_box = LogBox(log_frame, height=120)
        self.shared_log_box.pack(fill="x")
        
        self.panels["hide"].set_logger(self.shared_log_box)
        self.panels["extract"].set_logger(self.shared_log_box)
        
        self._switch_panel("hide")
        
        self.shared_log_box.log("Application started successfully", "SUCCESS")
        self.shared_log_box.log("Ready to hide or extract messages", "INFO")
        self.shared_log_box.log("Use the sidebar to switch between modes", "INFO")
    
    def _switch_panel(self, panel_name):
        for panel in self.panels.values():
            panel.pack_forget()
        
        self.panels[panel_name].pack(fill="both", expand=True)
        self.shared_log_box.log(f"Switched to {panel_name} mode", "INFO")


if __name__ == "__main__":
    app = SteganoApp()
    app.mainloop()
