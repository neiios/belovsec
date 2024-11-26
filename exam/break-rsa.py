# Just watch this: https://www.youtube.com/watch?v=-ShwJqAalOk

from math import ceil, isqrt
from textwrap import wrap
from sympy.ntheory.primetest import is_square

n = 46621583
e = 5557
# make sure every block is 8 digits long
ciphertext_blocks = [45722661, 37026161, 36593765]

a = ceil(isqrt(n))
while True:
    b2 = a**2 - n
    if is_square(b2):
        b = isqrt(b2)
        break
    a += 1
p = a + b
q = a - b
print(f"p = {p}, q = {q}")

phi_n = (p - 1) * (q - 1)
d = pow(e, -1, phi_n)
print(f"phi(n): {phi_n}, d: {d}")

deciphered_blocks = []
for ciphertext in ciphertext_blocks:
    m = pow(ciphertext, d, n)
    m_str = str(m).zfill(8)
    deciphered_blocks.append(m_str)

chars = wrap("".join(deciphered_blocks), 3)
print(deciphered_blocks)
print("".join([chr(int(c)) for c in chars]))
