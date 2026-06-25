import sqlite3

def create_table():
    conn = sqlite3.connect("interview.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_name TEXT,
        domain TEXT,
        score REAL
    )
    """)

    conn.commit()
    conn.close()

def save_result(name, domain, score):
    conn = sqlite3.connect("interview.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO interviews(candidate_name, domain, score) VALUES (?, ?, ?)",
        (name, domain, score)
    )

    conn.commit()
    conn.close()