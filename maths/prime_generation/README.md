# Miller–Rabin Prime Generation

## Objective
Generate a probable prime with exactly 512 bits using the Miller–Rabin primality test. A candidate that fails the test is discarded, and a new odd 512-bit candidate is generated until one passes all configured rounds.

## Contents
- `outputs/experimental_results.txt` — results from one recorded run.
- `screenshots/` — place screenshots showing compilation, program output, and verification here.
- `reports/report_template.md` — a short report template you can complete for submission.

## Build and run
Run these commands from the root of the `CryptoLabA3_Group14` project, assuming the C++ source is saved at `math/prime_generation/src/main.cpp`:

```bash
g++ math/prime_generation/src/main.cpp -o math/prime_generation/prime -std=c++17
./math/prime_generation/prime
```

The program uses Boost Multiprecision (`boost::multiprecision::cpp_int`) for large integer arithmetic. Boost headers must be installed and available to the compiler.

## Important verification note
Passing 20 Miller–Rabin rounds means the candidate is a *probable prime*, not a mathematical proof of primality. The output `Passes Miller-Rabin: 1` means the Boolean result is true. If the program reruns the test using newly generated bases, that is a repeat Miller–Rabin check—not an independent verification method.

For the assignment's independent-check requirement, verify the resulting number separately with a trusted implementation, such as OpenSSL's primality-checking API or a separate tool/library approved by your instructor. Record the method and result in your report.

## Experimental results
The values in `outputs/experimental_results.txt` are from one run and are not expected to remain the same on future runs. Update that file whenever you choose to submit results from a new run.
