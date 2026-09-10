
#include <bits/stdc++.h>
using namespace std;

// Standard English letter frequencies (A-Z)
const vector<double> ENG_FREQ = {
    8.17, 1.49, 2.78, 4.25, 12.70, 2.23, 2.02, 6.09, 6.97,
    0.15, 0.77, 4.03, 2.41, 6.75, 7.51, 1.93, 0.10, 5.99,
    6.33, 9.06, 2.76, 0.98, 2.36, 0.15, 1.97, 0.07
};

// 1. Clean non-alphabetic characters
string clean_ciphertext(const string& raw) {
    string cleaned = "";
    for (char c : raw) if (isalpha(c)) cleaned += toupper(c);
    return cleaned;
}

// 2. Find repeated trigrams
map<string, vector<int>> find_repeated_patterns(const string& text, int len = 3) {
    map<string, vector<int>> pos, repeats;
    for (size_t i = 0; i <= text.length() - len; ++i) 
        pos[text.substr(i, len)].push_back(i);
    for (auto& [pat, list] : pos) 
        if (list.size() > 1) repeats[pat] = list;
    return repeats;
}

// 3. Find distances between repeated patterns
vector<int> calculate_distances(const map<string, vector<int>>& repeats) {
    vector<int> dists;
    for (auto& [pat, list] : repeats)
        for (size_t i = 1; i < list.size(); ++i) dists.push_back(list[i] - list[i-1]);
    return dists;
}

// 4. Find factors of distances
map<int, int> find_factors(const vector<int>& dists) {
    map<int, int> factors;
    for (int d : dists)
        for (int f = 2; f <= 15; ++f) if (d % f == 0) factors[f]++;
    return factors;
}

// 5. Index of Coincidence
double calculate_ic(const string& text) {
    if (text.length() <= 1) return 0.0;
    vector<int> counts(26, 0);
    for (char c : text) counts[c - 'A']++;
    double num = 0.0;
    for (int c : counts) num += c * (c - 1);
    return num / (text.length() * (text.length() - 1));
}

// 6. Estimate key length using IC
int kasiski_analysis(const string& text, const map<int, int>&) {
    int best_k = 2;
    double max_ic = 0.0;
    for (int k = 2; k <= 12; ++k) {
        double avg_ic = 0.0;
        for (int g = 0; g < k; ++g) {
            string group = "";
            for (size_t i = g; i < text.length(); i += k) group += text[i];
            avg_ic += calculate_ic(group);
        }
        if (avg_ic / k > max_ic) { max_ic = avg_ic / k; best_k = k; }
    }
    return best_k;
}

// 7. Divide ciphertext into groups
vector<string> split_into_groups(const string& text, int k_len) {
    vector<string> groups(k_len, "");
    for (size_t i = 0; i < text.length(); ++i) groups[i % k_len] += text[i];
    return groups;
}

// 8. Frequency count for group
vector<int> frequency_analysis(const string& group) {
    vector<int> freq(26, 0);
    for (char c : group) freq[c - 'A']++;
    return freq;
}

// 9. Estimate Caesar shift using Chi-Square
int find_shift(const string& group) {
    int best_s = 0;
    double min_chi = 1e9;
    vector<int> counts = frequency_analysis(group);
    for (int s = 0; s < 26; ++s) {
        double chi = 0.0;
        for (int i = 0; i < 26; ++i) {
            double exp = (ENG_FREQ[i] / 100.0) * group.length();
            double obs = counts[(i + s) % 26];
            chi += ((obs - exp) * (obs - exp)) / exp;
        }
        if (chi < min_chi) { min_chi = chi; best_s = s; }
    }
    return best_s;
}

// 10. Combine shifts to form key
string find_key(const vector<int>& shifts) {
    string key = "";
    for (int s : shifts) key += (char)('A' + s);
    return key;
}

// 11. Decrypt ciphertext
string vigenere_decrypt(const string& text, const string& key) {
    string res = "";
    for (size_t i = 0; i < text.length(); ++i)
        res += (char)('A' + (text[i] - key[i % key.length()] + 26) % 26);
    return res;
}

// 12. Re-encrypt plaintext
string vigenere_encrypt(const string& text, const string& key) {
    string res = "";
    for (size_t i = 0; i < text.length(); ++i)
        res += (char)('A' + (text[i] - 'A' + key[i % key.length()] - 'A') % 26);
    return res;
}

// 13. Verify matching
bool verify(const string& orig, const string& recovered, const string& key) {
    return vigenere_encrypt(recovered, key) == orig;
}

int main() {
    ifstream file("ciphertext.txt");
    if (!file) { cerr << "Cannot open ciphertext.txt!\n"; return 1; }
    string raw((istreambuf_iterator<char>(file)), istreambuf_iterator<char>());

    string text = clean_ciphertext(raw);
    auto repeats = find_repeated_patterns(text);
    auto dists = calculate_distances(repeats);
    auto factors = find_factors(dists);

    int k_len = kasiski_analysis(text, factors);
    auto groups = split_into_groups(text, k_len);

    vector<int> shifts;
    cout << "Estimated Key Length: " << k_len << "\n\n";

    for (int i = 0; i < k_len; ++i) {
        int s = find_shift(groups[i]);
        shifts.push_back(s);
        cout << "Group " << i + 1 << " (Key: " << (char)('A' + s) << "):\n";
        auto freq = frequency_analysis(groups[i]);
        for (int c = 0; c < 26; ++c) cout << (char)('A' + c) << ":" << freq[c] << " ";
        cout << "\n\n";
    }

    string key = find_key(shifts);
    string plaintext = vigenere_decrypt(text, key);

    cout << "Recovered Key: " << key << "\n";
    cout << "Recovered Plaintext:\n" << plaintext << "\n\n";
    cout << "Verification: " << (verify(text, plaintext, key) ? "SUCCESS" : "FAILED") << "\n";

    return 0;
}
