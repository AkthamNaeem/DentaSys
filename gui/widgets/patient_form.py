import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, date
import re


class PatientForm:
    def __init__(self, parent, title="Patient Form", patient=None):
        self.parent = parent
        self.patient = patient
        self.result = None
        
        # Create dialog window with better size
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("550x650")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.center_dialog()
        
        # Setup UI
        self.setup_ui()
        
        # Pre-fill if editing
        if self.patient:
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
        
        self.dialog.geometry(f"550x650+{x}+{y}")
        
    def setup_ui(self):
        # Main frame with padding
        main_frame = ttk.Frame(self.dialog, padding=30)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_text = "Edit Patient" if self.patient else "Add New Patient"
        title_label = ttk.Label(main_frame, text=title_text, font=('Segoe UI', 16, 'bold'))
        title_label.pack(pady=(0, 30))
        
        # Form fields frame
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill='both', expand=True, pady=(0, 30))
        
        # Name field
        name_label = ttk.Label(fields_frame, text="Patient Name *", font=('Segoe UI', 11, 'bold'))
        name_label.pack(anchor='w', pady=(0, 8))
        
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(fields_frame, textvariable=self.name_var, font=('Segoe UI', 11))
        self.name_entry.pack(fill='x', pady=(0, 20), ipady=8)
        
        # Phone field
        phone_label = ttk.Label(fields_frame, text="Phone Number *", font=('Segoe UI', 11, 'bold'))
        phone_label.pack(anchor='w', pady=(0, 8))
        
        self.phone_var = tk.StringVar()
        self.phone_entry = ttk.Entry(fields_frame, textvariable=self.phone_var, font=('Segoe UI', 11))
        self.phone_entry.pack(fill='x', pady=(0, 20), ipady=8)
        
        # Gender field
        gender_label = ttk.Label(fields_frame, text="Gender", font=('Segoe UI', 11, 'bold'))
        gender_label.pack(anchor='w', pady=(0, 8))
        
        self.gender_var = tk.StringVar()
        gender_frame = ttk.Frame(fields_frame)
        gender_frame.pack(fill='x', pady=(0, 20))
        
        self.gender_combo = ttk.Combobox(
            gender_frame, 
            textvariable=self.gender_var,
            values=['Male', 'Female'],
            state='readonly',
            font=('Segoe UI', 11),
            height=8
        )
        self.gender_combo.pack(fill='x', ipady=8)
        
        # Birth date field
        birth_date_label = ttk.Label(fields_frame, text="Birth Date", font=('Segoe UI', 11, 'bold'))
        birth_date_label.pack(anchor='w', pady=(0, 8))
        
        birth_date_frame = ttk.Frame(fields_frame)
        birth_date_frame.pack(fill='x', pady=(0, 20))
        
        try:
            # Try to use DateEntry (tkcalendar)
            self.birth_date_entry = DateEntry(
                birth_date_frame,
                width=12,
                background='darkblue',
                foreground='white',
                borderwidth=2,
                date_pattern='yyyy-mm-dd',
                font=('Segoe UI', 11)
            )
            self.birth_date_entry.pack(fill='x', ipady=8)
            self.has_date_picker = True
        except ImportError:
            # Fallback to regular entry if tkcalendar is not available
            self.birth_date_var = tk.StringVar()
            self.birth_date_entry = ttk.Entry(
                birth_date_frame, 
                textvariable=self.birth_date_var,
                font=('Segoe UI', 11)
            )
            self.birth_date_entry.pack(fill='x', ipady=8)
            
            # Add format hint
            hint_label = ttk.Label(
                birth_date_frame, 
                text="Format: YYYY-MM-DD (e.g., 1990-01-15)",
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
        save_text = "Update" if self.patient else "Save"
        save_btn = ttk.Button(
            buttons_frame, 
            text=save_text, 
            command=self.save,
            style='Success.TButton'
        )
        save_btn.pack(side='right', ipadx=20, ipady=8)
        
        # Bind Enter key to save (only for single-line entries)
        self.name_entry.bind('<Return>', lambda e: self.save())
        self.phone_entry.bind('<Return>', lambda e: self.save())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
        
    def populate_fields(self):
        """Populate fields when editing"""
        if self.patient:
            self.name_var.set(self.patient.name or "")
            self.phone_var.set(self.patient.phone or "")
            self.gender_var.set(self.patient.gender or "")
            
            # Set birth date
            if self.patient.birth_date:
                if self.has_date_picker:
                    self.birth_date_entry.set_date(self.patient.birth_date)
                else:
                    self.birth_date_var.set(self.patient.birth_date.strftime("%Y-%m-%d"))
                    
            # Set notes
            if self.patient.notes:
                self.notes_text.insert('1.0', self.patient.notes)
                
    def validate_form(self):
        """Validate form data"""
        errors = []
        
        # Validate name
        name = self.name_var.get().strip()
        if not name:
            errors.append("Patient name is required")
        elif len(name) < 2:
            errors.append("Patient name must be at least 2 characters")
        elif len(name) > 100:
            errors.append("Patient name must be less than 100 characters")
            
        # Validate phone
        phone = self.phone_var.get().strip()
        if not phone:
            errors.append("Phone number is required")
        else:
            # Remove common phone formatting characters
            phone_clean = re.sub(r'[^\d+]', '', phone)
            if len(phone_clean) < 10:
                errors.append("Phone number must be at least 10 digits")
            elif len(phone_clean) > 15:
                errors.append("Phone number must be less than 15 digits")
            elif not re.match(r'^[\d+\-\s\(\)\.]+$', phone):
                errors.append("Phone number contains invalid characters")
                
        # Validate birth date
        birth_date = None
        if self.has_date_picker:
            try:
                birth_date = self.birth_date_entry.get_date()
                if birth_date > date.today():
                    errors.append("Birth date cannot be in the future")
            except:
                pass  # Birth date is optional
        else:
            birth_date_str = self.birth_date_var.get().strip()
            if birth_date_str:
                try:
                    birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
                    if birth_date > date.today():
                        errors.append("Birth date cannot be in the future")
                except ValueError:
                    errors.append("Birth date must be in YYYY-MM-DD format")
                    
        return errors
        
    def save(self):
        """Save the patient data"""
        # Validate form
        errors = self.validate_form()
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return
            
        # Prepare data
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        gender = self.gender_var.get() or None
        notes = self.notes_text.get('1.0', 'end-1c').strip() or None
        
        # Get birth date
        birth_date = None
        if self.has_date_picker:
            try:
                birth_date = self.birth_date_entry.get_date()
            except:
                pass
        else:
            birth_date_str = self.birth_date_var.get().strip()
            if birth_date_str:
                try:
                    birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
                except ValueError:
                    pass
        
        # Set result
        self.result = {
            'name': name,
            'phone': phone,
            'gender': gender,
            'birth_date': birth_date,
            'notes': notes
        }
        
        # Close dialog
        self.dialog.destroy()
        
    def cancel(self):
        """Cancel the dialog"""
        self.result = None
        self.dialog.destroy()