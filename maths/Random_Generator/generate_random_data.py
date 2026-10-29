import os
import subprocess

FILE_SIZE = 1048576  # 1 MB in bytes

# 1. Linux /dev/urandom
print("[+] Generating /dev/urandom dataset...")
with open("urandom_1mb.bin", "wb") as f:
    f.write(os.urandom(FILE_SIZE))

# 2. OpenSSL rand utility
print("[+] Generating OpenSSL dataset...")
subprocess.run(["openssl", "rand", "-out", "openssl_1mb.bin", str(FILE_SIZE)], check=True)

# 3. Genuine .NET Cryptographic RNG via PowerShell
print("[+] Generating genuine .NET API dataset via PowerShell...")
pwsh_cmd = (
    f"$rng = [System.Security.Cryptography.RandomNumberGenerator]::Create(); "
    f"$bytes = [byte[]]::new({FILE_SIZE}); "
    f"$rng.GetBytes($bytes); "
    f'[System.IO.File]::WriteAllBytes("windows_dotnet_1mb.bin", $bytes)'
)
subprocess.run(["pwsh", "-Command", pwsh_cmd], check=True)

print("[✓] All 3 datasets (1 MB each) generated successfully!")
