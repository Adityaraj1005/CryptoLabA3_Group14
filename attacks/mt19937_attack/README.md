# MT19937 Stream Cipher & Predictable Token Attack (Lab 10)

## Overview
This module demonstrates the severe cryptographic vulnerabilities of non-cryptographic PRNGs using **Mersenne Twister (MT19937)**. It covers two attack vectors:
1. **Part A:** Known-Plaintext Attack (KPA) and 16-bit seed brute-force on an MT19937 stream cipher.
2. **Part B:** Time-based seed recovery on predictable password reset tokens generated within a $\pm 300$ second window.

---

## How to Run

### Run Part A (Stream Cipher Seed Recovery):
```bash
python part_a_stream_cipher.py
```
```bash
python part_b_token_prediction.py
```
