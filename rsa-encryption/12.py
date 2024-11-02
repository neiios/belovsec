from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes


def generate_rsa_keys():
    # Generate two 256-bit prime numbers, p and q
    p = getPrime(256)
    q = getPrime(256)

    # Calculate n and φ(n)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Choose the public exponent e
    e = 65537

    # Calculate the private key exponent d
    d = inverse(e, phi_n)

    # Return the RSA key components
    return (e, n), (d, n), p, q


def encrypt_message(public_key, message):
    e, n = public_key

    # Convert the message to a number using bytes_to_long
    message_bytes = message.encode("utf-8")
    message_long = bytes_to_long(message_bytes)

    # Encrypt the message
    encrypted_message = pow(message_long, e, n)

    return encrypted_message


def decrypt_message(private_key, encrypted_message):
    d, n = private_key

    # Decrypt the message
    decrypted_message_long = pow(encrypted_message, d, n)

    # Convert the number back to bytes, then decode to a string
    decrypted_message = long_to_bytes(decrypted_message_long).decode("utf-8")

    return decrypted_message


public_key, private_key, p, q = generate_rsa_keys()

print(f"Public Key (e, n): {public_key}")
print(f"Private Key (d, n): {private_key}")
print(f"p: {p}")
print(f"q: {q}")

message = "Vardas Pavarde"
encrypted_message = encrypt_message(public_key, message)
print(f"Encrypted Message: {encrypted_message}")

decrypted_message = decrypt_message(private_key, encrypted_message)
print(f"Decrypted Message: {decrypted_message}")
