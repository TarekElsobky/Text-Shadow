import customtkinter as ctk
from tkinter import filedialog
import threading
import time
import os
from core.constants import COLORS
from ui.ui_widgets import HoverButton, LogBox
from core.steganography import SteganographyEngine


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, on_select, **kwargs):
        kwargs.setdefault("fg_color", COLORS["bg_panel"])
        kwargs.setdefault("corner_radius", 0)
        kwargs.setdefault("width", 250)
        super().__init__(master, **kwargs)
        self.on_select = on_select
        self.active = "hide"
        self._build()
    
    def _build(self):
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=(30, 40))
        ctk.CTkLabel(
            logo_frame,
            text="TEXT SHADOW",
            font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
            text_color=COLORS["cyan"]
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            logo_frame,
            text="Steganography Tool",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color=COLORS["text_dim"]
        ).pack(anchor="w")
        
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(fill="x", padx=15, pady=10)
        self.btn_hide = self._create_nav_button(
            nav_frame, "🔒  Hide Message", "hide"
        )
        self.btn_hide.pack(fill="x", pady=5)
        self.btn_extract = self._create_nav_button(
            nav_frame, "🔓  Extract Message", "extract"
        )
        self.btn_extract.pack(fill="x", pady=5)
        self._set_active("hide")
        
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        ctk.CTkLabel(
            bottom_frame,
            text="● Secure Encryption",
            font=ctk.CTkFont(size=10),
            text_color=COLORS["green"]
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            bottom_frame,
            text="AES-256 + Fernet",
            font=ctk.CTkFont(size=9),
            text_color=COLORS["text_dim"]
        ).pack(anchor="w")
    
    def _create_nav_button(self, parent, text, action):
        return ctk.CTkButton(
            parent,
            text=text,
            anchor="w",
            fg_color="transparent",
            hover_color="#1a2535",
            text_color=COLORS["text_main"],
            font=ctk.CTkFont(family="Consolas", size=13),
            height=45,
            corner_radius=8,
            command=lambda: self._on_click(action)
        )
    
    def _on_click(self, action):
        self._set_active(action)
        self.on_select(action)
    
    def _set_active(self, action):
        self.active = action
        if action == "hide":
            self.btn_hide.configure(
                fg_color="#1a2535",
                text_color=COLORS["cyan"],
                border_color=COLORS["cyan"],
                border_width=2
            )
            self.btn_extract.configure(
                fg_color="transparent",
                text_color=COLORS["text_main"],
                border_width=0
            )
        else:
            self.btn_extract.configure(
                fg_color="#1a2535",
                text_color=COLORS["cyan"],
                border_color=COLORS["cyan"],
                border_width=2
            )
            self.btn_hide.configure(
                fg_color="transparent",
                text_color=COLORS["text_main"],
                border_width=0
            )


class HidePanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("fg_color", COLORS["bg_dark"])
        super().__init__(master, **kwargs)
        self.log = None
        self._build()
    
    def set_logger(self, log):
        self.log = log
    
    def _build(self):
        self.main_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        
        header = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(30, 20))
        
        ctk.CTkLabel(
            header,
            text="Hide Message",
            font=ctk.CTkFont(family="Consolas", size=28, weight="bold"),
            text_color=COLORS["cyan"]
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header,
            text="Embed encrypted messages inside ordinary text using zero-width characters",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_dim"]
        ).pack(anchor="w", pady=(5, 0))
        
        content = ctk.CTkFrame(self.main_container, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=40, pady=20)
        
        left = ctk.CTkFrame(content, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        ctk.CTkLabel(
            left,
            text="ENCRYPTION KEY",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=COLORS["cyan"]
        ).pack(anchor="w", pady=(0, 5))
        
        self.key_entry = ctk.CTkEntry(
            left,
            placeholder_text="Enter a secret key (optional, auto-generated if empty)",
            fg_color=COLORS["bg_input"],
            border_color=COLORS["border"],
            text_color=COLORS["text_main"],
            height=40,
            font=ctk.CTkFont(size=12)
        )
        self.key_entry.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            left,
            text="SECRET MESSAGE",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=COLORS["cyan"]
        ).pack(anchor="w", pady=(0, 5))
        
        self.secret_text = ctk.CTkTextbox(
            left,
            height=150,
            fg_color=COLORS["bg_input"],
            border_color=COLORS["border"],
            text_color=COLORS["text_main"],
            font=ctk.CTkFont(size=12)
        )
        self.secret_text.pack(fill="x", pady=(0, 20))
        
        carrier_header = ctk.CTkFrame(left, fg_color="transparent")
        carrier_header.pack(fill="x", pady=(0, 5))
        
        ctk.CTkLabel(
            carrier_header,
            text="CARRIER TEXT",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=COLORS["cyan"]
        ).pack(side="left")
        
        import_btn = ctk.CTkButton(
            carrier_header,
            text="📁 Import File",
            width=100,
            height=28,
            fg_color="transparent",
            border_color=COLORS["border"],
            border_width=1,
            text_color=COLORS["text_dim"],
            font=ctk.CTkFont(size=11),
            command=self._import_file
        )
        import_btn.pack(side="right")
        
        self.carrier_text = ctk.CTkTextbox(
            left,
            height=150,
            fg_color=COLORS["bg_input"],
            border_color=COLORS["border"],
            text_color=COLORS["text_main"],
            font=ctk.CTkFont(size=12)
        )
        self.carrier_text.pack(fill="x", pady=(0, 20))
        
        self.generate_btn = HoverButton(
            left,
            text="GENERATE HIDDEN TEXT",
            fg_color=COLORS["cyan"],
            hover_color=COLORS["cyan_dim"],
            text_color=COLORS["bg_dark"],
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            height=48,
            corner_radius=8,
            command=self._generate
        )
        self.generate_btn.pack(fill="x", pady=(10, 0))
        
        right = ctk.CTkFrame(content, fg_color="transparent")
        right.pack(side="right", fill="both", expand=True)
        
        ctk.CTkLabel(
            right,
            text="OUTPUT",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=COLORS["cyan"]
        ).pack(anchor="w", pady=(0, 5))
        
        self.output_text = ctk.CTkTextbox(
            right,
            height=200,
            fg_color=COLORS["bg_card"],
            border_color=COLORS["border"],
            text_color=COLORS["green"],
            font=ctk.CTkFont(family="Consolas", size=12),
            state="disabled"
        )
        self.output_text.pack(fill="both", expand=True, pady=(0, 20))
        
        copy_btn = ctk.CTkButton(
            right,
            text="📋 Copy to Clipboard",
            height=40,
            fg_color="transparent",
            border_color=COLORS["border"],
            border_width=1,
            text_color=COLORS["text_main"],
            font=ctk.CTkFont(size=12),
            command=self._copy_output
        )
        copy_btn.pack(fill="x")
        
        stats = ctk.CTkFrame(right, fg_color=COLORS["bg_card"], corner_radius=8)
        stats.pack(fill="x", pady=(20, 0))
        
        self.stats_label = ctk.CTkLabel(
            stats,
            text="Ready to encode",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color=COLORS["text_dim"]
        )
        self.stats_label.pack(padx=15, pady=10)
    
    def _import_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.carrier_text.delete("1.0", "end")
                self.carrier_text.insert("1.0", content)
                if self.log:
                    self.log.log(f"Imported file: {os.path.basename(file_path)}", "SUCCESS")
            except Exception as e:
                if self.log:
                    self.log.log(f"Failed to import file: {e}", "ERROR")
    
    def _copy_output(self):
        output = self.output_text.get("1.0", "end-1c")
        if output:
            self.clipboard_clear()
            self.clipboard_append(output)
            if self.log:
                self.log.log("Output copied to clipboard", "SUCCESS")
    
    def _generate(self):
        key_text = self.key_entry.get().strip()
        secret = self.secret_text.get("1.0", "end-1c").strip()
        carrier = self.carrier_text.get("1.0", "end-1c").strip()
        
        if not secret:
            if self.log:
                self.log.log("Please enter a secret message", "ERROR")
            return
        if not carrier:
            if self.log:
                self.log.log("Please enter carrier text", "ERROR")
            return
        
        self.generate_btn.configure(state="disabled", text="PROCESSING...")
        thread = threading.Thread(
            target=self._process_generate,
            args=(key_text, secret, carrier),
            daemon=True
        )
        thread.start()
    
    def _process_generate(self, key_text, secret, carrier):
        try:
            if self.log:
                self.log.log("Starting encryption process...", "INFO")
                self.log.log(f"Secret message length: {len(secret)} characters", "INFO")
                self.log.log(f"Carrier text length: {len(carrier)} characters", "INFO")
            
            key = SteganographyEngine.generate_fernet_key(key_text.encode() if key_text else None)
            
            if self.log:
                self.log.log("Encrypting secret message...", "INFO")
            
            result = SteganographyEngine.hide_message(key, secret, carrier)
            
            if self.log:
                self.log.log(f"Success! Generated {len(result)} characters", "SUCCESS")
                self.log.log(f"Overhead: {len(result) - len(carrier)} zero-width chars", "INFO")
            
            self.after(0, self._update_output, result)
            
        except Exception as e:
            if self.log:
                self.log.log(f"Error: {str(e)}", "ERROR")
            self.after(0, self._reset_button)
    
    def _update_output(self, text):
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", text)
        self.output_text.configure(state="disabled")
        
        self.stats_label.configure(
            text=f"✓ Hidden message generated | Size: {len(text)} chars",
            text_color=COLORS["green"]
        )
        self._reset_button()
    
    def _reset_button(self):
        self.generate_btn.configure(state="normal", text="GENERATE HIDDEN TEXT")


class ExtractPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("fg_color", COLORS["bg_dark"])
        super().__init__(master, **kwargs)
        self.log = None
        self._build()
    
    def set_logger(self, log):
        self.log = log
    
    def _build(self):
        self.main_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        
        header = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(30, 20))
        
        ctk.CTkLabel(
            header,
            text="Extract Message",
            font=ctk.CTkFont(family="Consolas", size=28, weight="bold"),
            text_color=COLORS["cyan"]
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header,
            text="Extract hidden messages from text containing zero-width characters",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_dim"]
        ).pack(anchor="w", pady=(5, 0))
        
        content = ctk.CTkFrame(self.main_container, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=40, pady=20)
        
        left = ctk.CTkFrame(content, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        ctk.CTkLabel(
            left,
            text="ENCRYPTION KEY",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=COLORS["cyan"]
        ).pack(anchor="w", pady=(0, 5))
        
        self.key_entry = ctk.CTkEntry(
            left,
            placeholder_text="Enter the same key used for encryption",
            fg_color=COLORS["bg_input"],
            border_color=COLORS["border"],
            text_color=COLORS["text_main"],
            height=40,
            font=ctk.CTkFont(size=12)
        )
        self.key_entry.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            left,
            text="TEXT WITH HIDDEN MESSAGE",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=COLORS["cyan"]
        ).pack(anchor="w", pady=(0, 5))
        
        self.combined_text = ctk.CTkTextbox(
            left,
            height=300,
            fg_color=COLORS["bg_input"],
            border_color=COLORS["border"],
            text_color=COLORS["text_main"],
            font=ctk.CTkFont(size=12)
        )
        self.combined_text.pack(fill="x", pady=(0, 20))
        
        self.extract_btn = HoverButton(
            left,
            text="EXTRACT MESSAGE",
            fg_color=COLORS["cyan"],
            hover_color=COLORS["cyan_dim"],
            text_color=COLORS["bg_dark"],
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            height=48,
            corner_radius=8,
            command=self._extract
        )
        self.extract_btn.pack(fill="x", pady=(10, 0))
        
        right = ctk.CTkFrame(content, fg_color="transparent")
        right.pack(side="right", fill="both", expand=True)
        
        ctk.CTkLabel(
            right,
            text="EXTRACTED MESSAGE",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=COLORS["cyan"]
        ).pack(anchor="w", pady=(0, 5))
        
        self.result_text = ctk.CTkTextbox(
            right,
            height=300,
            fg_color=COLORS["bg_card"],
            border_color=COLORS["border"],
            text_color=COLORS["green"],
            font=ctk.CTkFont(size=12),
            state="disabled"
        )
        self.result_text.pack(fill="both", expand=True, pady=(0, 20))
        
        copy_btn = ctk.CTkButton(
            right,
            text="📋 Copy to Clipboard",
            height=40,
            fg_color="transparent",
            border_color=COLORS["border"],
            border_width=1,
            text_color=COLORS["text_main"],
            font=ctk.CTkFont(size=12),
            command=self._copy_result
        )
        copy_btn.pack(fill="x")
        
        info = ctk.CTkFrame(right, fg_color=COLORS["bg_card"], corner_radius=8)
        info.pack(fill="x", pady=(20, 0))
        
        self.info_label = ctk.CTkLabel(
            info,
            text="Ready to extract",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color=COLORS["text_dim"]
        )
        self.info_label.pack(padx=15, pady=10)
    
    def _copy_result(self):
        result = self.result_text.get("1.0", "end-1c")
        if result:
            self.clipboard_clear()
            self.clipboard_append(result)
            if self.log:
                self.log.log("Extracted message copied to clipboard", "SUCCESS")
    
    def _extract(self):
        key_text = self.key_entry.get().strip()
        combined = self.combined_text.get("1.0", "end-1c").strip()
        
        if not combined:
            if self.log:
                self.log.log("Please enter text to extract from", "ERROR")
            return
        
        self.extract_btn.configure(state="disabled", text="EXTRACTING...")
        thread = threading.Thread(
            target=self._process_extract,
            args=(key_text, combined),
            daemon=True
        )
        thread.start()
    
    def _process_extract(self, key_text, combined):
        try:
            if self.log:
                self.log.log("Starting extraction process...", "INFO")
                self.log.log(f"Analyzing {len(combined)} characters...", "INFO")
                if SteganographyEngine.has_zero_width_chars(combined):
                    self.log.log("Zero-width characters detected", "SUCCESS")
                else:
                    self.log.log("No zero-width characters found in text", "WARNING")
            
            key = SteganographyEngine.generate_fernet_key(key_text.encode() if key_text else None)
            
            if self.log:
                self.log.log("Decrypting message...", "INFO")
            
            result = SteganographyEngine.extract_message(key, combined)
            
            if self.log:
                self.log.log(f"Success! Extracted {len(result)} characters", "SUCCESS")
            
            self.after(0, self._update_result, result)
            
        except Exception as e:
            if self.log:
                self.log.log(f"Extraction failed: {str(e)}", "ERROR")
            self.after(0, self._reset_button)
    
    def _update_result(self, text):
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", text)
        self.result_text.configure(state="disabled")
        
        self.info_label.configure(
            text=f"✓ Message extracted successfully | {len(text)} characters",
            text_color=COLORS["green"]
        )
        self._reset_button()
    
    def _reset_button(self):
        self.extract_btn.configure(state="normal", text="EXTRACT MESSAGE")
