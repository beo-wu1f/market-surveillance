import sqlite3
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = PROJECT_DIR / "data" / "database" / "market.db"


def create_database():
    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            symbol TEXT NOT NULL,
            price REAL,
            change REAL,
            change_percent REAL,
            high REAL,
            low REAL,
            open REAL,
            previous_close REAL
        )
    """)

    connection.commit()
    connection.close()


def insert_quote(timestamp, symbol, quote):
    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO market_quotes (
            timestamp,
            symbol,
            price,
            change,
            change_percent,
            high,
            low,
            open,
            previous_close
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        symbol,
        quote["c"],
        quote["d"],
        quote["dp"],
        quote["h"],
        quote["l"],
        quote["o"],
        quote["pc"]
    ))

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
    print(f"Database created at: {DATABASE_PATH}")