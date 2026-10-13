from pathlib import Path
from base64 import b64encode, b64decode
import json

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

# TODO: BASE
BASE = Path(__file__).resolve().parent

# TODO: read plaintxt from BASE File
INPUT_FILE = BASE / "task2.txt"
PUB_KEY_FILE = BASE / "rsa_public.pem"
PRIV_KEY_FILE = BASE / "rsa_private.pem"
E_FILE = BASE / "encrypted_task2.json"
D_FILE = BASE / "decrypted_task2.txt"

# TODO: Gen RSA pub/priv key, 2048 bit RSA, no txtbook RSA, sha-256
def gen_rsa_keys():
    rsa_key = RSA.generate(2048)

    priv_k_b = rsa_key.export_key(formate="PEM", passphrase=None,pkcs=8)
    pub_k_b = rsa_key.publickey().export_key(format="PEM")

    # TODO: Save RSA in seperate files: rsa_pub.pem, rsa_priv.pem
    #print/write
    PRIV_KEY_FILE.write_bytes(priv_k_b)
    PUB_KEY_FILE.write_bytes(pub_k_b)
    print(f"Private Key Bytes: {priv_k_b}")
    print(f"Public Key Bytes: {pub_k_b}")

    return priv_k_b, pub_k_b

# TODO: Encrypt info in task2.txt with AES-GCM mode, needed: ciphertxt, auth tag, nonce?
# TODO: Encrypt AES key using person2 RSA pub key
# TODO: Store encrypted data
# TODO: Dispplay details in terminal
## RSA pub Key
## RSA priv key
## AES key
## RSA-encrypted AES key
## AES nonce
## auth tag
## encrypted ciphertxt
# TODO: save recovered plaintxt in normal txt
# TODO: display decry file contents in terminal
# TODO: verify
# TODO: ctrl f and replace all bad names with better ones

def gen_rsa_keys():
    """Gen RSA key pair and save each key in a seperate file"""
    rsa_k = RSA.generate(2048)

def e_file(pub_k_b, p_txt):
    """
    Hybrid encryption:
    - Encrypt task2.txt using random AES-256 key in GCM mode.
    - Encrypt AES key using RSA-OAEP with SHA-256.
    """

    return aes_k, e_data


def d_file(priv_k_b):
    """
    1. Decrypt AES key with RSA-OAEP private key.
    2. Decrypt and authenticate ciphertext using AES-GCM.
    """

    return aes_k, ptxt, e_data