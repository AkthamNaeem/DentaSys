import sqlite3
from database.connection import get_db_connection
from models.helper import handle_date_time, handle_date


class Patient:
    def __init__(self, patient_id=None, name=None, phone=None, gender=None,
                 birth_date=None, notes=None, created_at=None, deleted_at=None):
        self.id = patient_id
        self.name = name
        self.phone = phone
        self.gender = gender
        self.birth_date = handle_date(birth_date)
        self.notes = notes
        self.created_at = handle_date_time(created_at)
        self.deleted_at = handle_date_time(deleted_at)

    @classmethod
    def create(cls, name, phone, gender=None, birth_date=None, notes=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            birth_date = handle_date(birth_date)
            cursor.execute(
                """INSERT INTO patients 
                (name, phone, gender, birth_date, notes) 
                VALUES (?, ?, ?, ?, ?)""",
                (name, phone, gender, birth_date, notes)
            )
            conn.commit()
            return cls.get_by_id(cursor.lastrowid)
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Patient with this name or phone already exists: {e}")
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, patient_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
        patient_data = cursor.fetchone()
        conn.close()
        if patient_data:
            return cls(**patient_data)
        return None

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM patients
            WHERE deleted_at IS NULL
            ORDER BY name
            """)
        patients = [cls(**row) for row in cursor.fetchall()]
        conn.close()
        return patients

    @classmethod
    def update(cls, patient_id, name=None, phone=None, gender=None,
               birth_date=None, notes=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        updates = []
        params = []

        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if phone is not None:
            updates.append("phone = ?")
            params.append(phone)
        if gender is not None:
            updates.append("gender = ?")
            params.append(gender)

        if birth_date is not None:
            birth_date = handle_date(birth_date)
            updates.append("birth_date = ?")
            params.append(birth_date)

        if notes is not None:
            updates.append("notes = ?")
            params.append(notes)

        if not updates:
            return cls.get_by_id(patient_id)

        params.append(patient_id)
        query = f"UPDATE patients SET {', '.join(updates)} WHERE id = ?"

        try:
            cursor.execute(query, params)
            conn.commit()
            return cls.get_by_id(patient_id)
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Update would violate uniqueness constraint: {e}")
        finally:
            conn.close()

    @classmethod
    def patient_has_records(cls, patient_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 1 FROM records
            WHERE patient_id = ?
            LIMIT 1
        """, (patient_id,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    @classmethod
    def delete(cls, patient_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            if cls.patient_has_records(patient_id):
                # Soft delete
                cls.soft_delete(patient_id)
            else:
                # Hard delete
                cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))

            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @classmethod
    def soft_delete(cls, patient_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE patients
                SET deleted_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (patient_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @classmethod
    def search(cls, search_term):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM patients WHERE name LIKE ? OR phone LIKE ?",
                (f"%{search_term}%", f"%{search_term}%")
            )
            return [cls(**row) for row in cursor.fetchall()]
        finally:
            conn.close()

    @classmethod
    def records(cls, patient_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM records WHERE patient_id = ?",
                (patient_id,)
            )
            return [cls(**row) for row in cursor.fetchall()]
        finally:
            conn.close()

    @classmethod
    def treatments(cls, patient_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT r.*, t.id AS treatment_id, t.name AS treatment_name, 
                       t.cost, t.date AS treatment_date, t.notes AS treatment_notes
                FROM records r
                JOIN treatments t ON r.id = t.record_id
                WHERE r.patient_id = ?
                """,
                (patient_id,)
            )
            results = []
            for row in cursor.fetchall():
                record_data = {k: v for k, v in row.items() if not k.startswith('treatment_')}
                treatment_data = {
                    'id': row['treatment_id'],
                    'name': row['treatment_name'],
                    'cost': row['cost'],
                    'date': row['treatment_date'],
                    'notes': row['treatment_notes'],
                    'record_id': row['id']
                }
                results.append({
                    'record': cls(**record_data),
                    'treatment': treatment_data
                })
            return results
        finally:
            conn.close()

    @classmethod
    def payments(cls, patient_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT r.*, p.id AS payment_id, p.amount, 
                       p.date AS payment_date, p.notes AS payment_notes
                FROM records r
                JOIN payments p ON r.id = p.record_id
                WHERE r.patient_id = ?
                """,
                (patient_id,)
            )
            results = []
            for row in cursor.fetchall():
                record_data = {k: v for k, v in row.items() if not k.startswith('payment_')}
                payment_data = {
                    'id': row['payment_id'],
                    'amount': row['amount'],
                    'date': row['payment_date'],
                    'notes': row['payment_notes'],
                    'record_id': row['id']
                }
                results.append({
                    'record': cls(**record_data),
                    'payment': payment_data
                })
            return results
        finally:
            conn.close()
