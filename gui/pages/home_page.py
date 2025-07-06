import tkinter as tk
from tkinter import ttk
import threading
import time
from models import Doctor, Patient, Record
from localization.translations import translations


class HomePage:
    def __init__(self, parent):
        self.parent = parent
        self.search_thread = None
        self.search_delay = 0.5  # Delay in seconds before searching
        self.last_search_time = 0
        
        # Register for language change notifications
        translations.add_observer(self.update_ui)
        
        self.setup_ui()
        
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
        
        # Welcome section
        self.setup_welcome_section()
        
        # Search section
        self.setup_search_section()
        
        # Results section
        self.setup_results_section()
        
        # Load initial data
        self.load_dashboard_stats()
        
    def bind_mousewheel(self):
        """Bind mousewheel events to the main canvas for full page scrolling"""
        def _on_mousewheel(event):
            self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind to multiple widgets to ensure scrolling works everywhere
        self.main_canvas.bind("<MouseWheel>", _on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
        
        # Bind to the frame itself
        self.frame.bind("<MouseWheel>", _on_mousewheel)
        
        # Function to bind mousewheel to all child widgets recursively
        def bind_to_children(widget):
            widget.bind("<MouseWheel>", _on_mousewheel)
            for child in widget.winfo_children():
                bind_to_children(child)
        
        # Bind after a short delay to ensure all widgets are created
        self.frame.after(100, lambda: bind_to_children(self.scrollable_frame))
        
    def setup_welcome_section(self):
        # Welcome frame with full width and minimal padding
        welcome_frame = ttk.Frame(self.content_frame, style='Card.TFrame', padding=20)
        welcome_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        welcome_frame.columnconfigure(1, weight=1)
        
        # Welcome text with improved typography
        self.welcome_label = ttk.Label(
            welcome_frame, 
            text=translations.get('welcome_title'), 
            style='Title.TLabel'
        )
        self.welcome_label.grid(row=0, column=0, columnspan=2, sticky="w")
        
        # Stats frame with full width
        stats_frame = ttk.Frame(welcome_frame)
        stats_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(20, 0))
        stats_frame.columnconfigure((0, 1, 2), weight=1)
        
        # Stats cards with improved sizing
        self.doctors_stat = self.create_stat_card(stats_frame, translations.get('stat_doctors'), "0", "#3498db", 0)
        self.patients_stat = self.create_stat_card(stats_frame, translations.get('stat_patients'), "0", "#27ae60", 1)
        self.records_stat = self.create_stat_card(stats_frame, translations.get('stat_records'), "0", "#f39c12", 2)
        
    def create_stat_card(self, parent, title, value, color, column):
        card_frame = ttk.Frame(parent, style='Card.TFrame', padding=20)
        card_frame.grid(row=0, column=column, sticky="ew", padx=(0, 10) if column < 2 else 0)
        
        # Value label with larger font
        value_label = ttk.Label(
            card_frame, 
            text=value, 
            font=('Segoe UI', 24, 'bold'),
            foreground=color
        )
        value_label.pack()
        
        # Title label with better spacing
        title_label = ttk.Label(
            card_frame, 
            text=title, 
            font=('Segoe UI', 12),
            foreground="#7f8c8d"
        )
        title_label.pack(pady=(5, 0))
        
        return {'value': value_label, 'title': title_label}
        
    def setup_search_section(self):
        # Search frame with full width and minimal padding
        search_frame = ttk.Frame(self.content_frame, style='Card.TFrame', padding=20)
        search_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        search_frame.columnconfigure(1, weight=1)
        
        # Search label with improved typography
        self.search_label = ttk.Label(search_frame, text=translations.get('search_title'), style='Heading.TLabel')
        self.search_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))
        
        # Search entry with full width
        self.search_entry_label = ttk.Label(search_frame, text=translations.get('search_placeholder'), font=('Segoe UI', 11))
        self.search_entry_label.grid(row=1, column=0, sticky="w", pady=(0, 8))
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            search_frame, 
            textvariable=self.search_var,
            font=('Segoe UI', 12)
        )
        self.search_entry.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 12), ipady=8)
        
        # Bind search event
        self.search_var.trace('w', self.on_search_change)
        
        # Search status with better spacing
        self.search_status = ttk.Label(
            search_frame, 
            text=translations.get('search_instruction'),
            font=('Segoe UI', 10),
            foreground="#7f8c8d"
        )
        self.search_status.grid(row=3, column=0, columnspan=2, sticky="w")
        
    def setup_results_section(self):
        # Results frame with full width and minimal padding
        results_frame = ttk.Frame(self.content_frame, style='Card.TFrame', padding=20)
        results_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        results_frame.columnconfigure(0, weight=1)
        
        # Results label with improved spacing
        self.results_label = ttk.Label(results_frame, text=translations.get('dashboard_title'), style='Heading.TLabel')
        self.results_label.grid(row=0, column=0, sticky="w", pady=(0, 15))
        
        # Create notebook for different result types with full width
        self.results_notebook = ttk.Notebook(results_frame)
        self.results_notebook.grid(row=1, column=0, sticky="ew")
        
        # Doctors results
        self.setup_doctors_results()
        
        # Patients results
        self.setup_patients_results()
        
        # Records results
        self.setup_records_results()
        
    def setup_doctors_results(self):
        # Doctors frame with full width
        doctors_frame = ttk.Frame(self.results_notebook, padding=10)
        doctors_frame.columnconfigure(0, weight=1)
        
        # Doctors treeview with fixed height (no internal scrolling)
        doctors_columns = ('ID', 'Name', 'Phone', 'Created')
        self.doctors_tree = ttk.Treeview(doctors_frame, columns=doctors_columns, show='headings', height=8)
        
        # Configure columns with better widths
        self.doctors_tree.heading('ID', text=translations.get('col_id'))
        self.doctors_tree.heading('Name', text=translations.get('col_name'))
        self.doctors_tree.heading('Phone', text=translations.get('col_phone'))
        self.doctors_tree.heading('Created', text=translations.get('col_created'))
        
        self.doctors_tree.column('ID', width=60, anchor='center')
        self.doctors_tree.column('Name', width=250)
        self.doctors_tree.column('Phone', width=180)
        self.doctors_tree.column('Created', width=180)
        
        # Grid doctors treeview (no scrollbar - let page scroll handle it)
        self.doctors_tree.grid(row=0, column=0, sticky="ew")
        
        self.results_notebook.add(doctors_frame, text=translations.get('tab_doctors'))
        
    def setup_patients_results(self):
        # Patients frame with full width
        patients_frame = ttk.Frame(self.results_notebook, padding=10)
        patients_frame.columnconfigure(0, weight=1)
        
        # Patients treeview with fixed height (no internal scrolling)
        patients_columns = ('ID', 'Name', 'Phone', 'Gender', 'Birth Date')
        self.patients_tree = ttk.Treeview(patients_frame, columns=patients_columns, show='headings', height=8)
        
        # Configure columns with better widths
        self.patients_tree.heading('ID', text=translations.get('col_id'))
        self.patients_tree.heading('Name', text=translations.get('col_name'))
        self.patients_tree.heading('Phone', text=translations.get('col_phone'))
        self.patients_tree.heading('Gender', text=translations.get('col_gender'))
        self.patients_tree.heading('Birth Date', text=translations.get('col_birth_date'))
        
        self.patients_tree.column('ID', width=60, anchor='center')
        self.patients_tree.column('Name', width=250)
        self.patients_tree.column('Phone', width=180)
        self.patients_tree.column('Gender', width=120, anchor='center')
        self.patients_tree.column('Birth Date', width=140, anchor='center')
        
        # Grid patients treeview (no scrollbar - let page scroll handle it)
        self.patients_tree.grid(row=0, column=0, sticky="ew")
        
        self.results_notebook.add(patients_frame, text=translations.get('tab_patients'))
        
    def setup_records_results(self):
        # Records frame with full width
        records_frame = ttk.Frame(self.results_notebook, padding=10)
        records_frame.columnconfigure(0, weight=1)
        
        # Records treeview with fixed height (no internal scrolling)
        records_columns = ('ID', 'Doctor', 'Patient', 'Cost', 'Paid', 'Balance', 'Created')
        self.records_tree = ttk.Treeview(records_frame, columns=records_columns, show='headings', height=8)
        
        # Configure columns with better widths
        self.records_tree.heading('ID', text=translations.get('col_id'))
        self.records_tree.heading('Doctor', text=translations.get('col_doctor'))
        self.records_tree.heading('Patient', text=translations.get('col_patient'))
        self.records_tree.heading('Cost', text=translations.get('col_total_cost'))
        self.records_tree.heading('Paid', text=translations.get('col_total_paid'))
        self.records_tree.heading('Balance', text=translations.get('col_balance'))
        self.records_tree.heading('Created', text=translations.get('col_created'))
        
        self.records_tree.column('ID', width=60, anchor='center')
        self.records_tree.column('Doctor', width=180)
        self.records_tree.column('Patient', width=180)
        self.records_tree.column('Cost', width=120, anchor='center')
        self.records_tree.column('Paid', width=120, anchor='center')
        self.records_tree.column('Balance', width=120, anchor='center')
        self.records_tree.column('Created', width=180)
        
        # Grid records treeview (no scrollbar - let page scroll handle it)
        self.records_tree.grid(row=0, column=0, sticky="ew")
        
        self.results_notebook.add(records_frame, text=translations.get('tab_records'))
        
    def update_ui(self):
        """Update UI elements when language changes"""
        # Update welcome section
        self.welcome_label.config(text=translations.get('welcome_title'))
        
        # Update stat card titles
        self.doctors_stat['title'].config(text=translations.get('stat_doctors'))
        self.patients_stat['title'].config(text=translations.get('stat_patients'))
        self.records_stat['title'].config(text=translations.get('stat_records'))
        
        # Update search section
        self.search_label.config(text=translations.get('search_title'))
        self.search_entry_label.config(text=translations.get('search_placeholder'))
        self.search_status.config(text=translations.get('search_instruction'))
        
        # Update results section
        self.results_label.config(text=translations.get('dashboard_title'))
        
        # Update table headers
        # Doctors table
        self.doctors_tree.heading('ID', text=translations.get('col_id'))
        self.doctors_tree.heading('Name', text=translations.get('col_name'))
        self.doctors_tree.heading('Phone', text=translations.get('col_phone'))
        self.doctors_tree.heading('Created', text=translations.get('col_created'))
        
        # Patients table
        self.patients_tree.heading('ID', text=translations.get('col_id'))
        self.patients_tree.heading('Name', text=translations.get('col_name'))
        self.patients_tree.heading('Phone', text=translations.get('col_phone'))
        self.patients_tree.heading('Gender', text=translations.get('col_gender'))
        self.patients_tree.heading('Birth Date', text=translations.get('col_birth_date'))
        
        # Records table
        self.records_tree.heading('ID', text=translations.get('col_id'))
        self.records_tree.heading('Doctor', text=translations.get('col_doctor'))
        self.records_tree.heading('Patient', text=translations.get('col_patient'))
        self.records_tree.heading('Cost', text=translations.get('col_total_cost'))
        self.records_tree.heading('Paid', text=translations.get('col_total_paid'))
        self.records_tree.heading('Balance', text=translations.get('col_balance'))
        self.records_tree.heading('Created', text=translations.get('col_created'))
        
        # Update notebook tab texts
        self.results_notebook.tab(0, text=translations.get('tab_doctors'))
        self.results_notebook.tab(1, text=translations.get('tab_patients'))
        self.results_notebook.tab(2, text=translations.get('tab_records'))
        
        # Re-bind mousewheel after UI updates
        self.frame.after(100, self.bind_mousewheel)
        
    def load_dashboard_stats(self):
        """Load dashboard statistics"""
        try:
            # Get counts
            doctors = Doctor.get_all()
            patients = Patient.get_all()
            records = Record.get_all()
            
            # Update stats
            self.doctors_stat['value'].config(text=str(len(doctors)))
            self.patients_stat['value'].config(text=str(len(patients)))
            self.records_stat['value'].config(text=str(len(records)))
            
            # Load initial data in tables
            self.load_doctors_data(doctors)
            self.load_patients_data(patients)
            self.load_records_data(records)
            
        except Exception as e:
            print(f"Error loading dashboard stats: {e}")
            
    def load_doctors_data(self, doctors):
        """Load doctors data into treeview"""
        # Clear existing data
        for item in self.doctors_tree.get_children():
            self.doctors_tree.delete(item)
            
        # Insert new data
        for doctor in doctors:
            created_date = doctor.created_at.strftime("%Y-%m-%d %H:%M") if doctor.created_at else ""
            self.doctors_tree.insert('', 'end', values=(
                doctor.id,
                doctor.name,
                doctor.phone or "",
                created_date
            ))
            
    def load_patients_data(self, patients):
        """Load patients data into treeview"""
        # Clear existing data
        for item in self.patients_tree.get_children():
            self.patients_tree.delete(item)
            
        # Insert new data
        for patient in patients:
            birth_date = patient.birth_date.strftime("%Y-%m-%d") if patient.birth_date else ""
            gender_text = ""
            if patient.gender:
                gender_text = translations.get('gender_male') if patient.gender == 'Male' else translations.get('gender_female')
            
            self.patients_tree.insert('', 'end', values=(
                patient.id,
                patient.name,
                patient.phone,
                gender_text,
                birth_date
            ))
            
    def load_records_data(self, records):
        """Load records data into treeview"""
        # Clear existing data
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
            
        # Insert new data
        for record in records:
            created_date = record.created_at.strftime("%Y-%m-%d %H:%M") if record.created_at else ""
            
            # Use the cached financial data if available, otherwise calculate
            if hasattr(record, '_total_cost'):
                cost = f"${record._total_cost:.2f}"
                amount = f"${record._total_amount:.2f}"
                balance = f"${record._balance:.2f}"
            else:
                cost = f"${record.cost():.2f}"
                amount = f"${record.amount():.2f}"
                balance = f"${record.balance():.2f}"
            
            self.records_tree.insert('', 'end', values=(
                record.id,
                getattr(record, 'doctor_name', ''),
                getattr(record, 'patient_name', ''),
                cost,
                amount,
                balance,
                created_date
            ))
            
    def on_search_change(self, *args):
        """Handle search input change with debouncing"""
        self.last_search_time = time.time()
        
        # Cancel previous search thread if it exists
        if self.search_thread and self.search_thread.is_alive():
            return
            
        # Start new search thread with delay
        self.search_thread = threading.Thread(target=self.delayed_search)
        self.search_thread.daemon = True
        self.search_thread.start()
        
    def delayed_search(self):
        """Perform search after delay to avoid too many requests"""
        time.sleep(self.search_delay)
        
        # Check if this is still the latest search
        if time.time() - self.last_search_time < self.search_delay:
            return
            
        # Perform search on main thread
        self.content_frame.after(0, self.perform_search)
        
    def perform_search(self):
        """Perform the actual search"""
        search_term = self.search_var.get().strip()
        
        if not search_term:
            # If search is empty, load all data
            self.search_status.config(text=translations.get('showing_all'))
            self.load_dashboard_stats()
            self.results_label.config(text=translations.get('dashboard_title'))
            return
            
        try:
            # Update status
            self.search_status.config(text=f"{translations.get('searching_for')} '{search_term}'...")
            self.results_label.config(text=f"{translations.get('search_results')} '{search_term}'")
            
            # Search doctors
            doctors = Doctor.search(search_term)
            self.load_doctors_data(doctors)
            
            # Search patients
            patients = Patient.search(search_term)
            self.load_patients_data(patients)
            
            # For records, we need to search by doctor or patient names
            all_records = Record.get_all()
            filtered_records = []
            
            for record in all_records:
                doctor_name = getattr(record, 'doctor_name', '').lower()
                patient_name = getattr(record, 'patient_name', '').lower()
                
                if (search_term.lower() in doctor_name or 
                    search_term.lower() in patient_name):
                    filtered_records.append(record)
                    
            self.load_records_data(filtered_records)
            
            # Update status with results count
            total_results = len(doctors) + len(patients) + len(filtered_records)
            self.search_status.config(
                text=translations.get('found_results', 
                    total=total_results, 
                    doctors=len(doctors), 
                    patients=len(patients), 
                    records=len(filtered_records)
                )
            )
            
        except Exception as e:
            self.search_status.config(text=translations.get('search_error', error=str(e)))
            print(f"Search error: {e}")