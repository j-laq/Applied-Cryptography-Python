import os
import base64
from getpass import getpass
from PIL import Image

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
    payload = base64.b64decode(hidden_data[len(MAGIC): ])

    #salt: up to 16 bytes
    #nonce: 16 to 28
    # ctxt 28 over
    salt = payload[0:16]
    nonce = payload[16:28]
    ctxt = payload[28:]

    key = get_aes_k(word, salt)
    aesgcm = AESGCM(key)

    ptxt = aesgcm.decrypt(nonce, ctxt, None)
    return ptxt.decode("utf-8")

def hide_msg(img_path, out_path, msg, word):
    """Encrypt msg first, then store in JPEG EXIF UserComment metadata. Check if image is unchanged"""
    e_data = e_msg(msg, word)

    with Image.open(img_path) as img:
        exif = img.getexif()
        exif[EXIF_USER_COMMENT] = e_data

        img.save(out_path, format="JPEG", exif=exif.tobytes(), quality="keep", subsampling="keep")

def reveal_msg(tego_img_path, word):
    with Image.open(STEGO_IMAGE) as image:

        exif = image.getexif()
        hidden_data = exif.get(EXIF_USER_COMMENT)

    if isinstance(hidden_data, str):
        hidden_data = hidden_data.encode("utf-8")

    return d_msg(hidden_data, word)

def main():
    img_path = os.path.join(BASE, "in", "image.jpg")
    out_path = os.path.join(BASE, "out", "stego.jpg")

    os.makedirs(os.path.join(BASE, "in"), exist_ok=True)
    os.makedirs(os.path.join(BASE, "out"), exist_ok=True)

    print("[1] Hide encrypted message in JPEG")
    print("[2] Reveal encrypted message from JPEG")

    choice = input("Choose option (1/2): ").strip()

    if choice == "1":
        msg = input("Secret message: ")
        word = getpass("Encryption password: ")

        hide_msg(img_path, out_path, msg, word)

        print(f"Encrypted message hidden in: {out_path}")

    elif choice == "2":
        d_word = getpass("Decryption password: ")

        msg = reveal_msg(out_path, d_word)
        print(f"Decrypted secret message: {msg}")

    else:
        print("Invalid option.")


if __name__ == "__main__":
    main()