import sqlite3
from datetime import datetime
from .config import DB_PATH

class _APILogger:
    def __init__(self, db_path=DB_PATH):
        self.conn = sqlite3.connect(db_path)
        self._ensure_table()

    def _format_cost(self, cost):
        """Format cost as USD currency string."""
        return f"${cost:.6f}"

    def _ensure_table(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS api_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                provider TEXT,
                model TEXT,
                prompt_tokens INTEGER,
                completion_tokens INTEGER,
                cost REAL,
                formatted_cost TEXT,
                status TEXT,
                error_message TEXT,
                user_id TEXT,
                tenant_id TEXT
            )
        ''')

    def log_call(self, call_id=None, provider=None, model=None, prompt_tokens=None, completion_tokens=None, cost=None, status=None, error_message=None, user_id=None, tenant_id=None):
        formatted_cost = self._format_cost(cost) if cost is not None else None
        with self.conn:
            if call_id is None:
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO api_logs (timestamp, provider, model, prompt_tokens, completion_tokens, cost, formatted_cost, status, error_message, user_id, tenant_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (datetime.utcnow().isoformat(), provider, model, prompt_tokens, completion_tokens, cost, formatted_cost, status, error_message, user_id, tenant_id))
                return cursor.lastrowid
            else:
                self.conn.execute('''
                    UPDATE api_logs
                    SET prompt_tokens = ?, completion_tokens = ?, cost = ?, formatted_cost = ?, status = ?, error_message = ?, user_id = ?, tenant_id = ?
                    WHERE id = ?
                ''', (prompt_tokens, completion_tokens, cost, formatted_cost, status, error_message, user_id, tenant_id, call_id))

    def get_logs(self, model=None, status=None, provider=None, user_id=None, tenant_id=None):
        query = "SELECT id, timestamp, provider, model, prompt_tokens, completion_tokens, formatted_cost as cost, status, error_message FROM api_logs"
        filters = []
        params = []
        if model:
            filters.append("model = ?")
            params.append(model)
        if status:
            filters.append("status = ?")
            params.append(status)
        if provider:
            filters.append("provider = ?")
            params.append(provider)
        if user_id:
            filters.append("user_id = ?")
            params.append(user_id)
        if tenant_id:
            filters.append("tenant_id = ?")
            params.append(tenant_id)
        if filters:
            query += " WHERE " + " AND ".join(filters)
        query += " ORDER BY timestamp DESC"
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def get_total_cost(self, model=None, provider=None, user_id=None, tenant_id=None):
        query = "SELECT SUM(cost) FROM api_logs WHERE status = 'success'"
        params = []
        if model:
            query += " AND model = ?"
            params.append(model)
        if provider:
            query += " AND provider = ?"
            params.append(provider)
        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)
        if tenant_id:
            query += " AND tenant_id = ?"
            params.append(tenant_id)
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        total_cost = cursor.fetchone()[0] or 0.0
        return self._format_cost(total_cost)

    def __del__(self):
        self.conn.close()
