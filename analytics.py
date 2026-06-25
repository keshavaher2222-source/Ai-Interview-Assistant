import sqlite3
import pandas as pd

def get_data():
    conn = sqlite3.connect("interview.db")

    df = pd.read_sql(
        "SELECT * FROM interviews",
        conn
    )

    conn.close()

    return df