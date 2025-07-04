import tkinter as tk
from tkinter import ttk, messagebox
from models import Doctor, Patient


class RecordForm:
    def __init__(self, parent, title="Record Form", record=None):
        self.parent = parent
        self.record = record
        self.result = None
        
        # Create dialog window with better size
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x400")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.center_dialog()
        
        # Load data
        self.load_data()
        
        # Setup UI
        self.setup_ui()
        
        # Pre-fill if editing
        if self.record:
            self.populate_fields()
            
        # Focus on first field
        self.doctor_combo.focus()
        
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
        
        self.dialog.geometry(f"500x400+{x}+{y}")
        
    def load_data(self):
        """Load doctors and patients data"""
        try:
            self.doctors = Doctor.get_all()
            self.patients = Patient.get_all()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            self.doctors = []
            self.patients = []
            
    def setup_ui(self):
        # Main frame with padding
        main_frame = ttk.Frame(self.dialog, padding=30)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_text = "Edit Record" if self.record else "Add New Record"
        title_label = ttk.Label(main_frame, text=title_text, font=('Segoe UI', 16, 'bold'))
        title_label.pack(pady=(0, 30))
        
        # Form fields frame
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill='both', expand=True, pady=(0, 30))
        
        # Doctor field
        doctor_label = ttk.Label(fields_frame, text="Doctor *", font=('Segoe UI', 11, 'bold'))
        doctor_label.pack(anchor='w', pady=(0, 8))
        
        self.doctor_var = tk.StringVar()
        self.doctor_combo = ttk.Combobox(
            fields_frame, 
            textvariable=self.doctor_var,
            state='readonly',
            font=('Segoe UI', 11),
            height=10
        )
        
        # Populate doctor combobox
        doctor_values = []
        self.doctor_map = {}
        for doctor in self.doctors:
            display_text = f"{doctor.name}"
            if doctor.phone:
                display_text += f" ({doctor.phone})"
            doctor_values.append(display_text)
            self.doctor_map[display_text] = doctor.id
            
        self.doctor_combo['values'] = doctor_values
        self.doctor_combo.pack(fill='x', pady=(0, 20), ipady=8)
        
        # Patient field
        patient_label = ttk.Label(fields_frame, text="Patient *", font=('Segoe UI', 11, 'bold'))
        patient_label.pack(anchor='w', pady=(0, 8))
        
        self.patient_var = tk.StringVar()
        self.patient_combo = ttk.Combobox(
            fields_frame, 
            textvariable=self.patient_var,
            state='readonly',
            font=('Segoe UI', 11),
            height=10
        )
        
        # Populate patient combobox
        patient_values = []
        self.patient_map = {}
        for patient in self.patients:
            display_text = f"{patient.name}"
            if patient.phone:
                display_text += f" ({patient.phone})"
            patient_values.append(display_text)
            self.patient_map[display_text] = patient.id
            
        self.patient_combo['values'] = patient_values
        self.patient_combo.pack(fill='x', pady=(0, 20), ipady=8)
        
        # Info message
        if not self.doctors or not self.patients:
            info_frame = ttk.Frame(fields_frame, style='Card.TFrame', padding=15)
            info_frame.pack(fill='x', pady=(0, 20))
            
            info_text = "⚠️ "
            if not self.doctors and not self.patients:
                info_text += "No doctors or patients found. Please add doctors and patients first."
            elif not self.doctors:
                info_text += "No doctors found. Please add doctors first."
            else:
                info_text += "No patients found. Please add patients first."
                
            info_label = ttk.Label(
                info_frame, 
                text=info_text,
                font=('Segoe UI', 10),
                foreground='#f39c12',
                wraplength=400
            )
            info_label.pack(anchor='w')
        
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
        save_text = "Update" if self.record else "Save"
        save_btn = ttk.Button(
            buttons_frame, 
            text=save_text, 
            command=self.save,
            style='Success.TButton'
        )
        save_btn.pack(side='right', ipadx=20, ipady=8)
        
        # Disable save button if no data
        if not self.doctors or not self.patients:
            save_btn.config(state='disabled')
        
        # Bind Enter key to save
        self.dialog.bind('<Return>', lambda e: self.save())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
        
    def populate_fields(self):
        """Populate fields when editing"""
        if self.record:
            # Find and set doctor
            for display_text, doctor_id in self.doctor_map.items():
                if doctor_id == self.record.doctor_id:
                    self.doctor_var.set(display_text)
                    break
                    
            # Find and set patient
            for display_text, patient_id in self.patient_map.items():
                if patient_id == self.record.patient_id:
                    self.patient_var.set(display_text)
                    break
                    
    def validate_form(self):
        """Validate form data"""
        errors = []
        
        # Validate doctor selection
        doctor_selection = self.doctor_var.get()
        if not doctor_selection:
            errors.append("Please select a doctor")
        elif doctor_selection not in self.doctor_map:
            errors.append("Invalid doctor selection")
            
        # Validate patient selection
        patient_selection = self.patient_var.get()
        if not patient_selection:
            errors.append("Please select a patient")
        elif patient_selection not in self.patient_map:
            errors.append("Invalid patient selection")
            
        return errors
        
    def save(self):
        """Save the record data"""
        # Validate form
        errors = self.validate_form()
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return
            
        # Get selected IDs
        doctor_id = self.doctor_map[self.doctor_var.get()]
        patient_id = self.patient_map[self.patient_var.get()]
        
        # Set result
        self.result = {
            'doctor_id': doctor_id,
            'patient_id': patient_id
        }
        
        # Close dialog
        self.dialog.destroy()
        
    def cancel(self):
        """Cancel the dialog"""
        self.result = None
        self.dialog.destroy()