# Feel free to use https://www.cryptool.org/en/cto/openssl/ to generate primes
# openssl prime -generate -bits 1024
# run command twice to get the 2 needed primes
# Test Primes:
# 157595398469767760690207586396601310446607898987356401490702399958502058430274171048176284480159947224396151187117406783568235999086384155356073407253255414581288995308773779180793175339737736725616020364515101450684604764229103455084268129276579158781415954682152177230088842287582376825972864291747555837967
# 161411228099330168315324196237347618412944850352306148068423487610779544209470513640737409916459844160177507413400202527277902912002605938129887136533731981483531118368599216906563631994031900653805200277494503363578840950495730101905786102362552944113147284242370208441164901738321340496670139166010871214973
  
import hashlib
import math
from pathlib import Path
import secrets
  
BASE = Path(__file__).resolve().parent
  
INPUT_DIR = BASE / "input"
KEYS_DIR = BASE / "keys"
OUTPUT_DIR = BASE / "output"
  
FILE_KEY = KEYS_DIR / "key.txt"
FILE_CIPHER = OUTPUT_DIR / "cipher.txt"
  
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
  
        # Integer check
        if not value.isdecimal():
            print("Prime must be an integer")
            continue
  
        value = int(value)
  
        # Number of bits check, reccomended minimum of 1024
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
  
    # Hash random seed + an increasing 4-byte counter
    # Add the hash output for all of "length"
    while len(output) < length:
        counter_bytes = counter.to_bytes(4, byteorder="big")
        output += HASH(seed + counter_bytes).digest()
        counter += 1
  
    return output[:length]
  
  
def oaep_encode(msg, mod_length):
    """
    RSA-OAEP encoding with SHA-256. Random padding means same message encrypts differently each run
    """
    label = b""
    label_hash = HASH(label).digest()
  
    max_msg_length = mod_length - (2 * HASH_LEN) - 2
  
    # Plaintxt length check
    if len(msg) > max_msg_length:
        print(
            f"Plaintext is too long. Maximum length is "
            f"{max_msg_length} UTF-8 bytes."
        )
        return None
  
    # Setup padding sizes
    padding_length = max_msg_length - len(msg)
    padding = b"\x00" * padding_length
  
    data_block = label_hash + padding + b"\x01" + msg
  
    seed = secrets.token_bytes(HASH_LEN)
  
    # Data and seed to be masked with XOR
    data_mask = mgf1(seed, mod_length - HASH_LEN - 1)
    masked_data_block = xor_bytes(data_block, data_mask)
  
    seed_mask = mgf1(masked_data_block, HASH_LEN)
    masked_seed = xor_bytes(seed, seed_mask)
  
    return b"\x00" + masked_seed + masked_data_block
  
def rsa_oaep_e(ptxt, n):
    mod_length = (n.bit_length() + 7) // 8
    encoded_message = oaep_encode(ptxt.encode("utf-8"), mod_length)
  
    if encoded_message is None:
        return None
  
    message_int = int.from_bytes(encoded_message, byteorder="big")
  
    return pow(message_int, E, n)
  
  
  
def main():
    INPUT_DIR.mkdir(exist_ok=True)
    KEYS_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
  
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
  
    ctxt = rsa_oaep_e(ptxt, n)
  
    if ctxt is None:
        return
  
    FILE_KEY.write_text(f"({E}, {n})", encoding="utf-8")
  
    # Initials not used to encrypt the message
    FILE_CIPHER.write_text(f"{ctxt}\n{initials}\n", encoding="utf-8")
  
    print(f"\nCreated: {FILE_KEY}")
    print(f"Created: {FILE_CIPHER}")
    print(f"RSA modulus size: {n.bit_length()} bits")
  
  
if __name__ == "__main__":
    main()