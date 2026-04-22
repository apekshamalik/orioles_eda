import sqlite3
from pathlib import Path
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../database/mlb.db"))

print(f"DB_PATH is: {DB_PATH}")  

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    schema_path = Path("src/database/schema.sql")
    
    with get_connection() as conn:
        with open(schema_path) as f:
            conn.executescript(f.read())
        conn.commit()

if __name__ == "__main__":
    init_db()
