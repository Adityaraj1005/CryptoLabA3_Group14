
import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from validation import (
    validate_name,
    validate_email,
    validate_positive_integer,
    validate_search
)

def test_validate_name_valid():
    assert validate_name("Rishi Yadav") == "Rishi Yadav"

def test_validate_name_invalid():
    with pytest.raises(ValueError):
        validate_name("Rishi123!")

def test_validate_email_valid():
    assert validate_email("user@example.com") == "user@example.com"

def test_validate_email_invalid():
    with pytest.raises(ValueError):
        validate_email("invalid-email-format")

def test_validate_positive_integer_valid():
    assert validate_positive_integer("10", "Book ID") == 10

def test_validate_positive_integer_invalid():
    with pytest.raises(ValueError):
        validate_positive_integer("-5", "Book ID")
