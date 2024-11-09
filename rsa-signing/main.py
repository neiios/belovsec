import hashlib
import time


def read_key_pair_from_file(filename: str, start_line: int) -> tuple[int, int]:
    with open(filename, "r") as f:
        lines = f.readlines()
        n = int(lines[start_line].split("=")[1].strip())
        d = int(lines[start_line + 1].split("=")[1].strip())
    return (n, d)


def hash_file(filename: str) -> str:
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        content = f.read()
        sha256_hash.update(content)
    return sha256_hash.hexdigest()


def create_signature(hash_value_hex: str, private_key: tuple[int, int]) -> int:
    message = int(hash_value_hex, 16)
    n, d = private_key
    signature = pow(message, d, n)
    return signature

def verify_signature(hash_value_hex: str, signature: int, public_key: tuple[int, int]) -> bool:
    n, e = public_key
    decrypted_hash = pow(signature, e, n)
    calculated_hash = int(hash_value_hex, 16)
    return decrypted_hash == calculated_hash

def main() -> None:
    filename = "certificate.txt"
    private_key = read_key_pair_from_file("rsa_keys.txt", 7)
    public_key = read_key_pair_from_file("rsa_keys.txt", 3)

    hash = hash_file(filename)
    signature = create_signature(hash, private_key)

    timestamp = int(time.time())
    timestamp_hex = f"{timestamp:x}"
    combined = hash + timestamp_hex
    combined_hash = hashlib.sha256(combined.encode()).hexdigest()
    combined_signature = create_signature(combined_hash, private_key)

    with open("output.txt", "w") as f:
        f.write(f"Sertifikato piršto antspaudas: {hash}\n")
        f.write(f"Piršto antspaudo parašas: {signature}\n")
        f.write(f"Sertifikato ir laiko žymos piršto antspaudas: {combined_hash}\n")
        f.write(f"Laiko žyma: {timestamp}\n")
        f.write(f"Sertifikato ir laiko žymos piršto antspaudo parašas: {combined_signature}\n")

    with open("output.txt", "r") as f:
        print(f.read())

    is_valid = verify_signature(hash, signature, public_key)
    print("Parašo patvirtinimo rezultatas:", "Patvirtintas" if is_valid else "Nepatvirtintas")
    is_valid = verify_signature(combined_hash, combined_signature, public_key)
    print("Parašo su laiko žyma patvirtinimo rezultatas:", "Patvirtintas" if is_valid else "Nepatvirtintas")


if __name__ == "__main__":
    main()
