# Master Security Analysis & Remediation Report

**System:** Library Management System  
**Module:** `secure_application`  
**Lab Assignment:** Cryptography & Application Security SAST Analysis  

---

## 1. Executive Summary
This report documents the security audit and static application security testing (SAST) performed on the Library Management System. Three primary vulnerabilities were identified in `src/vulnerable_app.py`, successfully exploited, and remediated in `src/secure_version.py`.

---

## 2. Vulnerability Matrix

| Vulnerability | CWE ID | Severity | Affected Function | Fixed In |
| :--- | :--- | :--- | :--- | :--- |
| **Missing Authentication** | CWE-306 | High | `vulnerable_application()` | `secure_version.py` (`require_authentication`) |
| **Improper Input Validation** | CWE-20 | Medium | `register_member()`, `issue_book()` | `validation.py` (`validate_*`) |
| **Directory Traversal** | CWE-22 | High | `download_report()` | `secure_version.py` (`os.path.commonpath`) |

---

## 3. Verification & Testing
Remediation effectiveness was verified through automated unit testing (`testcases/`) and SAST code scanning (`sast/`). All input validation and directory containment controls passed security assertions.**
