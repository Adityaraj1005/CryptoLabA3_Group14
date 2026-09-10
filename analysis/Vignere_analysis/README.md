# Vigenère Cipher Cryptanalysis (Group 14)

Automated cryptanalysis implementation in C++17 to determine the key length and recover the key/plaintext of a polyalphabetic Vigenère cipher without prior knowledge of the key.

This project was developed for **Group 14** using **Ciphertext-2**.

---

## 📌 Features & Methodology

The cryptanalysis engine breaks the cipher using a two-phase statistical approach:

1. **Preprocessing (`clean_ciphertext`)**: Normalizes input text by removing non-alphabetic characters and converting to uppercase.
2. **Key Length Estimation**:
   - **Kasiski Examination (`find_repeated_patterns`, `calculate_distances`, `find_factors`)**: Scans for repeated trigrams/n-grams, measures index distances, and extracts common factors.
   - **Index of Coincidence Verification (`calculate_ic`, `kasiski_analysis`)**: Computes IC across interleaved stream candidate lengths ($M$) to confirm when streams shift from polyalphabetic ($\text{IC} \approx 0.038$) to monoalphabetic ($\text{IC} \approx 0.067$).
3. **Key & Plaintext Recovery**:
   - **Group Splitting (`split_into_groups`)**: Divides ciphertext into $M$ independent Caesar cipher streams.
   - **Chi-Square Minimization (`frequency_analysis`, `find_shift`)**: Performs letter frequency analysis on each group to identify individual character shifts.
   - **Decryption (`find_key`, `vigenere_decrypt`)**: Assembles the shifts into the keyword and decrypts the text.
4. **Verification (`vigenere_encrypt`, `verify`)**: Re-encrypts the recovered plaintext with the recovered key to guarantee a 100% exact match against the original ciphertext.

---

## 📁 Repository Structure

```text
analysis/Vignere_analysis/
├── .gitignore
├── README.md
├── ciphertext.txt
├── main.cpp
└── screenshots/


🛠️ Build & Run Instructions
# Navigate to the directory
cd analysis/Vignere_analysis

# Compile the C++ program using C++17
g++ -std=c++17 main.cpp -o vigenere_attack

# Execute the binary
./vigenere_attack
