import sqlite3

DB_NAME = "expenses.db"

SCHEMA = [
    """
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL CHECK (amount > 0),
        category TEXT NOT NULL ,
        date TEXT NOT NULL,
        note TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL UNIQUE,
        monthly_limit REAL NOT NULL CHECK (monthly_limit > 0)
    )
    """,
]


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn, conn.cursor()


def init_db():
    conn, cursor = get_connection()

    for statement in SCHEMA:
        cursor.execute(statement)

    conn.commit()
    conn.close()
