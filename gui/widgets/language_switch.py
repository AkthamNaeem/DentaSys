import tkinter as tk
from tkinter import ttk
from localization.translations import translations


class LanguageSwitch:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
        
        # Register for language change notifications
        translations.add_observer(self.update_ui)
        
    def setup_ui(self):
        # Language switch frame
        self.frame = ttk.Frame(self.parent)
        
        # Language label
        self.language_label = ttk.Label(
            self.frame,
            text=translations.get('language_switch'),
            font=('Segoe UI', 10, 'bold'),
            foreground='#2c3e50'
        )
        self.language_label.pack(side='left', padx=(0, 10))
        
        # Language buttons frame
        buttons_frame = ttk.Frame(self.frame)
        buttons_frame.pack(side='left')
        
        # English button
        self.english_btn = ttk.Button(
            buttons_frame,
            text="English",
            command=lambda: self.switch_language('en'),
            style='TButton' if translations.get_current_language() != 'en' else 'Success.TButton'
        )
        self.english_btn.pack(side='left', padx=(0, 5), ipadx=10, ipady=4)
        
        # Arabic button
        self.arabic_btn = ttk.Button(
            buttons_frame,
            text="العربية",
            command=lambda: self.switch_language('ar'),
            style='TButton' if translations.get_current_language() != 'ar' else 'Success.TButton'
        )
        self.arabic_btn.pack(side='left', ipadx=10, ipady=4)
        
    def switch_language(self, language_code):
        """Switch to the specified language"""
        translations.set_language(language_code)
        
    def update_ui(self):
        """Update UI elements when language changes"""
        # Update label text
        self.language_label.config(text=translations.get('language_switch'))
        
        # Update button styles based on current language
        current_lang = translations.get_current_language()
        
        self.english_btn.config(
            style='Success.TButton' if current_lang == 'en' else 'TButton'
        )
        self.arabic_btn.config(
            style='Success.TButton' if current_lang == 'ar' else 'TButton'
        )
        
        # Update text direction for Arabic
        if current_lang == 'ar':
            try:
                self.parent.option_add('*TLabel.anchor', 'e')
                self.parent.option_add('*TButton.anchor', 'e')
            except:
                pass
        else:
            try:
                self.parent.option_add('*TLabel.anchor', 'w')
                self.parent.option_add('*TButton.anchor', 'w')
            except:
                pass