import tkinter as tk
from tkinter import ttk, messagebox
from models import Patient
from gui.widgets.patient_form import PatientForm
from localization.translations import translations


class PatientsPage:
    def __init__(self, parent):
        self.parent = parent
        self.selected_patient = None
        
        # Register for language change notifications
        translations.add_observer(self.update_ui)
        
        self.setup_ui()
        self.load_patients()
        
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
        self.title_label = ttk.Label(header_frame, text=translations.get('patients_management'), style='Title.TLabel')
        self.title_label.grid(row=0, column=0, sticky="w")
        
        # Buttons frame with better spacing
        buttons_frame = ttk.Frame(header_frame)
        buttons_frame.grid(row=0, column=1, sticky="e")
        
        # Add Patient button with better sizing
        self.add_btn = ttk.Button(
            buttons_frame, 
            text=translations.get('add_patient'),
            style='Success.TButton',
            command=self.add_patient
        )
        self.add_btn.pack(side='right', padx=(15, 0), ipadx=15, ipady=8)
        
        # Edit Patient button
        self.edit_btn = ttk.Button(
            buttons_frame, 
            text=translations.get('edit_patient'),
            style='Warning.TButton',
            command=self.edit_patient,
            state='disabled'
        )
        self.edit_btn.pack(side='right', padx=(15, 0), ipadx=15, ipady=8)
        
        # Delete Patient button
        self.delete_btn = ttk.Button(
            buttons_frame, 
            text=translations.get('delete_patient'),
            style='Danger.TButton',
            command=self.delete_patient,
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
        self.search_label = ttk.Label(search_frame, text=translations.get('search_patients'), font=('Segoe UI', 12, 'bold'))
        self.search_label.grid(row=0, column=0, sticky="w", padx=(0, 15))
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, font=('Segoe UI', 11))
        self.search_entry.grid(row=0, column=1, sticky="ew", ipady=6)
        self.search_var.trace('w', self.on_search)
        
        # Table frame with full width
        table_frame = ttk.Frame(content_frame)
        table_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        table_frame.columnconfigure(0, weight=1)
        
        # Patients table without internal scrolling - let page handle it
        columns = (
            'Name',
            'Phone',
            'Gender',
            'Age',
        )
        self.patients_tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        # Configure columns with better widths for full screen
        self.patients_tree.heading('Name', text=translations.get('col_name'))
        self.patients_tree.heading('Phone', text=translations.get('col_phone'))
        self.patients_tree.heading('Gender', text=translations.get('col_gender'))
        self.patients_tree.heading('Age', text=translations.get('col_age'))
        
        self.patients_tree.column('Name', width=300)
        self.patients_tree.column('Phone', width=200)
        self.patients_tree.column('Gender', width=150, anchor='center')
        self.patients_tree.column('Age', width=150, anchor='center')
        
        # Grid table without scrollbars - full width
        self.patients_tree.grid(row=0, column=0, sticky="ew")
        
        # Bind events
        self.patients_tree.bind('<<TreeviewSelect>>', self.on_patient_select)
        self.patients_tree.bind('<Double-1>', self.on_patient_double_click)
        
        # Details section (initially hidden)
        self.setup_details_section()
        
    def setup_details_section(self):
        """Setup the details section for showing patient info and related records"""
        # Details frame (initially hidden)
        self.details_frame = ttk.Frame(self.content_frame, style='Card.TFrame', padding=20)
        # Don't grid it initially - will be shown when patient is selected
        
        # Patient details header
        self.details_header = ttk.Frame(self.details_frame)
        self.details_header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.details_header.columnconfigure(1, weight=1)
        
        # Patient info section
        self.patient_info_frame = ttk.Frame(self.details_header)
        self.patient_info_frame.grid(row=0, column=0, sticky="w")
        
        # Patient details title
        self.patient_details_title = ttk.Label(
            self.patient_info_frame,
            text="👤 Patient Details",
            font=('Segoe UI', 16, 'bold'),
            foreground='#2c3e50'
        )
        self.patient_details_title.pack(anchor='w')
        
        # Patient name
        self.patient_name_label = ttk.Label(
            self.patient_info_frame,
            text="Patient Name",
            font=('Segoe UI', 14, 'bold'),
            foreground='#3498db'
        )
        self.patient_name_label.pack(anchor='w', pady=(5, 0))
        
        # Patient info row
        patient_info_row = ttk.Frame(self.patient_info_frame)
        patient_info_row.pack(anchor='w', pady=(2, 0))
        
        # Patient phone
        self.patient_phone_label = ttk.Label(
            patient_info_row,
            text="📞 Phone: N/A",
            font=('Segoe UI', 11)
        )
        self.patient_phone_label.pack(side='left', padx=(0, 20))
        
        # Patient gender
        self.patient_gender_label = ttk.Label(
            patient_info_row,
            text="👤 Gender: N/A",
            font=('Segoe UI', 11)
        )
        self.patient_gender_label.pack(side='left', padx=(0, 20))
        
        # Patient age
        self.patient_age_label = ttk.Label(
            patient_info_row,
            text="🎂 Age: N/A",
            font=('Segoe UI', 11)
        )
        self.patient_age_label.pack(side='left')
        
        # Patient created date
        self.patient_created_label = ttk.Label(
            self.patient_info_frame,
            text="📅 Created: N/A",
            font=('Segoe UI', 10),
            foreground='#7f8c8d'
        )
        self.patient_created_label.pack(anchor='w')
        
        # Patient notes (if any)
        self.patient_notes_label = ttk.Label(
            self.patient_info_frame,
            text="",
            font=('Segoe UI', 10),
            foreground='#7f8c8d',
            wraplength=400
        )
        self.patient_notes_label.pack(anchor='w', pady=(5, 0))
        
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
        
        # Total spent
        self.spent_card = ttk.Frame(stats_cards_frame, style='Card.TFrame', padding=10)
        self.spent_card.pack(side='left')
        
        self.spent_amount = ttk.Label(
            self.spent_card,
            text="$0.00",
            font=('Segoe UI', 14, 'bold'),
            foreground='#27ae60'
        )
        self.spent_amount.pack()
        
        spent_label = ttk.Label(
            self.spent_card,
            text="Total Paid",
            font=('Segoe UI', 9),
            foreground='#7f8c8d'
        )
        spent_label.pack()
        
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
        records_columns = ('ID', 'Doctor', 'Total Cost', 'Total Paid', 'Balance', 'Created')
        self.patient_records_tree = ttk.Treeview(records_section, columns=records_columns, show='headings')
        
        # Configure columns
        self.patient_records_tree.heading('ID', text=translations.get('col_id'))
        self.patient_records_tree.heading('Doctor', text=translations.get('col_doctor'))
        self.patient_records_tree.heading('Total Cost', text=translations.get('col_total_cost'))
        self.patient_records_tree.heading('Total Paid', text=translations.get('col_total_paid'))
        self.patient_records_tree.heading('Balance', text=translations.get('col_balance'))
        self.patient_records_tree.heading('Created', text=translations.get('col_created'))
        
        self.patient_records_tree.column('ID', width=80, anchor='center')
        self.patient_records_tree.column('Doctor', width=250)
        self.patient_records_tree.column('Total Cost', width=150, anchor='center')
        self.patient_records_tree.column('Total Paid', width=150, anchor='center')
        self.patient_records_tree.column('Balance', width=150, anchor='center')
        self.patient_records_tree.column('Created', width=200, anchor='center')
        
        self.patient_records_tree.pack(fill='both', expand=True)
        
        # Bind double-click to open record details
        self.patient_records_tree.bind('<Double-1>', self.on_record_double_click)
        
    def update_ui(self):
        """Update UI elements when language changes"""
        # Update header
        self.title_label.config(text=translations.get('patients_management'))
        self.add_btn.config(text=translations.get('add_patient'))
        self.edit_btn.config(text=translations.get('edit_patient'))
        self.delete_btn.config(text=translations.get('delete_patient'))
        
        # Update search
        self.search_label.config(text=translations.get('search_patients'))
        
        # Update table headers
        self.patients_tree.heading('Name', text=translations.get('col_name'))
        self.patients_tree.heading('Phone', text=translations.get('col_phone'))
        self.patients_tree.heading('Gender', text=translations.get('col_gender'))
        self.patients_tree.heading('Age', text=translations.get('col_age'))
        
        # Reload data to update gender translations
        self.load_patients()
        
        # Re-bind mousewheel after UI updates
        self.frame.after(100, self.bind_mousewheel)
        
    def show_details(self, patient):
        """Show patient details and related records"""
        self.selected_patient = patient
        
        # Update patient info
        self.patient_name_label.config(text=patient.name)
        self.patient_phone_label.config(text=f"📞 Phone: {patient.phone or 'N/A'}")
        
        # Gender with translation
        gender_text = "N/A"
        if patient.gender:
            gender_text = translations.get('gender_male') if patient.gender == 'Male' else translations.get('gender_female')
        self.patient_gender_label.config(text=f"👤 Gender: {gender_text}")
        
        # Age
        age_text = f"{patient.age} years" if patient.age else "N/A"
        self.patient_age_label.config(text=f"🎂 Age: {age_text}")
        
        created_date = patient.created_at.strftime("%Y-%m-%d %H:%M") if patient.created_at else "N/A"
        self.patient_created_label.config(text=f"📅 Created: {created_date}")
        
        # Notes
        if patient.notes:
            self.patient_notes_label.config(text=f"📝 Notes: {patient.notes}")
        else:
            self.patient_notes_label.config(text="")
        
        # Load related records
        self.load_patient_records(patient.id)
        
        # Show details frame and hide main content
        self.details_frame.grid(row=2, column=0, sticky="ew", pady=(15, 0))
        self.content_frame.rowconfigure(2, weight=1)
        
        # Update button states
        self.edit_btn.config(state='normal')
        self.delete_btn.config(state='disabled')  # Disable delete when viewing details
        
    def hide_details(self):
        """Hide patient details and return to list view"""
        self.details_frame.grid_forget()
        self.selected_patient = None
        self.edit_btn.config(state='disabled')
        self.delete_btn.config(state='disabled')
        
    def load_patient_records(self, patient_id):
        """Load records for the selected patient"""
        # Clear existing data
        for item in self.patient_records_tree.get_children():
            self.patient_records_tree.delete(item)
            
        try:
            from models import Record
            records = Record.get_by_patient(patient_id)
            
            total_records = len(records)
            total_paid = 0
            
            for record in records:
                # Get financial data
                total_cost = record.cost()
                amount_paid = record.amount()
                balance = record.balance()
                total_paid += amount_paid
                
                created_date = record.created_at.strftime("%Y-%m-%d %H:%M") if record.created_at else ""
                
                # Color coding for balance
                if balance > 0:
                    tag = 'unpaid'
                elif balance == 0 and total_cost > 0:
                    tag = 'paid'
                else:
                    tag = 'no_treatments'
                
                self.patient_records_tree.insert('', 'end', values=(
                    record.id,
                    getattr(record, 'doctor_name', 'Unknown'),
                    f"${total_cost:.2f}",
                    f"${amount_paid:.2f}",
                    f"${balance:.2f}",
                    created_date
                ), tags=(tag,))
            
            # Configure tags for visual feedback
            self.patient_records_tree.tag_configure('unpaid', foreground='#e74c3c')
            self.patient_records_tree.tag_configure('paid', foreground='#27ae60')
            self.patient_records_tree.tag_configure('no_treatments', foreground='#7f8c8d')
            
            # Update statistics
            self.records_count.config(text=str(total_records))
            self.spent_amount.config(text=f"${total_paid:.2f}")
            
        except Exception as e:
            messagebox.showerror(translations.get('error'), f"Failed to load patient records: {str(e)}")
            
    def on_record_double_click(self, event):
        """Handle double-click on record in patient details view"""
        selection = self.patient_records_tree.selection()
        if selection:
            item = self.patient_records_tree.item(selection[0])
            record_id = item['values'][0]
            
            try:
                from models import Record
                from gui.widgets.record_details import RecordDetailsWindow
                
                record = Record.get_by_id(record_id)
                if record:
                    RecordDetailsWindow(self.content_frame, record)
                    # Refresh the records after closing details window
                    self.load_patient_records(self.selected_patient.id)
            except Exception as e:
                messagebox.showerror(translations.get('error'), f"Failed to open record details: {str(e)}")
        
    def load_patients(self, search_term=None):
        """Load patients data into the table"""
        # Clear existing data
        for item in self.patients_tree.get_children():
            self.patients_tree.delete(item)
            
        try:
            if search_term:
                patients = Patient.search(search_term)
            else:
                patients = Patient.get_all()
                
            for patient in patients:
                created_date = patient.created_at.strftime("%Y-%m-%d %H:%M") if patient.created_at else ""
                birth_date = patient.birth_date.strftime("%Y-%m-%d") if patient.birth_date else ""
                status = translations.get('status_deleted') if patient.deleted_at else translations.get('status_active')
                
                # Translate gender
                gender_text = ""
                if patient.gender:
                    gender_text = translations.get('gender_male') if patient.gender == 'Male' else translations.get('gender_female')
                
                self.patients_tree.insert('', 'end', values=(
                    patient.name,
                    patient.phone or "",
                    gender_text,
                    patient.age or "",
                ), tags=(status.lower(),))
                
            # Configure tags for visual feedback
            self.patients_tree.tag_configure('deleted', foreground='#e74c3c')
            self.patients_tree.tag_configure('active', foreground='#27ae60')
            
        except Exception as e:
            messagebox.showerror(translations.get('error'), translations.get('failed_to_load', item='patients', error=str(e)))
            
    def on_search(self, *args):
        """Handle search input"""
        search_term = self.search_var.get().strip()
        if search_term:
            self.load_patients(search_term)
        else:
            self.load_patients()
            
    def on_patient_select(self, event):
        """Handle patient selection"""
        selection = self.patients_tree.selection()
        if selection:
            item = self.patients_tree.item(selection[0])
            patient_name = item['values'][0]  # Since we removed ID, name is first
            # Find patient by name (this is not ideal, but works for now)
            all_patients = Patient.get_all()
            self.selected_patient = next((p for p in all_patients if p.name == patient_name), None)
            
            # Enable edit and delete buttons
            self.edit_btn.config(state='normal')
            self.delete_btn.config(state='normal')
        else:
            self.selected_patient = None
            self.edit_btn.config(state='disabled')
            self.delete_btn.config(state='disabled')
            
    def on_patient_double_click(self, event):
        """Handle double-click on patient row"""
        if self.selected_patient:
            self.show_details(self.selected_patient)
            
    def add_patient(self):
        """Open add patient dialog"""
        dialog = PatientForm(self.content_frame, title=translations.get('add_new_patient'))
        if dialog.result:
            try:
                Patient.create(
                    name=dialog.result['name'],
                    phone=dialog.result['phone'],
                    gender=dialog.result['gender'],
                    birth_date=dialog.result['birth_date'],
                    notes=dialog.result['notes']
                )
                self.load_patients()
                messagebox.showinfo(translations.get('success'), translations.get('patient_added_success'))
            except ValueError as e:
                messagebox.showerror(translations.get('error'), str(e))
            except Exception as e:
                messagebox.showerror(translations.get('error'), translations.get('failed_to_add', item='patient', error=str(e)))
                
    def edit_patient(self):
        """Open edit patient dialog"""
        if not self.selected_patient:
            return
            
        dialog = PatientForm(
            self.content_frame, 
            title=translations.get('edit_patient_title'),
            patient=self.selected_patient
        )
        
        if dialog.result:
            try:
                Patient.update(
                    self.selected_patient.id,
                    name=dialog.result['name'],
                    phone=dialog.result['phone'],
                    gender=dialog.result['gender'],
                    birth_date=dialog.result['birth_date'],
                    notes=dialog.result['notes']
                )
                self.load_patients()
                messagebox.showinfo(translations.get('success'), translations.get('patient_updated_success'))
            except ValueError as e:
                messagebox.showerror(translations.get('error'), str(e))
            except Exception as e:
                messagebox.showerror(translations.get('error'), translations.get('failed_to_update', item='patient', error=str(e)))
                
    def delete_patient(self):
        """Delete selected patient"""
        if not self.selected_patient:
            return
            
        # Confirm deletion
        result = messagebox.askyesno(
            translations.get('confirm_deletion'),
            translations.get('confirm_delete_patient', name=self.selected_patient.name)
        )
        
        if result:
            try:
                Patient.delete(self.selected_patient.id)
                self.load_patients()
                self.selected_patient = None
                self.edit_btn.config(state='disabled')
                self.delete_btn.config(state='disabled')
                messagebox.showinfo(translations.get('success'), translations.get('patient_deleted_success'))
            except Exception as e:
                messagebox.showerror(translations.get('error'), translations.get('failed_to_delete', item='patient', error=str(e)))