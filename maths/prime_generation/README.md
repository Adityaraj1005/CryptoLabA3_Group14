# Miller–Rabin Prime Generation

## Objective
Generate a probable prime of exactly 512 bits using a student-implemented Miller–Rabin primality test, then perform an additional primality check using OpenSSL.

## Files
- `outputs/experimental_results.txt` — recorded Miller–Rabin run and fields to complete after running OpenSSL verification.
- `reports/report.md` — report draft for the assignment.
- `screenshots/README.txt` — guidance for the screenshots to include.

## Build and run
From the directory containing `assign8.cpp`:

```bash
g++ assign8.cpp -o assign8 -std=c++17 -lcrypto
./assign8
```

This links the program with OpenSSL's crypto library. The source uses `BN_is_prime_ex()`, which is available in OpenSSL 1.1.1. The function is deprecated in OpenSSL 3.x, where `BN_check_prime()` is preferred.
