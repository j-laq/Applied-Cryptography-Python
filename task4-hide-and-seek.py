import os
import base64
from getpass import getpass

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

#base
BASE = os.path.dirname(os.path.abspath(__file__))

INPUT_IMAGE = os.path.join(BASE, "in", "cover.jpg")
STEGO_IMAGE = os.path.join(BASE, "out", "stego.jpg")

#EXIF tag id for JPEG, to use UserComment
EXIF_USER_COMMENT = 37510

# magic byte sequence, the header for metadata, will delete later
MAGIC = b"STEGO_AES_GCM_V1:"

def get_aes_k(word, salt):
    """Create 256-bit AES key from given password"""
    kdf = PBKDF2HMAC( algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600_000)
    return kdf.derive(word.encode("utf-8"))

def e_msg(msg, word):
    """Output formate: MAGIC + base64(salt + nonce + AES-GCM ctxt)"""
    payload = "..."

    #128 bits
    salt = os.urandom(16)
    #96 bits for AWS-GCM
    nonce = os.urandom(12)

    key = get_aes_k(word, salt)
    aesgcm = AESGCM(key)

    #.encrypt(nonce, data, associated data)
    ctxt = aesgcm.encrypt(nonce, msg.encode("utf-8"), None)
    
    payload = salt + nonce + ctxt
    return MAGIC + base64.b64encode(payload)

def d_msg(hidden_data, word):
    """Decrypt AES-GCM payload from JPEG metadata"""
    return "..."

def hide_msg(img_path, out_path, msg, word):
    """Encrypt msg first, then store in JPEG EXIF UserComment metadata. Check if image is unchanged"""

def reveal_msg(tego_img_path, word):
    return "..."

