import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "dental_center.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db_connection() as conn:
        with open(Path(__file__).parent / "schema.sql", "r") as f:
            conn.executescript(f.read())
