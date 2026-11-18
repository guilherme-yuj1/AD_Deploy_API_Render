import sqlite3
from database.db import get_db_connection


class UploadModel:
    @staticmethod
    def save_file(filename, filepath):
        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO uploads (filename, filepath) VALUES (?, ?)",
                (filename, filepath),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    @staticmethod
    def find_by_filename(filename):
        conn = get_db_connection()
        try:
            return conn.execute(
                "SELECT * FROM uploads WHERE filename = ?", (filename,)
            ).fetchone()
        finally:
            conn.close()
