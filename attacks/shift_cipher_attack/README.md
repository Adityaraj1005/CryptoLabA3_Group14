# Shift Cipher Cryptanalysis (Lab Assignment 4)

A simple Python project implementing the **Shift (Caesar) Cipher** and two automated cryptanalysis methods to recover secret keys: a **Dictionary Word-Matching Attack** and a **Chi-Square ($\chi^2$) Frequency Attack**.

---

## Directory Hierarchy

```text
attacks/shift_cipher_attack/
├── dictionary/
│   └── english_words.txt
├── src/
│   ├── shift_cipher.py
│   ├── brute_force_dictionary.py
│   ├── chi_square_attack.py
│   └── main.py
└── README.md

File Overviewshift_cipher.pyInput/Output: Text + Key $\rightarrow$ Encrypted/Decrypted TextWhat it does: Encrypts and decrypts text using modulo 26 shift math (x + key) % 26. Punctuation and spaces stay unchanged.english_words.txtWhat it is: A reference file containing common English words used as a cheat-sheet for dictionary lookups.brute_force_dictionary.pyInput/Output: Ciphertext $\rightarrow$ Best Secret Key (Integer)What it does: Tests all 26 shift keys, counts how many real English words appear in each attempt, and picks the key with the highest count.chi_square_attack.pyInput/Output: Ciphertext $\rightarrow$ Best Secret Key (Integer)What it does: Counts individual letters (A–Z) across all 26 shift attempts and uses letter frequency math to pick the key closest to standard English.main.pyWhat it does: The main script that runs test cases through both attacks and prints a table showing if each attack succeeded (YES/NO).How the Attacks Work1. Dictionary AttackDecrypts the ciphertext using every possible key ($K = 0 \dots 25$).Compares the resulting words against english_words.txt.Selects the shift key that produced the most real English words.2. Chi-Square ($\chi^2$) Frequency AttackAnalyzes letter habits across all 26 shifts (in standard English, E is very common, while Q and Z are rare).Calculates the Chi-Square variance score for each shift attempt:$$\chi^2 = \sum_{i=A}^{Z} \frac{(O_i - E_i)^2}{E_i}$$$O_i$ (Observed): How many times letter $i$ actually appeared.$E_i$ (Expected): How many times letter $i$ should appear based on standard English probabilities.Selects the key with the lowest score (closest match to English letter habits).
```


How to Run

First, navigate into the source folder from your terminal:
Bash

```bash
cd attacks/shift_cipher_attack/src
```

1. Run the Full Driver Suite (main.py)

Runs all test cases through both attacks and prints the final verification report:
Bash

```bash
python3 main.py
```

2. Run Cipher Functions directly (shift_cipher.py)

Tests basic encryption and decryption math:
Bash
```bash
python3 shift_cipher.py
```

3. Run Dictionary Attack standalone (brute_force_dictionary.py)

Tests word-matching key recovery on sample text:
Bash

```bash
python3 brute_force_dictionary.py
```

4. Run Chi-Square Attack standalone (chi_square_attack.py)

Tests statistical letter frequency key recovery on sample text:
Bash
```bash
python3 chi_square_attack.py
```
