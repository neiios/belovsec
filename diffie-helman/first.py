import sys


def read_parameters(filename):
    params = {}
    with open(filename, "r") as file:
        file.readline()
        for _ in range(4):
            line = file.readline()
            if line.strip() and "=" in line:
                key, value = line.split("=")
                params[key.strip()] = int(value.strip())
    return params


def diffie_hellman(g, p, a, b):
    A = pow(g, a, p)
    B = pow(g, b, p)
    secret_A = pow(B, a, p)
    secret_B = pow(A, b, p)
    return A, B, secret_A, secret_B


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py filename")
        sys.exit(1)

    filename = sys.argv[1]
    params = read_parameters(filename)
    g = params["g"]
    p = params["p"]
    a = params["a"]
    b = params["b"]

    public_A, public_B, secret_A, secret_B = diffie_hellman(g, p, a, b)

    print("Public Parameters:")
    print(f"g (generator): {g}")
    print(f"p (prime): {p}")

    print("\nPrivate Keys:")
    print(f"a (Alice's private key): {a}")
    print(f"b (Bob's private key): {b}")

    print("\nPublic Keys:")
    print(f"A (Alice's public key): {public_A}")
    print(f"B (Bob's public key): {public_B}")

    print("\nShared Secrets:")
    print(f"Alice's shared secret: {secret_A}")
    print(f"Bob's shared secret: {secret_B}")


if __name__ == "__main__":
    main()
