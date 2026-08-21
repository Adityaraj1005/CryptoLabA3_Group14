
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE = BASE_DIR / "library.db"


def get_connection():
    """Return a connection to the library database."""

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """Create tables and insert sample data."""

    connection = get_connection()

    cursor = connection.cursor()

    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            available INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            issue_date TEXT NOT NULL,
            return_date TEXT,
            fine REAL DEFAULT 0,

            FOREIGN KEY(book_id)
                REFERENCES books(id),

            FOREIGN KEY(member_id)
                REFERENCES members(id)
        );
        """
    )

    book_count = cursor.execute(
        "SELECT COUNT(*) FROM books"
    ).fetchone()[0]

    if book_count == 0:

        cursor.executemany(
            """
            INSERT INTO books(title, author)
            VALUES (?, ?)
            """,
            [
                ("The Hobbit", "J.R.R. Tolkien"),
                ("1984", "George Orwell"),
                ("Clean Code", "Robert C. Martin"),
                ("The Great Gatsby", "F. Scott Fitzgerald"),
                ("Pride and Prejudice", "Jane Austen"),
            ],
        )

    member_count = cursor.execute(
        "SELECT COUNT(*) FROM members"
    ).fetchone()[0]

    if member_count == 0:

        cursor.executemany(
            """
            INSERT INTO members(name, email)
            VALUES (?, ?)
            """,
            [
                ("Alice", "alice@example.com"),
                ("Bob", "bob@example.com"),
            ],
        )

    connection.commit()
    connection.close()


def get_current_day():
    """Returns the current date formatted as YYYY-MM-DD."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d")
