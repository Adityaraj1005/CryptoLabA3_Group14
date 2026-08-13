
# Vulnerability Report: Directory Traversal

- **CWE ID:** CWE-22 (Improper Limitation of a Pathname to a Restricted Directory)
- **Severity:** High
- **Target File:** `src/vulnerable_app.py`
- **Target Function:** `download_report()`

## 1. Description
The `download_report()` function constructs target file paths using `os.path.join(REPORTS_DIRECTORY, filename)` with un-sanitized user input. Because relative path traversal sequences (like `../`) are not stripped or validated, an attacker can escape `REPORTS_DIRECTORY` to read arbitrary system files.

## 2. Exploit Scenario
1. Select option `7` (Download report) in `vulnerable_app.py`.
2. Enter the input payload: `../README.md` or `../../../../etc/passwd`.
3. The application resolves the path outside the designated reports folder and dumps sensitive file contents to stdout.

## 3. Remediation Strategy
In `src/secure_version.py`:
- Resolve `REPORTS_DIRECTORY` and the requested file path using `os.path.realpath()`.
- Use `os.path.commonpath()` to verify that the target path remains strictly enclosed inside `REPORTS_DIRECTORY`.
