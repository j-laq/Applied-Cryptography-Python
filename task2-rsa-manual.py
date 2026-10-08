import os
import random
from math import gcd, isqrt

# for base requirement, 
BASE = os.path.dirname(os.path.abspath(__file__))

##STUDENT ID: s4171913
ptxt = 4171913
print(f"\n[*] START \nPLAIN TEXT: {ptxt}")

# TODO: choose 2 large primes p, q
# TODO: compute n = p*q and phi = (p-1)(q-1)
# TODO: public exponent, e, such that e is greater than 1, but smaller than phi AND gcd (e, phi) = 1
# TODO: compute private expontent, d such that d*e = 1 (mod phi(n))
# TODO: encrypt c = m^e(mod n)
# TODO: decrypt m = c^d(mod n)

# greatest common d 
def gcd(a, b):
    """Gives the greatest common divisor"""
    while b != 0:
        a, b = b, a % b
    return a

# FUNCTION: gcd+ 
def gcd_plus(a, b):
    return ex_gcd(a,b)

def is_prime(n):
    """True if n is prime, false if not"""
    
    # 2 is still prime
    if n == 2:
        return True

    # Less than or even numbers
    if n < 2 or n % 2 == 0:
        return False
    
    # Left with odd divisors, up to sqrt(n)
    # From 3 onwards, check every odd number after. Check if it can be dvisable perfectly
    for i in range (3, isqrt(n) + 1, 2):
        if n % i == 0:
            return False
    return True

def mod_exp(base, exp, mod):
    """Computes (base ** exp) % mod for majoritty of RSA"""
    result = 1
    base = base % mod
    while exp > 0:
        if exp & 1: #bitwise comparison: if current bit is 1, multiply into result
            result = (result * base) % mod

        # Square base, shift exp right, which is divide by 2
        base = (base * base) % mod
        exp >>= 1
    return result

def ex_gcd(a, b):
    """Returns (g,x ,y), where a*x + b*y = g = gcd(a,b)"""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = ex_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y

# FUNCTION: mod inverse
def mod_inverse(a,m):
    """Find x such that (a*x) mod m = 1, for finding exponent d"""
    g, x, _ = gcd_plus(a,m)

    if g!= 1:
        print(f"[!] mod_inverse: Modular inverse does not exist")
        return 0

    return x % m

def gen_prime(size):
    """Gen a prime number with aprox 'size' bits"""
    while True:
        out = random.getrandbits(size) #rand int up to "size boundary"
        #bitwise OR, force highest bit to 1 (even)
        out |= (1 << (size - 1))
        #Force lowest bit to 1 (odd)
        out |= 1

        # Test if prime, pass, if not, loop repeats with another number
        if is_prime(out):
            return out

# gen_keypair(size)
def gen_keypair(size = 128):
    """Gen RSA pub (pub_k) + priv (priv_k) keys"""
    #  choose p and q
    p = gen_prime(size)
    q = gen_prime(size)

    # Offchance that both p and q are the same
    while q == p:
        q = gen_prime(size)

    # Find n and phi
    n = p * q
    phi = (p - 1) * (q - 1)

    # RSA pub exponent
    e = 65537

    # Offchance 65537 is NOT coprime with phi
    while gcd(e, phi) != 1:
        e = random.randrange(3, phi - 1)
        if e % 2 == 0:
            e+=1

    # Compute priv exponent, d
    # d*e = 1 (mod phi(n))
    d = mod_inverse(e, phi)

    pub_k = (e, n)
    priv_k = (d, n)

    return pub_k, priv_k, p, q, phi

# TODO FUNCTION: encrypt
# def encrypt(ptxt, pub_k):
#     return 0

# TODO FNCUTON: decrypt()
# def decrypt(ctxt, priv_k):
#     return 0

