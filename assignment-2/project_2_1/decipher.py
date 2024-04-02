from oracle import *
import sys

AES_BLOCK_SIZE = 128
BYTES_IN_BLOCK = AES_BLOCK_SIZE//8

def hex_to_bytes(hex_str: str) -> bytearray:
    return bytearray(bytes.fromhex(hex_str))

def bytes_to_hex(b: bytearray) -> str:
    return b.hex()

def hex_to_ctext(hex_str: str) -> list[int]:
    return [(int(hex_str[i:i+2],16)) for i in range(0, len(hex_str), 2)]

def hex_to_ptext(hex_str: str) -> str:
    return bytes.fromhex(hex_str).decode('ascii')

def oracle_send(hex_str: str) -> int:
    return Oracle_Send(hex_to_ctext(hex_str), len(hex_str) // (BYTES_IN_BLOCK*2))
#############################################################################
def padding_length(ciphertext: str) -> int:
    ciphertext = ciphertext[-AES_BLOCK_SIZE//2:]
    iv = ciphertext[:AES_BLOCK_SIZE//4]
    noniv = ciphertext[AES_BLOCK_SIZE//4:]
    ivbytes = hex_to_bytes(iv)
    nonpad = 0

    while True:
        ivbytes[nonpad] = 0
        failed = (oracle_send(bytes_to_hex(ivbytes)+noniv) == 0)
        if failed:
            break

        nonpad += 1
    
    return BYTES_IN_BLOCK - nonpad

def decipher_two_block_ct(ciphertext: str, padded: bool) -> str:
    noniv = ciphertext[BYTES_IN_BLOCK*2:]
    pl = padding_length(ciphertext) if padded else 0
    
    ptext_bytes = [0] * 16
    for i in range(BYTES_IN_BLOCK-pl, BYTES_IN_BLOCK):
        ptext_bytes[i] = pl

    for i in range(BYTES_IN_BLOCK-pl-1, -1, -1):
        iv = ciphertext[:BYTES_IN_BLOCK*2]
        ivbytes = hex_to_bytes(iv)
    
        for ii in range(i+1, BYTES_IN_BLOCK):
            ivbytes[ii] = ivbytes[ii] ^ ptext_bytes[ii] ^ (BYTES_IN_BLOCK - i)

        for byte in range(256):
            ivbytes[i] = byte 
            if oracle_send(bytes_to_hex(ivbytes)+noniv):
                break

        ptext_bytes[i] = (BYTES_IN_BLOCK - i) ^ byte ^ hex_to_bytes(iv)[i]

    # print(ptext_bytes)
    res = hex_to_ptext(bytes_to_hex(bytearray(ptext_bytes)[:BYTES_IN_BLOCK-pl]))

    return res


def decipher(ciphertext: str) -> str:
    Oracle_Connect()

    last_block = decipher_two_block_ct(ciphertext[BYTES_IN_BLOCK*2: BYTES_IN_BLOCK*2*2]
                                        + ciphertext[BYTES_IN_BLOCK*2*2:], True)
    second_block = decipher_two_block_ct(ciphertext[:BYTES_IN_BLOCK*2*2], False)

    Oracle_Disconnect()

    return second_block+last_block

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 decipher.py <ciphertext filename>")
        return

    file = open(sys.argv[1])
    ciphertext = file.read()
    file.close()

    print(decipher(ciphertext)) 

if __name__ == "__main__":
    main()
