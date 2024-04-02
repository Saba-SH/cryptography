str_hex = input().strip()

def xor_decrypt(ciphertext, key):
    return ''.join(chr(ord(c) ^ key) for c in ciphertext)

def frequency_map(input_string):
    f_map = {}

    for char in input_string:
        if char.isalnum():
            char = char.upper()
        f_map[char] = f_map.get(char, 0) + 1
    return f_map

def top_n_characters(input_string, n=5):
    f_map = frequency_map(input_string)
    sorted_frequency = sorted(f_map.items(), key=lambda x: x[1], reverse=True)
    top_n = [p[0] for p in sorted_frequency[:n]]
    return top_n

int_hex = int(str_hex, 16)
byte_count = len(str_hex) / 2

acceptable_characters = [chr(i) for i in range(32, 127)]
acceptable_characters += ["\t", "\n"]
uppercase_letters = [chr(i) for i in range(65, 91)]

def is_acceptable(plaintext):
    for i, c in enumerate(plaintext):
        if c not in acceptable_characters:
            return False
        
    top_chars = top_n_characters(plaintext, 4)
    for c in top_chars:
        if c != " " and c.upper() not in uppercase_letters:
            return False

    return True

def single_char_decoding(hex_str):
    acceptable_plaintexts = []

    for i in range(0, 256):
        plaintext = xor_decrypt(bytes.fromhex(str_hex).decode('utf-8'), i)
        if is_acceptable(plaintext):
            acceptable_plaintexts.append(plaintext)

    if len(acceptable_plaintexts) > 0:
        return acceptable_plaintexts[0]
    else:
        return None

print(single_char_decoding(str_hex))
