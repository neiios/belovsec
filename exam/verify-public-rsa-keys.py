from sympy import isprime, factorint
from helpers import bool_with_color


def is_valid_rsa_key(n, e):
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

    # Step 4: Check if E is coprime to φ(N)
    def gcd(a, b):
        while b:
            a, b = b, a % b
        print(f"GCD of {e} and {phi_n} is {a}")
        return a

    if gcd(e, phi_n) != 1:
        return False, "E is not coprime to φ(N)."

    # Step 5: Ensure E is within the range (1, φ(N))
    if not (1 < e < phi_n):
        return False, "E is not in the range (1, φ(N))."

    # If all checks pass, the keys are valid
    return True, "The RSA keys are valid."


try:
    while True:
        n = int(input("Enter n: "))
        e = int(input("Enter e: "))
        is_valid, message = is_valid_rsa_key(n, e)
        print("Validity:", bool_with_color(is_valid))
        print("Message:", message)
except ValueError:
    print("Please enter valid integers.")
except KeyboardInterrupt:
    pass
