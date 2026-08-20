import os
from shift_cipher import encrypt
from brute_force_dictionary import dictionary_attack
from chi_square_attack import chi_square_attack

# Simple path lookup for dictionary
if os.path.exists("english_words.txt"):
    dict_path = "english_words.txt"
else:
    dict_path = "../dictionary/english_words.txt"

def run_experiments():
    test_cases = [
        ("THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG", 7),
        ("ATTACK AT DAWN UNLESS WEATHER IS BAD AND RAIN CONTINUES", 19),
        ("CRYPTOGRAPHY IS THE PRACTICE AND STUDY OF SECURE COMMUNICATION", 12),
        ("INFORMATION SECURITY AND CRYPTANALYSIS ARE ESSENTIAL SUBJECTS", 5)
    ]

    print("\n=======================================================")
    print("      ASSIGNMENT 4: SHIFT CIPHER EXPERIMENTS")
    print("=======================================================")

    for text, actual_key in test_cases:
        # Step 1: Encrypt text
        ciphertext = encrypt(text, actual_key)
        
        # Step 2: Run both attacks
        dict_key = dictionary_attack(ciphertext, dict_path)
        chi_key = chi_square_attack(ciphertext)
        
        # Step 3: Check if predictions match actual key
        if dict_key == actual_key:
            dict_status = "YES"
        else:
            dict_status = "NO"
            
        if chi_key == actual_key:
            chi_status = "YES"
        else:
            chi_status = "NO"

        # Step 4: Display results clearly
        print("\nPlaintext :", text[:35])
        print("True Key  :", actual_key)
        print("Dict Key  :", dict_key, "| Correct?", dict_status)
        print("Chi2 Key  :", chi_key, "| Correct?", chi_status)

    print("\n=======================================================\n")

if __name__ == "__main__":
    run_experiments()
