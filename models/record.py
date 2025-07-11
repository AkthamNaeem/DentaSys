import sqlite3
from database.connection import get_db_connection
from models.doctor import Doctor
from models.patient import Patient
from models.helper import handle_date_time


class Record:
    def __init__(self, id=None, doctor_id=None, patient_id=None, created_at=None,
                 doctor_name=None, patient_name=None):
        self.id = id
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.created_at = created_at
        self.doctor_name = doctor_name
        self.patient_name = patient_name
        self.created_at = handle_date_time(created_at)

    @property
    def doctor(self):
        return Doctor.get_by_id(self.doctor_id) if self.doctor_id else None

    @property
    def patient(self):
        return Patient.get_by_id(self.patient_id) if self.patient_id else None

    @classmethod
    def create(cls, doctor_id, patient_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO records (doctor_id, patient_id) VALUES (?, ?)",
                (doctor_id, patient_id)
            )
            conn.commit()
            return cls.get_by_id(cursor.lastrowid)
        except sqlite3.IntegrityError as e:
            if "FOREIGN KEY" in str(e):
                raise ValueError("Invalid doctor_id or patient_id")
            elif "UNIQUE" in str(e):
                raise ValueError("This doctor-patient record already exists")
            raise
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, record_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.*, d.name as doctor_name, p.name as patient_name 
            FROM records r
            JOIN doctors d ON r.doctor_id = d.id
            JOIN patients p ON r.patient_id = p.id
            WHERE r.id = ?
            """, (record_id,))
        record_data = cursor.fetchone()
        conn.close()
        if record_data:
            return cls(**record_data)
        return None

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.*, d.name as doctor_name, p.name as patient_name 
            FROM records r
            JOIN doctors d ON r.doctor_id = d.id
            JOIN patients p ON r.patient_id = p.id
            ORDER BY r.created_at DESC
        """)
        records = []
        for row in cursor.fetchall():
            record = cls(**{k: row[k] for k in row.keys()
                            if k in ['id', 'doctor_id', 'patient_id', 'created_at']})
            record.doctor_name = row['doctor_name']
            record.patient_name = row['patient_name']
            # Calculate financial data
            record._total_amount = record.get_total_amount()
            record._total_cost = record.get_total_cost()
            record._balance = record.get_balance()
            records.append(record)
        conn.close()
        return records

    @classmethod
    def get_by_doctor(cls, doctor_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.*, p.name as patient_name 
            FROM records r
            JOIN patients p ON r.patient_id = p.id
            WHERE r.doctor_id = ?
            ORDER BY r.created_at DESC
        """, (doctor_id,))

        records = []
        for row in cursor.fetchall():
            record_data = {
                'id': row['id'],
                'doctor_id': row['doctor_id'],
                'patient_id': row['patient_id'],
                'created_at': row['created_at'],
                'patient_name': row['patient_name']
            }
            records.append(cls(**record_data))
        conn.close()
        return records

    @classmethod
    def get_by_patient(cls, patient_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.*, d.name as doctor_name 
            FROM records r
            JOIN doctors d ON r.doctor_id = d.id
            WHERE r.patient_id = ?
            ORDER BY r.created_at DESC
        """, (patient_id,))

        records = []
        for row in cursor.fetchall():
            record_data = {
                'id': row['id'],
                'doctor_id': row['doctor_id'],
                'patient_id': row['patient_id'],
                'created_at': row['created_at'],
                'doctor_name': row['doctor_name']
            }
            records.append(cls(**record_data))
        conn.close()
        return records

    @classmethod
    def record_has_payments(cls, record_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 1 FROM payments
            WHERE record_id = ?
            LIMIT 1
        """, (record_id,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    @classmethod
    def record_has_treatments(cls, record_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 1 FROM treatments
            WHERE record_id = ?
            LIMIT 1
        """, (record_id,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    @classmethod
    def delete(cls, record_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            if cls.record_has_payments(record_id) or cls.record_has_treatments(record_id):
                return False
            else:
                cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def treatments(self):
        from models.treatment import Treatment
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM treatments 
            WHERE record_id = ?
            ORDER BY date DESC
        """, (self.id,))
        treatments = [Treatment(**row) for row in cursor.fetchall()]
        conn.close()
        return treatments

    def payments(self):
        from models.payment import Payment
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM payments 
            WHERE record_id = ?
            ORDER BY date DESC
        """, (self.id,))
        payments = [Payment(**row) for row in cursor.fetchall()]
        conn.close()
        return payments

    def get_total_amount(self):
        """Get total amount paid for this record"""
        payments = self.payments()
        return sum(p.amount for p in payments if p.amount)

    def get_total_cost(self):
        """Get total cost of treatments for this record"""
        treatments = self.treatments()
        return sum(t.cost for t in treatments if t.cost)

    def get_balance(self):
        """Get balance (cost - amount paid)"""
        return self.get_total_cost() - self.get_total_amount()

    # Keep the old method names for backward compatibility
    def amount(self):
        return self.get_total_amount()

    def cost(self):
        return self.get_total_cost()

    def balance(self):
        return self.get_balance()