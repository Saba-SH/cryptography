import sys


def string_to_int(input_string: str) -> int:
    byte_array = bytes(ord(char) for char in input_string)
    return int.from_bytes(byte_array, byteorder='big')

def int_to_string(input_int: int) -> str:
    byte_array = input_int.to_bytes((input_int.bit_length() + 7) // 8, byteorder='big')
    return byte_array.decode('utf-8')

key_str = input().strip()
plaintext = input().strip()

key = string_to_int(key_str)

key_len = len(key_str)
chunk_count = len(plaintext) // key_len

ciphertext = ""

for i in range(chunk_count):
    chunk = plaintext[i*key_len:(i+1)*key_len]
    cipherchunk = int_to_string(string_to_int(chunk) ^ key).rjust(key_len, "\x00")
    ciphertext += cipherchunk

if len(plaintext) / key_len != chunk_count:
    last_chunk = plaintext[(chunk_count)*key_len:]
    key_chunk_str = key_str[0:len(last_chunk)]
    cipherchunk = int_to_string(string_to_int(last_chunk) ^ string_to_int(key_chunk_str)).rjust(len(last_chunk), "\x00")
    ciphertext += cipherchunk

print(ciphertext.encode('utf-8').hex())
