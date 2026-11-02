# CryptoLabX Toolkit

**Course:** Cryptography Laboratory (22CPP307)  
**Assignment:** Assignment 1 - Build Your CryptoLabX Toolkit  

---

## 👥 Group Information

* **Group No:** 14
* **Batch:** A3
* **Members:**
  1. **Rishi Yadav** (`2024ucp1601`)
  2. **Adityaraj Shyamsundar Bhandari** (`2024ucp1639`)

---

## 📂 Project Structure

The repository is organized into distinct laboratory modules and attack demonstrations:

```text
CryptoLabA3_Group14/
│
├── analysis/                             # [Lab 6 - Vigenère Cryptanalysis Module]
│   ├── .gitignore
│   ├── README.md
│   ├── ciphertext.txt
│   ├── main.cpp
│   └── screenshots/
│
├── attacks/
│   ├── monoalphabetic_attack/            # [Lab 5 - Monoalphabetic Cipher Attack]
│   │   ├── .gitignore
│   │   ├── README.md
│   │   ├── ciphertext.txt
│   │   ├── plaintext.txt                 # Katz & Lindell (Page 44)
│   │   ├── main.cpp
│   │   └── screenshots/
│   │
│   ├── padding_oracle_attack/            # [Lab 7 - AES-CBC Padding Oracle Attack]
│   │   ├── .gitignore
│   │   ├── README.md
│   │   ├── main.py
│   │   └── screenshots/
│   │
│   └── shift_cipher_attack/              # [Lab 4 - Shift Cipher Attack Module]
│       ├── src/
│       │   ├── shift_cipher.py
│       │   ├── brute_force_dictionary.py
│       │   ├── chi_square_attack.py
│       │   └── main.py
│       ├── dictionary/
│       │   └── english_words.txt
│       ├── testcases/
│       │   └── test.txt
│       ├── outputs/
│       ├── screenshots/
│       ├── reports/
│       │   └── Assignment_4_Report.pdf
│       └── README.md
│
├── maths/                                # [Lab Module - Cryptographic Mathematics]
│   ├── Random_Generator/                 # [Lab 9 - CSPRNG Statistical Analysis]
│   │   ├── screenshots/
│   │   │   └── .gitkeep
│   │   ├── .gitkeep
│   │   ├── README.md
│   │   ├── analyze_randomness.ipynb
│   │   └── generate_random_data.py
│   │
│   └── prime_generation/                 # [Lab 8 - 512-Bit Miller-Rabin Prime Generation]
│       ├── outputs/
│       │   └── experimental_results.txt
│       ├── reports/
│       │   ├── .gitkeep
│       │   └── report.md
│       ├── screenshots/
│       │   ├── .gitkeep
│       │   ├── 100.png
│       │   ├── 101.png
│       │   └── 103.png
│       ├── src/
│       │   ├── main.cpp
│       │   └── README.md
│       └── README.md
│
├── secure_application/                   # [Lab 3 Module]
│   └── src/
│       ├── app.py
│       ├── vulnerable_app.py
│       ├── secure_app.py
│       └── database.py
│
├── classical/                            # [Lab 1 Base Directory]
├── modern/
├── datasets/
├── outputs/
├── docs/
├── tests/
├── utils/
│
├── main.py
├── requirements.txt
└── README.md
