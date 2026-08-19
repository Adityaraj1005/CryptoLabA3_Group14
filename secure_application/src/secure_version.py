
import os
from datetime import datetime

from database import get_connection
from validation import (
    validate_email,
    validate_name,
    validate_positive_integer,
    validate_search,
)


BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

REPORTS_DIRECTORY = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "reports"
    )
)


AUTHENTICATED = False


def login():
    """
    Simple demonstration authentication.

    In a real system, passwords should be stored
    using a proper password hashing mechanism.
    """

    global AUTHENTICATED

    username = input(
        "Username: "
    )

    password = input(
        "Password: "
    )

    if (
        username == "librarian"
        and password == "Library123!"
    ):

        AUTHENTICATED = True

        print(
            "Login successful."
        )

        return True

    print(
        "Invalid credentials."
    )

    return False


def require_authentication():
    """
    Security control for protected operations.
    """

    if not AUTHENTICATED:

        print(
            "Access denied. "
            "Please login first."
        )

        return False

    return True


def show_books():

    if not require_authentication():
        return

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

    if not require_authentication():
        return

    raw_search = input(
        "Enter book title/author: "
    )

    try:

        search = validate_search(
            raw_search
        )

    except ValueError as error:

        print(
            f"Input error: {error}"
        )

        return

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

    if not require_authentication():
        return

    try:

        name = validate_name(
            input("Enter member name: ")
        )

        email = validate_email(
            input("Enter member email: ")
        )

    except ValueError as error:

        print(
            f"Input error: {error}"
        )

        return

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO members(name, email)
        VALUES (?, ?)
        """,
        (
            name,
            email,
        ),
    )

    connection.commit()
    connection.close()

    print(
        "Member registered successfully."
    )


def issue_book():

    if not require_authentication():
        return

    try:

        book_id = validate_positive_integer(
            input("Enter book ID: "),
            "Book ID"
        )

        member_id = validate_positive_integer(
            input("Enter member ID: "),
            "Member ID"
        )

    except ValueError as error:

        print(
            f"Input error: {error}"
        )

        return

    connection = get_connection()

    book = connection.execute(
        """
        SELECT *
        FROM books
        WHERE id = ?
        """,
        (book_id,),
    ).fetchone()

    member = connection.execute(
        """
        SELECT *
        FROM members
        WHERE id = ?
        """,
        (member_id,),
    ).fetchone()

    if not book:

        print("Book does not exist.")
        connection.close()
        return

    if not member:

        print("Member does not exist.")
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

    print(
        "Book issued successfully."
    )


def return_book():

    if not require_authentication():
        return

    try:

        loan_id = validate_positive_integer(
            input("Enter loan ID: "),
            "Loan ID"
        )

    except ValueError as error:

        print(
            f"Input error: {error}"
        )

        return

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

        print(
            "Active loan not found."
        )

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

    print(
        "Book returned successfully."
    )


def calculate_fine():

    if not require_authentication():
        return

    try:

        loan_id = validate_positive_integer(
            input("Enter loan ID: "),
            "Loan ID"
        )

    except ValueError as error:

        print(
            f"Input error: {error}"
        )

        return

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

        print(
            "Loan not found."
        )

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

    if not require_authentication():
        return

    filename = input(
        "Enter report filename: "
    ).strip()

    if not filename:

        print(
            "Filename cannot be empty."
        )

        return

    # Resolve both paths to absolute paths.
    reports_directory = os.path.realpath(
        REPORTS_DIRECTORY
    )

    requested_path = os.path.realpath(
        os.path.join(
            reports_directory,
            filename
        )
    )

    # Directory traversal protection.
    try:

        common_path = os.path.commonpath(
            [
                reports_directory,
                requested_path,
            ]
        )

    except ValueError:

        print(
            "Invalid report path."
        )

        return

    if common_path != reports_directory:

        print(
            "Access denied: "
            "path is outside the reports directory."
        )

        return

    if not os.path.isfile(
        requested_path
    ):

        print(
            "Report not found."
        )

        return

    try:

        with open(
            requested_path,
            "r",
            encoding="utf-8"
        ) as report:

            print("\n--- REPORT ---")
            print(report.read())

    except OSError:

        print(
            "Unable to read report."
        )


def secure_application():

    print(
        "\n================================"
    )

    print(
        " SECURE LIBRARY MANAGEMENT SYSTEM"
    )

    print(
        "================================"
    )

    while True:

        print(
            """
1. Login
2. Show books
3. Search books
4. Register member
5. Issue book
6. Return book
7. Calculate fine
8. Download report
9. Exit
"""
        )

        choice = input(
            "Select an option: "
        )

        if choice == "1":

            login()

        elif choice == "2":

            show_books()

        elif choice == "3":

            search_books()

        elif choice == "4":

            register_member()

        elif choice == "5":

            issue_book()

        elif choice == "6":

            return_book()

        elif choice == "7":

            calculate_fine()

        elif choice == "8":

            download_report()

        elif choice == "9":

            print("Goodbye.")
            break

        else:

            print(
                "Invalid menu option."
            )

    if __name__ == "__main__":
        secure_application()
