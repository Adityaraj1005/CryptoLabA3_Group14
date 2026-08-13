
import os
import sqlite3
from datetime import datetime

from database import get_connection


REPORTS_DIRECTORY = (
    os.path.join(
        os.path.dirname(
            os.path.dirname(__file__)
        ),
        "reports"
    )
)


def show_books():
    """Display all books."""

    connection = get_connection()

    books = connection.execute(
        "SELECT * FROM books"
    ).fetchall()

    connection.close()

    print("\n--- BOOKS ---")

    for book in books:

        status = (
            "Available"
            if book["available"]
            else "Issued"
        )

        print(
            f"{book['id']}. "
            f"{book['title']} - "
            f"{book['author']} "
            f"[{status}]"
        )


def search_books():
    """
    VULNERABILITY 2:
    Improper Input Validation

    User input is accepted without checking
    length, type, or content.
    """

    search = input(
        "Enter book title/author: "
    )

    connection = get_connection()

    books = connection.execute(
        """
        SELECT *
        FROM books
        WHERE title LIKE ?
           OR author LIKE ?
        """,
        (
            f"%{search}%",
            f"%{search}%",
        ),
    ).fetchall()

    connection.close()

    print("\n--- SEARCH RESULTS ---")

    for book in books:

        print(
            f"{book['id']}. "
            f"{book['title']} - "
            f"{book['author']}"
        )


def register_member():
    """
    VULNERABILITY 2:
    Improper Input Validation

    No validation is performed on member
    name or email.
    """

    name = input(
        "Enter member name: "
    )

    email = input(
        "Enter member email: "
    )

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO members(name, email)
        VALUES (?, ?)
        """,
        (name, email),
    )

    connection.commit()
    connection.close()

    print(
        "Member registered successfully."
    )


def issue_book():
    """
    VULNERABILITY 2:
    Improper Input Validation

    Book and member IDs are converted directly
    without checking whether they are positive
    integers or whether the entities exist.
    """

    book_id = int(
        input("Enter book ID: ")
    )

    member_id = int(
        input("Enter member ID: ")
    )

    connection = get_connection()

    book = connection.execute(
        """
        SELECT *
        FROM books
        WHERE id = ?
        """,
        (book_id,),
    ).fetchone()

    if not book:

        print("Book does not exist.")
        connection.close()
        return

    if not book["available"]:

        print("Book is already issued.")
        connection.close()
        return

    connection.execute(
        """
        INSERT INTO loans(
            book_id,
            member_id,
            issue_date
        )
        VALUES (?, ?, ?)
        """,
        (
            book_id,
            member_id,
            datetime.now().isoformat(),
        ),
    )

    connection.execute(
        """
        UPDATE books
        SET available = 0
        WHERE id = ?
        """,
        (book_id,),
    )

    connection.commit()
    connection.close()

    print("Book issued successfully.")


def return_book():
    """
    VULNERABILITY 2:
    Improper Input Validation

    Loan ID is accepted without proper
    validation.
    """

    loan_id = int(
        input("Enter loan ID: ")
    )

    connection = get_connection()

    loan = connection.execute(
        """
        SELECT *
        FROM loans
        WHERE id = ?
          AND return_date IS NULL
        """,
        (loan_id,),
    ).fetchone()

    if not loan:

        print("Loan not found.")
        connection.close()
        return

    connection.execute(
        """
        UPDATE loans
        SET return_date = ?
        WHERE id = ?
        """,
        (
            datetime.now().isoformat(),
            loan_id,
        ),
    )

    connection.execute(
        """
        UPDATE books
        SET available = 1
        WHERE id = ?
        """,
        (loan["book_id"],),
    )

    connection.commit()
    connection.close()

    print("Book returned successfully.")


def calculate_fine():
    """
    Calculates a simple fine.

    Fine:
    2 currency units per day after 7 days.
    """

    loan_id = int(
        input("Enter loan ID: ")
    )

    connection = get_connection()

    loan = connection.execute(
        """
        SELECT *
        FROM loans
        WHERE id = ?
        """,
        (loan_id,),
    ).fetchone()

    if not loan:

        print("Loan not found.")
        connection.close()
        return

    issue_date = datetime.fromisoformat(
        loan["issue_date"]
    )

    days = (
        datetime.now() - issue_date
    ).days

    overdue_days = max(
        0,
        days - 7
    )

    fine = overdue_days * 2

    print(
        f"Fine: ₹{fine}"
    )

    connection.close()


def download_report():
    """
    VULNERABILITY 3:
    DIRECTORY TRAVERSAL

    The filename comes directly from the user
    and is combined with the reports directory.

    No verification is performed to ensure that
    the resulting path remains inside REPORTS_DIRECTORY.
    """

    filename = input(
        "Enter report filename: "
    )

    filepath = os.path.join(
        REPORTS_DIRECTORY,
        filename
    )

    print(
        f"Attempting to access: {filepath}"
    )

    try:

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as report:

            print("\n--- REPORT ---")
            print(report.read())

    except FileNotFoundError:

        print("Report not found.")

    except Exception as error:

        print(
            f"Error: {error}"
        )


def vulnerable_application():
    """
    VULNERABILITY 1:
    MISSING AUTHENTICATION

    The application directly enters the main
    menu without asking the user to authenticate.
    """

    print(
        "\n================================"
    )

    print(
        " LIBRARY MANAGEMENT SYSTEM"
    )

    print(
        "================================"
    )

    print(
        "\nWARNING: "
        "This is the intentionally vulnerable "
        "version for security testing."
    )

    while True:

        print(
            """
1. Show books
2. Search books
3. Register member
4. Issue book
5. Return book
6. Calculate fine
7. Download report
8. Exit
"""
        )

        choice = input(
            "Select an option: "
        )

        if choice == "1":

            show_books()

        elif choice == "2":

            search_books()

        elif choice == "3":

            register_member()

        elif choice == "4":

            issue_book()

        elif choice == "5":

            return_book()

        elif choice == "6":

            calculate_fine()

        elif choice == "7":

            download_report()

        elif choice == "8":

            print("Goodbye.")
            break

        else:

            print("Invalid menu option.")
