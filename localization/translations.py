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
                
                # Messages
                'success': 'Success',
                'error': 'Error',
                'validation_error': 'Validation Error',
                'confirm_deletion': 'Confirm Deletion',
                'cannot_delete': 'Cannot Delete',
                
                # Record Details
                'record_details': '📋 Record Details',
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
                
                # Messages
                'success': 'نجح',
                'error': 'خطأ',
                'validation_error': 'خطأ في التحقق',
                'confirm_deletion': 'تأكيد الحذف',
                'cannot_delete': 'لا يمكن الحذف',
                
                # Record Details
                'record_details': '📋 تفاصيل السجل',
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