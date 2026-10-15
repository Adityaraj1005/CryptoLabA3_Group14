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

## Before submitting
1. Run the program after compiling it with `-lcrypto`.
2. Copy the actual OpenSSL verification result and the new run's timing/candidate counts into `outputs/experimental_results.txt`.
3. Save screenshots of compilation and the final output in `screenshots/`.
4. Check that the report's recorded values match the run you are submitting.

A successful OpenSSL check is an independent implementation check, but it is still probabilistic rather than a formal mathematical proof of primality.
