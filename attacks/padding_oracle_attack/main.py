import os
from typing import Tuple
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# =====================================================================
# 1. SIMULATED ORACLE & ENVIRONMENT SETUP
# =====================================================================
SECRET_KEY = os.urandom(16)  # 128-bit AES Key

def encrypt_sample_text(plaintext_str: str) -> Tuple[bytes, bytes]:
    """Helper function to encrypt a sample plaintext using AES-CBC with PKCS#7 padding."""
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext_str.encode('utf-8')) + padder.finalize()
    
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    return ciphertext, iv

def padding_oracle(ciphertext: bytes, iv: bytes) -> bool:
    """
    Padding Oracle Function:
    Decrypts ciphertext and checks if the PKCS#7 padding is valid.
    Returns True if valid, False if invalid.
    """
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Manual PKCS#7 padding check
    pad_len = padded_plaintext[-1]
    if pad_len < 1 or pad_len > 16:
        return False
    return padded_plaintext[-pad_len:] == bytes([pad_len]) * pad_len


# =====================================================================
# 2. PADDING ORACLE ATTACK IMPLEMENTATION
# =====================================================================
def attack_block(target_block: bytes, prev_block: bytes) -> Tuple[bytes, int]:
    """
    Recovers 16 bytes of plaintext for target_block using prev_block.
    """
    intermediate = bytearray(16)
    recovered_plaintext = bytearray(16)
    query_count = 0

    # Process block from right to left (byte 15 down to 0)
    for byte_idx in range(15, -1, -1):
        target_pad = 16 - byte_idx
        modified_prev = bytearray(16)

        # Set already recovered trailing bytes to match target_pad
        for i in range(byte_idx + 1, 16):
            modified_prev[i] = intermediate[i] ^ target_pad

        found = False
        for val in range(256):
            modified_prev[byte_idx] = val
            query_count += 1

            # Send modified preceding block + target block to the oracle
            if padding_oracle(bytes(target_block), bytes(modified_prev)):
                # Handle edge case where natural padding matches higher values
                if target_pad == 1 and byte_idx > 0:
                    check_prev = bytearray(modified_prev)
                    check_prev[byte_idx - 1] ^= 0xFF
                    query_count += 1
                    if not padding_oracle(bytes(target_block), bytes(check_prev)):
                        continue
                
                intermediate[byte_idx] = val ^ target_pad
                recovered_plaintext[byte_idx] = intermediate[byte_idx] ^ prev_block[byte_idx]
                found = True
                break

        if not found:
            raise RuntimeError(f"Failed to recover byte at index {byte_idx}")

    return bytes(recovered_plaintext), query_count


def execute_attack(ciphertext: bytes, iv: bytes) -> Tuple[str, int]:
    """
    Splits ciphertext into blocks and decrypts each block byte-by-byte.
    """
    blocks = [iv] + [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    full_plaintext = bytearray()
    total_queries = 0

    print("\n[+] Starting Padding Oracle Attack...")
    for i in range(1, len(blocks)):
        pt_block, queries = attack_block(blocks[i], blocks[i-1])
        full_plaintext.extend(pt_block)
        total_queries += queries
        print(f"    Block {i}/{len(blocks)-1} Decrypted ({queries} queries)")

    # Strip PKCS#7 padding from recovered bytes
    pad_len = full_plaintext[-1]
    unpadded_plaintext = full_plaintext[:-pad_len]

    return unpadded_plaintext.decode('utf-8', errors='ignore'), total_queries


# =====================================================================
# 3. MAIN RUNNER
# =====================================================================
if __name__ == "__main__":
    sample_plaintext = "Group 14 Cryptography Lab: Padding Oracle Attack Demo!"
    
    print("=" * 65)
    print("      AES-CBC PADDING ORACLE ATTACK DEMONSTRATION")
    print("=" * 65)
    print(f"[*] Original Plaintext: '{sample_plaintext}'")
    
    # Encrypt target plaintext
    ciphertext, iv = encrypt_sample_text(sample_plaintext)
    print(f"[*] Ciphertext Length : {len(ciphertext)} bytes ({len(ciphertext)//16} blocks)")
    print(f"[*] IV                : {iv.hex()}")
    print(f"[*] Ciphertext Hex    : {ciphertext.hex()}")

    # Execute attack without passing SECRET_KEY
    recovered_text, total_oracle_queries = execute_attack(ciphertext, iv)

    print("\n" + "=" * 65)
    print("                      ATTACK RESULTS")
    print("=" * 65)
    print(f"[+] Recovered Plaintext    : '{recovered_text}'")
    print(f"[+] Total Oracle Queries   : {total_oracle_queries}")
    print(f"[+] Decryption Successful  : {recovered_text == sample_plaintext}")
    print("=" * 65)
