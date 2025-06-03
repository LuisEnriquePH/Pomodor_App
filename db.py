import sqlite3
from datetime import datetime

class ActivityDB:
    def __init__(self):
        self.conn = sqlite3.connect("pomodoro.db")
        self.create_table()

    def create_table(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                activity TEXT,
                duration INTEGER,
                timestamp TEXT
            )
        ''')
        self.conn.commit()

    def add_session(self, activity, duration):
        now = datetime.now().isoformat()
        self.conn.execute(
            "INSERT INTO activity_log (activity, duration, timestamp) VALUES (?, ?, ?)",
            (activity, duration, now)
        )
        self.conn.commit()

    def get_all_sessions(self):
        cursor = self.conn.execute(
            "SELECT activity, duration, timestamp FROM activity_log ORDER BY timestamp DESC"
        )
        return cursor.fetchall()
