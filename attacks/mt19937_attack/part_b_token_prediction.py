import random
import time

def generate_reset_token(timestamp: int) -> str:
    """
    Seeds MT19937 with Unix timestamp, generates 16 bytes,
    and returns a 32-character hexadecimal string token.
    """
    rng = random.Random(timestamp)
    token_bytes = bytes(rng.getrandbits(8) for _ in range(16))
    return token_bytes.hex()

def predict_token(target_token: str, approx_time: int, window: int = 300):
    """
    Searches candidate timestamps in range [approx_time - window, approx_time + window].
    Returns matched timestamp, candidate token, and candidate count.
    """
    start_time = approx_time - window
    end_time = approx_time + window
    total_tested = 0

    print(f"[*] Searching timestamp interval: [{start_time} to {end_time}]")
    print(f"[*] Total candidate seeds to test: {end_time - start_time + 1}")

    for candidate_time in range(start_time, end_time + 1):
        total_tested += 1
        candidate_token = generate_reset_token(candidate_time)
        if candidate_token == target_token:
            return candidate_time, candidate_token, total_tested

    return None, None, total_tested

if __name__ == "__main__":
    print("=" * 60)
    print("  LAB 10 - PART B: PREDICTABLE PASSWORD RESET TOKEN ATTACK")
    print("=" * 60)

    # 1. Simulated Victim Token Generation
    real_timestamp = int(time.time())
    generated_token = generate_reset_token(real_timestamp)

    print(f"[+] Real Generation Time (T) : {real_timestamp} Unix seconds")
    print(f"[+] Intercepted Reset Token  : {generated_token}")
    print("-" * 60)

    # 2. Attacker Setup (Assumes token created within T - 300 to T + 300)
    attacker_time_estimate = real_timestamp + random.randint(-50, 50) # Simulated offset
    search_window = 300 # ±300 seconds

    # 3. Predict / Recover Timestamp
    recovered_time, rec_token, tests_run = predict_token(
        generated_token, attacker_time_estimate, search_window
    )

    # 4. Verification
    print("-" * 60)
    print(f"[+] Total Timestamps Tested  : {tests_run}")
    if recovered_time:
        print(f"[✓] RECOVERED TIMESTAMP      : {recovered_time}")
        print(f"[✓] REGENERATED TOKEN        : {rec_token}")
        
        # Re-verify
        verification_check = generate_reset_token(recovered_time)
        if verification_check == generated_token and recovered_time == real_timestamp:
            print("[✓] VERIFICATION SUCCESS     : Recovered timestamp reproduces exact token!")
    else:
        print("[X] Attack failed: Token not found in search window.")
