import tkinter as tk
from tkinter import ttk
import threading
import time
from models import Doctor, Patient, Record


class HomePage:
    def __init__(self, parent):
        self.parent = parent
        self.search_thread = None
        self.search_delay = 0.5  # Delay in seconds before searching
        self.last_search_time = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame with scrollable canvas
        self.main_canvas = tk.Canvas(self.parent, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.main_canvas)
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas and scrollbar
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        self.main_canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)
        
        # Set up the actual frame content
        self.frame = self.scrollable_frame
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(2, weight=1)
        
        # Welcome section
        self.setup_welcome_section()
        
        # Search section
        self.setup_search_section()
        
        # Results section
        self.setup_results_section()
        
        # Load initial data
        self.load_dashboard_stats()
        
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def setup_welcome_section(self):
        # Welcome frame
        welcome_frame = ttk.Frame(self.frame, style='Card.TFrame', padding=20)
        welcome_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        welcome_frame.columnconfigure(1, weight=1)
        
        # Welcome text
        welcome_label = ttk.Label(
            welcome_frame, 
            text="Welcome to DentaSys", 
            style='Title.TLabel'
        )
        welcome_label.grid(row=0, column=0, columnspan=2, sticky="w")
        
        description_label = ttk.Label(
            welcome_frame, 
            text="Manage your dental practice efficiently with our comprehensive management system.",
            font=('Segoe UI', 10)
        )
        description_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 15))
        
        # Stats frame
        stats_frame = ttk.Frame(welcome_frame)
        stats_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
        stats_frame.columnconfigure((0, 1, 2), weight=1)
        
        # Stats cards
        self.doctors_stat = self.create_stat_card(stats_frame, "Doctors", "0", "#3498db", 0)
        self.patients_stat = self.create_stat_card(stats_frame, "Patients", "0", "#27ae60", 1)
        self.records_stat = self.create_stat_card(stats_frame, "Records", "0", "#f39c12", 2)
        
    def create_stat_card(self, parent, title, value, color, column):
        card_frame = ttk.Frame(parent, style='Card.TFrame', padding=15)
        card_frame.grid(row=0, column=column, sticky="ew", padx=(0, 10) if column < 2 else 0)
        
        # Value label
        value_label = ttk.Label(
            card_frame, 
            text=value, 
            font=('Segoe UI', 20, 'bold'),
            foreground=color
        )
        value_label.pack()
        
        # Title label
        title_label = ttk.Label(
            card_frame, 
            text=title, 
            font=('Segoe UI', 10),
            foreground="#7f8c8d"
        )
        title_label.pack()
        
        return value_label
        
    def setup_search_section(self):
        # Search frame
        search_frame = ttk.Frame(self.frame, style='Card.TFrame', padding=20)
        search_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        search_frame.columnconfigure(1, weight=1)
        
        # Search label
        search_label = ttk.Label(search_frame, text="🔍 Search", style='Heading.TLabel')
        search_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # Search entry
        search_entry_label = ttk.Label(search_frame, text="Search doctors, patients, or records:")
        search_entry_label.grid(row=1, column=0, sticky="w", pady=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            search_frame, 
            textvariable=self.search_var,
            font=('Segoe UI', 11),
            width=50
        )
        self.search_entry.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # Bind search event
        self.search_var.trace('w', self.on_search_change)
        
        # Search status
        self.search_status = ttk.Label(
            search_frame, 
            text="Type to search across doctors, patients, and records...",
            font=('Segoe UI', 9),
            foreground="#7f8c8d"
        )
        self.search_status.grid(row=3, column=0, columnspan=2, sticky="w")
        
    def setup_results_section(self):
        # Results frame
        results_frame = ttk.Frame(self.frame, style='Card.TFrame', padding=20)
        results_frame.grid(row=2, column=0, sticky="nsew")
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(1, weight=1)
        
        # Results label
        self.results_label = ttk.Label(results_frame, text="📊 Dashboard", style='Heading.TLabel')
        self.results_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Create notebook for different result types
        self.results_notebook = ttk.Notebook(results_frame)
        self.results_notebook.grid(row=1, column=0, sticky="nsew")
        
        # Doctors results
        self.setup_doctors_results()
        
        # Patients results
        self.setup_patients_results()
        
        # Records results
        self.setup_records_results()
        
    def setup_doctors_results(self):
        # Doctors frame
        doctors_frame = ttk.Frame(self.results_notebook)
        doctors_frame.columnconfigure(0, weight=1)
        doctors_frame.rowconfigure(0, weight=1)
        
        # Doctors treeview
        doctors_columns = ('ID', 'Name', 'Phone', 'Created')
        self.doctors_tree = ttk.Treeview(doctors_frame, columns=doctors_columns, show='headings', height=10)
        
        # Configure columns
        self.doctors_tree.heading('ID', text='ID')
        self.doctors_tree.heading('Name', text='Name')
        self.doctors_tree.heading('Phone', text='Phone')
        self.doctors_tree.heading('Created', text='Created')
        
        self.doctors_tree.column('ID', width=50, anchor='center')
        self.doctors_tree.column('Name', width=200)
        self.doctors_tree.column('Phone', width=150)
        self.doctors_tree.column('Created', width=150)
        
        # Scrollbar for doctors
        doctors_scrollbar = ttk.Scrollbar(doctors_frame, orient='vertical', command=self.doctors_tree.yview)
        self.doctors_tree.configure(yscrollcommand=doctors_scrollbar.set)
        
        # Grid doctors treeview and scrollbar
        self.doctors_tree.grid(row=0, column=0, sticky="nsew")
        doctors_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.results_notebook.add(doctors_frame, text="👨‍⚕️ Doctors")
        
    def setup_patients_results(self):
        # Patients frame
        patients_frame = ttk.Frame(self.results_notebook)
        patients_frame.columnconfigure(0, weight=1)
        patients_frame.rowconfigure(0, weight=1)
        
        # Patients treeview
        patients_columns = ('ID', 'Name', 'Phone', 'Gender', 'Birth Date')
        self.patients_tree = ttk.Treeview(patients_frame, columns=patients_columns, show='headings', height=10)
        
        # Configure columns
        self.patients_tree.heading('ID', text='ID')
        self.patients_tree.heading('Name', text='Name')
        self.patients_tree.heading('Phone', text='Phone')
        self.patients_tree.heading('Gender', text='Gender')
        self.patients_tree.heading('Birth Date', text='Birth Date')
        
        self.patients_tree.column('ID', width=50, anchor='center')
        self.patients_tree.column('Name', width=200)
        self.patients_tree.column('Phone', width=150)
        self.patients_tree.column('Gender', width=100, anchor='center')
        self.patients_tree.column('Birth Date', width=120, anchor='center')
        
        # Scrollbar for patients
        patients_scrollbar = ttk.Scrollbar(patients_frame, orient='vertical', command=self.patients_tree.yview)
        self.patients_tree.configure(yscrollcommand=patients_scrollbar.set)
        
        # Grid patients treeview and scrollbar
        self.patients_tree.grid(row=0, column=0, sticky="nsew")
        patients_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.results_notebook.add(patients_frame, text="👤 Patients")
        
    def setup_records_results(self):
        # Records frame
        records_frame = ttk.Frame(self.results_notebook)
        records_frame.columnconfigure(0, weight=1)
        records_frame.rowconfigure(0, weight=1)
        
        # Records treeview
        records_columns = ('ID', 'Doctor', 'Patient', 'Cost', 'Paid', 'Balance', 'Created')
        self.records_tree = ttk.Treeview(records_frame, columns=records_columns, show='headings', height=10)
        
        # Configure columns
        self.records_tree.heading('ID', text='ID')
        self.records_tree.heading('Doctor', text='Doctor')
        self.records_tree.heading('Patient', text='Patient')
        self.records_tree.heading('Cost', text='Cost')
        self.records_tree.heading('Paid', text='Paid')
        self.records_tree.heading('Balance', text='Balance')
        self.records_tree.heading('Created', text='Created')
        
        self.records_tree.column('ID', width=50, anchor='center')
        self.records_tree.column('Doctor', width=150)
        self.records_tree.column('Patient', width=150)
        self.records_tree.column('Cost', width=100, anchor='center')
        self.records_tree.column('Paid', width=100, anchor='center')
        self.records_tree.column('Balance', width=100, anchor='center')
        self.records_tree.column('Created', width=150)
        
        # Scrollbar for records
        records_scrollbar = ttk.Scrollbar(records_frame, orient='vertical', command=self.records_tree.yview)
        self.records_tree.configure(yscrollcommand=records_scrollbar.set)
        
        # Grid records treeview and scrollbar
        self.records_tree.grid(row=0, column=0, sticky="nsew")
        records_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.results_notebook.add(records_frame, text="📋 Records")
        
    def load_dashboard_stats(self):
        """Load dashboard statistics"""
        try:
            # Get counts
            doctors = Doctor.get_all()
            patients = Patient.get_all()
            records = Record.get_all()
            
            # Update stats
            self.doctors_stat.config(text=str(len(doctors)))
            self.patients_stat.config(text=str(len(patients)))
            self.records_stat.config(text=str(len(records)))
            
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
            self.patients_tree.insert('', 'end', values=(
                patient.id,
                patient.name,
                patient.phone,
                patient.gender or "",
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
            cost = f"${record.cost:.2f}" if hasattr(record, 'cost') else "$0.00"
            amount = f"${record.amount:.2f}" if hasattr(record, 'amount') else "$0.00"
            balance = f"${record.balance:.2f}" if hasattr(record, 'balance') else "$0.00"
            
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
        self.frame.after(0, self.perform_search)
        
    def perform_search(self):
        """Perform the actual search"""
        search_term = self.search_var.get().strip()
        
        if not search_term:
            # If search is empty, load all data
            self.search_status.config(text="Showing all records...")
            self.load_dashboard_stats()
            self.results_label.config(text="📊 Dashboard")
            return
            
        try:
            # Update status
            self.search_status.config(text=f"Searching for '{search_term}'...")
            self.results_label.config(text=f"🔍 Search Results for '{search_term}'")
            
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
                text=f"Found {total_results} results: {len(doctors)} doctors, {len(patients)} patients, {len(filtered_records)} records"
            )
            
        except Exception as e:
            self.search_status.config(text=f"Search error: {str(e)}")
            print(f"Search error: {e}")