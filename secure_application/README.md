
Secure Application: Library Management System (Group 14)

Course: Cryptography Laboratory (22CPP307)

Assignment: Lab Assignment 3 - Vulnerable Application & SAST Analysis

Assigned Topic: Library Management System (Group ID: 14 % 10 = 4)
📌 Project Overview

This project implements a lightweight, console-based Library Management System developed in Python. It simulates core library operations while intentionally incorporating 3 specific security vulnerabilities for educational demonstration and SAST (Static Application Security Testing) analysis.
🎯 Core Functionalities

    Member Registration: Register new library users and store profiles in the system database.

    Book Search Operations: Query books by title or author name using terminal prompts.

    Book Issue: Assign available library books to registered members.

    Book Return: Process returned items and clear active user checkout records.

    Fine Calculation: Calculate overdue late fees based on checkout duration.

    ⚠️ Intentionally Implemented Vulnerabilities

    1. **Missing Authorization / Broken Access Control:**
   * **Location:** `src/app.py` inside administrative functions (Member Registration & Book Issue).
   * **Flaw:** The application lacks access control checks, role verification, or authentication. Any user on the terminal can execute privileged admin     commands without providing credentials or proving elevated privileges.

2. **Directory Traversal (Path Traversal):**
   * **Location:** `src/app.py` inside the Book Catalog / Summary File Reader feature.
   * **Flaw:** User input is directly appended to construct file paths without sanitization or directory sandboxing (e.g., `open(f"outputs/        {user_input}")`). An attacker can supply dot-dot-slash (`../`) relative path sequences to escape the designated output folder and read arbitrary files on the operating system.

3. **Improper Input Validation:**
   * **Location:** `src/app.py` inside the Fine Calculation feature.
   * **Flaw:** Accepts unvalidated negative numerical inputs for overdue days without range checking. This causes logical state corruption where the system calculates negative fines (resulting in the library owing money to the user).

## 📂 Directory Structure

```text
secure_application/
├── src/                  # Source code (Library Management System)
│   ├── app.py            # Main entry point
│   ├── database.py       # SQLite database connection & setup
│   ├── vulnerable_app.py # Vulnerable application logic
│   ├── secure_version.py # Remediated application logic
│   ├── validation.py     # Input and path validation functions
│   └── requirements.txt  # Python dependencies
├── reports/              # SAST reports & security documentation
│   ├── security_report.md
│   ├── missing_authentication.md
│   ├── improper_input_validation.md
│   └── directory_traversal.md
├── screenshots/          # Execution proof and exploit screenshots
├── sast/                 # SAST scan configuration and outputs
│   ├── sast_report.md
│   └── bandit_report.txt
├── outputs/              # Application database and sample files
│   ├── sample_report.txt
│   └── library.db
├── testcases/            # Automated unit tests and exploit suites
│   ├── test_authentication.py
│   ├── test_input_validation.py
│   ├── test_directory_traversal.py
│   └── test_library.py
└── README.md             # Project documentation            # Project documentation



🚀 How to Run the Application
1. Install Dependencies
2. pip install -r secure_application/src/requirements.txt
```[cite: 6]

### 2. Launch Application
```bash
python3 secure_application/src/app.py
```[cite: 2]

### 3. Run Automated Unit Tests
```bash
pytest secure_application/testcases/

4. Execute SAST Security Scan
bandit -r secure_application/src/ -o secure_application/sast/bandit_report.txt -f txt
```[cite: 6]

---

## 🧪 Testing the Vulnerabilities

### 1. Missing Authorization (CWE-306)
* **Vulnerable Mode:** Select Option `3` (Register Member) or Option `4` (Issue Book)[cite: 1]. The system performs database updates without asking for credentials[cite: 1].
* **Secure Mode:** Select Option `2` (Register Member)[cite: 5]. The system blocks execution with `Access denied. Please login first.` until you authenticate via Option `1`[cite: 5].

### 2. Directory Traversal (CWE-22)
* **Vulnerable Mode:** Select Option `7` (Download Report) and enter `../README.md`[cite: 1]. The application escapes the `reports/` folder and prints the repository `README.md` contents on the console[cite: 1].
* **Secure Mode:** Select Option `8` (Download Report) and enter `../README.md`[cite: 5]. The system catches the path escape attempt and displays `Access denied: path is outside the reports directory`[cite: 5].

### 3. Improper Input Validation (CWE-20)
* **Vulnerable Mode:** Select Option `3` (Register Member) and input invalid names containing special symbols (`Rishi#123!`) or malformed emails[cite: 1].
* **Secure Mode:** Select Option `4` (Register Member) or Option `7` (Calculate Fine)[cite: 5]. Invalid string structures or negative integers are intercepted by `validation.py`[cite: 4, 5].




