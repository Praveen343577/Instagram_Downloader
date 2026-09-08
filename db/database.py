import sqlite3
from config import DB_FILE

def init_db():
    """Initializes the SQLite database and creates the downloads table if it does not exist."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS downloads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                account_name TEXT,
                description TEXT,
                status TEXT,
                download_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def is_downloaded(url: str) -> bool:
    """Checks if a sanitized URL already exists in the database."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM downloads WHERE url = ?", (url,))
        return cursor.fetchone() is not None

def insert_record(url: str, account_name: str | None, description: str | None, status: str):
    """Inserts or updates a download record upon sequence completion or explicit failure."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO downloads (url, account_name, description, status)
            VALUES (?, ?, ?, ?)
        ''', (url, account_name, description, status))
        conn.commit()