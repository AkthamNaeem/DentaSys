import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, date


class PaymentForm:
    def __init__(self, parent, title="Payment Form", payment=None, record_id=None):
        self.parent = parent
        self.payment = payment
        self.record_id = record_id
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("450x350")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.center_dialog()
        
        # Setup UI
        self.setup_ui()
        
        # Pre-fill if editing
        if self.payment:
            self.populate_fields()
            
        # Focus on first field
        self.amount_entry.focus()
        
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
        title_text = "Edit Payment" if self.payment else "Add New Payment"
        title_label = ttk.Label(main_frame, text=title_text, font=('Segoe UI', 14, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Form fields frame
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Amount field
        amount_label = ttk.Label(fields_frame, text="Payment Amount *", font=('Segoe UI', 9, 'bold'))
        amount_label.pack(anchor='w', pady=(0, 5))
        
        self.amount_var = tk.StringVar()
        self.amount_entry = ttk.Entry(fields_frame, textvariable=self.amount_var, font=('Segoe UI', 10))
        self.amount_entry.pack(fill='x', pady=(0, 15))
        
        # Date field
        date_label = ttk.Label(fields_frame, text="Payment Date", font=('Segoe UI', 9, 'bold'))
        date_label.pack(anchor='w', pady=(0, 5))
        
        date_frame = ttk.Frame(fields_frame)
        date_frame.pack(fill='x', pady=(0, 15))
        
        try:
            # Try to use DateEntry (tkcalendar)
            self.date_entry = DateEntry(
                date_frame,
                width=12,
                background='darkblue',
                foreground='white',
                borderwidth=2,
                date_pattern='yyyy-mm-dd',
                font=('Segoe UI', 10)
            )
            self.date_entry.pack(fill='x')
            self.has_date_picker = True
        except ImportError:
            # Fallback to regular entry if tkcalendar is not available
            self.date_var = tk.StringVar()
            self.date_entry = ttk.Entry(
                date_frame, 
                textvariable=self.date_var,
                font=('Segoe UI', 10)
            )
            self.date_entry.pack(fill='x')
            
            # Add format hint
            hint_label = ttk.Label(
                date_frame, 
                text="Format: YYYY-MM-DD (e.g., 2024-01-15)",
                font=('Segoe UI', 8),
                foreground='#7f8c8d'
            )
            hint_label.pack(anchor='w', pady=(2, 0))
            self.has_date_picker = False
        
        # Notes field
        notes_label = ttk.Label(fields_frame, text="Notes", font=('Segoe UI', 9, 'bold'))
        notes_label.pack(anchor='w', pady=(0, 5))
        
        notes_frame = ttk.Frame(fields_frame)
        notes_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        self.notes_text = tk.Text(
            notes_frame, 
            height=4, 
            font=('Segoe UI', 10),
            wrap='word'
        )
        notes_scrollbar = ttk.Scrollbar(notes_frame, orient='vertical', command=self.notes_text.yview)
        self.notes_text.configure(yscrollcommand=notes_scrollbar.set)
        
        self.notes_text.pack(side='left', fill='both', expand=True)
        notes_scrollbar.pack(side='right', fill='y')
        
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
        save_text = "Update" if self.payment else "Save"
        save_btn = ttk.Button(
            buttons_frame, 
            text=save_text, 
            command=self.save,
            style='Success.TButton'
        )
        save_btn.pack(side='right')
        
        # Bind Enter key to save (only for single-line entries)
        self.amount_entry.bind('<Return>', lambda e: self.save())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
        
    def populate_fields(self):
        """Populate fields when editing"""
        if self.payment:
            self.amount_var.set(str(self.payment.amount) if self.payment.amount else "")
            
            # Set date
            if self.payment.date:
                if self.has_date_picker:
                    self.date_entry.set_date(self.payment.date)
                else:
                    self.date_var.set(self.payment.date.strftime("%Y-%m-%d"))
                    
            # Set notes
            if self.payment.notes:
                self.notes_text.insert('1.0', self.payment.notes)
                
    def validate_form(self):
        """Validate form data"""
        errors = []
        
        # Validate amount
        amount_str = self.amount_var.get().strip()
        if not amount_str:
            errors.append("Payment amount is required")
        else:
            try:
                amount = float(amount_str)
                if amount <= 0:
                    errors.append("Payment amount must be greater than zero")
                elif amount > 999999.99:
                    errors.append("Payment amount is too large")
            except ValueError:
                errors.append("Payment amount must be a valid number")
                
        # Validate date
        payment_date = None
        if self.has_date_picker:
            try:
                payment_date = self.date_entry.get_date()
                if payment_date > date.today():
                    errors.append("Payment date cannot be in the future")
            except:
                pass  # Date is optional
        else:
            date_str = self.date_var.get().strip()
            if date_str:
                try:
                    payment_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    if payment_date > date.today():
                        errors.append("Payment date cannot be in the future")
                except ValueError:
                    errors.append("Payment date must be in YYYY-MM-DD format")
                    
        return errors
        
    def save(self):
        """Save the payment data"""
        # Validate form
        errors = self.validate_form()
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return
            
        # Prepare data
        amount = float(self.amount_var.get().strip())
        notes = self.notes_text.get('1.0', 'end-1c').strip() or None
        
        # Get date
        payment_date = None
        if self.has_date_picker:
            try:
                payment_date = self.date_entry.get_date()
            except:
                pass
        else:
            date_str = self.date_var.get().strip()
            if date_str:
                try:
                    payment_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    pass
        
        # Set result
        self.result = {
            'amount': amount,
            'date': payment_date,
            'notes': notes
        }
        
        # Close dialog
        self.dialog.destroy()
        
    def cancel(self):
        """Cancel the dialog"""
        self.result = None
        self.dialog.destroy()