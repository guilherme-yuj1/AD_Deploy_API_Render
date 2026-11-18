import os
import sqlite3
from pathlib import Path


def get_database_path():
    return Path(os.getenv("DATABASE_PATH", Path(__file__).resolve().parents[1] / "instance" / "database.db"))


def get_db_connection(database_path=None):
    path = Path(database_path) if database_path else get_database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), timeout=15)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(database_path=None):
    conn = get_db_connection(database_path)
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT UNIQUE NOT NULL,
                filepath TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    finally:
        conn.close()
