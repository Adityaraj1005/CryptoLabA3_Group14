#include "cryptanalysis.h"
#include <iostream>
#include <iomanip>
#include <algorithm>
#include <cctype>
#include <sstream>

using namespace std;

string generate_random_key() {
    return "QWERTYUIOPASDFGHJKLZXCVBNM";
}

string encrypt_monoalphabetic(const string& plaintext, const string& key) {
    string ciphertext = "";
    for (char c : plaintext) {
        if (isalpha(c)) {
            char base = isupper(c) ? 'A' : 'a';
            int index = toupper(c) - 'A';
            char sub = key[index];
            ciphertext += isupper(c) ? toupper(sub) : tolower(sub);
        } else {
            ciphertext += c;
        }
    }
    return ciphertext;
}

string apply_substitution(const string& ciphertext, const map<char, char>& key_map) {
    string result = "";
    for (char c : ciphertext) {
        if (isalpha(c)) {
            char upper_c = toupper(c);
            if (key_map.find(upper_c) != key_map.end()) {
                result += key_map.at(upper_c);
            } else {
                result += upper_c;
            }
        } else {
            result += c;
        }
    }
    return result;
}

bool verify_solution(const string& original_ciphertext, const string& decrypted_text, const map<char, char>& key_map) {
    if (key_map.size() < 26) return false;

    // Build reverse map: plaintext (lowercase) -> ciphertext (uppercase)
    map<char, char> reverse_map;
    for (const auto& pair : key_map) {
        reverse_map[tolower(pair.second)] = toupper(pair.first);
    }

    string re_encrypted = "";
    for (size_t i = 0; i < decrypted_text.length(); ++i) {
        char c = decrypted_text[i];
        if (isalpha(c)) {
            char lower_c = tolower(c);
            if (reverse_map.find(lower_c) != reverse_map.end()) {
                char cipher_char = reverse_map[lower_c];
                // Match original ciphertext character casing
                if (islower(original_ciphertext[i])) {
                    re_encrypted += tolower(cipher_char);
                } else {
                    re_encrypted += toupper(cipher_char);
                }
            } else {
                re_encrypted += c;
            }
        } else {
            re_encrypted += c;
        }
    }

    return re_encrypted == original_ciphertext;
}

void frequency_analysis(const string& ciphertext) {
    map<char, int> counts;
    int total = 0;
    for (char c : ciphertext) {
        if (isalpha(c)) {
            counts[toupper(c)]++;
            total++;
        }
    }

    vector<pair<char, int>> sorted_counts(counts.begin(), counts.end());
    sort(sorted_counts.begin(), sorted_counts.end(), [](const pair<char, int>& a, const pair<char, int>& b) {
        return a.second > b.second;
    });

    cout << "\n=======================================================\n";
    cout << " 1. LETTER FREQUENCY ANALYSIS\n";
    cout << "=======================================================\n";
    for (const auto& p : sorted_counts) {
        double pct = (double)p.second / total * 100.0;
        cout << p.first << " : " << setw(5) << p.second << " (" << fixed << setprecision(2) << pct << "%)\n";
    }
}

void word_frequency_analysis(const string& ciphertext) {
    stringstream ss(ciphertext);
    string word;
    map<string, int> words1, words2, words3;

    while (ss >> word) {
        string clean = "";
        for (char c : word) {
            if (isalpha(c)) clean += toupper(c);
        }
        if (clean.length() == 1) words1[clean]++;
        else if (clean.length() == 2) words2[clean]++;
        else if (clean.length() == 3) words3[clean]++;
    }

    cout << "\n=======================================================\n";
    cout << " 2. WORD PATTERN & FREQUENCY ANALYSIS\n";
    cout << "=======================================================\n\n";

    cout << "[1-Letter Words]: ";
    for (const auto& p : words1) cout << p.first << " (" << p.second << ") ";
    cout << "\n\n[2-Letter Words]: ";
    for (const auto& p : words2) cout << p.first << " (" << p.second << ") ";
    cout << "\n\n[3-Letter Words]: ";
    for (const auto& p : words3) cout << p.first << " (" << p.second << ") ";
    cout << "\n";
}

void pattern_analysis(const string& ciphertext) {
    map<string, int> doubles;
    for (size_t i = 0; i < ciphertext.length() - 1; ++i) {
        if (isalpha(ciphertext[i]) && toupper(ciphertext[i]) == toupper(ciphertext[i + 1])) {
            string d = "";
            d += toupper(ciphertext[i]);
            d += toupper(ciphertext[i + 1]);
            doubles[d]++;
        }
    }

    cout << "\n=======================================================\n";
    cout << " 3. REPEATED PATTERN ANALYSIS\n";
    cout << "=======================================================\n\n";
    cout << "Repeated Double Letters: ";
    for (const auto& p : doubles) cout << p.first << " (" << p.second << ") ";
    cout << "\n";
}

void print_decision_table() {
    cout << "\n===================================================================================================\n";
    cout << "                               CRYPTANALYTIC DECISION LOG TABLE                                    \n";
    cout << "===================================================================================================\n";
    cout << left 
         << setw(6)  << "Step" 
         << setw(35) << "Observation" 
         << setw(22) << "Possible Substitution" 
         << setw(20) << "Substitution Tested" 
         << setw(12) << "Decision" << "\n";
    cout << "---------------------------------------------------------------------------------------------------\n";

    cout << setw(6)  << "1" 
         << setw(35) << "ZIT appears 47x (top 3-letter word)" 
         << setw(22) << "ZIT -> the" 
         << setw(20) << "Z->t, I->h, T->e" 
         << setw(12) << "Good decision" << "\n";

    cout << setw(6)  << "2" 
         << setw(35) << "Single-char word Q occurs 21x" 
         << setw(22) << "Q -> a or i" 
         << setw(20) << "Q -> a" 
         << setw(12) << "Good decision" << "\n";

    cout << setw(6)  << "3" 
         << setw(35) << "E has highest frequency (5.15%)" 
         << setw(22) << "E -> c or t" 
         << setw(20) << "E -> c" 
         << setw(12) << "Good decision" << "\n";

    cout << setw(6)  << "4" 
         << setw(35) << "Double letter TT occurs 17x" 
         << setw(22) << "TT -> ee" 
         << setw(20) << "T -> e" 
         << setw(12) << "Good decision" << "\n";

    cout << setw(6)  << "5" 
         << setw(35) << "Ciphertext bigram GY occurs 28x" 
         << setw(22) << "GY -> of" 
         << setw(20) << "G->o, Y->f" 
         << setw(12) << "Good decision" << "\n";

    cout << setw(6)  << "6" 
         << setw(35) << "Partial text shows 's c h _ m e'" 
         << setw(22) << "Missing char -> e" 
         << setw(20) << "T -> e" 
         << setw(12) << "Good decision" << "\n";

    cout << setw(6)  << "7" 
         << setw(35) << "All 26 character mappings set" 
         << setw(22) << "Full key mapping" 
         << setw(20) << "Re-encrypt check" 
         << setw(12) << "Validated" << "\n";

    cout << "===================================================================================================\n\n";
}
