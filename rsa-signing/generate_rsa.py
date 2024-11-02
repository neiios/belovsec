import random


def is_prime(n, k=5):
    """Miller-Rabin primality test"""
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False

    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Witness loop
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bits):
    """Generate a prime number with specified number of bits"""
    while True:
        n = random.getrandbits(bits) | (1 << bits - 1) | 1
        if is_prime(n):
            return n


def mod_inverse(e, phi):
    """Calculate modular multiplicative inverse"""

    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    _, x, _ = extended_gcd(e, phi)
    return (x % phi + phi) % phi


def generate_rsa_keys():
    # Public exponent
    e = 65537

    # Generate two 256-bit prime numbers
    p = generate_prime(256)
    q = generate_prime(256)

    # Calculate n and phi
    n = p * q
    phi = (p - 1) * (q - 1)

    # Calculate private exponent
    d = mod_inverse(e, phi)

    # Public key: (n, e)
    # Private key: (n, d)
    return {"public_key": (n, e), "private_key": (n, d), "p": p, "q": q, "phi": phi}


# Generate keys
keys = generate_rsa_keys()

# Print results
print("RSA Key Generation Results:")
print("\nPublic Key (n, e):")
print(f"n = {keys['public_key'][0]}")
print(f"e = {keys['public_key'][1]}")
print("\nPrivate Key (n, d):")
print(f"n = {keys['private_key'][0]}")
print(f"d = {keys['private_key'][1]}")
print("\nOther Values:")
print(f"p = {keys['p']}")
print(f"q = {keys['q']}")
print(f"phi = {keys['phi']}")

# Verify key lengths
print("\nKey Lengths (bits):")
print(f"p length: {keys['p'].bit_length()}")
print(f"q length: {keys['q'].bit_length()}")
print(f"n length: {keys['public_key'][0].bit_length()}")
