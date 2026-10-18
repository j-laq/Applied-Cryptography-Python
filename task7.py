import hashlib
import math
from pathlib import Path

BASE = Path(__file__).resolve().parent

FILE_KEY = BASE / "key.txt"
FILE_CIPHER = BASE / "cipher.txt"

E = 65537
MIN_PRIME_BITS = 1024
HASH = hashlib.sha256
HASH_LEN = HASH().digest_size

def get_name(prompt):
    while True:
        value = input(prompt).strip()

        if value.isalpha():
            return value

        print("Name must contain letters only.")


def get_prime(prompt, other=None):
    """
    Checks for user input: primes, names, ptxt
    """
    while True:
        value = input(prompt).strip()

        # integer check
        if not value.isdecimal():
            print("Prime must be an integer")
            continue

        value = int(value)

        # no. of bits check, reccomended minimum of 1024
        if value.bit_length() < MIN_PRIME_BITS:
            print(f"Prime must be at least {MIN_PRIME_BITS} bits.")
            continue
        # p = q check
        if other is not None and value == other:
            print("The two primes must be different.")
            continue

        return value

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def mgf1(seed, length):
    """Mask gen function 1 using SHA-256."""
    output = b""
    counter = 0

    # hash  random seed + an increasing 4-byte counter
    # add the hash output for all of "length"
    while len(output) < length:
        counter_bytes = counter.to_bytes(4, byteorder="big")
        output += HASH(seed + counter_bytes).digest()
        counter += 1

    return output[:length]


def oaep_encode(msg, mod_length):
    """
    RSA-OAEP encoding with SHA-256. Random padding means same message encrypts differently each run
    """
    return 0

def rsa_oaep_e(ptxt, n):
    return 0



def main():
    first_name = get_name("Enter first name: ")
    last_name = get_name("Enter last name: ")
    initials = (first_name[0] + last_name[0]).upper()

    print(f"Enter two different valid primes of at least {MIN_PRIME_BITS} bits.")

    p = get_prime("Enter prime 1: ")
    q = get_prime("Enter prime 2: ", p)

    ptxt = input("Enter plaintext message: ")

    n = p * q
    phi = (p - 1) * (q - 1)

    if math.gcd(E, phi) != 1:
        print("Invalid prime values: 65537 is not coprime with phi(n).")
        return

    FILE_KEY.write_text(f"({E}, {n})", encoding="utf-8")

    # not used to encrypt the message.
    FILE_CIPHER.write_text(f"{ctxt}\n{initials}\n", encoding="utf-8")

    print(f"\nCreated: {FILE_KEY}")
    print(f"Created: {FILE_CIPHER}")
    print(f"RSA modulus size: {n.bit_length()} bits")


if __name__ == "__main__":
    main()