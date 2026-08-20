from shift_cipher import decrypt

# Standard English letter frequencies from A to Z
ENGLISH_FREQ = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
    0.00978, 0.02360, 0.00150, 0.01974, 0.00074
]

def chi_square_attack(ciphertext):
    best_key = 0
    lowest_chi_square = 999999999.0

    # Try all 26 keys
    for key in range(26):
        decrypted_text = decrypt(ciphertext, key)
        
        # Collect only alphabetic letters
        letters = []
        for char in decrypted_text.upper():
            if char.isalpha():
                letters.append(char)
        
        total_letters = len(letters)
        if total_letters == 0:
            continue

        chi_square_score = 0.0
        
        # Calculate Chi-Square formula for each letter A-Z
        for i in range(26):
            letter = chr(i + 65)  # 0 -> 'A', 1 -> 'B', etc.
            observed_count = letters.count(letter)
            expected_count = total_letters * ENGLISH_FREQ[i]
            
            # Formula: (Observed - Expected)^2 / Expected
            diff = observed_count - expected_count
            chi_square_score += (diff * diff) / expected_count

        # The key with lowest Chi-Square score matches standard English best
        if chi_square_score < lowest_chi_square:
            lowest_chi_square = chi_square_score
            best_key = key

    return best_key
