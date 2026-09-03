#ifndef CRYPTANALYSIS_H
#define CRYPTANALYSIS_H

#include <string>
#include <map>
#include <vector>

std::string generate_random_key();
std::string encrypt_monoalphabetic(const std::string& plaintext, const std::string& key);
std::string apply_substitution(const std::string& ciphertext, const std::map<char, char>& key_map);
bool verify_solution(const std::string& original_ciphertext, const std::string& decrypted_text, const std::map<char, char>& key_map);

void frequency_analysis(const std::string& ciphertext);
void word_frequency_analysis(const std::string& ciphertext);
void pattern_analysis(const std::string& ciphertext);
void print_decision_table();

#endif
