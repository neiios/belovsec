import random
import argparse
from typing import Optional
from sympy import isprime, primitive_root
from helpers import bool_with_color


def diffie_hellman(p: int, g: int, a: Optional[int] = None, b: Optional[int] = None):
    if a is None:
        a = random.randint(1, p - 1)
    if b is None:
        b = random.randint(1, p - 1)

    print(f"Party A's private key: {a}")
    print(f"Party B's private key: {b}")

    public_key_a = pow(g, a, p)  # A = g^a mod p
    public_key_b = pow(g, b, p)  # B = g^b mod p

    print(f"Party A's public key: {public_key_a}")
    print(f"Party B's public key: {public_key_b}")

    shared_secret_a = pow(public_key_b, a, p)  # s = B^a mod p
    shared_secret_b = pow(public_key_a, b, p)  # s = A^b mod p
    assert shared_secret_a == shared_secret_b, "Shared secrets do not match!"

    return shared_secret_a


def is_valid_generator(g, p):
    # Check if p is a prime
    if not isprime(p):
        return False, "p is not a prime number."

    # Check if g is in the valid range
    if g <= 1 or g >= p:
        return False, "g is out of valid range (1 < g < p)."

    # Check if g is a primitive root modulo p
    try:
        # Find a primitive root of p
        primitive = primitive_root(p)
        if g != primitive:
            return False, "g is not a primitive root of p."
    except ValueError:
        return False, "p does not have a primitive root."

    return True, "g is a valid generator."


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate the Diffie-Hellman key exchange algorithm.")
    parser.add_argument("-p", type=int, required=True, help="Prime number (public parameter)")
    parser.add_argument("-g", type=int, required=True, help="Primitive root modulo p (public parameter)")
    parser.add_argument("-a", type=int, help="Private key for Party A (optional)", default=None)
    parser.add_argument("-b", type=int, help="Private key for Party B (optional)", default=None)

    args = parser.parse_args()

    print(f"Is {args.g} a valid generator modulo {args.p}? {bool_with_color(is_valid_generator(args.g, args.p))}")
    shared_secret = diffie_hellman(args.p, args.g, args.a, args.b)
    print(f"Final shared secret: {shared_secret}")
