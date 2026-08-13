
# Vulnerability Report: Missing Authentication

- **CWE ID:** CWE-306 (Missing Authentication for Critical Function)
- **Severity:** High
- **Target File:** `src/vulnerable_app.py`
- **Target Function:** `vulnerable_application()`

## 1. Description
The vulnerable version of the application directly enters the main interactive menu without prompting the user to authenticate or verify their identity. Any local console user can invoke state-changing administrative operations—such as registering members, issuing books, returning books, and calculating late fines—without presenting credentials.

## 2. Exploit Scenario
1. Launch `python3 src/app.py`.
2. Select option `3` (Register member) or option `4` (Issue book).
3. The system executes the command and updates `library.db` without requesting a username or password.

## 3. Remediation Strategy
In `src/secure_version.py`, administrative workflows are gated by an explicit authentication check:
- `login()` verifies credentials (`librarian` / `Library123!`) and updates the global session flag `AUTHENTICATED`.
- `require_authentication()` checks `AUTHENTICATED` before allowing execution of sensitive functions.
