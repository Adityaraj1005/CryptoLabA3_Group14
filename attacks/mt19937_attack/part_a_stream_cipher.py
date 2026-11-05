import random

def mt19937_keystream(seed: int, length: int) -> bytes:
    """
    Generates a keystream of 'length' bytes using MT19937 seeded with 'seed'.
    Extracts 8-bit values (byte by byte) from Python's inbuilt random module.
    """
    rng = random.Random(seed)
    # Generate 8-bit bytes from MT19937
    return bytes(rng.getrandbits(8) for _ in range(length))

def encrypt_decrypt(data: bytes, seed: int) -> bytes:
    """XORs input data with the generated MT19937 keystream."""
    keystream = mt19937_keystream(seed, len(data))
    return bytes(b ^ k for b, k in zip(data, keystream))

def generate_target_plaintext() -> bytes:
    """Generates random prefix (5-20 chars) + 14 consecutive 'A's."""
    prefix_len = random.randint(5, 20)
    # Printable ASCII range (excluding whitespace for clean output)
    prefix = "".join(chr(random.randint(33, 126)) for _ in range(prefix_len))
    known_pattern = "AAAAAAAAAAAAAA"
    return (prefix + known_pattern).encode('utf-8')

def brute_force_16bit_seed(ciphertext: bytes, known_sequence: bytes):
    """
    Brute-forces all 2^16 (65,536) seeds to find a match 
    containing the known sequence in decrypted plaintext.
    """
    print("[*] Starting Brute-Force Attack on 16-bit seed space (0 to 65535)...")
    matches = []
    
    for candidate_seed in range(65536):
        decrypted = encrypt_decrypt(ciphertext, candidate_seed)
        if known_sequence in decrypted:
            matches.append((candidate_seed, decrypted))
            
    return matches

if __name__ == "__main__":
    print("=" * 60)
    print("      LAB 10 - PART A: MT19937 STREAM CIPHER ATTACK")
    print("=" * 60)

    # 1. Setup Plaintext & Secret Seed
    target_plaintext = generate_target_plaintext()
    secret_seed = random.randint(0, 65535)  # 16-bit seed
    
    print(f"[+] Generated Plaintext  : {target_plaintext.decode('utf-8')}")
    print(f"[+] Secret 16-bit Seed   : {secret_seed} (0x{secret_seed:04X})")

    # 2. Encrypt
    ciphertext = encrypt_decrypt(target_plaintext, secret_seed)
    print(f"[+] Ciphertext (Hex)     : {ciphertext.hex()}")
    print("-" * 60)

    # 3. Known Plaintext Attack (KPA) Brute Force
    known_seq = b"AAAAAAAAAAAAAA"
    recovered_matches = brute_force_16bit_seed(ciphertext, known_seq)

    # 4. Verification
    print(f"[+] Total Seeds Tested   : 65536")
    print(f"[+] Candidate Matches    : {len(recovered_matches)}")
    
    for rec_seed, rec_plaintext in recovered_matches:
        print(f"\n[✓] RECOVERED SEED       : {rec_seed}")
        print(f"[✓] RECOVERED PLAINTEXT  : {rec_plaintext.decode('utf-8')}")
        
        if rec_seed == secret_seed and rec_plaintext == target_plaintext:
            print("[✓] VERIFICATION SUCCESS : Recovered seed & plaintext match original!")
