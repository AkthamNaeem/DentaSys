"""
Translation system for DentaSys
Supports English and Arabic languages
"""

class Translations:
    def __init__(self):
        self.current_language = 'en'  # Default to English
        self.observers = []  # List of callbacks to notify when language changes
        
        # Translation dictionaries
        self.translations = {
            'en': {
                # Main Application
                'app_title': 'DentaSys - Dental Treatment Center Management',
                'app_subtitle': 'Dental Treatment Center Management System',
                
                # Navigation Tabs
                'tab_home': '🏠 Home',
                'tab_doctors': '👨‍⚕️ Doctors',
                'tab_patients': '👤 Patients',
                'tab_records': '📋 Records',
                
                # Language Switch
                'language_switch': '🌐 Language',
                'switch_to_arabic': 'العربية',
                'switch_to_english': 'English',
                
                # Home Page
                'welcome_title': 'Welcome to DentaSys',
                'welcome_description': 'Manage your dental practice efficiently with our comprehensive management system.',
                'search_title': '🔍 Search',
                'search_placeholder': 'Search doctors, patients, or records...',
                'search_instruction': 'Type to search across doctors, patients, and records...',
                'dashboard_title': '📊 Dashboard',
                'search_results': '🔍 Search Results for',
                'showing_all': 'Showing all records...',
                'searching_for': 'Searching for',
                'found_results': 'Found {total} results: {doctors} doctors, {patients} patients, {records} records',
                'search_error': 'Search error: {error}',
                
                # Stats Cards
                'stat_doctors': 'Doctors',
                'stat_patients': 'Patients',
                'stat_records': 'Records',
                
                # Doctors Page
                'doctors_management': '👨‍⚕️ Doctors Management',
                'add_doctor': '➕ Add Doctor',
                'edit_doctor': '✏️ Edit Doctor',
                'delete_doctor': '🗑️ Delete Doctor',
                'search_doctors': '🔍 Search Doctors:',
                
                # Patients Page
                'patients_management': '👤 Patients Management',
                'add_patient': '➕ Add Patient',
                'edit_patient': '✏️ Edit Patient',
                'delete_patient': '🗑️ Delete Patient',
                'search_patients': '🔍 Search Patients:',
                
                # Records Page
                'records_management': '📋 Records Management',
                'add_record': '➕ Add Record',
                'view_details': '👁️ View Details',
                'delete_record': '🗑️ Delete Record',
                'search_records': '🔍 Search Records:',
                
                # Table Headers
                'col_id': 'ID',
                'col_name': 'Name',
                'col_phone': 'Phone',
                'col_gender': 'Gender',
                'col_age': 'Age',
                'col_birth_date': 'Birth Date',
                'col_created': 'Created',
                'col_status': 'Status',
                'col_doctor': 'Doctor',
                'col_patient': 'Patient',
                'col_total_cost': 'Total Cost',
                'col_total_paid': 'Total Paid',
                'col_balance': 'Balance',
                'col_treatment_name': 'Treatment Name',
                'col_cost': 'Cost',
                'col_date': 'Date',
                'col_notes': 'Notes',
                'col_amount': 'Amount',
                
                # Status Values
                'status_active': 'Active',
                'status_deleted': 'Deleted',
                
                # Gender Values
                'gender_male': 'Male',
                'gender_female': 'Female',
                
                # Common Buttons
                'btn_save': 'Save',
                'btn_update': 'Update',
                'btn_cancel': 'Cancel',
                'btn_close': 'Close',
                'btn_add': 'Add',
                'btn_edit': 'Edit',
                'btn_delete': 'Delete',
                
                # Form Labels
                'doctor_name': 'Doctor Name',
                'patient_name': 'Patient Name',
                'phone_number': 'Phone Number',
                'treatment_name': 'Treatment Name',
                'payment_amount': 'Payment Amount',
                'treatment_date': 'Treatment Date',
                'payment_date': 'Payment Date',
                'required_fields': '* Required fields',
                'optional_field': '(Optional)',
                'birth_date': 'Birth Date',
                'notes': 'Notes',
                'gender': 'Gender',
                'cost': 'Cost',
                'amount': 'Amount',
                'date': 'Date',
                
                # Messages
                'success': 'Success',
                'error': 'Error',
                'validation_error': 'Validation Error',
                'confirm_deletion': 'Confirm Deletion',
                'cannot_delete': 'Cannot Delete',
                'doctor_added_success': 'Doctor added successfully!',
                'doctor_updated_success': 'Doctor updated successfully!',
                'doctor_deleted_success': 'Doctor deleted successfully!',
                'patient_added_success': 'Patient added successfully!',
                'patient_updated_success': 'Patient updated successfully!',
                'patient_deleted_success': 'Patient deleted successfully!',
                'record_added_success': 'Record added successfully!',
                'record_deleted_success': 'Record deleted successfully!',
                'treatment_added_success': 'Treatment added successfully!',
                'treatment_updated_success': 'Treatment updated successfully!',
                'treatment_deleted_success': 'Treatment deleted successfully!',
                'payment_added_success': 'Payment added successfully!',
                'payment_updated_success': 'Payment updated successfully!',
                'payment_deleted_success': 'Payment deleted successfully!',
                
                # Record Details
                'record_details': '📋 Record Details',
                'record_information': 'Record Information',
                'record_id': 'Record ID',
                'treatments_tab': '🦷 Treatments',
                'payments_tab': '💰 Payments',
                'add_treatment': '➕ Add Treatment',
                'edit_treatment': '✏️ Edit Treatment',
                'delete_treatment': '🗑️ Delete Treatment',
                'add_payment': '➕ Add Payment',
                'edit_payment': '✏️ Edit Payment',
                'delete_payment': '🗑️ Delete Payment',
                'account_summary': '📊 Account Summary',
                'total_cost': 'Total Cost',
                'total_paid': 'Total Paid',
                'balance': 'Balance',
                'unknown': 'Unknown',
                
                # PDF Export
                'export_pdf': 'Export PDF',
                'save_pdf': 'Save PDF Report',
                'pdf_exported_success': 'PDF report "{filename}" exported successfully!',
                'pdf_export_error': 'Failed to export PDF: {error}',
                'generated_on': 'Generated on',
                
                # Form Titles
                'add_new_doctor': 'Add New Doctor',
                'edit_doctor_title': 'Edit Doctor',
                'add_new_patient': 'Add New Patient',
                'edit_patient_title': 'Edit Patient',
                'add_new_record': 'Add New Record',
                'edit_record_title': 'Edit Record',
                'add_new_treatment': 'Add New Treatment',
                'edit_treatment_title': 'Edit Treatment',
                'add_new_payment': 'Add New Payment',
                'edit_payment_title': 'Edit Payment',
                
                # Form Field Labels
                'doctor_name_required': 'Doctor Name *',
                'patient_name_required': 'Patient Name *',
                'phone_number_required': 'Phone Number *',
                'treatment_name_required': 'Treatment Name *',
                'cost_required': 'Cost *',
                'payment_amount_required': 'Payment Amount *',
                'doctor_required': 'Doctor *',
                'patient_required': 'Patient *',
                
                # Validation Messages
                'doctor_name_required_msg': 'Doctor name is required',
                'patient_name_required_msg': 'Patient name is required',
                'phone_required_msg': 'Phone number is required',
                'treatment_name_required_msg': 'Treatment name is required',
                'cost_required_msg': 'Cost is required',
                'amount_required_msg': 'Payment amount is required',
                'select_doctor_msg': 'Please select a doctor',
                'select_patient_msg': 'Please select a patient',
                
                # Confirmation Messages
                'confirm_delete_doctor': 'Are you sure you want to delete Dr. {name}?\n\nNote: If this doctor has records, they will be soft-deleted (marked as deleted but kept for data integrity).',
                'confirm_delete_patient': 'Are you sure you want to delete {name}?\n\nNote: If this patient has records, they will be soft-deleted (marked as deleted but kept for data integrity).',
                'confirm_delete_record': 'Are you sure you want to delete this record?\n\nDoctor: {doctor}\nPatient: {patient}\n\nThis action cannot be undone.',
                'confirm_delete_treatment': 'Are you sure you want to delete the treatment \'{name}\'?\n\nThis action cannot be undone.',
                'confirm_delete_payment': 'Are you sure you want to delete this payment of ${amount:.2f}?\n\nThis action cannot be undone.',
                
                # Error Messages
                'cannot_delete_record': 'This record cannot be deleted because it has associated treatments or payments.\n\nPlease remove all treatments and payments first.',
                'failed_to_load': 'Failed to load {item}: {error}',
                'failed_to_add': 'Failed to add {item}: {error}',
                'failed_to_update': 'Failed to update {item}: {error}',
                'failed_to_delete': 'Failed to delete {item}: {error}',
                
                # Info Messages
                'no_doctors_patients': 'No doctors or patients found. Please add doctors and patients first.',
                'no_doctors': 'No doctors found. Please add doctors first.',
                'no_patients': 'No patients found. Please add patients first.',
                
                # Format Hints
                'date_format_hint': 'Format: YYYY-MM-DD (e.g., 2024-01-15)',
                'birth_date_format_hint': 'Format: YYYY-MM-DD (e.g., 1990-01-15)',
            },
            
            'ar': {
                # Main Application
                'app_title': 'دينتاسيس - نظام إدارة مركز العلاج السني',
                'app_subtitle': 'نظام إدارة مركز العلاج السني',
                
                # Navigation Tabs
                'tab_home': '🏠 الرئيسية',
                'tab_doctors': '👨‍⚕️ الأطباء',
                'tab_patients': '👤 المرضى',
                'tab_records': '📋 السجلات',
                
                # Language Switch
                'language_switch': '🌐 اللغة',
                'switch_to_arabic': 'العربية',
                'switch_to_english': 'English',
                
                # Home Page
                'welcome_title': 'مرحباً بك في دينتاسيس',
                'welcome_description': 'إدارة عيادتك السنية بكفاءة مع نظام الإدارة الشامل الخاص بنا.',
                'search_title': '🔍 البحث',
                'search_placeholder': 'البحث في الأطباء والمرضى والسجلات...',
                'search_instruction': 'اكتب للبحث في الأطباء والمرضى والسجلات...',
                'dashboard_title': '📊 لوحة التحكم',
                'search_results': '🔍 نتائج البحث عن',
                'showing_all': 'عرض جميع السجلات...',
                'searching_for': 'البحث عن',
                'found_results': 'تم العثور على {total} نتيجة: {doctors} أطباء، {patients} مرضى، {records} سجلات',
                'search_error': 'خطأ في البحث: {error}',
                
                # Stats Cards
                'stat_doctors': 'الأطباء',
                'stat_patients': 'المرضى',
                'stat_records': 'السجلات',
                
                # Doctors Page
                'doctors_management': '👨‍⚕️ إدارة الأطباء',
                'add_doctor': '➕ إضافة طبيب',
                'edit_doctor': '✏️ تعديل طبيب',
                'delete_doctor': '🗑️ حذف طبيب',
                'search_doctors': '🔍 البحث في الأطباء:',
                
                # Patients Page
                'patients_management': '👤 إدارة المرضى',
                'add_patient': '➕ إضافة مريض',
                'edit_patient': '✏️ تعديل مريض',
                'delete_patient': '🗑️ حذف مريض',
                'search_patients': '🔍 البحث في المرضى:',
                
                # Records Page
                'records_management': '📋 إدارة السجلات',
                'add_record': '➕ إضافة سجل',
                'view_details': '👁️ عرض التفاصيل',
                'delete_record': '🗑️ حذف سجل',
                'search_records': '🔍 البحث في السجلات:',
                
                # Table Headers
                'col_id': 'المعرف',
                'col_name': 'الاسم',
                'col_phone': 'الهاتف',
                'col_gender': 'الجنس',
                'col_age': 'العمر',
                'col_birth_date': 'تاريخ الميلاد',
                'col_created': 'تاريخ الإنشاء',
                'col_status': 'الحالة',
                'col_doctor': 'الطبيب',
                'col_patient': 'المريض',
                'col_total_cost': 'التكلفة الإجمالية',
                'col_total_paid': 'المبلغ المدفوع',
                'col_balance': 'الرصيد',
                'col_treatment_name': 'اسم العلاج',
                'col_cost': 'التكلفة',
                'col_date': 'التاريخ',
                'col_notes': 'الملاحظات',
                'col_amount': 'المبلغ',
                
                # Status Values
                'status_active': 'نشط',
                'status_deleted': 'محذوف',
                
                # Gender Values
                'gender_male': 'ذكر',
                'gender_female': 'أنثى',
                
                # Common Buttons
                'btn_save': 'حفظ',
                'btn_update': 'تحديث',
                'btn_cancel': 'إلغاء',
                'btn_close': 'إغلاق',
                'btn_add': 'إضافة',
                'btn_edit': 'تعديل',
                'btn_delete': 'حذف',
                
                # Form Labels
                'doctor_name': 'اسم الطبيب',
                'patient_name': 'اسم المريض',
                'phone_number': 'رقم الهاتف',
                'treatment_name': 'اسم العلاج',
                'payment_amount': 'مبلغ الدفع',
                'treatment_date': 'تاريخ العلاج',
                'payment_date': 'تاريخ الدفع',
                'required_fields': '* الحقول المطلوبة',
                'optional_field': '(اختياري)',
                'birth_date': 'تاريخ الميلاد',
                'notes': 'الملاحظات',
                'gender': 'الجنس',
                'cost': 'التكلفة',
                'amount': 'المبلغ',
                'date': 'التاريخ',
                
                # Messages
                'success': 'نجح',
                'error': 'خطأ',
                'validation_error': 'خطأ في التحقق',
                'confirm_deletion': 'تأكيد الحذف',
                'cannot_delete': 'لا يمكن الحذف',
                'doctor_added_success': 'تم إضافة الطبيب بنجاح!',
                'doctor_updated_success': 'تم تحديث الطبيب بنجاح!',
                'doctor_deleted_success': 'تم حذف الطبيب بنجاح!',
                'patient_added_success': 'تم إضافة المريض بنجاح!',
                'patient_updated_success': 'تم تحديث المريض بنجاح!',
                'patient_deleted_success': 'تم حذف المريض بنجاح!',
                'record_added_success': 'تم إضافة السجل بنجاح!',
                'record_deleted_success': 'تم حذف السجل بنجاح!',
                'treatment_added_success': 'تم إضافة العلاج بنجاح!',
                'treatment_updated_success': 'تم تحديث العلاج بنجاح!',
                'treatment_deleted_success': 'تم حذف العلاج بنجاح!',
                'payment_added_success': 'تم إضافة الدفعة بنجاح!',
                'payment_updated_success': 'تم تحديث الدفعة بنجاح!',
                'payment_deleted_success': 'تم حذف الدفعة بنجاح!',
                
                # Record Details
                'record_details': '📋 تفاصيل السجل',
                'record_information': 'معلومات السجل',
                'record_id': 'رقم السجل',
                'treatments_tab': '🦷 العلاجات',
                'payments_tab': '💰 المدفوعات',
                'add_treatment': '➕ إضافة علاج',
                'edit_treatment': '✏️ تعديل علاج',
                'delete_treatment': '🗑️ حذف علاج',
                'add_payment': '➕ إضافة دفعة',
                'edit_payment': '✏️ تعديل دفعة',
                'delete_payment': '🗑️ حذف دفعة',
                'account_summary': '📊 ملخص الحساب',
                'total_cost': 'التكلفة الإجمالية',
                'total_paid': 'المبلغ المدفوع',
                'balance': 'الرصيد',
                'unknown': 'غير معروف',
                
                # PDF Export
                'export_pdf': 'تصدير PDF',
                'save_pdf': 'حفظ تقرير PDF',
                'pdf_exported_success': 'تم تصدير تقرير PDF "{filename}" بنجاح!',
                'pdf_export_error': 'فشل في تصدير PDF: {error}',
                'generated_on': 'تم الإنشاء في',
                
                # Form Titles
                'add_new_doctor': 'إضافة طبيب جديد',
                'edit_doctor_title': 'تعديل طبيب',
                'add_new_patient': 'إضافة مريض جديد',
                'edit_patient_title': 'تعديل مريض',
                'add_new_record': 'إضافة سجل جديد',
                'edit_record_title': 'تعديل سجل',
                'add_new_treatment': 'إضافة علاج جديد',
                'edit_treatment_title': 'تعديل علاج',
                'add_new_payment': 'إضافة دفعة جديدة',
                'edit_payment_title': 'تعديل دفعة',
                
                # Form Field Labels
                'doctor_name_required': 'اسم الطبيب *',
                'patient_name_required': 'اسم المريض *',
                'phone_number_required': 'رقم الهاتف *',
                'treatment_name_required': 'اسم العلاج *',
                'cost_required': 'التكلفة *',
                'payment_amount_required': 'مبلغ الدفع *',
                'doctor_required': 'الطبيب *',
                'patient_required': 'المريض *',
                
                # Validation Messages
                'doctor_name_required_msg': 'اسم الطبيب مطلوب',
                'patient_name_required_msg': 'اسم المريض مطلوب',
                'phone_required_msg': 'رقم الهاتف مطلوب',
                'treatment_name_required_msg': 'اسم العلاج مطلوب',
                'cost_required_msg': 'التكلفة مطلوبة',
                'amount_required_msg': 'مبلغ الدفع مطلوب',
                'select_doctor_msg': 'يرجى اختيار طبيب',
                'select_patient_msg': 'يرجى اختيار مريض',
                
                # Confirmation Messages
                'confirm_delete_doctor': 'هل أنت متأكد من حذف الدكتور {name}؟\n\nملاحظة: إذا كان لدى هذا الطبيب سجلات، فسيتم حذفها بشكل مؤقت (تُعلم كمحذوفة ولكن تُحفظ للحفاظ على سلامة البيانات).',
                'confirm_delete_patient': 'هل أنت متأكد من حذف {name}؟\n\nملاحظة: إذا كان لدى هذا المريض سجلات، فسيتم حذفها بشكل مؤقت (تُعلم كمحذوفة ولكن تُحفظ للحفاظ على سلامة البيانات).',
                'confirm_delete_record': 'هل أنت متأكد من حذف هذا السجل؟\n\nالطبيب: {doctor}\nالمريض: {patient}\n\nلا يمكن التراجع عن هذا الإجراء.',
                'confirm_delete_treatment': 'هل أنت متأكد من حذف العلاج \'{name}\'؟\n\nلا يمكن التراجع عن هذا الإجراء.',
                'confirm_delete_payment': 'هل أنت متأكد من حذف هذه الدفعة بقيمة ${amount:.2f}؟\n\nلا يمكن التراجع عن هذا الإجراء.',
                
                # Error Messages
                'cannot_delete_record': 'لا يمكن حذف هذا السجل لأنه يحتوي على علاجات أو مدفوعات مرتبطة.\n\nيرجى إزالة جميع العلاجات والمدفوعات أولاً.',
                'failed_to_load': 'فشل في تحميل {item}: {error}',
                'failed_to_add': 'فشل في إضافة {item}: {error}',
                'failed_to_update': 'فشل في تحديث {item}: {error}',
                'failed_to_delete': 'فشل في حذف {item}: {error}',
                
                # Info Messages
                'no_doctors_patients': 'لم يتم العثور على أطباء أو مرضى. يرجى إضافة الأطباء والمرضى أولاً.',
                'no_doctors': 'لم يتم العثور على أطباء. يرجى إضافة الأطباء أولاً.',
                'no_patients': 'لم يتم العثور على مرضى. يرجى إضافة المرضى أولاً.',
                
                # Format Hints
                'date_format_hint': 'التنسيق: سنة-شهر-يوم (مثال: 2024-01-15)',
                'birth_date_format_hint': 'التنسيق: سنة-شهر-يوم (مثال: 1990-01-15)',
            }
        }
    
    def get(self, key, **kwargs):
        """Get translated text for the current language"""
        text = self.translations.get(self.current_language, {}).get(key, key)
        
        # Handle string formatting
        if kwargs:
            try:
                text = text.format(**kwargs)
            except (KeyError, ValueError):
                pass
                
        return text
    
    def set_language(self, language_code):
        """Set the current language and notify observers"""
        if language_code in self.translations:
            self.current_language = language_code
            self.notify_observers()
    
    def get_current_language(self):
        """Get the current language code"""
        return self.current_language
    
    def add_observer(self, callback):
        """Add a callback to be notified when language changes"""
        if callback not in self.observers:
            self.observers.append(callback)
    
    def remove_observer(self, callback):
        """Remove a callback from observers"""
        if callback in self.observers:
            self.observers.remove(callback)
    
    def notify_observers(self):
        """Notify all observers that language has changed"""
        for callback in self.observers:
            try:
                callback()
            except Exception as e:
                print(f"Error notifying observer: {e}")

# Global translation instance
translations = Translations()