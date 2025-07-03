import tkinter as tk
from tkinter import ttk


class PatientsPage:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        self.frame = ttk.Frame(self.parent)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        # Placeholder content
        placeholder_label = ttk.Label(
            self.frame, 
            text="Patients Management\n(Coming Soon)", 
            style='Title.TLabel',
            anchor='center'
        )
        placeholder_label.grid(row=0, column=0, sticky="nsew")