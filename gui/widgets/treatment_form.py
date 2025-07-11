import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, date
import re


class TreatmentForm:
    def __init__(self, parent, title="Treatment Form", treatment=None, record_id=None):
        self.parent = parent
        self.treatment = treatment
        self.record_id = record_id
        self.result = None
        
        # Create dialog window with better size
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("550x550")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.center_dialog()
        
        # Setup UI
        self.setup_ui()
        
        # Pre-fill if editing
        if self.treatment:
            self.populate_fields()
            
        # Focus on first field
        self.name_entry.focus()
        
        # Wait for dialog to close
        self.dialog.wait_window()
        
    def center_dialog(self):
        """Center the dialog on the parent window"""
        self.dialog.update_idletasks()
        
        # Get parent window position and size
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Calculate center position
        dialog_width = self.dialog.winfo_reqwidth()
        dialog_height = self.dialog.winfo_reqheight()
        
        x = parent_x + (parent_width // 2) - (dialog_width // 2)
        y = parent_y + (parent_height // 2) - (dialog_height // 2)
        
        self.dialog.geometry(f"550x550+{x}+{y}")
        
    def setup_ui(self):
        # Main frame with padding
        main_frame = ttk.Frame(self.dialog, padding=30)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_text = "Edit Treatment" if self.treatment else "Add New Treatment"
        title_label = ttk.Label(main_frame, text=title_text, font=('Segoe UI', 16, 'bold'))
        title_label.pack(pady=(0, 30))
        
        # Form fields frame
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill='both', expand=True, pady=(0, 30))
        
        # Treatment name field
        name_label = ttk.Label(fields_frame, text="Treatment Name *", font=('Segoe UI', 11, 'bold'))
        name_label.pack(anchor='w', pady=(0, 8))
        
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(fields_frame, textvariable=self.name_var, font=('Segoe UI', 11))
        self.name_entry.pack(fill='x', pady=(0, 20), ipady=8)
        
        # Cost field
        cost_label = ttk.Label(fields_frame, text="Cost *", font=('Segoe UI', 11, 'bold'))
        cost_label.pack(anchor='w', pady=(0, 8))
        
        self.cost_var = tk.StringVar()
        self.cost_entry = ttk.Entry(fields_frame, textvariable=self.cost_var, font=('Segoe UI', 11))
        self.cost_entry.pack(fill='x', pady=(0, 20), ipady=8)
        
        # Date field
        date_label = ttk.Label(fields_frame, text="Treatment Date", font=('Segoe UI', 11, 'bold'))
        date_label.pack(anchor='w', pady=(0, 8))
        
        date_frame = ttk.Frame(fields_frame)
        date_frame.pack(fill='x', pady=(0, 20))
        
        try:
            # Try to use DateEntry (tkcalendar)
            self.date_entry = DateEntry(
                date_frame,
                width=12,
                background='darkblue',
                foreground='white',
                borderwidth=2,
                date_pattern='yyyy-mm-dd',
                font=('Segoe UI', 11)
            )
            self.date_entry.pack(fill='x', ipady=8)
            self.has_date_picker = True
        except ImportError:
            # Fallback to regular entry if tkcalendar is not available
            self.date_var = tk.StringVar()
            self.date_entry = ttk.Entry(
                date_frame, 
                textvariable=self.date_var,
                font=('Segoe UI', 11)
            )
            self.date_entry.pack(fill='x', ipady=8)
            
            # Add format hint
            hint_label = ttk.Label(
                date_frame, 
                text="Format: YYYY-MM-DD (e.g., 2024-01-15)",
                font=('Segoe UI', 9),
                foreground='#7f8c8d'
            )
            hint_label.pack(anchor='w', pady=(5, 0))
            self.has_date_picker = False
        
        # Notes field
        notes_label = ttk.Label(fields_frame, text="Notes", font=('Segoe UI', 11, 'bold'))
        notes_label.pack(anchor='w', pady=(0, 8))
        
        notes_frame = ttk.Frame(fields_frame)
        notes_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        self.notes_text = tk.Text(
            notes_frame, 
            height=6, 
            font=('Segoe UI', 11),
            wrap='word'
        )
        notes_scrollbar = ttk.Scrollbar(notes_frame, orient='vertical', command=self.notes_text.yview)
        self.notes_text.configure(yscrollcommand=notes_scrollbar.set)
        
        self.notes_text.pack(side='left', fill='both', expand=True)
        notes_scrollbar.pack(side='right', fill='y')
        
        # Required fields note
        note_label = ttk.Label(fields_frame, text="* Required fields", font=('Segoe UI', 9), foreground='#e74c3c')
        note_label.pack(anchor='w', pady=(10, 0))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill='x', pady=(20, 0))
        
        # Cancel button
        cancel_btn = ttk.Button(
            buttons_frame, 
            text="Cancel", 
            command=self.cancel,
            style='TButton'
        )
        cancel_btn.pack(side='right', padx=(15, 0), ipadx=20, ipady=8)
        
        # Save button
        save_text = "Update" if self.treatment else "Save"
        save_btn = ttk.Button(
            buttons_frame, 
            text=save_text, 
            command=self.save,
            style='Success.TButton'
        )
        save_btn.pack(side='right', ipadx=20, ipady=8)
        
        # Bind Enter key to save (only for single-line entries)
        self.name_entry.bind('<Return>', lambda e: self.save())
        self.cost_entry.bind('<Return>', lambda e: self.save())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
        
    def populate_fields(self):
        """Populate fields when editing"""
        if self.treatment:
            self.name_var.set(self.treatment.name or "")
            self.cost_var.set(str(self.treatment.cost) if self.treatment.cost else "")
            
            # Set date
            if self.treatment.date:
                if self.has_date_picker:
                    self.date_entry.set_date(self.treatment.date)
                else:
                    self.date_var.set(self.treatment.date.strftime("%Y-%m-%d"))
                    
            # Set notes
            if self.treatment.notes:
                self.notes_text.insert('1.0', self.treatment.notes)
                
    def validate_form(self):
        """Validate form data"""
        errors = []
        
        # Validate name
        name = self.name_var.get().strip()
        if not name:
            errors.append("Treatment name is required")
        elif len(name) < 2:
            errors.append("Treatment name must be at least 2 characters")
        elif len(name) > 200:
            errors.append("Treatment name must be less than 200 characters")
            
        # Validate cost
        cost_str = self.cost_var.get().strip()
        if not cost_str:
            errors.append("Cost is required")
        else:
            try:
                cost = float(cost_str)
                if cost < 0:
                    errors.append("Cost cannot be negative")
                elif cost > 999999.99:
                    errors.append("Cost is too large")
            except ValueError:
                errors.append("Cost must be a valid number")
                
        # Validate date
        treatment_date = None
        if self.has_date_picker:
            try:
                treatment_date = self.date_entry.get_date()
                if treatment_date > date.today():
                    errors.append("Treatment date cannot be in the future")
            except:
                pass  # Date is optional
        else:
            date_str = self.date_var.get().strip()
            if date_str:
                try:
                    treatment_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    if treatment_date > date.today():
                        errors.append("Treatment date cannot be in the future")
                except ValueError:
                    errors.append("Treatment date must be in YYYY-MM-DD format")
                    
        return errors
        
    def save(self):
        """Save the treatment data"""
        # Validate form
        errors = self.validate_form()
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return
            
        # Prepare data
        name = self.name_var.get().strip()
        cost = float(self.cost_var.get().strip())
        notes = self.notes_text.get('1.0', 'end-1c').strip() or None
        
        # Get date
        treatment_date = None
        if self.has_date_picker:
            try:
                treatment_date = self.date_entry.get_date()
            except:
                pass
        else:
            date_str = self.date_var.get().strip()
            if date_str:
                try:
                    treatment_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    pass
        
        # Set result
        self.result = {
            'name': name,
            'cost': cost,
            'date': treatment_date,
            'notes': notes
        }
        
        # Close dialog
        self.dialog.destroy()
        
    def cancel(self):
        """Cancel the dialog"""
        self.result = None
        self.dialog.destroy()