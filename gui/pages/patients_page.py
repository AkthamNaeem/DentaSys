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
            self.edit_patient()
            
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