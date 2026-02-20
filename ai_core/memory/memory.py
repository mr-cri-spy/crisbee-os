import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(
    os.path.expanduser("~"),
    "CrisbeeWorkspace",
    "crisbee_memory.db"
)

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
    c.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            role TEXT,
            intent TEXT,
            target TEXT,
            status TEXT,
            timestamp TEXT
        )
    """)   



    conn.commit()
    conn.close()


def log_audit(user, role, intent, target, status):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO audit_log (user, role, intent, target, status, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
        (user, role, intent, target, status, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()



def save_memory(user, intent, target):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO memory (user, intent, target, timestamp) VALUES (?, ?, ?, ?)",
        (user, intent, target, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def most_frequent_targets(user, intent, limit=3):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT target, COUNT(*) as count
        FROM memory
        WHERE user = ? AND intent = ?
        GROUP BY target
        ORDER BY count DESC
        LIMIT ?
    """, (user, intent, limit))
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]
