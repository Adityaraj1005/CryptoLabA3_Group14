# 🛡️ AES-CBC Padding Oracle Attack Module

---

## 📌 Module Overview

This module demonstrates a side-channel **Padding Oracle Attack** against **AES-128-CBC** encryption using **PKCS#7** padding. The attack allows an adversary to decrypt an arbitrary ciphertext block-by-block and byte-by-byte without knowing or accessing the AES secret key.

The implementation models a realistic threat scenario where a server/oracle decrypts submitted ciphertexts and reveals whether the resulting plaintext has valid PKCS#7 padding (e.g., via HTTP 500 error responses or distinct timing side-channels).

---

## 📐 Mathematical & Theoretical Foundation

### 1. AES-CBC Decryption Mechanics
In Cipher Block Chaining (CBC) decryption, ciphertext block $C_i$ is passed through the block cipher decryption function $D_K$ to yield an intermediate byte array $I_i$. $I_i$ is then XORed with the preceding ciphertext block $C_{i-1}$ (or the $\text{IV}$ for $C_1$) to derive plaintext block $P_i$:

$$I_i = D_K(C_i)$$
$$P_i = I_i \oplus C_{i-1}$$

### 2. Exploiting the Padding Oracle
If an attacker alters byte $k$ of $C_{i-1}$ to value $C'_{i-1}[k]$, the corresponding decrypted plaintext byte $P'_i[k]$ becomes:

$$P'_i[k] = I_i[k] \oplus C'_{i-1}[k]$$

By systematically testing values for $C'_{i-1}[k]$ until the Oracle signals **valid PKCS#7 padding** (e.g., target pad byte `0x01`), the intermediate value $I_i[k]$ is isolated:

$$I_i[k] = C'_{i-1}[k] \oplus \text{Target\_Pad}$$

Once $I_i[k]$ is known, the original plaintext byte $P_i[k]$ is recovered using the unmodified original ciphertext byte $C_{i-1}[k]$:

$$I_i[k] = C'_{i-1}[k] \oplus \text{Pad}$$

---

## 🛠️ Algorithmic Implementation Steps

1. **Block Segmentation:** Split input ciphertext into 16-byte blocks $C_1, C_2, \dots, C_n$, prepended with $C_0 = \text{IV}$.
2. **Right-to-Left Traversal:** For target block $C_i$, iterate through byte positions $k = 15$ down to $0$.
3. **Tail Padding Alignment:** For position $k$, compute target padding value $L = 16 - k$. Adjust previously recovered trailing bytes in $C'_{i-1}$ such that $P'_i[j] = L$ for all $j > k$.
4. **Byte Brute-Force:** Iterate $C'_{i-1}[k]$ through all 256 possible byte values (`0x00`–`0xFF`) and query `padding_oracle(C_i, C'_{i-1})`.
5. **False-Positive Mitigation:** If target padding $L = 1$, verify that a single-byte pad `0x01` triggered the valid response (rather than accidental multi-byte padding like `0x02 0x02`) by flipping byte $k-1$ and re-querying.
6. **Plaintext Reconstruction:** Reconstruct $I_i[k]$ and calculate $P_i[k]$. Repeat until all blocks are decrypted, then strip final PKCS#7 padding.

---

## 📂 File Structure

```text
attacks/padding_oracle_attack/
├── README.md               # Detailed module documentation
├── main.py                 # Standalone attack implementation
└── screenshots/            # Verification output screenshots
