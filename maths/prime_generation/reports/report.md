# Lab Report: Cryptographic Prime Generation Using Miller–Rabin

## 1. Objective
To generate a probable prime of exactly 512-bit length using the Miller–Rabin primality test and perform an additional verification using OpenSSL.

## 2. Algorithm
1. Generate an odd candidate with the requested bit length.
2. Decompose `n - 1` into `2^s × d`, where `d` is odd.
3. For each Miller–Rabin round, select a base `a` and calculate `x = a^d mod n`.
4. If `x` is neither `1` nor `n - 1`, repeatedly square `x` modulo `n` for that same base.
5. If a candidate fails, discard it and generate another candidate.
6. When a candidate passes all configured rounds, check its bit length and test it using OpenSSL's separate implementation.

## 3. Implementation
The candidate generation and Miller–Rabin test are implemented in C++ using Boost Multiprecision (`cpp_int`). Independent checking is performed using OpenSSL's `BN_is_prime_ex()` function, compatible with the OpenSSL 1.1.1f version reported for this system.

## 4. Experimental results
Fill this section using the output from the **updated program**:
- Assigned bit length: 512
- Generated candidate: [copy from updated program]
- Actual bit length: [copy from updated program]
- Number of candidates tested: [copy from updated program]
- Miller–Rabin rounds: [copy from updated program]
- Execution time: [copy from updated program]
- Miller–Rabin result: [copy from updated program]
- OpenSSL independent check: [copy actual result from updated program]

The earlier run recorded in `../outputs/experimental_results.txt` was obtained before OpenSSL verification was added. Do not present its timing as the timing of the updated program.

## 5. Independent verification
The program converts the candidate to a decimal string, imports it into an OpenSSL `BIGNUM`, and calls `BN_is_prime_ex()` with 20 requested checks. The result is independent of the student's own Miller–Rabin function because it is provided by a separate library implementation.

Interpretation:
- Return value `1`: OpenSSL considers the number probably prime.
- Return value `0`: OpenSSL reports the number is composite.
- Negative return value: verification error.

This is an independent implementation check, not a formal mathematical proof of primality.

## 6. Conclusion
Complete this paragraph after running the updated program:

“The program generated a candidate with an actual bit length of [value] bits. It [passed/did not pass] the configured Miller–Rabin rounds. OpenSSL's independent check [passed/failed/returned an error]. Therefore, the result [satisfies/does not yet satisfy] the assignment's verification requirements.”

## 7. Screenshots
Include screenshots of:
1. Successful compilation with `-lcrypto`.
2. The complete output from the updated program.
3. The OpenSSL verification result.
