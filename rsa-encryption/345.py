from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Util.number import inverse, long_to_bytes, bytes_to_long
from gmpy2 import iroot
from sympy import factorint


def generate_rsa_keypair(e, bit_length):
    """Generate RSA keypair with the specified bit length and public exponent e."""
    key = RSA.generate(bit_length, e=e)
    return key.publickey(), key


def encrypt_rsa(message, public_key):
    """Encrypt a message using RSA public key."""
    cipher = PKCS1_v1_5.new(public_key)
    message_bytes = message.encode("utf-8")
    ciphertext = cipher.encrypt(message_bytes)
    return bytes_to_long(ciphertext)


def decrypt_rsa(ciphertext, private_key):
    """Decrypt a ciphertext using RSA private key."""
    cipher = PKCS1_v1_5.new(private_key)
    ciphertext_bytes = long_to_bytes(ciphertext)
    message_bytes = cipher.decrypt(ciphertext_bytes, None)
    return message_bytes.decode("utf-8", errors="ignore").strip()


def decrypt_rsa_manual(ciphertext, n, d):
    """Decrypt a ciphertext manually using the private key components (n, d)."""
    plaintext_int = pow(ciphertext, d, n)
    plaintext_bytes = long_to_bytes(plaintext_int)
    return plaintext_bytes.decode("utf-8", errors="ignore").strip()


def strip_left_of_first_null_byte(plaintext_bytes):
    """Removes everything to the left of the first 0x00 byte in the plaintext bytes."""
    null_byte_index = plaintext_bytes.find(b"\x00")
    return (
        plaintext_bytes[null_byte_index + 1 :].decode("utf-8", errors="ignore")
        if null_byte_index != -1
        else plaintext_bytes.decode("utf-8", errors="ignore")
    )


def manual_rsa_decrypt(ciphertext, d, n):
    """Decrypt ciphertext using RSA manually and strip non-UTF-8 sequences."""
    plaintext_int = pow(ciphertext, d, n)
    plaintext_bytes = long_to_bytes(plaintext_int)
    return strip_left_of_first_null_byte(plaintext_bytes)


def break_rsa_small_m(c, e, n):
    """Attempt to decrypt a ciphertext by finding the e-th root directly."""
    m, exact = iroot(c, e)
    if exact:
        return long_to_bytes(m).decode("utf-8", errors="ignore")
    raise ValueError("Could not find the exact e-th root.")


def find_small_factor_optimized(n, factor_bit_length):
    """Find small factors of n within the specified bit length."""
    factors = factorint(n)
    for p in factors:
        if p.bit_length() <= factor_bit_length:
            return p
    return None


def break_rsa_small_factor(c, e, n, factor_bit_length):
    """Break RSA by finding small factors of n and manually decrypting the ciphertext."""
    p = find_small_factor_optimized(n, factor_bit_length)
    if not p:
        raise ValueError("Small factor not found.")
    q = n // p
    phi = (p - 1) * (q - 1)
    d = inverse(e, phi)
    return decrypt_rsa_manual(c, n, d)


if __name__ == "__main__":
    # Task 1: Generate RSA keys
    e = 65537
    bit_length = 1024
    public_key, private_key = generate_rsa_keypair(e, bit_length)

    # Output the results in the specified format
    print("Sugeneruoti RSA kriptosistemos viešąjį ir privatųjį raktą, kai e = 65537, o p ir q 256 bitų ilgio.")
    print("Atsakymas:")
    print(f"    p reikšmė: {private_key.p}")
    print(f"    q reikšmė: {private_key.q}")
    print(f"    (e, n): ({public_key.e}, {public_key.n})")
    print(f"    (d, n): ({private_key.d}, {private_key.n})")

    # Task 2: Encrypt name
    name = "Igor Repkin"
    ciphertext = encrypt_rsa(name, public_key)

    # Task 3: Decrypt given c using e and n
    e_3 = 3
    n_3 = 51674937335246900428382143093344306683761121728918667222507707766636574886417
    c_3 = 51093277015909060597198051109390625
    decrypted_text_3 = break_rsa_small_m(c_3, e_3, n_3)

    # Task 4: Decrypt given c with known small factor
    e_4 = 65537
    n_4 = 69286134577246899236174909229130069262197473886051829179263792294441333605537
    c_4 = 56638188982805541434810993513024567082168061758312013524404545250241101421880
    factor_bit_length = 40
    decrypted_text_4 = break_rsa_small_factor(c_4, e_4, n_4, factor_bit_length)

    # Task 5: Manual RSA decryption
    d_5 = 43696543653720653873897763902642928449201898017755253746570668893935683807659
    n_5 = 65544815480580980810846645853964392674327778875152889097773153296673353587193
    c_5 = 41318696177636845443451183168955305064699946432795076676996155315329349484826
    decrypted_text_5 = manual_rsa_decrypt(c_5, d_5, n_5)

    # Print Results
    print("Results:")
    print(f"Ciphertext: {ciphertext}")
    print(f"Decrypted text 3: {decrypted_text_3}")
    print(f"Decrypted text 4: {decrypted_text_4}")
    print(f"Decrypted text 5: {decrypted_text_5}")
