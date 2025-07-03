import tkinter as tk
from tkinter import ttk, messagebox
import re


class DoctorForm:
    def __init__(self, parent, title="Doctor Form", doctor=None):
        self.parent = parent
        self.doctor = doctor
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.center_dialog()
        
        # Setup UI
        self.setup_ui()
        
        # Pre-fill if editing
        if self.doctor:
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
        
        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
    def setup_ui(self):
        # Main frame with padding
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_text = "Edit Doctor" if self.doctor else "Add New Doctor"
        title_label = ttk.Label(main_frame, text=title_text, font=('Segoe UI', 14, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Form fields frame
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill='x', pady=(0, 20))
        
        # Name field
        name_label = ttk.Label(fields_frame, text="Doctor Name *", font=('Segoe UI', 9, 'bold'))
        name_label.pack(anchor='w', pady=(0, 5))
        
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(fields_frame, textvariable=self.name_var, font=('Segoe UI', 10))
        self.name_entry.pack(fill='x', pady=(0, 15))
        
        # Phone field
        phone_label = ttk.Label(fields_frame, text="Phone Number", font=('Segoe UI', 9, 'bold'))
        phone_label.pack(anchor='w', pady=(0, 5))
        
        self.phone_var = tk.StringVar()
        self.phone_entry = ttk.Entry(fields_frame, textvariable=self.phone_var, font=('Segoe UI', 10))
        self.phone_entry.pack(fill='x', pady=(0, 15))
        
        # Required fields note
        note_label = ttk.Label(fields_frame, text="* Required fields", font=('Segoe UI', 8), foreground='#e74c3c')
        note_label.pack(anchor='w')
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill='x')
        
        # Cancel button
        cancel_btn = ttk.Button(
            buttons_frame, 
            text="Cancel", 
            command=self.cancel,
            style='TButton'
        )
        cancel_btn.pack(side='right', padx=(10, 0))
        
        # Save button
        save_text = "Update" if self.doctor else "Save"
        save_btn = ttk.Button(
            buttons_frame, 
            text=save_text, 
            command=self.save,
            style='Success.TButton'
        )
        save_btn.pack(side='right')
        
        # Bind Enter key to save
        self.dialog.bind('<Return>', lambda e: self.save())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
        
    def populate_fields(self):
        """Populate fields when editing"""
        if self.doctor:
            self.name_var.set(self.doctor.name or "")
            self.phone_var.set(self.doctor.phone or "")
            
    def validate_form(self):
        """Validate form data"""
        errors = []
        
        # Validate name
        name = self.name_var.get().strip()
        if not name:
            errors.append("Doctor name is required")
        elif len(name) < 2:
            errors.append("Doctor name must be at least 2 characters")
        elif len(name) > 100:
            errors.append("Doctor name must be less than 100 characters")
            
        # Validate phone (optional but if provided, must be valid)
        phone = self.phone_var.get().strip()
        if phone:
            # Remove common phone formatting characters
            phone_clean = re.sub(r'[^\d+]', '', phone)
            if len(phone_clean) < 10:
                errors.append("Phone number must be at least 10 digits")
            elif len(phone_clean) > 15:
                errors.append("Phone number must be less than 15 digits")
            elif not re.match(r'^[\d+\-\s\(\)\.]+$', phone):
                errors.append("Phone number contains invalid characters")
                
        return errors
        
    def save(self):
        """Save the doctor data"""
        # Validate form
        errors = self.validate_form()
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return
            
        # Prepare data
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip() or None
        
        # Set result
        self.result = {
            'name': name,
            'phone': phone
        }
        
        # Close dialog
        self.dialog.destroy()
        
    def cancel(self):
        """Cancel the dialog"""
        self.result = None
        self.dialog.destroy()