import os

from database import (
    get_connection,
    get_current_day,
    set_current_day,
    advance_day,
)


REPORTS_DIRECTORY = (
    os.path.join(
        os.path.dirname(
            os.path.dirname(__file__)
        ),
        "reports"
    )
)


def show_loans():
    """Display all loans with their IDs and simulated days."""

    connection = get_connection()

    loans = connection.execute(
        """
        SELECT
            loans.id AS loan_id,
            books.title AS book_title,
            members.name AS member_name,
            loans.issue_day,
            loans.return_day
        FROM loans
        JOIN books
            ON loans.book_id = books.id
        JOIN members
            ON loans.member_id = members.id
        ORDER BY loans.id
        """
    ).fetchall()

    connection.close()

    print("\n--- LOANS ---")

    if not loans:
        print("No loans found.")
        return

    for loan in loans:

        status = (
            "Returned"
            if loan["return_day"] is not None
            else "Active"
        )

        print(
            f"Loan ID   : {loan['loan_id']}\n"
            f"  Book    : {loan['book_title']}\n"
            f"  Member  : {loan['member_name']}\n"
            f"  Issue Day: {loan['issue_day']}\n"
            f"  Return Day: "
            f"{loan['return_day'] if loan['return_day'] else '-'}\n"
            f"  Status  : {status}\n"
        )


def show_books():
    """Display all books."""

    connection = get_connection()

    books = connection.execute(
        "SELECT * FROM books"
    ).fetchall()

    connection.close()

    print("\n--- BOOKS ---")

    if not books:
        print("No books found.")
        return

    for book in books:

        status = (
            "Available"
            if book["available"]
            else "Issued"
        )

        print(
            f"ID: {book['id']} | "
            f"{book['title']} - "
            f"{book['author']} "
            f"[{status}]"
        )


def show_members():
    """Display all members and their IDs."""

    connection = get_connection()

    members = connection.execute(
        """
        SELECT id, name, email
        FROM members
        ORDER BY id
        """
    ).fetchall()

    connection.close()

    print("\n--- MEMBERS ---")

    if not members:
        print("No members found.")
        return

    for member in members:

        print(
            f"ID: {member['id']} | "
            f"Name: {member['name']} | "
            f"Email: {member['email']}"
        )


def show_current_day():
    """Display the current simulated application day."""

    print(
        f"\nCurrent simulated day: "
        f"Day {get_current_day()}"
    )


def change_application_day():
    """Advance or set the simulated application day."""

    current_day = get_current_day()

    print(
        f"\nCurrent simulated day: Day {current_day}"
    )

    print(
        """
1. Advance days
2. Set exact day
"""
    )

    choice = input(
        "Select an option: "
    )

    try:

        if choice == "1":

            days = int(
                input(
                    "Advance by how many days: "
                )
            )

            if days <= 0:

                print(
                    "Days must be greater than zero."
                )

                return

            new_day = advance_day(days)

            print(
                f"Application day is now "
                f"Day {new_day}."
            )

        elif choice == "2":

            day = int(
                input(
                    "Enter application day: "
                )
            )

            if day < current_day:

                print(
                    "You cannot move the clock backwards."
                )

                return

            set_current_day(day)

            print(
                f"Application day is now "
                f"Day {day}."
            )

        else:

            print("Invalid option.")

    except ValueError as error:

        print(
            f"Input error: {error}"
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

    if not books:
        print("No books found.")
        return

    for book in books:

        print(
            f"ID: {book['id']} | "
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

    print("\n--- AVAILABLE BOOKS ---")

    connection = get_connection()

    books = connection.execute(
        """
        SELECT *
        FROM books
        WHERE available = 1
        ORDER BY id
        """
    ).fetchall()

    connection.close()

    if not books:

        print("No books are currently available.")
        return

    for book in books:

        print(
            f"ID: {book['id']} | "
            f"{book['title']} - "
            f"{book['author']}"
        )

    book_id = int(
        input("\nEnter book ID: ")
    )

    print("\n--- MEMBERS ---")

    connection = get_connection()

    members = connection.execute(
        """
        SELECT id, name, email
        FROM members
        ORDER BY id
        """
    ).fetchall()

    connection.close()

    for member in members:

        print(
            f"ID: {member['id']} | "
            f"{member['name']} | "
            f"{member['email']}"
        )

    member_id = int(
        input("\nEnter member ID: ")
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

    current_day = get_current_day()

    connection.execute(
        """
        INSERT INTO loans(
            book_id,
            member_id,
            issue_day
        )
        VALUES (?, ?, ?)
        """,
        (
            book_id,
            member_id,
            current_day,
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

    loan = connection.execute(
        """
        SELECT id
        FROM loans
        WHERE book_id = ?
          AND member_id = ?
          AND issue_day = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (
            book_id,
            member_id,
            current_day,
        ),
    ).fetchone()

    connection.close()

    print("\n--- LOAN CREATED ---")

    print(
        f"Loan ID   : {loan['id']}"
    )

    print(
        f"Book      : {book['title']}"
    )

    print(
        f"Member    : {member['name']}"
    )

    print(
        f"Issue Day : Day {current_day}"
    )

    print(
        "Status    : Active"
    )


def return_book():
    """
    VULNERABILITY 2:
    Improper Input Validation

    Loan ID is accepted without proper
    validation.
    """

    show_loans()

    loan_id = int(
        input("\nEnter loan ID: ")
    )

    connection = get_connection()

    loan = connection.execute(
        """
        SELECT *
        FROM loans
        WHERE id = ?
          AND return_day IS NULL
        """,
        (loan_id,),
    ).fetchone()

    if not loan:

        print("Loan not found.")
        connection.close()
        return

    current_day = get_current_day()

    connection.execute(
        """
        UPDATE loans
        SET return_day = ?
        WHERE id = ?
        """,
        (
            current_day,
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
        f"Book returned successfully "
        f"on Day {current_day}."
    )


def calculate_fine():
    """
    Calculates a simple fine.

    First 7 days are free.
    Fine is ₹2 per overdue day.
    """

    show_loans()

    loan_id = int(
        input("\nEnter loan ID: ")
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

    connection.close()

    if not loan:

        print("Loan not found.")
        return

    current_day = get_current_day()

    days = (
        current_day - loan["issue_day"]
    )

    overdue_days = max(
        0,
        days - 7
    )

    fine = overdue_days * 2

    print(
        "\n--- FINE CALCULATION ---"
    )

    print(
        f"Loan ID       : {loan['id']}"
    )

    print(
        f"Issue Day     : Day {loan['issue_day']}"
    )

    print(
        f"Current Day   : Day {current_day}"
    )

    print(
        f"Days Borrowed : {days}"
    )

    print(
        f"Overdue Days  : {overdue_days}"
    )

    print(
        f"Fine          : ₹{fine}"
    )


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
        f"\nCURRENT APPLICATION DAY: "
        f"Day {get_current_day()}"
    )

    print(
        "\nWARNING: "
        "This is the intentionally vulnerable "
        "version for security testing."
    )

    while True:

        print(
            """
================================
            MENU
================================

1.  Show books
2.  Show members
3.  Search books
4.  Register member
5.  Issue book
6.  Return book
7.  Show loans
8.  Calculate fine
9.  Download report
10. Show current day
11. Change application day
12. Exit
"""
        )

        choice = input(
            "Select an option: "
        )

        if choice == "1":

            show_books()

        elif choice == "2":

            show_members()

        elif choice == "3":

            search_books()

        elif choice == "4":

            register_member()

        elif choice == "5":

            issue_book()

        elif choice == "6":

            return_book()

        elif choice == "7":

            show_loans()

        elif choice == "8":

            calculate_fine()

        elif choice == "9":

            download_report()

        elif choice == "10":

            show_current_day()

        elif choice == "11":

            change_application_day()

        elif choice == "12":

            print("Goodbye.")
            break

        else:

            print(
                "Invalid menu option."
            )
