Group No-14
Batch-A3
Members:->
1.)Rishi Yadav-2024ucp1601
2.)Adityaraj Shyamsundar Bhandari-2024ucp1639

**Course:** Cryptography Laboratory (22CPP307)  
**Assignment:** Assignment 1- Build Your CryptoLabX Toolkit

## 📂 Project Structure

The repository is organized to support future cryptographic implementations and attacks:

```text
CryptoLabA3_Group14/
│
├── analysis/
│   └── Vignere_analysis/           # [Lab 3 - Vigenère Cryptanalysis Module]
│       ├── .gitignore
│       ├── README.md
│       ├── ciphertext.txt
│       ├── main.cpp
│       └── screenshots/
│
├── attacks/
│   ├── monoalphabetic_attack/      # [Lab 4 - Monoalphabetic Cipher Attack]
│   │   ├── .gitignore
│   │   ├── README.md
│   │   ├── ciphertext.txt
│   │   ├── plaintext.txt           # Katz & Lindell (Page 44)
│   │   ├── main.cpp
│   │   └── screenshots/
│   │
│   └── shift_cipher_attack/        # [Lab 4 - Shift Cipher Attack Module]
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
├── secure_application/             # [Lab 3 Module]
│   └── src/
│       ├── app.py
│       ├── vulnerable_app.py
│       ├── secure_app.py
│       └── database.py
│
├── classical/                      # [Lab 1 Base Directory]
├── math/
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
