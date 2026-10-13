from pathlib import Path
from base64 import b64encode, b64decode
import json

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

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

# TODO: Encrypt info in task2.txt with AES-GCM mode, needed: ciphertxt, auth tag, nonce?
def e_file(pub_k_b, p_txt):
    """
    Hybrid encryption:
    - Encrypt task2.txt using random AES-256 key in GCM mode.
    - Encrypt AES key using RSA-OAEP with SHA-256.
    """
    aes_k = get_random_bytes(32)

    aes_cipher = AES.net(aes_k, AES.MODE_GCM)
    c_txt, tag = aes_cipher.encrypt_and_digest(p_txt)

    pub_k = RSA.import_key(pub_k_b)

    #RSA-OAEP for secure padding, double check if txtbook RSA
    rsa_cipher = PKCS1_OAEP.net(pub_k, hashAlgo=SHA256)
    e_aes_k = rsa_cipher.encrypt(aes_k)

    e_data = {"encrypted_aes_key": b64encode(e_aes_k).decode("utf-8"), "nonce": b64encode(aes_cipher.nonce).decode("utf-8"), "tag": b64encode(tag).decode("utf-8"), "ciphertext": b64encode(c_txt).decode("utf-8")}

    E_FILE.write_text(json.dumps(e_data, indent=4), encoding="utf-8")

    return aes_k, e_data


def d_file(priv_k_b):
    """
    1. Decrypt AES key with RSA-OAEP private key.
    2. Decrypt and authenticate ciphertext using AES-GCM.
    """

    return aes_k, ptxt, e_data