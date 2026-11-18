from database.db import get_db_connection


class DownloadModel:
    @staticmethod
    def find_by_filename(filename):
        conn = get_db_connection()
        try:
            return conn.execute(
                "SELECT * FROM uploads WHERE filename = ?", (filename,)
            ).fetchone()
        finally:
            conn.close()
