import tkinter as tk
from tkinter import ttk
import threading
from gui.pages.home_page import HomePage
from gui.pages.doctors_page import DoctorsPage
from gui.pages.patients_page import PatientsPage
from gui.pages.records_page import RecordsPage
from gui.widgets.language_switch import LanguageSwitch
from gui.styles import apply_styles
from database.schema import create_schema
from localization.translations import translations


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(translations.get('app_title'))
        
        # Set full-screen mode by default
        self.root.state('zoomed')  # Windows
        # For cross-platform compatibility
        try:
            self.root.attributes('-zoomed', True)  # Linux
        except:
            pass
        try:
            self.root.attributes('-fullscreen', False)  # Keep windowed but maximized
        except:
            pass
        
        # Set minimum size for when not maximized
        self.root.minsize(1200, 800)
        
        # Initialize database
        create_schema()
        
        # Apply modern styling
        apply_styles(self.root)
        
        # Register for language change notifications
        translations.add_observer(self.update_ui)
        
        # Create main container
        self.setup_ui()
        
        # Initialize pages
        self.setup_pages()
        
        # Apply initial RTL/LTR layout
        self.apply_text_direction()
        
    def setup_ui(self):
        # Main container with minimal padding for full width usage
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        
        # Header frame with minimal padding
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.header_frame.columnconfigure(1, weight=1)
        
        # Left side - Title and subtitle
        title_frame = ttk.Frame(self.header_frame)
        title_frame.grid(row=0, column=0, sticky="w")
        
        # Application title with better sizing
        self.title_label = ttk.Label(
            title_frame, 
            text="DentaSys", 
            font=("Segoe UI", 28, "bold"),
            foreground="#2c3e50"
        )
        self.title_label.pack(anchor='w')
        
        # Right side - Language switch
        language_frame = ttk.Frame(self.header_frame)
        language_frame.grid(row=0, column=1, sticky="e")
        
        # Language switch widget
        self.language_switch = LanguageSwitch(language_frame)
        self.language_switch.frame.pack(anchor='e')
        
        # Create notebook for tabs with full width
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=1, column=0, sticky="nsew")
        
    def setup_pages(self):
        # Home Page
        self.home_page = HomePage(self.notebook)
        self.notebook.add(self.home_page.frame, text=translations.get('tab_home'), padding=0)
        
        # Doctors Page
        self.doctors_page = DoctorsPage(self.notebook)
        self.notebook.add(self.doctors_page.frame, text=translations.get('tab_doctors'), padding=0)
        
        # Patients Page
        self.patients_page = PatientsPage(self.notebook)
        self.notebook.add(self.patients_page.frame, text=translations.get('tab_patients'), padding=0)
        
        # Records Page
        self.records_page = RecordsPage(self.notebook)
        self.notebook.add(self.records_page.frame, text=translations.get('tab_records'), padding=0)
        
    def apply_text_direction(self):
        """Apply RTL or LTR text direction based on current language"""
        is_rtl = translations.is_rtl()
        
        try:
            if is_rtl:
                # Configure RTL layout for Arabic
                self.root.option_add('*TLabel.justify', 'right')
                self.root.option_add('*TButton.justify', 'right')
                self.root.option_add('*TEntry.justify', 'right')
                
                # Update header layout for RTL
                self.title_label.pack(anchor='e')
                self.language_switch.frame.pack(anchor='w')
                
                # Reconfigure header grid for RTL
                title_frame = self.title_label.master
                language_frame = self.language_switch.frame.master
                title_frame.grid(row=0, column=1, sticky="e")
                language_frame.grid(row=0, column=0, sticky="w")
                
            else:
                # Configure LTR layout for English
                self.root.option_add('*TLabel.justify', 'left')
                self.root.option_add('*TButton.justify', 'left')
                self.root.option_add('*TEntry.justify', 'left')
                
                # Update header layout for LTR
                self.title_label.pack(anchor='w')
                self.language_switch.frame.pack(anchor='e')
                
                # Reconfigure header grid for LTR
                title_frame = self.title_label.master
                language_frame = self.language_switch.frame.master
                title_frame.grid(row=0, column=0, sticky="w")
                language_frame.grid(row=0, column=1, sticky="e")
                
        except Exception as e:
            print(f"Error applying text direction: {e}")
        
    def update_ui(self):
        """Update UI elements when language changes"""
        # Update window title
        self.root.title(translations.get('app_title'))
        
        # Update tab texts
        self.notebook.tab(0, text=translations.get('tab_home'))
        self.notebook.tab(1, text=translations.get('tab_doctors'))
        self.notebook.tab(2, text=translations.get('tab_patients'))
        self.notebook.tab(3, text=translations.get('tab_records'))
        
        # Apply text direction changes
        self.apply_text_direction()
        
        # Force UI refresh
        self.root.update_idletasks()
        
    def run(self):
        self.root.mainloop()