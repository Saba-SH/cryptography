import base64
import binascii
import re

def xor_decrypt(ciphertext, key):
    return ''.join(chr(ord(c) ^ key) for c in ciphertext)
####################################################################################
def base64_to_hex(base64_string):
    binary_data = base64.b64decode(base64_string)
    return binascii.hexlify(binary_data).decode('ascii')

def str_to_bin(ascii_string):
    return ''.join(format(ord(char), '08b') for char in ascii_string)
    
def hamming_distance(str1, str2):
    return sum(bit1 != bit2 for bit1, bit2 in zip(str1, str2))

def bit_hamming_distance(str1, str2):
    return hamming_distance(str_to_bin(str1), str_to_bin(str2))

english_letter_frequency = {
        'a': 8.2, 'b': 1.5, 'c': 2.8, 'd': 4.3, 'e': 12.7,
        'f': 2.2, 'g': 2.0, 'h': 6.1, 'i': 7.0, 'j': 0.2,
        'k': 0.8, 'l': 4.0, 'm': 2.4, 'n': 6.7, 'o': 7.5,
        'p': 1.9, 'q': 0.1, 'r': 6.0, 's': 6.3, 't': 9.1,
        'u': 2.8, 'v': 1.0, 'w': 2.4, 'x': 0.2, 'y': 2.0,
        'z': 0.1, ' ': 20.0
    }

def english_score(plaintext):
    return sum(english_letter_frequency[c.lower()] for c in plaintext if c.lower() in english_letter_frequency)

def single_char_decodings(hex_str) -> list[tuple[int, str]]:
    plaintexts = []

    for i in range(0, 256):
        plaintext = xor_decrypt(bytes.fromhex(hex_str).decode('ascii'), i)
        plaintexts.append((i, plaintext))

    plaintexts = sorted(plaintexts, key=lambda x: english_score(x[1]), reverse=True)
    return plaintexts

def probable_keysizes(ct):
    hs_map = {}

    for keysize in range(2, 40+1):
        hss = []
        for i in range(4):
            for j in range(i+1, 4):
                hss.append(bit_hamming_distance(ct[i * keysize:(i+1) * keysize], 
                                            ct[j * keysize:(j+1) * keysize]) / keysize)
                
        hs_map[keysize] = sum(hss) / len(hss)

    return sorted(hs_map, key=lambda k: hs_map[k])

ciphertext_base64 = input().strip()
ciphertext_hex = base64_to_hex(ciphertext_base64)
ciphertext_bytes = bytes.fromhex(ciphertext_hex)
ciphertext = ciphertext_bytes.decode('ascii')

probable_plaintexts = []

for probable_keysize in probable_keysizes(ciphertext)[:3]:
    num_blocks = (len(ciphertext) + probable_keysize - 1) // probable_keysize
    blocks = [ciphertext[i * probable_keysize: (i + 1) * probable_keysize] for i in range(num_blocks)]

    key_hex = ""

    tblocks = [''.join(block[i] for block in blocks[:-1]) for i in range(len(blocks[0]))]
    for tblock in tblocks:
        key = single_char_decodings(tblock.encode('ascii').hex())[0][0]
        key_hex += hex(key)[2:].zfill(2)

    try:
        key_bytes = bytes.fromhex(key_hex)
        repeated_key = (key_bytes * (len(ciphertext_bytes) // len(key_bytes) + 1))[:len(ciphertext_bytes)]
        plaintext_bytes = bytes([ciphertext_byte ^ key_byte for ciphertext_byte, key_byte in zip(ciphertext_bytes, repeated_key)])

        probable_plaintext = plaintext_bytes.decode('ascii')
        pattern = re.compile(r'[.,;!?](?![\s$])')
        if not pattern.findall(probable_plaintext + "\n"):
            probable_plaintexts.append(probable_plaintext)
    except Exception as e:
        continue

sorted_plaintexts = sorted(probable_plaintexts, key=english_score, reverse=True)
chosen = sorted_plaintexts[0]

print(chosen)
