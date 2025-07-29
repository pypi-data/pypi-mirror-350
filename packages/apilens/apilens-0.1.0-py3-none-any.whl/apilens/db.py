import sqlite3
from .config import DB_PATH

class DB:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, isolation_level=None)

    def query(self, sql, params=None):
        cur = self.conn.cursor()
        cur.execute(sql, params or ())
        return cur.fetchall()

    def close(self):
        self.conn.close()

    # Placeholder for future Postgres support
