# CSPRNG Statistical Analysis Module (Lab 9)

## Overview
This module evaluates three Cryptographically Secure Pseudo-Random Number Generators (CSPRNGs) operating at different architectural levels:
1. **Kernel Level:** Linux `/dev/urandom` (ChaCha20 stream cipher backed by hardware/system noise)
2. **User-Space Library:** OpenSSL `RAND_bytes` (AES-CTR-DRBG / HMAC-DRBG)
3. **Managed Application Framework:** Windows .NET `RandomNumberGenerator` (Executed via PowerShell `pwsh` on Linux, delegating to native OpenSSL / kernel `getrandom()`)

Each source generated a **1 MB binary file (1,048,576 bytes)**, which was evaluated across four statistical metrics to test distribution, entropy, and independence.

---

## Directory Structure
```text
maths/Random_Generator/
├── screenshots/
│   └── .gitkeep
├── .gitkeep
├── README.md
├── analyze_randomness.ipynb
└── generate_random_data.py
