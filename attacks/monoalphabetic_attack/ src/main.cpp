
#include <bits/stdc++.h>
#include "cryptanalysis.h"

using namespace std;

int main() {
    ifstream file("katz_lindell_p44.txt");
    if (!file.is_open()) {
        cerr << "Error: Could not open dataset file katz_lindell_p44.txt\n";
        return 1;
    }

    stringstream buffer;
    buffer << file.rdbuf();
    string plaintext = buffer.str();
    file.close();

    string random_key = generate_random_key();
    string ciphertext = encrypt_monoalphabetic(plaintext, random_key);

    cout << "=======================================================\n";
    cout << "          MONOALPHABETIC CRYPTANALYSIS MODULE          \n";
    cout << "=======================================================\n";
    cout << "\n[Generated Ciphertext Snippet]:\n" << ciphertext.substr(0, 200) << "...\n";

    frequency_analysis(ciphertext);
    word_frequency_analysis(ciphertext);
    pattern_analysis(ciphertext);

    map<char, char> key_map;

    ifstream keyfile("keymap.txt");
    if (keyfile.is_open()) {
        char c, p;
        while (keyfile >> c >> p) {
            key_map[toupper(c)] = tolower(p);
        }
        keyfile.close();
        cout << "\n[INFO] Loaded " << key_map.size() << " character mappings from keymap.txt\n";
    }

    char cipher_char, plain_char;
    int choice;

    while (true) {
        string partial = apply_substitution(ciphertext, key_map);

        cout << "\nCurrent Mappings (" << key_map.size() << "/26): ";
        for (const auto& p : key_map) cout << p.first << "->" << p.second << " ";
        cout << "\n\nOptions:\n1. Add/Update Mapping\n2. Remove Mapping\n3. Verify Solution & Display Full Report\n4. Exit\nChoice: ";
        if (!(cin >> choice)) break;

        if (choice == 1) {
            cout << "Enter Ciphertext char (Uppercase) and Plaintext replacement (Lowercase): ";
            cin >> cipher_char >> plain_char;
            key_map[toupper(cipher_char)] = tolower(plain_char);
        } else if (choice == 2) {
            cout << "Enter Ciphertext char to unmap: ";
            cin >> cipher_char;
            key_map.erase(toupper(cipher_char));
        } else if (choice == 3) {
            bool valid = verify_solution(ciphertext, partial, key_map);
            if (valid) {
                cout << "\n=======================================================\n";
                cout << "        FINAL CRYPTANALYSIS & DECRYPTION REPORT        \n";
                cout << "=======================================================\n\n";
                cout << "[FULL RECOVERED PLAINTEXT]:\n";
                cout << "-------------------------------------------------------\n";
                cout << partial << "\n";
                cout << "-------------------------------------------------------\n\n";
                cout << "[RECOVERED SUBSTITUTION KEY TABLE]:\n";
                int col = 0;
                for (const auto& p : key_map) {
                    cout << p.first << " -> " << p.second << "\t";
                    if (++col % 4 == 0) cout << "\n";
                }
                cout << "\n\n=======================================================\n";
                cout << " [SUCCESS] Solution 100% verified against original ciphertext!\n";
                cout << "=======================================================\n";
                break;
            } else {
                cout << "\n[WARNING] Re-encryption check failed or incomplete mapping.\n";
            }
        } else {
            break;
        }
    }

    return 0;
}
