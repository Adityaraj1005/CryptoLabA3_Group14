
#include <bits/stdc++.h>
#include "cryptanalysis.h"

using namespace std;

string generate_random_key() {
    return "QWERTYUIOPASDFGHJKLZXCVBNM";
}

string encrypt_monoalphabetic(const string& plaintext, const string& key) {
    string ciphertext = "";
    for (char c : plaintext) {
        if (isalpha(c)) {
            char upper_c = toupper(c);
            char encrypted = key[upper_c - 'A'];
            ciphertext += isupper(c) ? encrypted : (char)tolower(encrypted);
        } else {
            ciphertext += c;
        }
    }
    return ciphertext;
}

void frequency_analysis(const string& ciphertext) {
    map<char, int> freq;
    int total_letters = 0;

    for (char c : ciphertext) {
        if (isalpha(c)) {
            freq[toupper(c)]++;
            total_letters++;
        }
    }

    vector<pair<char, int>> sorted_freq(freq.begin(), freq.end());
    sort(sorted_freq.begin(), sorted_freq.end(), [](const auto& a, const auto& b) {
        return a.second > b.second;
    });

    cout << "\n========================================\n";
    cout << " 1. LETTER FREQUENCY ANALYSIS\n";
    cout << "========================================\n";
    cout << "Total Letters: " << total_letters << "\n\n";
    cout << left << setw(8) << "Letter" 
         << setw(12) << "Count" 
         << "Percentage\n";
    cout << "----------------------------------------\n";

    for (const auto& item : sorted_freq) {
        double percentage = (double)item.second / total_letters * 100.0;
        cout << left << setw(8) << item.first 
             << setw(12) << item.second 
             << fixed << setprecision(2) << percentage << "%\n";
    }
}

void word_frequency_analysis(const string& ciphertext) {
    map<string, int> word_freq;
    string current_word = "";

    for (char c : ciphertext) {
        if (isalpha(c)) {
            current_word += toupper(c);
        } else {
            if (!current_word.empty()) {
                word_freq[current_word]++;
                current_word = "";
            }
        }
    }
    if (!current_word.empty()) word_freq[current_word]++;

    map<int, vector<string>> words_by_length;
    for (const auto& pair : word_freq) {
        words_by_length[pair.first.length()].push_back(pair.first);
    }

    cout << "\n========================================\n";
    cout << " 2. WORD PATTERN & FREQUENCY ANALYSIS\n";
    cout << "========================================\n";

    for (int len = 1; len <= 3; len++) {
        cout << "\n[" << len << "-Letter Words]: ";
        if (words_by_length.count(len)) {
            for (const auto& w : words_by_length[len]) {
                cout << w << " (" << word_freq[w] << ") ";
            }
        } else {
            cout << "None";
        }
        cout << "\n";
    }
}

void pattern_analysis(const string& ciphertext) {
    map<string, int> doubles;
    for (size_t i = 0; i < ciphertext.length() - 1; i++) {
        if (isalpha(ciphertext[i]) && toupper(ciphertext[i]) == toupper(ciphertext[i+1])) {
            string d = "";
            d += toupper(ciphertext[i]);
            d += toupper(ciphertext[i+1]);
            doubles[d]++;
        }
    }

    cout << "\n========================================\n";
    cout << " 3. REPEATED PATTERN ANALYSIS\n";
    cout << "========================================\n";
    cout << "Repeated Double Letters: ";
    if (doubles.empty()) {
        cout << "None found\n";
    } else {
        for (const auto& pair : doubles) {
            cout << pair.first << " (" << pair.second << ") ";
        }
        cout << "\n";
    }
}

string apply_substitution(const string& ciphertext, const map<char, char>& key_map) {
    string result = "";
    for (char c : ciphertext) {
        if (isalpha(c)) {
            char upper_c = toupper(c);
            if (key_map.find(upper_c) != key_map.end()) {
                char sub = key_map.at(upper_c);
                result += isupper(c) ? (char)toupper(sub) : (char)tolower(sub);
            } else {
                result += upper_c;
            }
        } else {
            result += c;
        }
    }
    return result;
}

void display_partial_plaintext(const string& partial_text) {
    cout << "\n--- CURRENT PARTIAL DECRYPTION ---\n";
    cout << partial_text << "\n";
    cout << "-----------------------------------\n";
}

bool verify_solution(const string& original_ciphertext, const string& recovered_plaintext, const map<char, char>& key_map) {
    map<char, char> reverse_map;
    for (const auto& pair : key_map) {
        reverse_map[tolower(pair.second)] = pair.first;
        reverse_map[toupper(pair.second)] = pair.first;
    }

    string re_encrypted = "";
    for (char c : recovered_plaintext) {
        if (isalpha(c)) {
            if (reverse_map.count(c)) {
                re_encrypted += isupper(c) ? (char)toupper(reverse_map[c]) : (char)tolower(reverse_map[c]);
            } else {
                re_encrypted += c;
            }
        } else {
            re_encrypted += c;
        }
    }

    return re_encrypted == original_ciphertext;
}
