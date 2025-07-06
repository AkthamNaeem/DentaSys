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
            self.delete_btn.config(state='disabled')
        else:
            self.selected_doctor = None
            self.edit_btn.config(state='disabled')
            self.delete_btn.config(state='disabled')
            
    def on_doctor_double_click(self, event):
        """Handle double-click on doctor row"""
        if self.selected_doctor:
            self.edit_doctor()
            
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