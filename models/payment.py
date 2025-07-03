import sqlite3
from database.connection import get_db_connection
from models.helper import handle_date


class Payment:
    def __init__(self, payment_id=None, record_id=None, amount=None, payment_date=None, notes=None):
        self.id = payment_id
        self.record_id = record_id
        self.amount = amount
        self.payment_date = handle_date(payment_date)
        self.notes = notes

    @classmethod
    def create(cls, record_id, amount, payment_date=None, notes=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            payment_date = handle_date(payment_date)
            cursor.execute(
                """INSERT INTO payments 
                (record_id, amount, date, notes) 
                VALUES (?, ?, ?, ?, ?)""",
                (record_id, amount, payment_date, notes)
            )
            conn.commit()
            return cls.get_by_id(cursor.lastrowid)
        except sqlite3.IntegrityError as e:
            if "FOREIGN KEY" in str(e):
                raise ValueError("Invalid record_id")
            raise
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, payment_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM payments WHERE id = ?", (payment_id,))
        payment_data = cursor.fetchone()
        conn.close()
        if payment_data:
            return cls(**payment_data)
        return None

    @classmethod
    def get_by_record(cls, record_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM payments 
            WHERE record_id = ?
            ORDER BY payment_date DESC
        """, (record_id,))
        payments = [cls(**row) for row in cursor.fetchall()]
        conn.close()
        return payments

    @classmethod
    def update(cls, payment_id, amount=None, payment_date=None, notes=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        updates = []
        params = []

        if amount is not None:
            updates.append("amount = ?")
            params.append(amount)
        if payment_date is not None:
            updates.append("date = ?")
            params.append(payment_date)
        if notes is not None:
            updates.append("notes = ?")
            params.append(notes)

        if not updates:
            return cls.get_by_id(payment_id)

        params.append(payment_id)
        query = f"UPDATE payments SET {', '.join(updates)} WHERE id = ?"

        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return cls.get_by_id(payment_id)

    @classmethod
    def delete(cls, payment_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM payments WHERE id = ?", (payment_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
