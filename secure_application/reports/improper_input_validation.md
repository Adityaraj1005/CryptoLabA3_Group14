
# Vulnerability Report: Improper Input Validation

- **CWE ID:** CWE-20 (Improper Input Validation)
- **Severity:** Medium
- **Target File:** `src/vulnerable_app.py`
- **Target Functions:** `register_member()`, `issue_book()`, `search_books()`, `return_book()`

## 1. Description
The vulnerable application accepts user input directly into system operations without verifying length, data type, numeric range, or formatting:
- `register_member()` allows empty or arbitrarily long string inputs for name and email.
- `issue_book()` and `return_book()` attempt direct integer casting without checking if IDs are positive integers or if corresponding records exist in SQLite.
- `search_books()` accepts unvalidated search strings.

## 2. Exploit Scenario
1. In `register_member()`, enter special characters or blank spaces to create invalid database profiles.
2. In `issue_book()`, enter negative integers (e.g., `-5`) or nonexistent IDs, causing unhandled exceptions or state corruption in the database.

## 3. Remediation Strategy
In `src/validation.py` and `src/secure_version.py`:
- `validate_name()` enforces regex alphabetic rules (`[A-Za-z ]+`) and a length limit of 50 characters.
- `validate_email()` verifies standard RFC-compliant email structure via regex.
- `validate_positive_integer()` verifies that numeric inputs are strictly greater than zero (`value > 0`).
