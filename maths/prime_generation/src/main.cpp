#include <iostream>
#include <boost/multiprecision/cpp_int.hpp>
#include <random>
#include <chrono>
#include <vector>
#include <openssl/bn.h>
#include <openssl/err.h>

using namespace std;
using namespace boost::multiprecision;
using namespace chrono;

mt19937_64 rng(random_device{}());

cpp_int randomNumber(int bits)
{
    cpp_int n = 0;

    for (int i = 0; i < bits; i += 64)
    {
        n <<= 64;
        n |= rng();
    }

    n &= (cpp_int(1) << bits) - 1;
    n |= cpp_int(1) << (bits - 1);
    n |= 1;

    return n;
}

cpp_int modPow(cpp_int a, cpp_int b, cpp_int m)
{
    cpp_int result = 1;
    a = a % m;

    while (b > 0)
    {
        if (b % 2 == 1)
            result = (result * a) % m;

        a = (a * a) % m;
        b = b / 2;
    }

    return result;
}

bool millerRabin(cpp_int n, int rounds,
                 vector<cpp_int>& usedBases)
{
    if (n < 2)
        return false;

    if (n == 2 || n == 3)
        return true;

    if (n % 2 == 0)
        return false;

    cpp_int d = n - 1;
    int s = 0;

    while (d % 2 == 0)
    {
        d /= 2;
        s++;
    }

    for (int i = 0; i < rounds; i++)
    {
        cpp_int a = 2 + rng() % 1000000000ULL;

        a = 2 + a % (n - 3);

        usedBases.push_back(a);

        cpp_int x = modPow(a, d, n);

        if (x == 1 || x == n - 1)
            continue;

        bool passed = false;

        for (int j = 0; j < s - 1; j++)
        {
            x = (x * x) % n;

            if (x == n - 1)
            {
                passed = true;
                break;
            }
        }

        if (!passed)
            return false;
    }

    return true;
}


int independentVerification(const cpp_int& number)
{
    string decimal = number.convert_to<string>();

    BIGNUM *bn = nullptr;

    if (BN_dec2bn(&bn, decimal.c_str()) == 0 || bn == nullptr)
    {
        BN_free(bn);
        return -1;
    }

    BN_CTX *ctx = BN_CTX_new();

    if (ctx == nullptr)
    {
        BN_free(bn);
        return -1;
    }

    int result = BN_is_prime_ex(bn, 20, ctx, nullptr);

    BN_free(bn);
    BN_CTX_free(ctx);

    return result;
}





int main()
{
    int bits = 512;
    int rounds = 20;
    int candidates = 0;

    cpp_int prime;
    vector<cpp_int> bases;

    auto start = high_resolution_clock::now();

    while (true)
    {
        cpp_int n = randomNumber(bits);
        candidates++;

        vector<cpp_int> currentBases;

        if (millerRabin(n, rounds, currentBases))
        {
            prime = n;
            bases = currentBases;
            break;
        }
    }

    auto stop = high_resolution_clock::now();

    double elapsed =
        duration<double>(stop - start).count();

    cout << "CRYPTographic PRIME GENERATION\n";
    cout << "-------------------------------\n";

    cout << "Assigned bit length: " << bits << endl;
    cout << "Generated prime candidate: " << prime << endl;
    cout << "Actual bit length: "
         << msb(prime) + 1 << endl;

    cout << "Number of candidates tested: "
         << candidates << endl;

    cout << "Number of Miller-Rabin rounds: "
         << rounds << endl;

    cout << "Total execution time: "
         << elapsed << " seconds\n";

    cout << "\nMILLER-RABIN BASES\n";
    cout << "-------------------------------\n";

    for (int i = 0; i < bases.size(); i++)
    {
        cout << "Round " << i + 1
             << ": " << bases[i] << endl;
    }

    cout << "\nVERIFICATION\n";
    cout << "-------------------------------\n";

    cout << "Correct bit length: "
         << (msb(prime) + 1 == bits) << endl;

    vector<cpp_int> checkBases;

    cout << "Passes Miller-Rabin: "
         << millerRabin(prime, rounds, checkBases)
         << endl;
int independentResult = independentVerification(prime);

if (independentResult == 1)
{
    cout << "Independent verification (OpenSSL): Passed";
    cout << " - probable prime" << endl;
}
else if (independentResult == 0)
{
    cout << "Independent verification (OpenSSL): Failed";
    cout << " - composite number" << endl;
}
else
{
    cout << "Independent verification (OpenSSL): Error";
    cout << " - check OpenSSL installation" << endl;
}

    return 0;
}
