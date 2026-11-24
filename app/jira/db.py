# app/jira/db.py

import sqlite3
from pathlib import Path

DB_PATH = "data/smartdesk.db"


def get_connection():

    Path("data").mkdir(
        exist_ok=True
    )

    conn = sqlite3.connect(
        DB_PATH
    )

    conn.row_factory = (
        sqlite3.Row
    )

    return conn


def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets(

        id TEXT PRIMARY KEY,
        email TEXT,
        summary TEXT,
        description TEXT,
        category TEXT,
        priority TEXT,
        status TEXT,
        created_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    conn.close()


initialize_database()