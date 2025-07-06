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
        
        # Single toggle button
        self.toggle_btn = ttk.Button(
            self.frame,
            text=self.get_toggle_text(),
            command=self.toggle_language,
            style='Success.TButton'
        )
        
        # Pack elements based on current language direction
        self.pack_elements()
        
    def pack_elements(self):
        """Pack elements based on text direction"""
        # Clear existing packing
        for widget in self.frame.winfo_children():
            widget.pack_forget()
            
        is_rtl = translations.is_rtl()
        
        if is_rtl:
            # RTL layout: button first, then label
            self.toggle_btn.pack(side='right', ipadx=15, ipady=6)
            self.language_label.pack(side='right', padx=(10, 0))
        else:
            # LTR layout: label first, then button
            self.language_label.pack(side='left', padx=(0, 10))
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
        
        # Repack elements for new direction
        self.pack_elements()
        
        # Apply text direction styles
        is_rtl = translations.is_rtl()
        try:
            if is_rtl:
                self.language_label.config(anchor='e')
                self.toggle_btn.config(anchor='e')
            else:
                self.language_label.config(anchor='w')
                self.toggle_btn.config(anchor='w')
        except Exception as e:
            print(f"Error updating language switch direction: {e}")