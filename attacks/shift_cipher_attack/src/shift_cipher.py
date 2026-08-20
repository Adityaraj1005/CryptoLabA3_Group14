def encrypt(plaintext, key):
    ciphertext = ""
    
    for char in plaintext.upper():
        if char.isalpha():
            # Convert letter 'A'-'Z' to range 0-25
            ascii_code = ord(char) - 65
            # Apply shift key with modulo 26 wrap-around
            shifted_code = (ascii_code + key) % 26
            # Convert back to character
            new_char = chr(shifted_code + 65)
            ciphertext += new_char
        else:
            # Leave spaces and punctuation unchanged
            ciphertext += char
            
    return ciphertext

def decrypt(ciphertext, key):
    # Decryption is just shifting backward by key
    return encrypt(ciphertext, -key)
    
if __name__ == "__main__":
    text = "THE QUICK BROWN FOX"
    key = 7
    
    cipher = encrypt(text, key)
    plain = decrypt(cipher, key)
    
    print("Original  :", text)
    print("Encrypted :", cipher)
    print("Decrypted :", plain)
