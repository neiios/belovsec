import math
import sys
from typing import Optional


def baby_step_giant_step(g: int, p: int, x: int) -> Optional[int]:
    m = math.ceil(math.sqrt(p - 1))
    baby_steps = {}
    value = 1
    for j in range(m):
        baby_steps[value] = j
        value = (value * g) % p
    factor = pow(g, m * (p - 2), p)
    value = x
    for i in range(m):
        if value in baby_steps:
            return (i * m + baby_steps[value]) % (p - 1)
        value = (value * factor) % p
    return None


def read_parameters(filename: str) -> dict[str, int]:
    params = {}
    with open(filename, "r") as file:
        for line in file:
            if line.strip() == "2.":
                for _ in range(3):
                    line = file.readline()
                    if line.strip() and "=" in line:
                        key, value = line.split("=")
                        params[key.strip()] = int(value.strip())
                break
    return params


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python script.py filename")
        sys.exit(1)

    filename = sys.argv[1]
    params = read_parameters(filename)
    g = params["g"]
    p = params["p"]
    x = params["x"]

    result = baby_step_giant_step(g, p, x)

    if result is not None:
        print(f"The discrete logarithm a = {result}")
        if pow(g, result, p) == x:
            print("Verification successful: g^a mod p = x")
        else:
            print("Verification failed!")
    else:
        print("No solution found")


if __name__ == "__main__":
    main()
