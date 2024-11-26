from sympy import isprime, factorint
from helpers import bool_with_color


def is_valid_private_key(n, e, d):
    # Step 1: Factorize N to find p and q
    def factorize(n):
        factors = factorint(n)
        print(f"Factors of {n}: {factors}")
        if len(factors) == 2 and all(exp == 1 for exp in factors.values()):
            return tuple(factors.keys())
        return None, None

    p, q = factorize(n)
    print(f"p = {p}, q = {q}")
    if p is None or q is None:
        return False, "N is not a product of two primes."

    # Step 2: Check if p and q are prime
    if not (isprime(p) and isprime(q)):
        return False, "N is not the product of two prime numbers."

    # Step 3: Compute φ(N)
    phi_n = (p - 1) * (q - 1)
    print(f"φ(N) = {phi_n}")

    # Step 4: Check if d satisfies d * e ≡ 1 mod φ(N)
    print(f"d * e mod φ(N) = {(d * e) % phi_n}")
    if (d * e) % phi_n != 1:
        return False, "d is not a valid private key; d * e ≢ 1 mod φ(N)."

    # Step 5: Ensure d is within the range (0, φ(N))
    if not (0 < d < phi_n):
        return False, "d is not in the valid range (0, φ(N))."

    # If all checks pass, d is valid
    return True, "d is a valid private key."


try:
    n = int(input("Enter n: "))
    e = int(input("Enter e: "))
    while True:
        d = int(input("Enter d: "))
        is_valid, message = is_valid_private_key(n, e, d)
        print("Validity:", bool_with_color(is_valid))
        print("Message:", message)
except ValueError:
    print("Please enter valid integers.")
except KeyboardInterrupt:
    pass
