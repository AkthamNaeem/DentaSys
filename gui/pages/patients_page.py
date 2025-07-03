import tkinter as tk
from tkinter import ttk, messagebox
from models import Patient
from gui.widgets.patient_form import PatientForm


class PatientsPage:
    def __init__(self, parent):
        self.parent = parent
        self.selected_patient = None
        self.setup_ui()
        self.load_patients()
        
    def setup_ui(self):
        # Main frame for the tab
        self.frame = ttk.Frame(self.parent)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        # Create scrollable canvas inside the main frame
        self.main_canvas = tk.Canvas(self.frame, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.main_canvas)
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Grid canvas and scrollbar
        self.main_canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure grid weights for the frame
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        # Bind mousewheel to canvas
        self.main_canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)
        
        # Set up the content frame structure
        self.content_frame = self.scrollable_frame
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(1, weight=1)
        
        # Header frame
        self.setup_header()
        
        # Content frame
        self.setup_content()
        
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def setup_header(self):
        header_frame = ttk.Frame(self.content_frame, style='Card.TFrame', padding=20)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(header_frame, text="👤 Patients Management", style='Title.TLabel')
        title_label.grid(row=0, column=0, sticky="w")
        
        # Buttons frame
        buttons_frame = ttk.Frame(header_frame)
        buttons_frame.grid(row=0, column=1, sticky="e")
        
        # Add Patient button
        self.add_btn = ttk.Button(
            buttons_frame, 
            text="➕ Add Patient", 
            style='Success.TButton',
            command=self.add_patient
        )
        self.add_btn.pack(side='right', padx=(10, 0))
        
        # Edit Patient button
        self.edit_btn = ttk.Button(
            buttons_frame, 
            text="✏️ Edit Patient", 
            style='Warning.TButton',
            command=self.edit_patient,
            state='disabled'
        )
        self.edit_btn.pack(side='right', padx=(10, 0))
        
        # Delete Patient button
        self.delete_btn = ttk.Button(
            buttons_frame, 
            text="🗑️ Delete Patient", 
            style='Danger.TButton',
            command=self.delete_patient,
            state='disabled'
        )
        self.delete_btn.pack(side='right')
        
    def setup_content(self):
        # Content frame
        content_frame = ttk.Frame(self.content_frame, style='Card.TFrame', padding=20)
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(1, weight=1)
        
        # Search frame
        search_frame = ttk.Frame(content_frame)
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        search_frame.columnconfigure(1, weight=1)
        
        # Search label and entry
        search_label = ttk.Label(search_frame, text="🔍 Search Patients:")
        search_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.grid(row=0, column=1, sticky="w")
        self.search_var.trace('w', self.on_search)
        
        # Table frame
        table_frame = ttk.Frame(content_frame)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Patients table
        columns = ('ID', 'Name', 'Phone', 'Gender', 'Birth Date', 'Created', 'Status')
        self.patients_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.patients_tree.heading('ID', text='ID')
        self.patients_tree.heading('Name', text='Name')
        self.patients_tree.heading('Phone', text='Phone')
        self.patients_tree.heading('Gender', text='Gender')
        self.patients_tree.heading('Birth Date', text='Birth Date')
        self.patients_tree.heading('Created', text='Created')
        self.patients_tree.heading('Status', text='Status')
        
        self.patients_tree.column('ID', width=60, anchor='center')
        self.patients_tree.column('Name', width=180)
        self.patients_tree.column('Phone', width=130)
        self.patients_tree.column('Gender', width=80, anchor='center')
        self.patients_tree.column('Birth Date', width=100, anchor='center')
        self.patients_tree.column('Created', width=130, anchor='center')
        self.patients_tree.column('Status', width=80, anchor='center')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.patients_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=self.patients_tree.xview)
        self.patients_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid table and scrollbars
        self.patients_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Bind events
        self.patients_tree.bind('<<TreeviewSelect>>', self.on_patient_select)
        self.patients_tree.bind('<Double-1>', self.on_patient_double_click)
        
        # Bind mousewheel to treeview
        self.patients_tree.bind("<MouseWheel>", self._on_mousewheel)
        
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
                status = "Deleted" if patient.deleted_at else "Active"
                
                self.patients_tree.insert('', 'end', values=(
                    patient.id,
                    patient.name,
                    patient.phone or "",
                    patient.gender or "",
                    birth_date,
                    created_date,
                    status
                ), tags=(status.lower(),))
                
            # Configure tags for visual feedback
            self.patients_tree.tag_configure('deleted', foreground='#e74c3c')
            self.patients_tree.tag_configure('active', foreground='#27ae60')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load patients: {str(e)}")
            
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
            patient_id = item['values'][0]
            self.selected_patient = Patient.get_by_id(patient_id)
            
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
            self.edit_patient()
            
    def add_patient(self):
        """Open add patient dialog"""
        dialog = PatientForm(self.content_frame, title="Add New Patient")
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
                messagebox.showinfo("Success", "Patient added successfully!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add patient: {str(e)}")
                
    def edit_patient(self):
        """Open edit patient dialog"""
        if not self.selected_patient:
            return
            
        dialog = PatientForm(
            self.content_frame, 
            title="Edit Patient",
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
                messagebox.showinfo("Success", "Patient updated successfully!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update patient: {str(e)}")
                
    def delete_patient(self):
        """Delete selected patient"""
        if not self.selected_patient:
            return
            
        # Confirm deletion
        result = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete {self.selected_patient.name}?\n\n"
            "Note: If this patient has records, they will be soft-deleted (marked as deleted but kept for data integrity)."
        )
        
        if result:
            try:
                Patient.delete(self.selected_patient.id)
                self.load_patients()
                self.selected_patient = None
                self.edit_btn.config(state='disabled')
                self.delete_btn.config(state='disabled')
                messagebox.showinfo("Success", "Patient deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete patient: {str(e)}")