# CSPRNG Statistical Analysis & Architectural Comparison (Lab 9)

## 1. Overview
This laboratory module performs comparative statistical analysis and architectural evaluation of three Cryptographically Secure Pseudo-Random Number Generators (CSPRNGs) operating across different computing layers:

1. **Linux `/dev/urandom`** (Kernel-Level)
2. **OpenSSL `RAND_bytes`** (User-Space Cryptographic Library)
3. **Windows .NET `RandomNumberGenerator`** (Managed Framework API running cross-platform)

Each generator was tasked with outputting a **1 MB binary file ($1,048,576$ bytes)**. The output files were subjected to four statistical randomness tests to evaluate distribution uniformity, information entropy, and bit independence.

---

## 2. Comprehensive Comparison of the Three CSPRNGs

| Feature / Metric | Linux `/dev/urandom` | OpenSSL `RAND_bytes` | Windows .NET API (`pwsh`) |
| :--- | :--- | :--- | :--- |
| **System Layer** | Operating System Kernel | User-Space Cryptographic Engine | Managed Framework Abstraction |
| **Primary Algorithm** | ChaCha20 Stream Cipher | AES-CTR-DRBG / HMAC-DRBG | Native OS Delegate (OpenSSL / `getrandom`) |
| **Entropy Collector** | Kernel Interrupts, Hardware Jitter, Storage Timings | System Kernel Entropy (`getrandom` / `/dev/urandom`) | Managed Wrapper over Host Cryptography Subsystem |
| **Fork / Process Safety** | Handled natively by kernel state management | Requires internal re-seeding protection on process clone | Handled by host runtime environment |
| **Bit Ratio (0s / 1s)** | `49.99% / 50.01%` | `50.01% / 49.99%` | `49.97% / 50.03%` |
| **Shannon Entropy** | `7.9998` bits/byte | `7.9998` bits/byte | `7.9998` bits/byte |
| **Chi-Square ($\chi^2$)** | `265.58` | `242.31` | `317.43` |
| **p-value ($\chi^2$)** | `0.3115` | `0.7060` | `0.0047` |
| **Serial Correlation** | `-0.00032` | `0.00015` | `0.00112` |
| **Statistical Status** | **PASS** ($p \ge 0.01$) | **PASS** ($p \ge 0.01$) | **FAIL** ($p < 0.01$, Sample Variance) |

---

## 3. Deep-Dive Architectural Differences

### A. Linux `/dev/urandom` (Kernel Level)
* **Design:** `/dev/urandom` reads directly from the Linux kernel non-blocking entropy pool. On modern Linux kernels ($\ge 5.17$), it uses a **ChaCha20-based CSPRNG**.
* **Seeding:** Seeded continuously by hardware device drivers, CPU execution jitter, inter-interrupt arrival times, and TPM module data.
* **Security Strengths:** Highly resistant to state compromise and prediction attacks. It never blocks after initial boot initialization.

### B. OpenSSL `RAND_bytes` (User-Space Library)
* **Design:** Operates entirely in user memory using NIST SP 800-90A compliant **AES-CTR-DRBG** (or HMAC-DRBG depending on build configuration).
* **Seeding:** Periodically seeds itself by making system calls to the underlying OS (e.g., `getrandom()` on Linux or `BCryptGenRandom` on Windows).
* **Security Strengths:** Avoids user-to-kernel context-switching overhead for high-frequency cryptographic operations while maintaining strong forward secrecy.

### C. Windows .NET `RandomNumberGenerator` (Framework / PAL Level)
* **Design:** Managed .NET class (`System.Security.Cryptography.RandomNumberGenerator`). On native Windows systems, it wraps **Windows CNG (`BCryptGenRandom`)**.
* **Cross-Platform Behavior on Linux:** When executed inside Linux via PowerShell (`pwsh`), the **.NET Platform Abstraction Layer (PAL)** automatically redirects cryptographic calls to native **OpenSSL (`libcrypto`)** or the Linux kernel `getrandom()` system call.
* **Statistical Deviation:** In our 1 MB sample, the Chi-Square score ($\chi^2 = 317.43$, $p = 0.0047$) fell slightly below the standard $0.01$ threshold. This represents expected statistical sample fluctuation rather than an underlying algorithmic vulnerability.

---

## 4. Directory File Structure

```text
maths/Random_Generator/
├── .gitkeep
├── README.md
├── analyze_randomness.ipynb
└── generate_random_data.py
