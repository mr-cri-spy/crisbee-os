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
            user TEXT,
            intent TEXT,
            target TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()





def save_memory(user, intent, target):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO memory (user , intent, target, timestamp) VALUES (?, ?, ?)",
        (user, intent, target, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def most_frequent_targets(intent, limit=3):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT target, COUNT(*) as count
        FROM memory
        WHERE intent = ?
        GROUP BY target
        ORDER BY count DESC
        LIMIT ?
    """, (intent, limit))
    results = c.fetchall()
    conn.close()
    return [r[0] for r in results]


CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    intent TEXT,
    target TEXT,
    timestamp TEXT
)
