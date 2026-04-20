import sqlite3
from pathlib import Path

def get_connection():
    conn = sqlite3.connect('mlb.db', check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    schema_path = Path(__file__).parent / "schema.sql"
    
    with get_connection() as conn:
        with open(schema_path) as f:
            conn.executescript(f.read())
        conn.commit()

if __name__ == "__main__":
    init_db()
