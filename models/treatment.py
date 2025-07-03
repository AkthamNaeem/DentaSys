import sqlite3
from database.connection import get_db_connection
from models.helper import handle_date


class Treatment:
    def __init__(self, treatment_id=None, record_id=None, name=None, cost=None, treatment_date=None, notes=None):
        self.id = treatment_id
        self.record_id = record_id
        self.name = name
        self.cost = cost
        self.date = handle_date(treatment_date)
        self.notes = notes

    @classmethod
    def create(cls, record_id, name, cost, treatment_date=None, notes=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            treatment_date = handle_date(treatment_date)
            cursor.execute(
                """INSERT INTO treatments 
                (record_id, name, cost, date, notes) 
                VALUES (?, ?, ?, ?, ?)""",
                (record_id, name, cost, treatment_date, notes)
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
    def get_by_id(cls, treatment_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM treatments WHERE id = ?", (treatment_id,))
        treatment_data = cursor.fetchone()
        conn.close()
        if treatment_data:
            return cls(**treatment_data)
        return None

    @classmethod
    def get_by_record(cls, record_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM treatments 
            WHERE record_id = ?
            ORDER BY treatment_date DESC
        """, (record_id,))
        treatments = [cls(**row) for row in cursor.fetchall()]
        conn.close()
        return treatments

    @classmethod
    def update(cls, treatment_id, treatment_name=None, cost=None, treatment_date=None, notes=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        updates = []
        params = []

        if treatment_name is not None:
            updates.append("treatment_name = ?")
            params.append(treatment_name)
        if cost is not None:
            updates.append("cost = ?")
            params.append(cost)
        if treatment_date is not None:
            if hasattr(treatment_date, 'strftime'):
                treatment_date = treatment_date.strftime("%Y-%m-%d %H:%M:%S")
            updates.append("treatment_date = ?")
            params.append(treatment_date)
        if notes is not None:
            updates.append("notes = ?")
            params.append(notes)

        if not updates:
            return cls.get_by_id(treatment_id)

        params.append(treatment_id)
        query = f"UPDATE treatments SET {', '.join(updates)} WHERE id = ?"

        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return cls.get_by_id(treatment_id)

    @classmethod
    def delete(cls, treatment_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM treatments WHERE id = ?", (treatment_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
