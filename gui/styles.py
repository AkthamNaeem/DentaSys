import tkinter as tk
from tkinter import ttk


def apply_styles(root):
    """Apply modern styling to the application"""
    
    # Create a style object
    style = ttk.Style()
    
    # Configure the theme
    style.theme_use('clam')
    
    # Define color palette
    colors = {
        'primary': '#3498db',
        'primary_dark': '#2980b9',
        'secondary': '#2c3e50',
        'success': '#27ae60',
        'warning': '#f39c12',
        'danger': '#e74c3c',
        'light': '#ecf0f1',
        'dark': '#34495e',
        'white': '#ffffff',
        'gray': '#95a5a6',
        'gray_light': '#bdc3c7'
    }
    
    # Configure Notebook (tabs) with better sizing
    style.configure('TNotebook', 
                   background=colors['light'],
                   borderwidth=0,
                   tabmargins=[2, 5, 2, 0])
    
    style.configure('TNotebook.Tab',
                   background=colors['white'],
                   foreground=colors['secondary'],
                   padding=[25, 12],
                   font=('Segoe UI', 11, 'normal'))
    
    style.map('TNotebook.Tab',
              background=[('selected', colors['primary']),
                         ('active', colors['primary_dark'])],
              foreground=[('selected', colors['white']),
                         ('active', colors['white'])])
    
    # Configure Frames
    style.configure('TFrame',
                   background=colors['white'])
    
    style.configure('Card.TFrame',
                   background=colors['white'],
                   relief='solid',
                   borderwidth=1)
    
    # Configure Labels with better typography
    style.configure('TLabel',
                   background=colors['white'],
                   foreground=colors['secondary'],
                   font=('Segoe UI', 10))
    
    style.configure('Heading.TLabel',
                   background=colors['white'],
                   foreground=colors['secondary'],
                   font=('Segoe UI', 14, 'bold'))
    
    style.configure('Title.TLabel',
                   background=colors['white'],
                   foreground=colors['primary'],
                   font=('Segoe UI', 18, 'bold'))
    
    # Configure Entry widgets with better sizing
    style.configure('TEntry',
                   fieldbackground=colors['white'],
                   borderwidth=1,
                   relief='solid',
                   padding=10,
                   font=('Segoe UI', 10))
    
    style.map('TEntry',
              focuscolor=[('!focus', colors['gray_light']),
                         ('focus', colors['primary'])])
    
    # Configure Buttons with better sizing
    style.configure('TButton',
                   background=colors['primary'],
                   foreground=colors['white'],
                   borderwidth=0,
                   padding=[18, 10],
                   font=('Segoe UI', 10, 'bold'))
    
    style.map('TButton',
              background=[('active', colors['primary_dark']),
                         ('pressed', colors['primary_dark'])])
    
    # Success button
    style.configure('Success.TButton',
                   background=colors['success'],
                   foreground=colors['white'])
    
    style.map('Success.TButton',
              background=[('active', '#229954'),
                         ('pressed', '#229954')])
    
    # Warning button
    style.configure('Warning.TButton',
                   background=colors['warning'],
                   foreground=colors['white'])
    
    style.map('Warning.TButton',
              background=[('active', '#d68910'),
                         ('pressed', '#d68910')])
    
    # Danger button
    style.configure('Danger.TButton',
                   background=colors['danger'],
                   foreground=colors['white'])
    
    style.map('Danger.TButton',
              background=[('active', '#c0392b'),
                         ('pressed', '#c0392b')])
    
    # Configure Treeview with better sizing
    style.configure('Treeview',
                   background=colors['white'],
                   foreground=colors['secondary'],
                   fieldbackground=colors['white'],
                   borderwidth=1,
                   relief='solid',
                   font=('Segoe UI', 10),
                   rowheight=25)
    
    style.configure('Treeview.Heading',
                   background=colors['light'],
                   foreground=colors['secondary'],
                   borderwidth=1,
                   relief='solid',
                   font=('Segoe UI', 10, 'bold'))
    
    style.map('Treeview',
              background=[('selected', colors['primary'])],
              foreground=[('selected', colors['white'])])
    
    # Configure Scrollbar
    style.configure('Vertical.TScrollbar',
                   background=colors['light'],
                   troughcolor=colors['light'],
                   borderwidth=0,
                   arrowcolor=colors['gray'],
                   darkcolor=colors['light'],
                   lightcolor=colors['light'])
    
    # Configure Combobox
    style.configure('TCombobox',
                   fieldbackground=colors['white'],
                   background=colors['white'],
                   borderwidth=1,
                   relief='solid',
                   padding=10,
                   font=('Segoe UI', 10))
    
    style.map('TCombobox',
              focuscolor=[('!focus', colors['gray_light']),
                         ('focus', colors['primary'])])