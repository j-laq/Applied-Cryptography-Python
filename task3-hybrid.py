from pathlib import Path
from base64 import b64encode, b64decode
import json

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

BASE = Path(__file__).resolve().parent

INPUT_FILE = BASE / "task2.txt"
PUB_KEY_FILE = BASE / "rsa_public.pem"
PRIV_KEY_FILE = BASE / "rsa_private.pem"
E_FILE = BASE / "encrypted_task2.json"
D_FILE = BASE / "decrypted_task2.txt"

def gen_rsa_keys():
    rsa_key = RSA.generate(2048)

    priv_k_b = rsa_key.export_key(format="PEM", passphrase=None,pkcs=8)
    pub_k_b = rsa_key.publickey().export_key(format="PEM")

    #write
    PRIV_KEY_FILE.write_bytes(priv_k_b)
    PUB_KEY_FILE.write_bytes(pub_k_b)

    return priv_k_b, pub_k_b

def e_file(pub_k_b, p_txt):
    """
    Hybrid encryption:
    - Encrypt task2.txt using random AES-256 key in GCM mode.
    - Encrypt AES key using RSA-OAEP with SHA-256.
    """
    aes_k = get_random_bytes(32)

    aes_cipher = AES.new(aes_k, AES.MODE_GCM)
    c_txt, tag = aes_cipher.encrypt_and_digest(p_txt)

    pub_k = RSA.import_key(pub_k_b)

    #RSA-OAEP for secure padding, double check if txtbook RSA
    rsa_cipher = PKCS1_OAEP.new(pub_k, hashAlgo=SHA256)
    e_aes_k = rsa_cipher.encrypt(aes_k)

    e_data = {"encrypted_aes_key": b64encode(e_aes_k).decode("utf-8"), "nonce": b64encode(aes_cipher.nonce).decode("utf-8"), "tag": b64encode(tag).decode("utf-8"), "ciphertext": b64encode(c_txt).decode("utf-8")}

    E_FILE.write_text(json.dumps(e_data, indent=4), encoding="utf-8")

    return aes_k, e_data


def d_file(priv_k_b):
    """
    1. Decrypt AES key with RSA-OAEP private key.
    2. Decrypt and authenticate ciphertext using AES-GCM.
    """
    e_data = json.loads(E_FILE.read_text(encoding="utf-8"))
    e_aes_k = b64decode(e_data["encrypted_aes_key"])
    nonce = b64decode(e_data["nonce"])
    tag = b64decode(e_data["tag"])
    c_txt = b64decode(e_data["ciphertext"])

    priv_k = RSA.import_key(priv_k_b)

    rsa_cipher = PKCS1_OAEP.new(priv_k, hashAlgo=SHA256)
    aes_k = rsa_cipher.decrypt(e_aes_k)

    aes_cipher = AES.new(aes_k, AES.MODE_GCM, nonce=nonce)
    p_txt = aes_cipher.decrypt_and_verify(c_txt, tag)

    D_FILE.write_bytes(p_txt)

    return aes_k, p_txt, e_data

def main():
    if not INPUT_FILE.exists():
        print(f"Missing input file: {INPUT_FILE}")
        return

    p_txt = INPUT_FILE.read_bytes()

    priv_k_b, pub_k_b = gen_rsa_keys()

    aes_k, e_data = e_file(pub_k_b, p_txt)
    _, d_txt, _ = d_file(priv_k_b)


    print("\n[*] Keys")
    print("  RSA Public Key: ")
    print(pub_k_b.decode("utf-8"))

    print(f"  AES Key: {aes_k.hex()}")

    print("\n[*] Encrypted output")
    print(f"RSA-encrypted AES key: {e_data['encrypted_aes_key']}")
    print(f"AES nonce: {e_data['nonce']}")
    print(f"AES authentication tag: {e_data['tag']}")
    print(f"AES ciphertext: {e_data['ciphertext']}")

    print("\n[*] Decrypted output")
    print(d_txt.decode("utf-8", errors="replace"))

    print("\n[*] Verify/Summary")
    print(f"Original and decrypted data match: {p_txt == d_txt}")
    print(f"Public key file: {PUB_KEY_FILE}")
    print(f"Private key file: {PRIV_KEY_FILE}")
    print(f"Encrypted file: {E_FILE}")
    print(f"Decrypted file: {D_FILE}")


if __name__ == "__main__":
    main()