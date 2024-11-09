from constants import sbox, sboxInv, mult_2, mult_3, mult_9, mult_b, mult_d, mult_e


def byte_length(input):
    return (input.bit_length() + 7) // 8


def string_to_bytes(input):
    return str.encode(input)


def bytes_to_int(input):
    return int.from_bytes(input, "big")


def int_to_bytes(input, size=None):
    if size is None:
        return input.to_bytes(byte_length(input), "big")
    else:
        return input.to_bytes(size, "big")


def bytes_to_string(input):
    return input.decode("utf-8")


def int_to_string(input):
    return bytes_to_string(int_to_bytes(input))


def string_to_int(input):
    return bytes_to_int(string_to_bytes(input))


def split(array, chunk_size):
    return [array[i : i + chunk_size] for i in range(0, len(array), chunk_size)]


def bytes_to_blocks(input):
    padding_length = (16 - (len(input) % 16)) % 16
    for i in range(padding_length):
        input += b"\x00"
    blocks = []
    for b in split(input, 16):
        blocks.append(
            [
                [b[0], b[4], b[8], b[12]],
                [b[1], b[5], b[9], b[13]],
                [b[2], b[6], b[10], b[14]],
                [b[3], b[7], b[11], b[15]],
            ]
        )
    return blocks


def string_to_blocks(string):
    byte_array = string_to_bytes(string)
    return bytes_to_blocks(byte_array)


def blocks_to_string(blocks):
    byte_blocks = []
    for block in blocks:
        r = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        for i in range(4):
            for j in range(4):
                r[i][j] = int_to_bytes(block[i][j], 1)
        byte_blocks.append(r)
    result = b""
    for block in byte_blocks:
        for i in range(4):
            for j in range(4):
                result += block[j][i]
    return bytes_to_string(result.rstrip(b"\x00"))


def byte_string_to_blocks(string):
    return bytes_to_blocks(bytes.fromhex(string))


def blocks_to_byte_string(blocks):
    result = b""
    for block in blocks:
        for i in range(4):
            for j in range(4):
                result += int_to_bytes(block[j][i], 1)
    return result.hex()


# AES functions
def add_round_key(state, key):
    for i in range(4):
        for j in range(4):
            state[i][j] ^= key[i][j]
    return state


def sub_bytes(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = sbox[state[i][j]]
    return state


def inv_sub_bytes(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = sboxInv[state[i][j]]
    return state


def shift_rows(state):
    state[1][0], state[1][1], state[1][2], state[1][3] = state[1][1], state[1][2], state[1][3], state[1][0]
    state[2][0], state[2][1], state[2][2], state[2][3] = state[2][2], state[2][3], state[2][0], state[2][1]
    state[3][0], state[3][1], state[3][2], state[3][3] = state[3][3], state[3][0], state[3][1], state[3][2]
    return state


def inv_shift_rows(state):
    state[1][0], state[1][1], state[1][2], state[1][3] = state[1][3], state[1][0], state[1][1], state[1][2]
    state[2][0], state[2][1], state[2][2], state[2][3] = state[2][2], state[2][3], state[2][0], state[2][1]
    state[3][0], state[3][1], state[3][2], state[3][3] = state[3][1], state[3][2], state[3][3], state[3][0]
    return state


def mix_columns(state):
    for i in range(4):
        a = [state[j][i] for j in range(4)]
        b = [
            mult_2[a[0]] ^ mult_3[a[1]] ^ a[2] ^ a[3],
            a[0] ^ mult_2[a[1]] ^ mult_3[a[2]] ^ a[3],
            a[0] ^ a[1] ^ mult_2[a[2]] ^ mult_3[a[3]],
            mult_3[a[0]] ^ a[1] ^ a[2] ^ mult_2[a[3]],
        ]
        for j in range(4):
            state[j][i] = b[j]
    return state


def inv_mix_columns(state):
    for i in range(4):
        a = [state[j][i] for j in range(4)]
        b = [
            mult_e[a[0]] ^ mult_b[a[1]] ^ mult_d[a[2]] ^ mult_9[a[3]],
            mult_9[a[0]] ^ mult_e[a[1]] ^ mult_b[a[2]] ^ mult_d[a[3]],
            mult_d[a[0]] ^ mult_9[a[1]] ^ mult_e[a[2]] ^ mult_b[a[3]],
            mult_b[a[0]] ^ mult_d[a[1]] ^ mult_9[a[2]] ^ mult_e[a[3]],
        ]
        for j in range(4):
            state[j][i] = b[j]
    return state


def read_variants(filename):
    variants = {}
    with open(filename, "r") as f:
        lines = f.read().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.endswith("."):
            variant_num = int(line.rstrip("."))
            key = lines[i + 1].strip()
            text = lines[i + 2].strip()
            variants[variant_num] = {"key": key, "text": text}
            i += 3
        else:
            i += 1
    return variants


def get_round_keys(key_hex):
    key_bytes = bytes.fromhex(key_hex)
    keys = []
    for i in range(0, len(key_bytes), 16):
        key_block = key_bytes[i : i + 16]
        key_block_matrix = [
            [key_block[0], key_block[4], key_block[8], key_block[12]],
            [key_block[1], key_block[5], key_block[9], key_block[13]],
            [key_block[2], key_block[6], key_block[10], key_block[14]],
            [key_block[3], key_block[7], key_block[11], key_block[15]],
        ]
        keys.append(key_block_matrix)
    return keys


def aes_encrypt_block(block, round_keys):
    state = [row[:] for row in block]
    state = add_round_key(state, round_keys[0])
    for round in range(1, 3):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_keys[round])
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, round_keys[3])
    return state


def aes_decrypt_block(block, round_keys):
    state = [row[:] for row in block]
    state = add_round_key(state, round_keys[3])
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    for round in range(2, 0, -1):
        state = add_round_key(state, round_keys[round])
        state = inv_mix_columns(state)
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
    state = add_round_key(state, round_keys[0])
    return state


def main():
    variants = read_variants("variantai.txt")

    # TODO: CHANGEME
    variant_num = 10
    print(f"Your variant number is: {variant_num}")
    variant_data = variants.get(variant_num)

    if not variant_data:
        print("Variant not found.")
        return

    key_hex = variant_data["key"]
    text_hex = variant_data["text"]
    round_keys = get_round_keys(key_hex)
    ciphertext_blocks = byte_string_to_blocks(text_hex)
    decrypted_blocks = []

    for block in ciphertext_blocks:
        decrypted_block = aes_decrypt_block(block, round_keys)
        decrypted_blocks.append(decrypted_block)
    decrypted_text = blocks_to_string(decrypted_blocks)

    print("Atšifruotas tekstas:")
    print(decrypted_text)

    # TODO: CHANGEME
    surname = "Surname"
    plaintext_blocks = string_to_blocks(surname)
    encrypted_blocks = []

    for block in plaintext_blocks:
        encrypted_block = aes_encrypt_block(block, round_keys)
        encrypted_blocks.append(encrypted_block)

    encrypted_text_hex = blocks_to_byte_string(encrypted_blocks)

    print("Šifras:")
    print(encrypted_text_hex)
    print("Naudotas raktas:")
    print(key_hex)

    def decrypt_ecb(ciphertext_blocks, round_keys):
        decrypted_blocks = []
        for block in ciphertext_blocks:
            decrypted_block = aes_decrypt_block(block, round_keys)
            decrypted_blocks.append(decrypted_block)
        return blocks_to_string(decrypted_blocks)

    def decrypt_cbc(ciphertext_blocks, round_keys, iv_block):
        decrypted_blocks = []
        previous_block = iv_block
        for block in ciphertext_blocks:
            decrypted_block = aes_decrypt_block(block, round_keys)
            # XOR with the previous block (or IV for the first block)
            decrypted_block = [[decrypted_block[i][j] ^ previous_block[i][j] for j in range(4)] for i in range(4)]
            decrypted_blocks.append(decrypted_block)
            previous_block = block  # Update the previous block for the next iteration
        return blocks_to_string(decrypted_blocks)

    def decrypt_cfb(ciphertext_blocks, round_keys, iv_block):
        decrypted_blocks = []
        feedback_block = iv_block
        for block in ciphertext_blocks:
            encrypted_iv = aes_encrypt_block(feedback_block, round_keys)
            decrypted_block = [[block[i][j] ^ encrypted_iv[i][j] for j in range(4)] for i in range(4)]
            decrypted_blocks.append(decrypted_block)
            feedback_block = block  # Update feedback block for the next iteration
        return blocks_to_string(decrypted_blocks)

    def decrypt_ofb(ciphertext_blocks, round_keys, iv_block):
        decrypted_blocks = []
        output_block = iv_block
        for block in ciphertext_blocks:
            output_block = aes_encrypt_block(output_block, round_keys)
            decrypted_block = [[block[i][j] ^ output_block[i][j] for j in range(4)] for i in range(4)]
            decrypted_blocks.append(decrypted_block)
        return blocks_to_string(decrypted_blocks)

    # TODO: CHANGEME
    key = bytes.fromhex("eba25db9f3afd418796f7c1e960b32660e203f698f1bdd9bfd3834ca6b13477facad009cea8bb30a0f94f3cdf84a4190db0febf5d1ae59e18ef86266237816ab")
    iv = bytes.fromhex("94e1ff98cf1445e432c81637151590b6")

    iv_block = byte_string_to_blocks(iv.hex())[0]
    round_keys = get_round_keys(key.hex())

    # TODO: CHANGEME
    ciphertexts = [
        "5f4fcd87716c8cb1c571d703d585f8b13dd84e57f3498bb626044ad80bea8fd447171bc00677d56ad17f12c0cacb111cac54f1626c894646968ecbc1a2261201",
        "fdc1a900d84a7efde25e06e5339d35ae2a24e88c433d5c9b8fb0f1938c2fcb462313b7dd29f5f474a64d96f48b49d72b",
        "b1d5eb5c4ba0df0339bd1b2ccde6fc45437fea411aaced8e1bf6a8b496ae2bde377982b660905739904eb376550e600e",
        "56fedf076fd7ecc88d973e5de4642a008c9079258d8e61186be2ba00fddd616b74bddaf81651fe50476dd225b1d80445255eb4b47061286e7bf7dba9db4277e9",
        "c522c302d8ad009dcf369bfc3b63270380cf26fe855e2e8d4ae5d02a39849462a2e6f9d19537719229b688105e3fdd945a47aeed5ce6c0dcc3c33742277b15cb",
    ]

    ciphertext_blocks_list = [byte_string_to_blocks(ct) for ct in ciphertexts]

    plaintext_ecb = decrypt_ecb(ciphertext_blocks_list[0], round_keys)
    plaintext_cbc = decrypt_cbc(ciphertext_blocks_list[1], round_keys, iv_block)
    plaintext_cfb = decrypt_cfb(ciphertext_blocks_list[3], round_keys, iv_block)
    plaintext_ofb = decrypt_ofb(ciphertext_blocks_list[4], round_keys, iv_block)

    print("AES-EBC atviras tekstas:", plaintext_ecb)
    print("AES-CBC atviras tekstas:", plaintext_cbc)
    print("AES-CFB atviras tekstas:", plaintext_cfb)
    print("AES-OFB atviras tekstas:", plaintext_ofb)

    def decrypt_pcbc(ciphertext_blocks, round_keys, iv_block):
        decrypted_blocks = []
        previous_ciphertext_block = iv_block

        for block in ciphertext_blocks:
            decrypted_block = aes_decrypt_block(block, round_keys)
            decrypted_block = [[decrypted_block[i][j] ^ previous_ciphertext_block[i][j] for j in range(4)] for i in range(4)]
            decrypted_blocks.append(decrypted_block)
            previous_ciphertext_block = [[decrypted_block[i][j] ^ block[i][j] for j in range(4)] for i in range(4)]

        return blocks_to_string(decrypted_blocks)

    plaintext_pcbc = decrypt_pcbc(ciphertext_blocks_list[2], round_keys, iv_block)

    print("AES-PCBC atviras tekstas:", plaintext_pcbc)


if __name__ == "__main__":
    main()
