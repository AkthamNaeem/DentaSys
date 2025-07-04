import tkinter as tk
from tkinter import ttk
import threading
from gui.pages.home_page import HomePage
from gui.pages.doctors_page import DoctorsPage
from gui.pages.patients_page import PatientsPage
from gui.pages.records_page import RecordsPage
from gui.styles import apply_styles
from database.schema import create_schema


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DentaSys - Dental Treatment Center Management")
        
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
        
        # Create main container
        self.setup_ui()
        
        # Initialize pages
        self.setup_pages()
        
    def setup_ui(self):
        # Main container with optimized padding
        self.main_frame = ttk.Frame(self.root, padding="15")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        
        # Header frame with better proportions
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        self.header_frame.columnconfigure(1, weight=1)
        
        # Application title with better sizing
        title_label = ttk.Label(
            self.header_frame, 
            text="DentaSys", 
            font=("Segoe UI", 28, "bold"),
            foreground="#2c3e50"
        )
        title_label.grid(row=0, column=0, sticky="w")
        
        # Subtitle with improved spacing
        subtitle_label = ttk.Label(
            self.header_frame, 
            text="Dental Treatment Center Management System", 
            font=("Segoe UI", 12),
            foreground="#7f8c8d"
        )
        subtitle_label.grid(row=1, column=0, sticky="w", pady=(5, 0))
        
        # Create notebook for tabs with better sizing
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=1, column=0, sticky="nsew")
        
    def setup_pages(self):
        # Home Page
        self.home_page = HomePage(self.notebook)
        self.notebook.add(self.home_page.frame, text="🏠 Home", padding=15)
        
        # Doctors Page
        self.doctors_page = DoctorsPage(self.notebook)
        self.notebook.add(self.doctors_page.frame, text="👨‍⚕️ Doctors", padding=15)
        
        # Patients Page
        self.patients_page = PatientsPage(self.notebook)
        self.notebook.add(self.patients_page.frame, text="👤 Patients", padding=15)
        
        # Records Page
        self.records_page = RecordsPage(self.notebook)
        self.notebook.add(self.records_page.frame, text="📋 Records", padding=15)
        
    def run(self):
        self.root.mainloop()