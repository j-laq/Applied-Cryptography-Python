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

# greatest common denominator 
# print (gcd(48, 18))
# answer: 6
def gcd(a, b):
    """Give me the greatest common denominator"""
    while b != 0:
        a, b = b, a % b
    return a

# FUNCTION: gcd+ 
def gcd_plus(a, b):
    return ex_gcd(a,b)


def is_prime(n):
    """True if n is prime, false if not"""

    # Less than or even numbers
    if n < 2 or n % 2 == 0:
        return False
    
    # 2 is still prime
    if n == 2:
        return True

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

# TODO FUNCTION: mod inverse
# def mod_inverse(a,m):
#     """Find x such that (a*x) mod m = 1, for finding exponent d"""
#     g, x, _ = gcd_plus(a,m)

#     if g!= 1:
#         print(f"[!] mod_inverse: Modular inverse does not exist")
#         return 0

#     return x % m

# TODO FUNCTION: gen_keypair(size)
# def gen_keypair(size):
#     return 0

# TODO FUNCTION: encrypt
# def encrypt(ptxt, pub_k):
#     return 0

# TODO FNCUTON: decrypt()
# def decrypt(ctxt, priv_k):
#     return 0