import random
from typing import Tuple
from sympy.ntheory import primefactors


def is_generator(g: int, p: int) -> bool:
    """Check if g is a generator modulo p"""
    n = p - 1
    prime_factors = primefactors(n)
    for factor in prime_factors:
        power = n // factor
        if pow(g, power, p) == 1:
            return False
    return True


def generate_prime_with_generator() -> Tuple[int, int]:
    """Generate 100-bit prime p where 2 is a generator"""
    while True:
        p = random.getrandbits(100) | 1

        if all(p % i != 0 for i in range(2, min(int(p**0.5) + 1, 100))):
            if is_generator(2, p):
                return p, 2


def main() -> None:
    p, g = generate_prime_with_generator()
    print(f"Found prime p = {p}")
    print(f"Generator g = {g}")
    print(f"Number of bits in p: {p.bit_length()}")

    n = p - 1
    factors = primefactors(n)

    print("\nVerification:")
    print(f"1. φ({p}) = {p} - 1 = {n}")
    print(f"2. Prime factors of {n}: {factors}")
    print("3. Remainders:")

    for factor in factors:
        power = n // factor
        remainder = pow(g, power, p)
        print(f"   {g}^({n}/{factor}) mod {p} = {g}^{power} mod {p} ≡ {remainder}")


if __name__ == "__main__":
    main()
