import tkinter as tk
from tkinter import ttk, messagebox
from models import Doctor
from gui.widgets.doctor_form import DoctorForm
from localization.translations import translations


class DoctorsPage:
    def __init__(self, parent):
        self.parent = parent
        self.selected_doctor = None
        
        # Register for language change notifications
        translations.add_observer(self.update_ui)
        
        self.setup_ui()
        self.load_doctors()
        
    def setup_ui(self):
        # Main frame for the tab - full width
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
        
        # Set up the content frame structure with full width
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
        header_frame = ttk.Frame(self.content_frame, style='Card.TFrame', padding=20)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        header_frame.columnconfigure(1, weight=1)
        
        # Title with better typography
        self.title_label = ttk.Label(header_frame, text=translations.get('doctors_management'), style='Title.TLabel')
        self.title_label.grid(row=0, column=0, sticky="w")
        
        # Buttons frame with better spacing
        buttons_frame = ttk.Frame(header_frame)
        buttons_frame.grid(row=0, column=1, sticky="e")
        
        # Add Doctor button with better sizing
        self.add_btn = ttk.Button(
            buttons_frame, 
            text=translations.get('add_doctor'), 
            style='Success.TButton',
            command=self.add_doctor
        )
        self.add_btn.pack(side='right', padx=(15, 0), ipadx=15, ipady=8)
        
        # Edit Doctor button
        self.edit_btn = ttk.Button(
            buttons_frame, 
            text=translations.get('edit_doctor'), 
            style='Warning.TButton',
            command=self.edit_doctor,
            state='disabled'
        )
        self.edit_btn.pack(side='right', padx=(15, 0), ipadx=15, ipady=8)
        
        # Delete Doctor button
        self.delete_btn = ttk.Button(
            buttons_frame, 
            text=translations.get('delete_doctor'), 
            style='Danger.TButton',
            command=self.delete_doctor,
            state='disabled'
        )
        self.delete_btn.pack(side='right', ipadx=15, ipady=8)
        
    def setup_content(self):
        # Content frame with full width and minimal padding
        content_frame = ttk.Frame(self.content_frame, style='Card.TFrame', padding=20)
        content_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        content_frame.columnconfigure(0, weight=1)
        
        # Search frame with full width
        search_frame = ttk.Frame(content_frame)
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        search_frame.columnconfigure(1, weight=1)
        
        # Search label and entry with full width
        self.search_label = ttk.Label(search_frame, text=translations.get('search_doctors'), font=('Segoe UI', 12, 'bold'))
        self.search_label.grid(row=0, column=0, sticky="w", padx=(0, 15))
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, font=('Segoe UI', 11))
        self.search_entry.grid(row=0, column=1, sticky="ew", ipady=6)
        self.search_var.trace('w', self.on_search)
        
        # Table frame with full width
        table_frame = ttk.Frame(content_frame)
        table_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        table_frame.columnconfigure(0, weight=1)
        
        # Doctors table without internal scrolling - let page handle it
        columns = ('ID', 'Name', 'Phone', 'Created', 'Status')
        self.doctors_tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        # Configure columns with better widths
        self.doctors_tree.heading('ID', text=translations.get('col_id'))
        self.doctors_tree.heading('Name', text=translations.get('col_name'))
        self.doctors_tree.heading('Phone', text=translations.get('col_phone'))
        self.doctors_tree.heading('Created', text=translations.get('col_created'))
        self.doctors_tree.heading('Status', text=translations.get('col_status'))
        
        self.doctors_tree.column('ID', width=80, anchor='center')
        self.doctors_tree.column('Name', width=250)
        self.doctors_tree.column('Phone', width=180)
        self.doctors_tree.column('Created', width=180, anchor='center')
        self.doctors_tree.column('Status', width=120, anchor='center')
        
        # Grid table without scrollbars - full width
        self.doctors_tree.grid(row=0, column=0, sticky="ew")
        
        # Bind events
        self.doctors_tree.bind('<<TreeviewSelect>>', self.on_doctor_select)
        self.doctors_tree.bind('<Double-1>', self.on_doctor_double_click)
        
        # Details section (initially hidden)
        self.setup_details_section()
        
    def setup_details_section(self):
        """Setup the details section for showing doctor info and related records"""
        # Details frame (initially hidden)
        self.details_frame = ttk.Frame(self.content_frame, style='Card.TFrame', padding=20)
        # Don't grid it initially - will be shown when doctor is selected
        
        # Doctor details header
        self.details_header = ttk.Frame(self.details_frame)
        self.details_header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.details_header.columnconfigure(1, weight=1)
        
        # Doctor info section
        self.doctor_info_frame = ttk.Frame(self.details_header)
        self.doctor_info_frame.grid(row=0, column=0, sticky="w")
        
        # Doctor details title
        self.doctor_details_title = ttk.Label(
            self.doctor_info_frame,
            text="👨‍⚕️ Doctor Details",
            font=('Segoe UI', 16, 'bold'),
            foreground='#2c3e50'
        )
        self.doctor_details_title.pack(anchor='w')
        
        # Doctor name
        self.doctor_name_label = ttk.Label(
            self.doctor_info_frame,
            text="Dr. Name",
            font=('Segoe UI', 14, 'bold'),
            foreground='#3498db'
        )
        self.doctor_name_label.pack(anchor='w', pady=(5, 0))
        
        # Doctor phone
        self.doctor_phone_label = ttk.Label(
            self.doctor_info_frame,
            text="📞 Phone: N/A",
            font=('Segoe UI', 11)
        )
        self.doctor_phone_label.pack(anchor='w')
        
        # Doctor created date
        self.doctor_created_label = ttk.Label(
            self.doctor_info_frame,
            text="📅 Created: N/A",
            font=('Segoe UI', 10),
            foreground='#7f8c8d'
        )
        self.doctor_created_label.pack(anchor='w')
        
        # Statistics section
        self.stats_frame = ttk.Frame(self.details_header)
        self.stats_frame.grid(row=0, column=1, sticky="e")
        
        # Stats title
        stats_title = ttk.Label(
            self.stats_frame,
            text="📊 Statistics",
            font=('Segoe UI', 12, 'bold'),
            foreground='#2c3e50'
        )
        stats_title.pack(anchor='e', pady=(0, 10))
        
        # Stats cards
        stats_cards_frame = ttk.Frame(self.stats_frame)
        stats_cards_frame.pack(anchor='e')
        
        # Records count
        self.records_card = ttk.Frame(stats_cards_frame, style='Card.TFrame', padding=10)
        self.records_card.pack(side='left', padx=(0, 10))
        
        self.records_count = ttk.Label(
            self.records_card,
            text="0",
            font=('Segoe UI', 14, 'bold'),
            foreground='#3498db'
        )
        self.records_count.pack()
        
        records_label = ttk.Label(
            self.records_card,
            text=translations.get('stat_records'),
            font=('Segoe UI', 9),
            foreground='#7f8c8d'
        )
        records_label.pack()
        
        # Total revenue
        self.revenue_card = ttk.Frame(stats_cards_frame, style='Card.TFrame', padding=10)
        self.revenue_card.pack(side='left')
        
        self.revenue_amount = ttk.Label(
            self.revenue_card,
            text="$0.00",
            font=('Segoe UI', 14, 'bold'),
            foreground='#27ae60'
        )
        self.revenue_amount.pack()
        
        revenue_label = ttk.Label(
            self.revenue_card,
            text="Total Revenue",
            font=('Segoe UI', 9),
            foreground='#7f8c8d'
        )
        revenue_label.pack()
        
        # Back button
        self.back_btn = ttk.Button(
            self.details_header,
            text="← Back to List",
            command=self.hide_details,
            style='TButton'
        )
        self.back_btn.grid(row=0, column=2, sticky="ne", padx=(20, 0))
        
        # Related records section
        records_section = ttk.Frame(self.details_frame)
        records_section.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        records_section.columnconfigure(0, weight=1)
        
        # Records title
        records_title = ttk.Label(
            records_section,
            text="📋 Related Records",
            font=('Segoe UI', 14, 'bold'),
            foreground='#2c3e50'
        )
        records_title.pack(anchor='w', pady=(0, 15))
        
        # Records table
        records_columns = ('ID', 'Patient', 'Total Cost', 'Total Paid', 'Balance', 'Created')
        self.doctor_records_tree = ttk.Treeview(records_section, columns=records_columns, show='headings')
        
        # Configure columns
        self.doctor_records_tree.heading('ID', text=translations.get('col_id'))
        self.doctor_records_tree.heading('Patient', text=translations.get('col_patient'))
        self.doctor_records_tree.heading('Total Cost', text=translations.get('col_total_cost'))
        self.doctor_records_tree.heading('Total Paid', text=translations.get('col_total_paid'))
        self.doctor_records_tree.heading('Balance', text=translations.get('col_balance'))
        self.doctor_records_tree.heading('Created', text=translations.get('col_created'))
        
        self.doctor_records_tree.column('ID', width=80, anchor='center')
        self.doctor_records_tree.column('Patient', width=250)
        self.doctor_records_tree.column('Total Cost', width=150, anchor='center')
        self.doctor_records_tree.column('Total Paid', width=150, anchor='center')
        self.doctor_records_tree.column('Balance', width=150, anchor='center')
        self.doctor_records_tree.column('Created', width=200, anchor='center')
        
        self.doctor_records_tree.pack(fill='both', expand=True)
        
        # Bind double-click to open record details
        self.doctor_records_tree.bind('<Double-1>', self.on_record_double_click)
        
    def update_ui(self):
        """Update UI elements when language changes"""
        # Update header
        self.title_label.config(text=translations.get('doctors_management'))
        self.add_btn.config(text=translations.get('add_doctor'))
        self.edit_btn.config(text=translations.get('edit_doctor'))
        self.delete_btn.config(text=translations.get('delete_doctor'))
        
        # Update search
        self.search_label.config(text=translations.get('search_doctors'))
        
        # Update table headers
        self.doctors_tree.heading('ID', text=translations.get('col_id'))
        self.doctors_tree.heading('Name', text=translations.get('col_name'))
        self.doctors_tree.heading('Phone', text=translations.get('col_phone'))
        self.doctors_tree.heading('Created', text=translations.get('col_created'))
        self.doctors_tree.heading('Status', text=translations.get('col_status'))
        
        # Reload data to update status translations
        self.load_doctors()
        
        # Re-bind mousewheel after UI updates
        self.frame.after(100, self.bind_mousewheel)
        
    def show_details(self, doctor):
        """Show doctor details and related records"""
        self.selected_doctor = doctor
        
        # Update doctor info
        self.doctor_name_label.config(text=f"Dr. {doctor.name}")
        self.doctor_phone_label.config(text=f"📞 Phone: {doctor.phone or 'N/A'}")
        
        created_date = doctor.created_at.strftime("%Y-%m-%d %H:%M") if doctor.created_at else "N/A"
        self.doctor_created_label.config(text=f"📅 Created: {created_date}")
        
        # Load related records
        self.load_doctor_records(doctor.id)
        
        # Show details frame and hide main content
        self.details_frame.grid(row=2, column=0, sticky="ew", pady=(15, 0))
        self.content_frame.rowconfigure(2, weight=1)
        
        # Update button states
        self.edit_btn.config(state='normal')
        self.delete_btn.config(state='disabled')  # Disable delete when viewing details
        
    def hide_details(self):
        """Hide doctor details and return to list view"""
        self.details_frame.grid_forget()
        self.selected_doctor = None
        self.edit_btn.config(state='disabled')
        self.delete_btn.config(state='disabled')
        
    def load_doctor_records(self, doctor_id):
        """Load records for the selected doctor"""
        # Clear existing data
        for item in self.doctor_records_tree.get_children():
            self.doctor_records_tree.delete(item)
            
        try:
            from models import Record
            records = Record.get_by_doctor(doctor_id)
            
            total_records = len(records)
            total_revenue = 0
            
            for record in records:
                # Get financial data
                total_cost = record.cost()
                total_paid = record.amount()
                balance = record.balance()
                total_revenue += total_paid
                
                created_date = record.created_at.strftime("%Y-%m-%d %H:%M") if record.created_at else ""
                
                # Color coding for balance
                if balance > 0:
                    tag = 'unpaid'
                elif balance == 0 and total_cost > 0:
                    tag = 'paid'
                else:
                    tag = 'no_treatments'
                
                self.doctor_records_tree.insert('', 'end', values=(
                    record.id,
                    getattr(record, 'patient_name', 'Unknown'),
                    f"${total_cost:.2f}",
                    f"${total_paid:.2f}",
                    f"${balance:.2f}",
                    created_date
                ), tags=(tag,))
            
            # Configure tags for visual feedback
            self.doctor_records_tree.tag_configure('unpaid', foreground='#e74c3c')
            self.doctor_records_tree.tag_configure('paid', foreground='#27ae60')
            self.doctor_records_tree.tag_configure('no_treatments', foreground='#7f8c8d')
            
            # Update statistics
            self.records_count.config(text=str(total_records))
            self.revenue_amount.config(text=f"${total_revenue:.2f}")
            
        except Exception as e:
            messagebox.showerror(translations.get('error'), f"Failed to load doctor records: {str(e)}")
            
    def on_record_double_click(self, event):
        """Handle double-click on record in doctor details view"""
        selection = self.doctor_records_tree.selection()
        if selection:
            item = self.doctor_records_tree.item(selection[0])
            record_id = item['values'][0]
            
            try:
                from models import Record
                from gui.widgets.record_details import RecordDetailsWindow
                
                record = Record.get_by_id(record_id)
                if record:
                    RecordDetailsWindow(self.content_frame, record)
                    # Refresh the records after closing details window
                    self.load_doctor_records(self.selected_doctor.id)
            except Exception as e:
                messagebox.showerror(translations.get('error'), f"Failed to open record details: {str(e)}")
        
    def load_doctors(self, search_term=None):
        """Load doctors data into the table"""
        # Clear existing data
        for item in self.doctors_tree.get_children():
            self.doctors_tree.delete(item)
            
        try:
            if search_term:
                doctors = Doctor.search(search_term)
            else:
                doctors = Doctor.get_all()
                
            for doctor in doctors:
                created_date = doctor.created_at.strftime("%Y-%m-%d %H:%M") if doctor.created_at else ""
                status = translations.get('status_deleted') if doctor.deleted_at else translations.get('status_active')
                
                self.doctors_tree.insert('', 'end', values=(
                    doctor.id,
                    doctor.name,
                    doctor.phone or "",
                    created_date,
                    status
                ), tags=(status.lower(),))
                
            # Configure tags for visual feedback
            self.doctors_tree.tag_configure('deleted', foreground='#e74c3c')
            self.doctors_tree.tag_configure('active', foreground='#27ae60')
            
        except Exception as e:
            messagebox.showerror(translations.get('error'), f"Failed to load doctors: {str(e)}")
            
    def on_search(self, *args):
        """Handle search input"""
        search_term = self.search_var.get().strip()
        if search_term:
            self.load_doctors(search_term)
        else:
            self.load_doctors()
            
    def on_doctor_select(self, event):
        """Handle doctor selection"""
        selection = self.doctors_tree.selection()
        if selection:
            item = self.doctors_tree.item(selection[0])
            doctor_id = item['values'][0]
            self.selected_doctor = Doctor.get_by_id(doctor_id)
            
            # Enable edit and delete buttons
            self.edit_btn.config(state='normal')
            self.delete_btn.config(state='normal')
        else:
            self.selected_doctor = None
            self.edit_btn.config(state='disabled')
            self.delete_btn.config(state='disabled')
            
    def on_doctor_double_click(self, event):
        """Handle double-click on doctor row"""
        if self.selected_doctor:
            self.show_details(self.selected_doctor)
            
    def add_doctor(self):
        """Open add doctor dialog"""
        dialog = DoctorForm(self.content_frame, title=translations.get('add_new_doctor'))
        if dialog.result:
            try:
                Doctor.create(
                    name=dialog.result['name'],
                    phone=dialog.result['phone']
                )
                self.load_doctors()
                messagebox.showinfo(translations.get('success'), "Doctor added successfully!")
            except ValueError as e:
                messagebox.showerror(translations.get('error'), str(e))
            except Exception as e:
                messagebox.showerror(translations.get('error'), f"Failed to add doctor: {str(e)}")
                
    def edit_doctor(self):
        """Open edit doctor dialog"""
        if not self.selected_doctor:
            return
            
        dialog = DoctorForm(
            self.content_frame, 
            title=translations.get('edit_doctor_title'),
            doctor=self.selected_doctor
        )
        
        if dialog.result:
            try:
                Doctor.update(
                    self.selected_doctor.id,
                    name=dialog.result['name'],
                    phone=dialog.result['phone']
                )
                self.load_doctors()
                messagebox.showinfo(translations.get('success'), "Doctor updated successfully!")
            except ValueError as e:
                messagebox.showerror(translations.get('error'), str(e))
            except Exception as e:
                messagebox.showerror(translations.get('error'), f"Failed to update doctor: {str(e)}")
                
    def delete_doctor(self):
        """Delete selected doctor"""
        if not self.selected_doctor:
            return
            
        # Confirm deletion
        result = messagebox.askyesno(
            translations.get('confirm_deletion'),
            f"Are you sure you want to delete Dr. {self.selected_doctor.name}?\n\n"
            "Note: If this doctor has records, they will be soft-deleted (marked as deleted but kept for data integrity)."
        )
        
        if result:
            try:
                Doctor.delete(self.selected_doctor.id)
                self.load_doctors()
                self.selected_doctor = None
                self.edit_btn.config(state='disabled')
                self.delete_btn.config(state='disabled')
                messagebox.showinfo(translations.get('success'), "Doctor deleted successfully!")
            except Exception as e:
                messagebox.showerror(translations.get('error'), f"Failed to delete doctor: {str(e)}")