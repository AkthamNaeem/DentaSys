import tkinter as tk
from tkinter import ttk, messagebox
from models import Treatment, Payment
from gui.widgets.treatment_form import TreatmentForm
from gui.widgets.payment_form import PaymentForm


class RecordDetailsWindow:
    def __init__(self, parent, record):
        self.parent = parent
        self.record = record
        self.selected_treatment = None
        self.selected_payment = None
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title(f"Record Details - {record.doctor_name} & {record.patient_name}")
        self.window.geometry("900x700")
        self.window.resizable(True, True)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Center the window
        self.center_window()
        
        # Setup UI
        self.setup_ui()
        
        # Load data
        self.load_data()
        
        # Wait for window to close
        self.window.wait_window()
        
    def center_window(self):
        """Center the window on the parent"""
        self.window.update_idletasks()
        
        # Get parent window position and size
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Calculate center position
        window_width = self.window.winfo_reqwidth()
        window_height = self.window.winfo_reqheight()
        
        x = parent_x + (parent_width // 2) - (window_width // 2)
        y = parent_y + (parent_height // 2) - (window_height // 2)
        
        self.window.geometry(f"900x700+{x}+{y}")
        
    def setup_ui(self):
        # Main frame with padding
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Header frame
        self.setup_header(main_frame)
        
        # Content notebook
        self.setup_content(main_frame)
        
        # Summary frame
        self.setup_summary(main_frame)
        
        # Buttons frame
        self.setup_buttons(main_frame)
        
    def setup_header(self, parent):
        header_frame = ttk.Frame(parent, style='Card.TFrame', padding=15)
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Title
        title_label = ttk.Label(
            header_frame, 
            text="📋 Record Details", 
            font=('Segoe UI', 16, 'bold'),
            foreground='#2c3e50'
        )
        title_label.pack(anchor='w')
        
        # Record info
        info_frame = ttk.Frame(header_frame)
        info_frame.pack(fill='x', pady=(10, 0))
        
        # Doctor info
        doctor_label = ttk.Label(
            info_frame, 
            text=f"👨‍⚕️ Doctor: {self.record.doctor_name}",
            font=('Segoe UI', 11)
        )
        doctor_label.pack(anchor='w')
        
        # Patient info
        patient_label = ttk.Label(
            info_frame, 
            text=f"👤 Patient: {self.record.patient_name}",
            font=('Segoe UI', 11)
        )
        patient_label.pack(anchor='w')
        
        # Created date
        created_date = self.record.created_at.strftime("%Y-%m-%d %H:%M") if self.record.created_at else "Unknown"
        created_label = ttk.Label(
            info_frame, 
            text=f"📅 Created: {created_date}",
            font=('Segoe UI', 10),
            foreground='#7f8c8d'
        )
        created_label.pack(anchor='w')
        
    def setup_content(self, parent):
        # Create notebook for treatments and payments
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill='both', expand=True, pady=(0, 20))
        
        # Treatments tab
        self.setup_treatments_tab()
        
        # Payments tab
        self.setup_payments_tab()
        
    def setup_treatments_tab(self):
        # Treatments frame
        treatments_frame = ttk.Frame(self.notebook)
        treatments_frame.columnconfigure(0, weight=1)
        treatments_frame.rowconfigure(1, weight=1)
        
        # Treatments header
        treatments_header = ttk.Frame(treatments_frame, padding=10)
        treatments_header.grid(row=0, column=0, sticky="ew")
        treatments_header.columnconfigure(1, weight=1)
        
        treatments_title = ttk.Label(
            treatments_header, 
            text="🦷 Treatments", 
            font=('Segoe UI', 12, 'bold')
        )
        treatments_title.grid(row=0, column=0, sticky="w")
        
        # Treatment buttons
        treatment_buttons = ttk.Frame(treatments_header)
        treatment_buttons.grid(row=0, column=1, sticky="e")
        
        self.add_treatment_btn = ttk.Button(
            treatment_buttons,
            text="➕ Add Treatment",
            style='Success.TButton',
            command=self.add_treatment
        )
        self.add_treatment_btn.pack(side='right', padx=(10, 0))
        
        self.edit_treatment_btn = ttk.Button(
            treatment_buttons,
            text="✏️ Edit Treatment",
            style='Warning.TButton',
            command=self.edit_treatment,
            state='disabled'
        )
        self.edit_treatment_btn.pack(side='right', padx=(10, 0))
        
        self.delete_treatment_btn = ttk.Button(
            treatment_buttons,
            text="🗑️ Delete Treatment",
            style='Danger.TButton',
            command=self.delete_treatment,
            state='disabled'
        )
        self.delete_treatment_btn.pack(side='right')
        
        # Treatments table
        treatments_table_frame = ttk.Frame(treatments_frame, padding=10)
        treatments_table_frame.grid(row=1, column=0, sticky="nsew")
        treatments_table_frame.columnconfigure(0, weight=1)
        treatments_table_frame.rowconfigure(0, weight=1)
        
        treatment_columns = ('ID', 'Name', 'Cost', 'Date', 'Notes')
        self.treatments_tree = ttk.Treeview(
            treatments_table_frame, 
            columns=treatment_columns, 
            show='headings', 
            height=8
        )
        
        # Configure treatment columns
        self.treatments_tree.heading('ID', text='ID')
        self.treatments_tree.heading('Name', text='Treatment Name')
        self.treatments_tree.heading('Cost', text='Cost')
        self.treatments_tree.heading('Date', text='Date')
        self.treatments_tree.heading('Notes', text='Notes')
        
        self.treatments_tree.column('ID', width=50, anchor='center')
        self.treatments_tree.column('Name', width=200)
        self.treatments_tree.column('Cost', width=100, anchor='center')
        self.treatments_tree.column('Date', width=100, anchor='center')
        self.treatments_tree.column('Notes', width=200)
        
        # Treatment scrollbars
        treatment_v_scrollbar = ttk.Scrollbar(
            treatments_table_frame, 
            orient='vertical', 
            command=self.treatments_tree.yview
        )
        treatment_h_scrollbar = ttk.Scrollbar(
            treatments_table_frame, 
            orient='horizontal', 
            command=self.treatments_tree.xview
        )
        self.treatments_tree.configure(
            yscrollcommand=treatment_v_scrollbar.set,
            xscrollcommand=treatment_h_scrollbar.set
        )
        
        # Grid treatment table and scrollbars
        self.treatments_tree.grid(row=0, column=0, sticky="nsew")
        treatment_v_scrollbar.grid(row=0, column=1, sticky="ns")
        treatment_h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Bind treatment events
        self.treatments_tree.bind('<<TreeviewSelect>>', self.on_treatment_select)
        self.treatments_tree.bind('<Double-1>', self.on_treatment_double_click)
        
        self.notebook.add(treatments_frame, text="🦷 Treatments")
        
    def setup_payments_tab(self):
        # Payments frame
        payments_frame = ttk.Frame(self.notebook)
        payments_frame.columnconfigure(0, weight=1)
        payments_frame.rowconfigure(1, weight=1)
        
        # Payments header
        payments_header = ttk.Frame(payments_frame, padding=10)
        payments_header.grid(row=0, column=0, sticky="ew")
        payments_header.columnconfigure(1, weight=1)
        
        payments_title = ttk.Label(
            payments_header, 
            text="💰 Payments", 
            font=('Segoe UI', 12, 'bold')
        )
        payments_title.grid(row=0, column=0, sticky="w")
        
        # Payment buttons
        payment_buttons = ttk.Frame(payments_header)
        payment_buttons.grid(row=0, column=1, sticky="e")
        
        self.add_payment_btn = ttk.Button(
            payment_buttons,
            text="➕ Add Payment",
            style='Success.TButton',
            command=self.add_payment
        )
        self.add_payment_btn.pack(side='right', padx=(10, 0))
        
        self.edit_payment_btn = ttk.Button(
            payment_buttons,
            text="✏️ Edit Payment",
            style='Warning.TButton',
            command=self.edit_payment,
            state='disabled'
        )
        self.edit_payment_btn.pack(side='right', padx=(10, 0))
        
        self.delete_payment_btn = ttk.Button(
            payment_buttons,
            text="🗑️ Delete Payment",
            style='Danger.TButton',
            command=self.delete_payment,
            state='disabled'
        )
        self.delete_payment_btn.pack(side='right')
        
        # Payments table
        payments_table_frame = ttk.Frame(payments_frame, padding=10)
        payments_table_frame.grid(row=1, column=0, sticky="nsew")
        payments_table_frame.columnconfigure(0, weight=1)
        payments_table_frame.rowconfigure(0, weight=1)
        
        payment_columns = ('ID', 'Amount', 'Date', 'Notes')
        self.payments_tree = ttk.Treeview(
            payments_table_frame, 
            columns=payment_columns, 
            show='headings', 
            height=8
        )
        
        # Configure payment columns
        self.payments_tree.heading('ID', text='ID')
        self.payments_tree.heading('Amount', text='Amount')
        self.payments_tree.heading('Date', text='Date')
        self.payments_tree.heading('Notes', text='Notes')
        
        self.payments_tree.column('ID', width=50, anchor='center')
        self.payments_tree.column('Amount', width=100, anchor='center')
        self.payments_tree.column('Date', width=100, anchor='center')
        self.payments_tree.column('Notes', width=300)
        
        # Payment scrollbars
        payment_v_scrollbar = ttk.Scrollbar(
            payments_table_frame, 
            orient='vertical', 
            command=self.payments_tree.yview
        )
        payment_h_scrollbar = ttk.Scrollbar(
            payments_table_frame, 
            orient='horizontal', 
            command=self.payments_tree.xview
        )
        self.payments_tree.configure(
            yscrollcommand=payment_v_scrollbar.set,
            xscrollcommand=payment_h_scrollbar.set
        )
        
        # Grid payment table and scrollbars
        self.payments_tree.grid(row=0, column=0, sticky="nsew")
        payment_v_scrollbar.grid(row=0, column=1, sticky="ns")
        payment_h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Bind payment events
        self.payments_tree.bind('<<TreeviewSelect>>', self.on_payment_select)
        self.payments_tree.bind('<Double-1>', self.on_payment_double_click)
        
        self.notebook.add(payments_frame, text="💰 Payments")
        
    def setup_summary(self, parent):
        # Summary frame
        summary_frame = ttk.Frame(parent, style='Card.TFrame', padding=15)
        summary_frame.pack(fill='x', pady=(0, 20))
        
        summary_title = ttk.Label(
            summary_frame, 
            text="📊 Account Summary", 
            font=('Segoe UI', 12, 'bold')
        )
        summary_title.pack(anchor='w', pady=(0, 10))
        
        # Summary grid
        summary_grid = ttk.Frame(summary_frame)
        summary_grid.pack(fill='x')
        summary_grid.columnconfigure((0, 1, 2), weight=1)
        
        # Total cost
        self.cost_frame = ttk.Frame(summary_grid, style='Card.TFrame', padding=10)
        self.cost_frame.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.cost_value = ttk.Label(
            self.cost_frame, 
            text="$0.00", 
            font=('Segoe UI', 16, 'bold'),
            foreground='#3498db'
        )
        self.cost_value.pack()
        
        cost_label = ttk.Label(
            self.cost_frame, 
            text="Total Cost", 
            font=('Segoe UI', 10),
            foreground='#7f8c8d'
        )
        cost_label.pack()
        
        # Total paid
        self.paid_frame = ttk.Frame(summary_grid, style='Card.TFrame', padding=10)
        self.paid_frame.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        
        self.paid_value = ttk.Label(
            self.paid_frame, 
            text="$0.00", 
            font=('Segoe UI', 16, 'bold'),
            foreground='#27ae60'
        )
        self.paid_value.pack()
        
        paid_label = ttk.Label(
            self.paid_frame, 
            text="Total Paid", 
            font=('Segoe UI', 10),
            foreground='#7f8c8d'
        )
        paid_label.pack()
        
        # Balance
        self.balance_frame = ttk.Frame(summary_grid, style='Card.TFrame', padding=10)
        self.balance_frame.grid(row=0, column=2, sticky="ew")
        
        self.balance_value = ttk.Label(
            self.balance_frame, 
            text="$0.00", 
            font=('Segoe UI', 16, 'bold'),
            foreground='#e74c3c'
        )
        self.balance_value.pack()
        
        balance_label = ttk.Label(
            self.balance_frame, 
            text="Balance", 
            font=('Segoe UI', 10),
            foreground='#7f8c8d'
        )
        balance_label.pack()
        
    def setup_buttons(self, parent):
        # Buttons frame
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill='x')
        
        # Close button
        close_btn = ttk.Button(
            buttons_frame, 
            text="Close", 
            command=self.close_window,
            style='TButton'
        )
        close_btn.pack(side='right')
        
    def load_data(self):
        """Load treatments and payments data"""
        self.load_treatments()
        self.load_payments()
        self.update_summary()
        
    def load_treatments(self):
        """Load treatments into the table"""
        # Clear existing data
        for item in self.treatments_tree.get_children():
            self.treatments_tree.delete(item)
            
        try:
            treatments = self.record.treatments()
            for treatment in treatments:
                treatment_date = treatment.date.strftime("%Y-%m-%d") if treatment.date else ""
                self.treatments_tree.insert('', 'end', values=(
                    treatment.id,
                    treatment.name,
                    f"${treatment.cost:.2f}",
                    treatment_date,
                    treatment.notes or ""
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load treatments: {str(e)}")
            
    def load_payments(self):
        """Load payments into the table"""
        # Clear existing data
        for item in self.payments_tree.get_children():
            self.payments_tree.delete(item)
            
        try:
            payments = self.record.payments()
            for payment in payments:
                payment_date = payment.date.strftime("%Y-%m-%d") if payment.date else ""
                self.payments_tree.insert('', 'end', values=(
                    payment.id,
                    f"${payment.amount:.2f}",
                    payment_date,
                    payment.notes or ""
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load payments: {str(e)}")
            
    def update_summary(self):
        """Update the summary section"""
        try:
            total_cost = self.record.cost()
            total_paid = self.record.amount()
            balance = self.record.balance()
            
            self.cost_value.config(text=f"${total_cost:.2f}")
            self.paid_value.config(text=f"${total_paid:.2f}")
            self.balance_value.config(text=f"${balance:.2f}")
            
            # Update balance color
            if balance > 0:
                self.balance_value.config(foreground='#e74c3c')  # Red
            elif balance == 0:
                self.balance_value.config(foreground='#27ae60')  # Green
            else:
                self.balance_value.config(foreground='#f39c12')  # Orange (overpaid)
                
        except Exception as e:
            print(f"Error updating summary: {e}")
            
    # Treatment event handlers
    def on_treatment_select(self, event):
        """Handle treatment selection"""
        selection = self.treatments_tree.selection()
        if selection:
            item = self.treatments_tree.item(selection[0])
            treatment_id = item['values'][0]
            self.selected_treatment = Treatment.get_by_id(treatment_id)
            
            self.edit_treatment_btn.config(state='normal')
            self.delete_treatment_btn.config(state='normal')
        else:
            self.selected_treatment = None
            self.edit_treatment_btn.config(state='disabled')
            self.delete_treatment_btn.config(state='disabled')
            
    def on_treatment_double_click(self, event):
        """Handle double-click on treatment"""
        if self.selected_treatment:
            self.edit_treatment()
            
    def add_treatment(self):
        """Add new treatment"""
        dialog = TreatmentForm(self.window, title="Add Treatment", record_id=self.record.id)
        if dialog.result:
            try:
                Treatment.create(
                    record_id=self.record.id,
                    name=dialog.result['name'],
                    cost=dialog.result['cost'],
                    treatment_date=dialog.result['date'],
                    notes=dialog.result['notes']
                )
                self.load_treatments()
                self.update_summary()
                messagebox.showinfo("Success", "Treatment added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add treatment: {str(e)}")
                
    def edit_treatment(self):
        """Edit selected treatment"""
        if not self.selected_treatment:
            return
            
        dialog = TreatmentForm(
            self.window, 
            title="Edit Treatment", 
            treatment=self.selected_treatment
        )
        if dialog.result:
            try:
                Treatment.update(
                    self.selected_treatment.id,
                    name=dialog.result['name'],
                    cost=dialog.result['cost'],
                    treatment_date=dialog.result['date'],
                    notes=dialog.result['notes']
                )
                self.load_treatments()
                self.update_summary()
                messagebox.showinfo("Success", "Treatment updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update treatment: {str(e)}")
                
    def delete_treatment(self):
        """Delete selected treatment"""
        if not self.selected_treatment:
            return
            
        result = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete the treatment '{self.selected_treatment.name}'?\n\n"
            "This action cannot be undone."
        )
        
        if result:
            try:
                Treatment.delete(self.selected_treatment.id)
                self.load_treatments()
                self.update_summary()
                self.selected_treatment = None
                self.edit_treatment_btn.config(state='disabled')
                self.delete_treatment_btn.config(state='disabled')
                messagebox.showinfo("Success", "Treatment deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete treatment: {str(e)}")
                
    # Payment event handlers
    def on_payment_select(self, event):
        """Handle payment selection"""
        selection = self.payments_tree.selection()
        if selection:
            item = self.payments_tree.item(selection[0])
            payment_id = item['values'][0]
            self.selected_payment = Payment.get_by_id(payment_id)
            
            self.edit_payment_btn.config(state='normal')
            self.delete_payment_btn.config(state='normal')
        else:
            self.selected_payment = None
            self.edit_payment_btn.config(state='disabled')
            self.delete_payment_btn.config(state='disabled')
            
    def on_payment_double_click(self, event):
        """Handle double-click on payment"""
        if self.selected_payment:
            self.edit_payment()
            
    def add_payment(self):
        """Add new payment"""
        dialog = PaymentForm(self.window, title="Add Payment", record_id=self.record.id)
        if dialog.result:
            try:
                Payment.create(
                    record_id=self.record.id,
                    amount=dialog.result['amount'],
                    payment_date=dialog.result['date'],
                    notes=dialog.result['notes']
                )
                self.load_payments()
                self.update_summary()
                messagebox.showinfo("Success", "Payment added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add payment: {str(e)}")
                
    def edit_payment(self):
        """Edit selected payment"""
        if not self.selected_payment:
            return
            
        dialog = PaymentForm(
            self.window, 
            title="Edit Payment", 
            payment=self.selected_payment
        )
        if dialog.result:
            try:
                Payment.update(
                    self.selected_payment.id,
                    amount=dialog.result['amount'],
                    payment_date=dialog.result['date'],
                    notes=dialog.result['notes']
                )
                self.load_payments()
                self.update_summary()
                messagebox.showinfo("Success", "Payment updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update payment: {str(e)}")
                
    def delete_payment(self):
        """Delete selected payment"""
        if not self.selected_payment:
            return
            
        result = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete this payment of ${self.selected_payment.amount:.2f}?\n\n"
            "This action cannot be undone."
        )
        
        if result:
            try:
                Payment.delete(self.selected_payment.id)
                self.load_payments()
                self.update_summary()
                self.selected_payment = None
                self.edit_payment_btn.config(state='disabled')
                self.delete_payment_btn.config(state='disabled')
                messagebox.showinfo("Success", "Payment deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete payment: {str(e)}")
                
    def close_window(self):
        """Close the details window"""
        self.window.destroy()