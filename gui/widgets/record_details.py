import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from models import Treatment, Payment
from gui.widgets.treatment_form import TreatmentForm
from gui.widgets.payment_form import PaymentForm
from localization.translations import translations
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os
from datetime import datetime


class RecordDetailsWindow:
    def __init__(self, parent, record):
        self.parent = parent
        self.record = record
        self.selected_treatment = None
        self.selected_payment = None
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title(f"Record Details - {record.doctor_name} & {record.patient_name}")
        self.window.geometry("1200x900")
        self.window.resizable(True, True)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Center the window
        self.center_window()
        
        # Setup UI with full window scrolling
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
        
        self.window.geometry(f"1200x900+{x}+{y}")
        
    def setup_ui(self):
        # Main frame for the window
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill='both', expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Create scrollable canvas for the entire window
        self.main_canvas = tk.Canvas(main_frame, highlightthickness=0)
        self.main_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.main_canvas.yview)
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
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Bind mousewheel for full window scrolling
        self.bind_mousewheel()
        
        # Set up content with minimal padding for full width
        content_frame = ttk.Frame(self.scrollable_frame, padding=15)
        content_frame.pack(fill='both', expand=True)
        content_frame.columnconfigure(0, weight=1)
        
        # Header frame with account summary
        self.setup_header(content_frame)
        
        # Content notebook
        self.setup_content(content_frame)
        
        # Buttons frame
        self.setup_buttons(content_frame)
        
    def bind_mousewheel(self):
        """Bind mousewheel events for full window scrolling"""
        def _on_mousewheel(event):
            self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind to multiple widgets to ensure scrolling works everywhere
        self.main_canvas.bind("<MouseWheel>", _on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
        self.window.bind("<MouseWheel>", _on_mousewheel)
        
        # Function to bind mousewheel to all child widgets recursively
        def bind_to_children(widget):
            widget.bind("<MouseWheel>", _on_mousewheel)
            for child in widget.winfo_children():
                bind_to_children(child)
        
        # Bind after a short delay to ensure all widgets are created
        self.window.after(100, lambda: bind_to_children(self.scrollable_frame))
        
    def setup_header(self, parent):
        header_frame = ttk.Frame(parent, style='Card.TFrame', padding=15)
        header_frame.pack(fill='x', pady=(0, 15))
        header_frame.columnconfigure(1, weight=1)
        
        # Left side - Record info
        info_frame = ttk.Frame(header_frame)
        info_frame.grid(row=0, column=0, sticky="w", padx=(0, 20))
        
        # Title
        title_label = ttk.Label(
            info_frame, 
            text=translations.get('record_details'), 
            font=('Segoe UI', 18, 'bold'),
            foreground='#2c3e50'
        )
        title_label.pack(anchor='w')
        
        # Record info
        # Doctor info
        doctor_label = ttk.Label(
            info_frame, 
            text=f"👨‍⚕️ {translations.get('col_doctor')}: {self.record.doctor_name}",
            font=('Segoe UI', 12)
        )
        doctor_label.pack(anchor='w', pady=(5, 0))
        
        # Patient info
        patient_label = ttk.Label(
            info_frame, 
            text=f"👤 {translations.get('col_patient')}: {self.record.patient_name}",
            font=('Segoe UI', 12)
        )
        patient_label.pack(anchor='w')
        
        # Created date
        created_date = self.record.created_at.strftime("%Y-%m-%d %H:%M") if self.record.created_at else translations.get('unknown')
        created_label = ttk.Label(
            info_frame, 
            text=f"📅 {translations.get('col_created')}: {created_date}",
            font=('Segoe UI', 10),
            foreground='#7f8c8d'
        )
        created_label.pack(anchor='w')
        
        # Right side - Account Summary
        summary_frame = ttk.Frame(header_frame)
        summary_frame.grid(row=0, column=1, sticky="e")
        
        # Summary title
        summary_title = ttk.Label(
            summary_frame, 
            text=f"📊 {translations.get('account_summary')}", 
            font=('Segoe UI', 14, 'bold'),
            foreground='#2c3e50'
        )
        summary_title.pack(anchor='e', pady=(0, 10))
        
        # Summary grid
        summary_grid = ttk.Frame(summary_frame)
        summary_grid.pack(anchor='e')
        
        # Create summary cards in a horizontal layout
        cards_frame = ttk.Frame(summary_grid)
        cards_frame.pack()
        
        # Total cost card
        self.cost_frame = ttk.Frame(cards_frame, style='Card.TFrame', padding=15)
        self.cost_frame.pack(side='left', padx=(0, 10))
        
        self.cost_value = ttk.Label(
            self.cost_frame, 
            text="$0.00", 
            font=('Segoe UI', 16, 'bold'),
            foreground='#3498db'
        )
        self.cost_value.pack()
        
        cost_label = ttk.Label(
            self.cost_frame, 
            text=translations.get('total_cost'), 
            font=('Segoe UI', 10),
            foreground='#7f8c8d'
        )
        cost_label.pack()
        
        # Total paid card
        self.paid_frame = ttk.Frame(cards_frame, style='Card.TFrame', padding=15)
        self.paid_frame.pack(side='left', padx=(0, 10))
        
        self.paid_value = ttk.Label(
            self.paid_frame, 
            text="$0.00", 
            font=('Segoe UI', 16, 'bold'),
            foreground='#27ae60'
        )
        self.paid_value.pack()
        
        paid_label = ttk.Label(
            self.paid_frame, 
            text=translations.get('total_paid'), 
            font=('Segoe UI', 10),
            foreground='#7f8c8d'
        )
        paid_label.pack()
        
        # Balance card
        self.balance_frame = ttk.Frame(cards_frame, style='Card.TFrame', padding=15)
        self.balance_frame.pack(side='left')
        
        self.balance_value = ttk.Label(
            self.balance_frame, 
            text="$0.00", 
            font=('Segoe UI', 16, 'bold'),
            foreground='#e74c3c'
        )
        self.balance_value.pack()
        
        balance_label = ttk.Label(
            self.balance_frame, 
            text=translations.get('balance'), 
            font=('Segoe UI', 10),
            foreground='#7f8c8d'
        )
        balance_label.pack()
        
    def setup_content(self, parent):
        # Create notebook for treatments and payments with full width
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill='both', expand=True, pady=(0, 15))
        
        # Treatments tab
        self.setup_treatments_tab()
        
        # Payments tab
        self.setup_payments_tab()
        
    def setup_treatments_tab(self):
        # Treatments frame with full width
        treatments_frame = ttk.Frame(self.notebook)
        treatments_frame.columnconfigure(0, weight=1)
        
        # Treatments header
        treatments_header = ttk.Frame(treatments_frame, padding=15)
        treatments_header.grid(row=0, column=0, sticky="ew")
        treatments_header.columnconfigure(1, weight=1)
        
        treatments_title = ttk.Label(
            treatments_header, 
            text=f"🦷 {translations.get('treatments_tab')}", 
            font=('Segoe UI', 14, 'bold')
        )
        treatments_title.grid(row=0, column=0, sticky="w")
        
        # Treatment buttons
        treatment_buttons = ttk.Frame(treatments_header)
        treatment_buttons.grid(row=0, column=1, sticky="e")
        
        self.add_treatment_btn = ttk.Button(
            treatment_buttons,
            text=translations.get('add_treatment'),
            style='Success.TButton',
            command=self.add_treatment
        )
        self.add_treatment_btn.pack(side='right', padx=(10, 0), ipadx=15, ipady=8)
        
        self.edit_treatment_btn = ttk.Button(
            treatment_buttons,
            text=translations.get('edit_treatment'),
            style='Warning.TButton',
            command=self.edit_treatment,
            state='disabled'
        )
        self.edit_treatment_btn.pack(side='right', padx=(10, 0), ipadx=15, ipady=8)
        
        self.delete_treatment_btn = ttk.Button(
            treatment_buttons,
            text=translations.get('delete_treatment'),
            style='Danger.TButton',
            command=self.delete_treatment,
            state='disabled'
        )
        self.delete_treatment_btn.pack(side='right', ipadx=15, ipady=8)
        
        # Treatments table with full width
        treatments_table_frame = ttk.Frame(treatments_frame, padding=15)
        treatments_table_frame.grid(row=1, column=0, sticky="ew")
        treatments_table_frame.columnconfigure(0, weight=1)
        
        treatment_columns = ('ID', 'Name', 'Cost', 'Date', 'Notes')
        self.treatments_tree = ttk.Treeview(
            treatments_table_frame, 
            columns=treatment_columns, 
            show='headings'
        )
        
        # Configure treatment columns with better widths for full screen
        self.treatments_tree.heading('ID', text=translations.get('col_id'))
        self.treatments_tree.heading('Name', text=translations.get('treatment_name'))
        self.treatments_tree.heading('Cost', text=translations.get('col_cost'))
        self.treatments_tree.heading('Date', text=translations.get('col_date'))
        self.treatments_tree.heading('Notes', text=translations.get('col_notes'))
        
        self.treatments_tree.column('ID', width=60, anchor='center')
        self.treatments_tree.column('Name', width=300)
        self.treatments_tree.column('Cost', width=150, anchor='center')
        self.treatments_tree.column('Date', width=150, anchor='center')
        self.treatments_tree.column('Notes', width=400)
        
        # Grid treatment table without scrollbars - full width
        self.treatments_tree.grid(row=0, column=0, sticky="ew")
        
        # Bind treatment events
        self.treatments_tree.bind('<<TreeviewSelect>>', self.on_treatment_select)
        self.treatments_tree.bind('<Double-1>', self.on_treatment_double_click)
        
        self.notebook.add(treatments_frame, text=translations.get('treatments_tab'))
        
    def setup_payments_tab(self):
        # Payments frame with full width
        payments_frame = ttk.Frame(self.notebook)
        payments_frame.columnconfigure(0, weight=1)
        
        # Payments header
        payments_header = ttk.Frame(payments_frame, padding=15)
        payments_header.grid(row=0, column=0, sticky="ew")
        payments_header.columnconfigure(1, weight=1)
        
        payments_title = ttk.Label(
            payments_header, 
            text=f"💰 {translations.get('payments_tab')}", 
            font=('Segoe UI', 14, 'bold')
        )
        payments_title.grid(row=0, column=0, sticky="w")
        
        # Payment buttons
        payment_buttons = ttk.Frame(payments_header)
        payment_buttons.grid(row=0, column=1, sticky="e")
        
        self.add_payment_btn = ttk.Button(
            payment_buttons,
            text=translations.get('add_payment'),
            style='Success.TButton',
            command=self.add_payment
        )
        self.add_payment_btn.pack(side='right', padx=(10, 0), ipadx=15, ipady=8)
        
        self.edit_payment_btn = ttk.Button(
            payment_buttons,
            text=translations.get('edit_payment'),
            style='Warning.TButton',
            command=self.edit_payment,
            state='disabled'
        )
        self.edit_payment_btn.pack(side='right', padx=(10, 0), ipadx=15, ipady=8)
        
        self.delete_payment_btn = ttk.Button(
            payment_buttons,
            text=translations.get('delete_payment'),
            style='Danger.TButton',
            command=self.delete_payment,
            state='disabled'
        )
        self.delete_payment_btn.pack(side='right', ipadx=15, ipady=8)
        
        # Payments table with full width
        payments_table_frame = ttk.Frame(payments_frame, padding=15)
        payments_table_frame.grid(row=1, column=0, sticky="ew")
        payments_table_frame.columnconfigure(0, weight=1)
        
        payment_columns = ('ID', 'Amount', 'Date', 'Notes')
        self.payments_tree = ttk.Treeview(
            payments_table_frame, 
            columns=payment_columns, 
            show='headings'
        )
        
        # Configure payment columns with better widths for full screen
        self.payments_tree.heading('ID', text=translations.get('col_id'))
        self.payments_tree.heading('Amount', text=translations.get('col_amount'))
        self.payments_tree.heading('Date', text=translations.get('col_date'))
        self.payments_tree.heading('Notes', text=translations.get('col_notes'))
        
        self.payments_tree.column('ID', width=60, anchor='center')
        self.payments_tree.column('Amount', width=150, anchor='center')
        self.payments_tree.column('Date', width=150, anchor='center')
        self.payments_tree.column('Notes', width=500)
        
        # Grid payment table without scrollbars - full width
        self.payments_tree.grid(row=0, column=0, sticky="ew")
        
        # Bind payment events
        self.payments_tree.bind('<<TreeviewSelect>>', self.on_payment_select)
        self.payments_tree.bind('<Double-1>', self.on_payment_double_click)
        
        self.notebook.add(payments_frame, text=translations.get('payments_tab'))
        
    def setup_buttons(self, parent):
        # Buttons frame
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill='x', pady=(15, 0))
        
        # Export PDF button
        export_btn = ttk.Button(
            buttons_frame, 
            text=f"📄 {translations.get('export_pdf')}",
            command=self.export_to_pdf,
            style='Warning.TButton'
        )
        export_btn.pack(side='left', ipadx=20, ipady=8)
        
        # Close button
        close_btn = ttk.Button(
            buttons_frame, 
            text=translations.get('btn_close'), 
            command=self.close_window,
            style='TButton'
        )
        close_btn.pack(side='right', ipadx=20, ipady=8)
        
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
            messagebox.showerror(translations.get('error'), f"Failed to load treatments: {str(e)}")
            
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
            messagebox.showerror(translations.get('error'), f"Failed to load payments: {str(e)}")
            
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
            
    def export_to_pdf(self):
        """Export record details to PDF"""
        try:
            # Ask user for save location
            filename = filedialog.asksaveasfilename(
                title=translations.get('save_pdf'),
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                initialfile=f"Record_{self.record.doctor_name}_{self.record.patient_name}_{datetime.now().strftime('%Y%m%d')}.pdf"
            )
            
            if not filename:
                return
                
            # Create PDF
            self.create_pdf(filename)
            
            # Show success message
            messagebox.showinfo(
                translations.get('success'), 
                translations.get('pdf_exported_success', filename=os.path.basename(filename))
            )
            
        except Exception as e:
            messagebox.showerror(
                translations.get('error'), 
                translations.get('pdf_export_error', error=str(e))
            )
            
    def create_pdf(self, filename):
        """Create the PDF document"""
        doc = SimpleDocTemplate(filename, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2c3e50')
        )
        
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.HexColor('#3498db')
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6
        )
        
        # Title
        story.append(Paragraph(translations.get('record_details'), title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Record Information
        story.append(Paragraph(translations.get('record_information'), header_style))
        
        record_info = [
            [translations.get('col_doctor'), self.record.doctor_name],
            [translations.get('col_patient'), self.record.patient_name],
            [translations.get('col_created'), self.record.created_at.strftime("%Y-%m-%d %H:%M") if self.record.created_at else ""],
            [translations.get('record_id'), str(self.record.id)]
        ]
        
        record_table = Table(record_info, colWidths=[2*inch, 4*inch])
        record_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(record_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Account Summary
        story.append(Paragraph(translations.get('account_summary'), header_style))
        
        total_cost = self.record.cost()
        total_paid = self.record.amount()
        balance = self.record.balance()
        
        summary_info = [
            [translations.get('total_cost'), f"${total_cost:.2f}"],
            [translations.get('total_paid'), f"${total_paid:.2f}"],
            [translations.get('balance'), f"${balance:.2f}"]
        ]
        
        summary_table = Table(summary_info, colWidths=[2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        # Color code the balance
        if balance > 0:
            summary_table.setStyle(TableStyle([
                ('TEXTCOLOR', (1, 2), (1, 2), colors.HexColor('#e74c3c'))
            ]))
        elif balance == 0:
            summary_table.setStyle(TableStyle([
                ('TEXTCOLOR', (1, 2), (1, 2), colors.HexColor('#27ae60'))
            ]))
        else:
            summary_table.setStyle(TableStyle([
                ('TEXTCOLOR', (1, 2), (1, 2), colors.HexColor('#f39c12'))
            ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Treatments
        treatments = self.record.treatments()
        if treatments:
            story.append(Paragraph(translations.get('treatments_tab'), header_style))
            
            treatment_data = [[
                translations.get('col_id'),
                translations.get('treatment_name'),
                translations.get('col_cost'),
                translations.get('col_date'),
                translations.get('col_notes')
            ]]
            
            for treatment in treatments:
                treatment_data.append([
                    str(treatment.id),
                    treatment.name or "",
                    f"${treatment.cost:.2f}" if treatment.cost else "$0.00",
                    treatment.date.strftime("%Y-%m-%d") if treatment.date else "",
                    treatment.notes or ""
                ])
            
            treatment_table = Table(treatment_data, colWidths=[0.5*inch, 2*inch, 1*inch, 1*inch, 2.5*inch])
            treatment_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),  # ID column center
                ('ALIGN', (2, 0), (2, -1), 'RIGHT'),   # Cost column right
                ('ALIGN', (3, 0), (3, -1), 'CENTER'),  # Date column center
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
            ]))
            
            story.append(treatment_table)
            story.append(Spacer(1, 0.2*inch))
        
        # Payments
        payments = self.record.payments()
        if payments:
            story.append(Paragraph(translations.get('payments_tab'), header_style))
            
            payment_data = [[
                translations.get('col_id'),
                translations.get('col_amount'),
                translations.get('col_date'),
                translations.get('col_notes')
            ]]
            
            for payment in payments:
                payment_data.append([
                    str(payment.id),
                    f"${payment.amount:.2f}" if payment.amount else "$0.00",
                    payment.date.strftime("%Y-%m-%d") if payment.date else "",
                    payment.notes or ""
                ])
            
            payment_table = Table(payment_data, colWidths=[0.5*inch, 1.5*inch, 1.5*inch, 3.5*inch])
            payment_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),  # ID column center
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),   # Amount column right
                ('ALIGN', (2, 0), (2, -1), 'CENTER'),  # Date column center
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
            ]))
            
            story.append(payment_table)
        
        # Footer
        story.append(Spacer(1, 0.3*inch))
        footer_text = f"{translations.get('generated_on')}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        story.append(Paragraph(footer_text, ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#7f8c8d')
        )))
        
        # Build PDF
        doc.build(story)
        
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
        dialog = TreatmentForm(self.window, title=translations.get('add_new_treatment'), record_id=self.record.id)
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
                messagebox.showinfo(translations.get('success'), translations.get('treatment_added_success'))
            except Exception as e:
                messagebox.showerror(translations.get('error'), f"Failed to add treatment: {str(e)}")
                
    def edit_treatment(self):
        """Edit selected treatment"""
        if not self.selected_treatment:
            return
            
        dialog = TreatmentForm(
            self.window, 
            title=translations.get('edit_treatment_title'), 
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
                messagebox.showinfo(translations.get('success'), translations.get('treatment_updated_success'))
            except Exception as e:
                messagebox.showerror(translations.get('error'), f"Failed to update treatment: {str(e)}")
                
    def delete_treatment(self):
        """Delete selected treatment"""
        if not self.selected_treatment:
            return
            
        result = messagebox.askyesno(
            translations.get('confirm_deletion'),
            translations.get('confirm_delete_treatment', name=self.selected_treatment.name)
        )
        
        if result:
            try:
                Treatment.delete(self.selected_treatment.id)
                self.load_treatments()
                self.update_summary()
                self.selected_treatment = None
                self.edit_treatment_btn.config(state='disabled')
                self.delete_treatment_btn.config(state='disabled')
                messagebox.showinfo(translations.get('success'), translations.get('treatment_deleted_success'))
            except Exception as e:
                messagebox.showerror(translations.get('error'), f"Failed to delete treatment: {str(e)}")
                
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
        dialog = PaymentForm(self.window, title=translations.get('add_new_payment'), record_id=self.record.id)
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
                messagebox.showinfo(translations.get('success'), translations.get('payment_added_success'))
            except Exception as e:
                messagebox.showerror(translations.get('error'), f"Failed to add payment: {str(e)}")
                
    def edit_payment(self):
        """Edit selected payment"""
        if not self.selected_payment:
            return
            
        dialog = PaymentForm(
            self.window, 
            title=translations.get('edit_payment_title'), 
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
                messagebox.showinfo(translations.get('success'), translations.get('payment_updated_success'))
            except Exception as e:
                messagebox.showerror(translations.get('error'), f"Failed to update payment: {str(e)}")
                
    def delete_payment(self):
        """Delete selected payment"""
        if not self.selected_payment:
            return
            
        result = messagebox.askyesno(
            translations.get('confirm_deletion'),
            translations.get('confirm_delete_payment', amount=self.selected_payment.amount)
        )
        
        if result:
            try:
                Payment.delete(self.selected_payment.id)
                self.load_payments()
                self.update_summary()
                self.selected_payment = None
                self.edit_payment_btn.config(state='disabled')
                self.delete_payment_btn.config(state='disabled')
                messagebox.showinfo(translations.get('success'), translations.get('payment_deleted_success'))
            except Exception as e:
                messagebox.showerror(translations.get('error'), f"Failed to delete payment: {str(e)}")
                
    def close_window(self):
        """Close the details window"""
        self.window.destroy()