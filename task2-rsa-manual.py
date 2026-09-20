import os
from math import gcd, isqrt #TODO: check with tutor on use of gcd and isqrt for math library, worse case: do it manual

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

# TODO FUNCTION: karatsuba?? (will need to research on how it works)
# def karatsuba(x, y):
#     return 0

# TODO FUNCTION: is_prime
# def is_prime(n):
#     return True

# TODO FUNCTION: mod_inverse
# def mod_inverse(a,m):
#     return 0

# TODO FUNCTION: gen_keypair(size)
# def gen_keypair(size):
#     return 0

# TODO FUNCTION: encrypt
# def encrypt(ptxt, pub_k):
#     return 0

# TODO FNCUTON: decrypt()
# def decrypt(ctxt, priv_k):
#     return 0