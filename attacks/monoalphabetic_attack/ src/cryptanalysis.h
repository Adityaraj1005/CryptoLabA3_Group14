#pragma once
#include <bits/stdc++.h>

using namespace std;

string encrypt_monoalphabetic(const string& plaintext, const string& key);
string generate_random_key();

void frequency_analysis(const string& ciphertext);
void word_frequency_analysis(const string& ciphertext);
void pattern_analysis(const string& ciphertext);
string apply_substitution(const string& ciphertext, const map<char, char>& key_map);
void display_partial_plaintext(const string& partial_text);
bool verify_solution(const string& original_ciphertext, const string& recovered_plaintext, const map<char, char>& key_map);
