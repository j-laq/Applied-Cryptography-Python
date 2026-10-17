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