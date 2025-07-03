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
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Initialize database
        create_schema()
        
        # Apply modern styling
        apply_styles(self.root)
        
        # Create main container
        self.setup_ui()
        
        # Initialize pages
        self.setup_pages()
        
    def setup_ui(self):
        # Main container with padding
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        
        # Header frame
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.header_frame.columnconfigure(1, weight=1)
        
        # Application title
        title_label = ttk.Label(
            self.header_frame, 
            text="DentaSys", 
            font=("Segoe UI", 24, "bold"),
            foreground="#2c3e50"
        )
        title_label.grid(row=0, column=0, sticky="w")
        
        # Subtitle
        subtitle_label = ttk.Label(
            self.header_frame, 
            text="Dental Treatment Center Management System", 
            font=("Segoe UI", 10),
            foreground="#7f8c8d"
        )
        subtitle_label.grid(row=1, column=0, sticky="w")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=1, column=0, sticky="nsew")
        
    def setup_pages(self):
        # Home Page
        self.home_page = HomePage(self.notebook)
        self.notebook.add(self.home_page.frame, text="🏠 Home", padding=10)
        
        # Doctors Page
        self.doctors_page = DoctorsPage(self.notebook)
        self.notebook.add(self.doctors_page.frame, text="👨‍⚕️ Doctors", padding=10)
        
        # Patients Page
        self.patients_page = PatientsPage(self.notebook)
        self.notebook.add(self.patients_page.frame, text="👤 Patients", padding=10)
        
        # Records Page
        self.records_page = RecordsPage(self.notebook)
        self.notebook.add(self.records_page.frame, text="📋 Records", padding=10)
        
    def run(self):
        self.root.mainloop()