import sqlite3
import os
from datetime import datetime

# Absolute path to this directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "crisbee_memory.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            intent TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_memory(user_input, intent):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO memory (user_input, intent, timestamp) VALUES (?, ?, ?)",
        (user_input, intent, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
