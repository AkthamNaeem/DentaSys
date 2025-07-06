import tkinter as tk
from tkinter import ttk, messagebox
from models import Record, Doctor, Patient, Treatment, Payment
from gui.widgets.record_form import RecordForm
from gui.widgets.record_details import RecordDetailsWindow
from localization.translations import translations


class RecordsPage:
    def __init__(self, parent):
        self.parent = parent
        self.selected_record = None
        
        # Register for language change notifications
        translations.add_observer(self.update_ui)
        
        self.setup_ui()
        self.load_records()
        
    def setup_ui(self):
        # Main frame for the tab
        self.frame = ttk.Frame(self.parent)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        # Create scrollable canvas for the entire page
        self.main_canvas = tk.Canvas(self.frame, highlightthickness=0)
        self.main_scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.main_canvas)
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.main_scrollbar.set)
        
        # Grid canvas and scrollbar
        self.main_canvas.grid(row=0, column=0, sticky="nsew")
        self.main_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure grid weights for the frame
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        # Bind mousewheel to canvas for full page scrolling
        self.bind_mousewheel()
        
        # Set up the content frame structure
        self.content_frame = self.scrollable_frame
        self.content_frame.columnconfigure(0, weight=1)
        
        # Header frame
        self.setup_header()
        
        # Content frame
        self.setup_content()
        
    def bind_mousewheel(self):
        """Bind mousewheel events for full page scrolling"""
        def _on_mousewheel(event):
            self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind to multiple widgets to ensure scrolling works everywhere
        self.main_canvas.bind("<MouseWheel>", _on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
        self.frame.bind("<MouseWheel>", _on_mousewheel)
        
        # Function to bind mousewheel to all child widgets recursively
        def bind_to_children(widget):
            widget.bind("<MouseWheel>", _on_mousewheel)
            for child in widget.winfo_children():
                bind_to_children(child)
        
        # Bind after a short delay to ensure all widgets are created
        self.frame.after(100, lambda: bind_to_children(self.scrollable_frame))
        
    def setup_header(self):
        header_frame = ttk.Frame(self.content_frame, style='Card.TFrame', padding=25)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.columnconfigure(1, weight=1)
        
        # Title with better typography
        self.title_label = ttk.Label(header_frame, text=translations.get('records_management'), style='Title.TLabel')
        self.title_label.grid(row=0, column=0, sticky="w")
        
        # Buttons frame with better spacing
        buttons_frame = ttk.Frame(header_frame)
        buttons_frame.grid(row=0, column=1, sticky="e")
        
        # Add Record button with better sizing
        self.add_btn = ttk.Button(
            buttons_frame, 
            text=translations.get('add_record'), 
            style='Success.TButton',
            command=self.add_record
        )
        self.add_btn.pack(side='right', padx=(15, 0), ipadx=15, ipady=8)
        
        # View Details button
        self.view_btn = ttk.Button(
            buttons_frame, 
            text=translations.get('view_details'), 
            style='Warning.TButton',
            command=self.view_record_details,
            state='disabled'
        )
        self.view_btn.pack(side='right', padx=(15, 0), ipadx=15, ipady=8)
        
        # Delete Record button
        self.delete_btn = ttk.Button(
            buttons_frame, 
            text=translations.get('delete_record'), 
            style='Danger.TButton',
            command=self.delete_record,
            state='disabled'
        )
        self.delete_btn.pack(side='right', ipadx=15, ipady=8)
        
    def setup_content(self):
        # Content frame with better padding
        content_frame = ttk.Frame(self.content_frame, style='Card.TFrame', padding=25)
        content_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        content_frame.columnconfigure(0, weight=1)
        
        # Search frame with improved layout
        search_frame = ttk.Frame(content_frame)
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        search_frame.columnconfigure(1, weight=1)
        
        # Search label and entry with better sizing
        self.search_label = ttk.Label(search_frame, text=translations.get('search_records'), font=('Segoe UI', 12, 'bold'))
        self.search_label.grid(row=0, column=0, sticky="w", padx=(0, 15))
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, font=('Segoe UI', 11), width=40)
        self.search_entry.grid(row=0, column=1, sticky="w", ipady=6)
        self.search_var.trace('w', self.on_search)
        
        # Table frame
        table_frame = ttk.Frame(content_frame)
        table_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        table_frame.columnconfigure(0, weight=1)
        
        # Records table without internal scrolling - let page handle it
        columns = ('ID', 'Doctor', 'Patient', 'Total Cost', 'Total Paid', 'Balance', 'Created')
        self.records_tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        # Configure columns with better widths
        self.records_tree.heading('ID', text=translations.get('col_id'))
        self.records_tree.heading('Doctor', text=translations.get('col_doctor'))
        self.records_tree.heading('Patient', text=translations.get('col_patient'))
        self.records_tree.heading('Total Cost', text=translations.get('col_total_cost'))
        self.records_tree.heading('Total Paid', text=translations.get('col_total_paid'))
        self.records_tree.heading('Balance', text=translations.get('col_balance'))
        self.records_tree.heading('Created', text=translations.get('col_created'))
        
        self.records_tree.column('ID', width=80, anchor='center')
        self.records_tree.column('Doctor', width=180)
        self.records_tree.column('Patient', width=180)
        self.records_tree.column('Total Cost', width=120, anchor='center')
        self.records_tree.column('Total Paid', width=120, anchor='center')
        self.records_tree.column('Balance', width=120, anchor='center')
        self.records_tree.column('Created', width=180, anchor='center')
        
        # Grid table without scrollbars
        self.records_tree.grid(row=0, column=0, sticky="ew")
        
        # Bind events
        self.records_tree.bind('<<TreeviewSelect>>', self.on_record_select)
        self.records_tree.bind('<Double-1>', self.on_record_double_click)
        
    def update_ui(self):
        """Update UI elements when language changes"""
        # Update header
        self.title_label.config(text=translations.get('records_management'))
        self.add_btn.config(text=translations.get('add_record'))
        self.view_btn.config(text=translations.get('view_details'))
        self.delete_btn.config(text=translations.get('delete_record'))
        
        # Update search
        self.search_label.config(text=translations.get('search_records'))
        
        # Update table headers
        self.records_tree.heading('ID', text=translations.get('col_id'))
        self.records_tree.heading('Doctor', text=translations.get('col_doctor'))
        self.records_tree.heading('Patient', text=translations.get('col_patient'))
        self.records_tree.heading('Total Cost', text=translations.get('col_total_cost'))
        self.records_tree.heading('Total Paid', text=translations.get('col_total_paid'))
        self.records_tree.heading('Balance', text=translations.get('col_balance'))
        self.records_tree.heading('Created', text=translations.get('col_created'))
        
        # Re-bind mousewheel after UI updates
        self.frame.after(100, self.bind_mousewheel)
        
    def load_records(self, search_term=None):
        """Load records data into the table"""
        # Clear existing data
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
            
        try:
            records = Record.get_all()
            
            # Filter by search term if provided
            if search_term:
                search_term = search_term.lower()
                filtered_records = []
                for record in records:
                    if (search_term in (record.doctor_name or "").lower() or
                        search_term in (record.patient_name or "").lower() or
                        search_term in str(record.id)):
                        filtered_records.append(record)
                records = filtered_records
                
            for record in records:
                created_date = record.created_at.strftime("%Y-%m-%d %H:%M") if record.created_at else ""
                total_cost = record.cost()
                total_paid = record.amount()
                balance = record.balance()
                
                # Color coding for balance
                if balance > 0:
                    tag = 'unpaid'
                elif balance == 0 and total_cost > 0:
                    tag = 'paid'
                else:
                    tag = 'no_treatments'
                
                self.records_tree.insert('', 'end', values=(
                    record.id,
                    record.doctor_name or "",
                    record.patient_name or "",
                    f"${total_cost:.2f}",
                    f"${total_paid:.2f}",
                    f"${balance:.2f}",
                    created_date
                ), tags=(tag,))
                
            # Configure tags for visual feedback
            self.records_tree.tag_configure('unpaid', foreground='#e74c3c')  # Red for unpaid
            self.records_tree.tag_configure('paid', foreground='#27ae60')    # Green for paid
            self.records_tree.tag_configure('no_treatments', foreground='#7f8c8d')  # Gray for no treatments
            
        except Exception as e:
            messagebox.showerror(translations.get('error'), translations.get('failed_to_load', item='records', error=str(e)))
            
    def on_search(self, *args):
        """Handle search input"""
        search_term = self.search_var.get().strip()
        if search_term:
            self.load_records(search_term)
        else:
            self.load_records()
            
    def on_record_select(self, event):
        """Handle record selection"""
        selection = self.records_tree.selection()
        if selection:
            item = self.records_tree.item(selection[0])
            record_id = item['values'][0]
            self.selected_record = Record.get_by_id(record_id)
            
            # Enable view and delete buttons
            self.view_btn.config(state='normal')
            self.delete_btn.config(state='normal')
        else:
            self.selected_record = None
            self.view_btn.config(state='disabled')
            self.delete_btn.config(state='disabled')
            
    def on_record_double_click(self, event):
        """Handle double-click on record row"""
        if self.selected_record:
            self.view_record_details()
            
    def add_record(self):
        """Open add record dialog"""
        dialog = RecordForm(self.content_frame, title=translations.get('add_new_record'))
        if dialog.result:
            try:
                Record.create(
                    doctor_id=dialog.result['doctor_id'],
                    patient_id=dialog.result['patient_id']
                )
                self.load_records()
                messagebox.showinfo(translations.get('success'), translations.get('record_added_success'))
            except ValueError as e:
                messagebox.showerror(translations.get('error'), str(e))
            except Exception as e:
                messagebox.showerror(translations.get('error'), translations.get('failed_to_add', item='record', error=str(e)))
                
    def view_record_details(self):
        """Open record details window"""
        if not self.selected_record:
            return
            
        details_window = RecordDetailsWindow(self.content_frame, self.selected_record)
        # Refresh the records list after the details window is closed
        self.load_records()
        
    def delete_record(self):
        """Delete selected record"""
        if not self.selected_record:
            return
            
        # Check if record has treatments or payments
        has_treatments = Record.record_has_treatments(self.selected_record.id)
        has_payments = Record.record_has_payments(self.selected_record.id)
        
        if has_treatments or has_payments:
            messagebox.showerror(
                translations.get('cannot_delete'),
                translations.get('cannot_delete_record')
            )
            return
            
        # Confirm deletion
        result = messagebox.askyesno(
            translations.get('confirm_deletion'),
            translations.get('confirm_delete_record', 
                doctor=self.selected_record.doctor_name,
                patient=self.selected_record.patient_name)
        )
        
        if result:
            try:
                Record.delete(self.selected_record.id)
                self.load_records()
                self.selected_record = None
                self.view_btn.config(state='disabled')
                self.delete_btn.config(state='disabled')
                messagebox.showinfo(translations.get('success'), translations.get('record_deleted_success'))
            except Exception as e:
                messagebox.showerror(translations.get('error'), translations.get('failed_to_delete', item='record', error=str(e)))