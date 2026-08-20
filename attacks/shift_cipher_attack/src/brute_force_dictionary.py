import os
from shift_cipher import decrypt

def load_dictionary(filepath):
    words = set()
    
    if os.path.exists(filepath):
        file = open(filepath, "r")
        for line in file:
            clean_word = line.strip().upper()
            if clean_word != "":
                words.add(clean_word)
        file.close()
    else:
        # Simple fallback dictionary if file is missing
        words = {"THE", "QUICK", "BROWN", "FOX", "ATTACK", "DAWN", "BAD"}
        
    return words

def dictionary_attack(ciphertext, dict_path):
    dictionary = load_dictionary(dict_path)
    best_key = 0
    max_words_found = -1

    # Try all 26 possible shift keys
    for key in range(26):
        decrypted_text = decrypt(ciphertext, key)
        words_in_text = decrypted_text.split()
        
        match_count = 0
        for word in words_in_text:
            # Remove non-alphabet characters from the word
            clean_word = ""
            for letter in word:
                if letter.isalpha():
                    clean_word += letter.upper()
            
            # Check if cleaned word exists in English dictionary
            if clean_word in dictionary:
                match_count += 1

        # Keep track of key with highest English word matches
        if match_count > max_words_found:
            max_words_found = match_count
            best_key = key

    return best_key
