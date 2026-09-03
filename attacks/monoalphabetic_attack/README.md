# Monoalphabetic Substitution Cipher Cryptanalysis Tool

A C++17 command-line tool designed for frequency analysis, interactive cryptanalysis, and mathematical key verification of Monoalphabetic Substitution Ciphers. Developed to satisfy academic lab requirements for a ~600-word ciphertext dataset (*Introduction to Modern Cryptography*, Katz & Lindell, p. 44).

---

## Repository Structure

```text
CryptoLabA3_Group14/
│
├── .gitignore
├── README.md
│
├── src/
│   ├── main.cpp            # Primary application driver & terminal interface
│   ├── cryptanalysis.cpp   # Statistical engines & verification logic
│   └── cryptanalysis.h     # Function prototypes & data structures
│
└── data/
    ├── katz_lindell_p44.txt # Dataset plaintext file
    └── keymap.txt           # Substitution key database file
