import sqlite3
from database.connection import get_db_connection
from models.helper import handle_date_time


class Doctor:
    def __init__(self, doctor_id=None, name=None, phone=None, created_at=None, deleted_at=None):
        self.id = doctor_id
        self.name = name
        self.phone = phone
        self.created_at = handle_date_time(created_at)
        self.deleted_at = handle_date_time(deleted_at)

    @classmethod
    def create(cls, name, phone=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO doctors (name, phone) VALUES (?, ?)",
                (name, phone)
            )
            conn.commit()
            return cls.get_by_id(cursor.lastrowid)
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Doctor with this name or phone already exists: {e}")
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, doctor_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
        doctor_data = cursor.fetchone()
        conn.close()
        if doctor_data:
            return cls(**doctor_data)
        return None

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM doctors
            WHERE deleted_at IS NULL
            ORDER BY name
        """)
        doctors = [cls(**row) for row in cursor.fetchall()]
        conn.close()
        return doctors

    @classmethod
    def update(cls, doctor_id, name=None, phone=None):
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

        if not updates:
            return cls.get_by_id(doctor_id)

        params.append(doctor_id)
        query = f"UPDATE doctors SET {', '.join(updates)} WHERE id = ?"

        try:
            cursor.execute(query, params)
            conn.commit()
            return cls.get_by_id(doctor_id)
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Update would violate uniqueness constraint: {e}")
        finally:
            conn.close()

    @classmethod
    def doctor_has_records(cls, doctor_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 1 FROM records
            WHERE doctor_id = ?
            LIMIT 1
        """, (doctor_id,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    @classmethod
    def delete(cls, doctor_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            if cls.doctor_has_records(doctor_id):
                # Soft delete
                cls.soft_delete(doctor_id)
            else:
                # Hard delete
                cursor.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))

            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @classmethod
    def soft_delete(cls, doctor_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE doctors
                SET deleted_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (doctor_id,))
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
                "SELECT * FROM doctors WHERE name LIKE ? OR phone LIKE ?",
                (f"%{search_term}%", f"%{search_term}%")
            )
            return [cls(**row) for row in cursor.fetchall()]
        finally:
            conn.close()

    @classmethod
    def records(cls, doctor_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM records WHERE doctor_id = ?",
                (doctor_id,)
            )
            return [cls(**row) for row in cursor.fetchall()]
        finally:
            conn.close()

    @classmethod
    def treatments(cls, doctor_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT r.*, t.id AS treatment_id, t.name AS treatment_name, 
                       t.cost, t.date AS treatment_date, t.notes AS treatment_notes
                FROM records r
                JOIN treatments t ON r.id = t.record_id
                WHERE r.doctor_id = ?
                """,
                (doctor_id,)
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
    def payments(cls, doctor_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT r.*, p.id AS payment_id, p.amount, 
                       p.date AS payment_date, p.notes AS payment_notes
                FROM records r
                JOIN payments p ON r.id = p.record_id
                WHERE r.doctor_id = ?
                """,
                (doctor_id,)
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
