# Shift Cipher Cryptanalysis (Lab Assignment 4)

A complete Python implementation of the classic **Shift (Caesar) Cipher** along with two automated cryptanalysis engines to break secret keys without prior knowledge: a **Dictionary Word-Matching Attack** and a **Chi-Square ($\chi^2$) Letter Frequency Attack**.

---

**Directory Hierarchy**

attacks/shift_cipher_attack/
├── dictionary/
│   └── english_words.txt
├── src/
│   ├── shift_cipher.py
│   ├── brute_force_dictionary.py
│   ├── chi_square_attack.py
│   └── main.py
└── README.md

```markdown
# Shift Cipher Cryptanalysis (Lab Assignment 4)

A complete Python implementation of the classic **Shift (Caesar) Cipher** along with two automated cryptanalysis engines to break secret keys without prior knowledge: a **Dictionary Word-Matching Attack** and a **Chi-Square ($\chi^2$) Letter Frequency Attack**.

---

**Directory Hierarchy**


```

attacks/shift_cipher_attack/
├── dictionary/
│   └── english_words.txt
├── src/
│   ├── shift_cipher.py
│   ├── brute_force_dictionary.py
│   ├── chi_square_attack.py
│   └── main.py
└── README.md

```

---

**Module Breakdown**

| File | Module Type | Input $\rightarrow$ Output | How It Works |
| :--- | :--- | :--- | :--- |
| `shift_cipher.py` | Cipher Engine | Text + Key $\rightarrow$ Ciphertext String | Converts characters to numbers (0–25), applies shift key using modulo 26 math `(x + k) % 26`, and converts back to ASCII. |
| `english_words.txt` | Word Dataset | Reference Text File | Contains common uppercase English words line-by-line to act as a reference cheat-sheet for dictionary lookups. |
| `brute_force_dictionary.py` | Rule-Based Attack | Ciphertext $\rightarrow$ Key Integer | Tests all 26 shift keys, splits decrypted candidates into words, and selects the key yielding the highest count of real English words. |
| `chi_square_attack.py` | Statistical Attack | Ciphertext $\rightarrow$ Key Integer | Measures letter distributions against standard English frequencies across all 26 keys. Selects the key with the smallest deviation. |
| `main.py` | Test Driver | Test Cases $\rightarrow$ Terminal Table | Encrypts test sentences, passes ciphertext to both attack scripts, and prints verification results (`YES`/`NO`). |

---

**Cryptanalysis Logic Simplified**

**1. Dictionary Attack (Word Counter)**
* Decrypts ciphertext with keys $K = 0 \dots 25$.
* Counts how many words in each attempt exist inside `english_words.txt`.
* **Selection:** Key with the **highest match count** wins.

**2. Chi-Square Frequency Attack (Letter Detective)**
* Evaluates letter frequencies against standard English probabilities ('E' $\approx 12.7\%$, 'Z' $\approx 0.07\%$).
* Computes the formula for all 26 shift attempts:

$$\chi^2 = \sum_{i=A}^{Z} \frac{(O_i - E_i)^2}{E_i}$$

* **$O_i$ (Observed):** Actual count of letter $i$ in decrypted candidate text.
* **$E_i$ (Expected):** Expected count of letter $i$ in standard English for a text of that length.
* **Selection:** Key with the **lowest $\chi^2$ score** (closest match to English letter distributions) wins.

---

**How to Run**

Run the project driver directly from your terminal:

```bash
# Run from inside src directory:
python3 main.py

# Or run from the repository root:
python3 attacks/shift_cipher_attack/src/main.py

```

```

```
