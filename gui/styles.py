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
    
    # Configure Notebook (tabs)
    style.configure('TNotebook', 
                   background=colors['light'],
                   borderwidth=0)
    
    style.configure('TNotebook.Tab',
                   background=colors['white'],
                   foreground=colors['secondary'],
                   padding=[20, 10],
                   font=('Segoe UI', 10, 'normal'))
    
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
    
    # Configure Labels
    style.configure('TLabel',
                   background=colors['white'],
                   foreground=colors['secondary'],
                   font=('Segoe UI', 9))
    
    style.configure('Heading.TLabel',
                   background=colors['white'],
                   foreground=colors['secondary'],
                   font=('Segoe UI', 12, 'bold'))
    
    style.configure('Title.TLabel',
                   background=colors['white'],
                   foreground=colors['primary'],
                   font=('Segoe UI', 16, 'bold'))
    
    # Configure Entry widgets
    style.configure('TEntry',
                   fieldbackground=colors['white'],
                   borderwidth=1,
                   relief='solid',
                   padding=8,
                   font=('Segoe UI', 9))
    
    style.map('TEntry',
              focuscolor=[('!focus', colors['gray_light']),
                         ('focus', colors['primary'])])
    
    # Configure Buttons
    style.configure('TButton',
                   background=colors['primary'],
                   foreground=colors['white'],
                   borderwidth=0,
                   padding=[15, 8],
                   font=('Segoe UI', 9, 'bold'))
    
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
    
    # Configure Treeview
    style.configure('Treeview',
                   background=colors['white'],
                   foreground=colors['secondary'],
                   fieldbackground=colors['white'],
                   borderwidth=1,
                   relief='solid',
                   font=('Segoe UI', 9))
    
    style.configure('Treeview.Heading',
                   background=colors['light'],
                   foreground=colors['secondary'],
                   borderwidth=1,
                   relief='solid',
                   font=('Segoe UI', 9, 'bold'))
    
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