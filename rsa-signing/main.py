import hashlib
import time


def read_private_key_from_file(filename: str, start_line: int) -> tuple[int, int]:
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


def create_signature(hash_value_hex: str, private_key: tuple[int, int]) -> str:
    message = int(hash_value_hex, 16)
    n, d = private_key
    signature = pow(message, d, n)
    return hex(signature)[2:]


def main() -> None:
    filename = "certificate.txt"
    private_key = read_private_key_from_file("rsa_keys.txt", 7)

    hash_value = hash_file(filename)
    signature = create_signature(hash_value, private_key)

    timestamp = int(time.time())
    timestamp_hex = hex(timestamp)[2:]

    combined = hash_value + timestamp_hex
    timestamp_hash = hashlib.sha256(combined.encode()).hexdigest()

    timestamp_signature = create_signature(timestamp_hash, private_key)

    with open("output.txt", "w") as f:
        f.write(f"Sertifikato piršto antspaudas: {hash_value}\n")
        f.write(f"Piršto antspaudo parašas: {signature}\n")
        f.write(f"Sertifikato ir laiko žymos piršto antspaudas: {timestamp_hash}\n")
        f.write(f"Laiko žyma: {timestamp}\n")
        f.write(f"Sertifikato ir laiko žymos piršto antspaudo parašas: {timestamp_signature}\n")

    with open("output.txt", "r") as f:
        print(f.read())


if __name__ == "__main__":
    main()
