# Applied Cryptography in Python

Four small Python projects that implement and attack common public-key and symmetric cryptography techniques. They range from writing RSA by hand to replacing a broken RSA scheme with a hardened RSA-OAEP version.

> **About this project**
> I completed this work for an assignment for a university course. The assignment asked for working implementations of core cryptographic building blocks: RSA built from first principles, hybrid encryption, and steganography. It also included a security investigation, in which I tested a deliberately flawed "secure messaging" program, worked out why an attacker could break it, and built a replacement that the attack can't break. This repo contains only my programming work.

| # | Project | What it shows | Libraries |
|---|---------|---------------|-----------|
| 01 | [RSA from scratch](01-rsa-from-scratch/) | Prime generation, key generation, modular exponentiation, and encryption/decryption with no crypto libraries | standard library only |
| 02 | [Hybrid RSA + AES](02-hybrid-rsa-aes/) | Secure file exchange: AES-256-GCM encrypts the data, RSA-OAEP wraps the AES key | `pycryptodome` |
| 03 | [AES image steganography](03-aes-image-steganography/) | Password-encrypts a secret message and hides it in a JPEG's EXIF metadata, then extracts and decrypts it | `cryptography`, `Pillow` |
| 04 | [Hardened RSA-OAEP cipher](04-rsa-oaep-hardened-cipher/) | Replaces a breakable RSA tool with a manually implemented RSA-OAEP (SHA-256 / MGF1) scheme | standard library only |

---

## Getting started

```bash
git clone <this-repo>
cd <this-repo>
python -m venv .venv
# Windows: .venv\Scripts\activate   |   macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Each project is self-contained. Run its script from anywhere:

```bash
python 01-rsa-from-scratch/rsa_from_scratch.py
```

All file paths are built from a `BASE` variable (the script's own directory), so the scripts work the same way on Windows, macOS and Linux. Each script creates its own `keys/` and `output/` folders at runtime. These folders are git-ignored so that private keys never get committed.

---

## 01 · RSA from scratch

`01-rsa-from-scratch/rsa_from_scratch.py`

Textbook RSA built only on Python integers, with no cryptographic libraries:

- **Prime generation:** random odd numbers of a fixed bit length, tested with trial division up to √n
- **Key generation:** `n = p·q`, `φ(n) = (p−1)(q−1)`, `e = 65537` (another coprime `e` is chosen if needed), and `d = e⁻¹ mod φ(n)` from the extended Euclidean algorithm
- **Modular exponentiation:** square-and-multiply, written by hand
- **Encrypt/decrypt:** each character of `input/plaintext.txt` is encrypted, then decrypted and checked against the original

The script prints `p, q, n, φ, e, d`, the ciphertext and the recovered plaintext. It writes the keys to `keys/` and the results to `output/`.

> ⚠️ This is a learning tool. The small primes and per-character, unpadded encryption make it deterministic and easy to break (see project 04).

## 02 · Hybrid encryption (RSA-OAEP + AES-GCM)

`02-hybrid-rsa-aes/hybrid_rsa_aes.py`

Simulates sending a file securely to another person:

1. Generates a **2048-bit RSA** key pair and saves it as PEM files (`keys/`)
2. Encrypts `input/message.txt` with a random **AES-256-GCM** key, which gives both confidentiality and integrity through the auth tag
3. Wraps the AES key with **RSA-OAEP (SHA-256)**. Textbook RSA is not used anywhere.
4. Packages the wrapped key, nonce, tag and ciphertext as base64 JSON (`output/encrypted_message.json`)
5. Reverses the process, verifies the GCM tag, and writes `output/decrypted_message.txt`

All keys, intermediate values and outputs are printed so each step can be checked.

## 03 · AES image steganography

`03-aes-image-steganography/aes_image_stego.py`

Hides an encrypted message in a JPEG without visibly changing the image:

- **Key derivation:** PBKDF2-HMAC-SHA256 (600,000 iterations, random 16-byte salt) turns a password into a 256-bit key
- **Encryption:** AES-256-GCM with a random 96-bit nonce. The payload is `base64(salt ‖ nonce ‖ ciphertext+tag)`.
- **Hiding:** the payload is stored in the EXIF `UserComment` tag (0x9286). The image is re-saved with `quality="keep"`, so the pixel data is untouched.
- **Revealing:** the script reads the tag back, re-derives the key from the password, and decrypts. A wrong password or tampered data fails GCM authentication.

```
[1] Hide encrypted message in JPEG
[2] Reveal encrypted message from JPEG
```

The carrier is `input/image.jpg`, a generated gradient you can replace with any JPEG. The stego image is written to `output/stego.jpg`.

**Trade-offs:** metadata steganography is simple and lossless. It is also easy to detect with any EXIF viewer, and it is lost if a platform strips metadata on upload. LSB embedding would hide the data better, but JPEG recompression destroys it. AES-GCM keeps the message confidential even if someone finds it.

## 04 · Hardened RSA-OAEP cipher

`04-rsa-oaep-hardened-cipher/rsa_oaep_cipher.py`

**Background:** I was given a closed-source "secure messaging" tool and a matching cracking tool, provided by the class professors. The task was to find out why the cracker could recover plaintexts, and then build a replacement that it cannot break.

**What was wrong with the original:** the analysis found the weaknesses that classic textbook RSA misuse creates: small (~1M) primes that are easy to factor, and deterministic, unpadded encryption in which the same input always gives the same output. Unrelated inputs, such as the user's name, were displayed as if they were part of the scheme, to mislead the analyst.

**The fix.** The replacement takes the same inputs (first name, last name, two primes, plaintext) and writes the same `key.txt` / `cipher.txt` format, but:

- requires each prime to be **at least 1024 bits**, so the modulus is 2048 bits or more and cannot practically be factored
- checks that `p ≠ q` and that `gcd(e, φ(n)) = 1`
- implements **OAEP padding by hand** (SHA-256 with MGF1) using a cryptographically secure random seed from `secrets`. The same message encrypts differently every time, and the padding stops the malleability and small-message attacks that work on textbook RSA.
- encrypts the whole message as one OAEP block instead of character by character
- writes the initials to `cipher.txt` for format compatibility, but never uses them in encryption

Large primes can be generated with `openssl prime -generate -bits 1024` (run it twice).

---

## Tech

Python 3 · RSA · RSA-OAEP · AES-256-GCM · PBKDF2 · SHA-256 / MGF1 · EXIF steganography · pycryptodome · cryptography · Pillow

---

Made with the help of multiple 12oz flat white's. ☕
~ Jamal L (jlaq)
