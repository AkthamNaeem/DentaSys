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
        
        # Single toggle button
        self.toggle_btn = ttk.Button(
            self.frame,
            text=self.get_toggle_text(),
            command=self.toggle_language,
            style='Success.TButton'
        )
        self.toggle_btn.pack(side='left', ipadx=15, ipady=6)
        
    def get_toggle_text(self):
        """Get the text for the toggle button based on current language"""
        current_lang = translations.get_current_language()
        if current_lang == 'en':
            return "🌐 العربية"  # Show Arabic when current is English
        else:
            return "🌐 English"  # Show English when current is Arabic
            
    def toggle_language(self):
        """Toggle between English and Arabic"""
        current_lang = translations.get_current_language()
        new_lang = 'ar' if current_lang == 'en' else 'en'
        translations.set_language(new_lang)
        
    def update_ui(self):
        """Update UI elements when language changes"""
        # Update label text
        self.language_label.config(text=translations.get('language_switch'))
        
        # Update toggle button text
        self.toggle_btn.config(text=self.get_toggle_text())
        
        # Update text direction for Arabic
        current_lang = translations.get_current_language()
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