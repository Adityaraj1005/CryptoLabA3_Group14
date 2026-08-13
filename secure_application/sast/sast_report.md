
# SAST Scan Summary (Bandit Tool)

- **Tool:** Bandit v1.7.8
- **Target Folder:** `secure_application/src/`
- **Scan Date:** August 2026

## Key Findings

1. **Path Traversal Risk (High/CWE-22):**
   - **Location:** `src/vulnerable_app.py` line 245
   - **Issue:** Direct use of `os.path.join()` with raw `input()` string allows path manipulation.
   - **Status in Secure Version:** Fixed using `os.path.realpath()` and `os.path.commonpath()`.

2. **Unvalidated Input Conversions (Medium/CWE-20):**
   - **Location:** `src/vulnerable_app.py` lines 85, 132
   - **Issue:** Direct integer typecasts (`int(input())`) without range bounds or try-catch blocks.
   - **Status in Secure Version:** Fixed using helper functions in `validation.py`.
