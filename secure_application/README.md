
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


    📂 Directory Structure
Plaintext

secure_application/
├── src/                     # Source code (Library Management System)
│   └── app.py               # Main vulnerable application logic
├── reports/                 # SAST analysis scan reports (PDF/JSON/Text)
├── screenshots/             # Screenshots of execution and exploits
├── sast/                    # SAST configuration rules (e.g., semgrep.yml)
├── outputs/                 # Application outputs (e.g., library.db)
├── testcases/               # Test inputs and exploit payloads
└── README.md                # Application documentation



🚀 How to Run the Application



🧪 Testing the Vulnerabilities
