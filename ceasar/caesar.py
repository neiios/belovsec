from inputs import (
    LOWERCASE,
    UPPERCASE,
    encryption_inputs,
    decryption_inputs,
)


def rotl(c: str, shift: int) -> str:
    if c.islower():
        return LOWERCASE[(LOWERCASE.index(c) + shift) % len(LOWERCASE)]
    elif c.isupper():
        return UPPERCASE[(UPPERCASE.index(c) + shift) % len(UPPERCASE)]
    else:
        return c


def rotr(c: str, shift: int) -> str:
    if c.islower():
        return LOWERCASE[(LOWERCASE.index(c) - shift) % len(LOWERCASE)]
    elif c.isupper():
        return UPPERCASE[(UPPERCASE.index(c) - shift) % len(UPPERCASE)]
    else:
        return c


def encrypt(sentence: str, shift: int) -> str:
    return "".join([rotl(c, shift) for c in sentence])


def decrypt(sentence: str) -> None:
    for shift in range(1, len(LOWERCASE) + 1):
        decrypted_sentence = "".join([rotr(c, shift) for c in sentence])
        print(f"Shift: {shift} --- {decrypted_sentence}")


for i, (sentence, shift) in enumerate(encryption_inputs, 1):
    print(f"{i}. Encrypt: {sentence}")
    print(f"   Shift: {shift}")
    print(f"   Encrypted: {encrypt(sentence, shift)}")
    print()

for i, sentence in enumerate(decryption_inputs, 1):
    print(f"\n\n{i}. Encrypted: {sentence}")
    decrypt(sentence)
