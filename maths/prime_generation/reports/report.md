# Lab Report: Cryptographic Prime Generation Using Miller–Rabin

## 1. Objective
Generate a probable prime of exactly 512-bit length using the Miller–Rabin primality test.

## 2. Algorithm summary
1. Generate a random 512-bit odd candidate.
2. Write `n - 1` as `2^s × d`, where `d` is odd.
3. For each Miller–Rabin round, choose a base `a` and compute `x = a^d mod n`.
4. If `x` is neither `1` nor `n - 1`, repeatedly square `x` modulo `n` for that same base.
5. If the candidate fails a round, discard it and generate another candidate.
6. Stop when a candidate passes all configured rounds, then check its bit length and verify it independently.

## 3. Experimental results
Copy the final run's values from `../outputs/experimental_results.txt`. Include the candidate, actual bit length, number of candidates tested, rounds, execution time, and bases used.

## 4. Independent verification
- Tool/library used:
- Version:
- Exact command or API:
- Result:
- Date of verification:

Use a trusted, separate primality checker. Do not describe a second run of the same Miller–Rabin function as independent verification.

## 5. Discussion
Explain why failed candidates are discarded, why the top bit is set to ensure 512-bit length, why the lowest bit is set to ensure an odd candidate, and why multiple Miller–Rabin rounds reduce the chance of accepting a composite number.

## 6. Conclusion
State whether the generated candidate had exactly 512 bits, whether it passed all configured Miller–Rabin rounds, and whether the separate independent check succeeded.
