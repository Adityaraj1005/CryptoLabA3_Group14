import re


def validate_name(name):
    """Validate a member name."""

    if not name:
        raise ValueError("Name cannot be empty.")

    name = name.strip()

    if not name:
        raise ValueError("Name cannot be empty.")

    if len(name) > 50:
        raise ValueError(
            "Name must be 50 characters or fewer."
        )

    if not re.fullmatch(
        r"[A-Za-z ]+",
        name
    ):
        raise ValueError(
            "Name can contain only letters and spaces."
        )

    return name


def validate_email(email):
    """Validate a basic email address."""

    if not email:
        raise ValueError(
            "Email cannot be empty."
        )

    email = email.strip()

    pattern = (
        r"^[A-Za-z0-9._%+-]+@"
        r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    if not re.fullmatch(pattern, email):
        raise ValueError(
            "Invalid email address."
        )

    if len(email) > 100:
        raise ValueError(
            "Email must be 100 characters or fewer."
        )

    return email


def validate_positive_integer(value, field_name):
    """Validate a positive integer."""

    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ValueError(
            f"{field_name} must be an integer."
        )

    if number <= 0:
        raise ValueError(
            f"{field_name} must be greater than zero."
        )

    return number


def validate_search(search):
    """Validate book search input."""

    if search is None:
        return ""

    search = search.strip()

    if len(search) > 100:
        raise ValueError(
            "Search text is too long."
        )

    return search

