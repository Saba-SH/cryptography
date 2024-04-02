from oracle import *
import sys

BITS_IN_BLOCK = 128
BYTES_IN_BLOCK = BITS_IN_BLOCK//8

def bytes_to_hex(b: bytearray) -> str:
    return b.hex()

def xor_str_with_bytes(str_: str, bytes_: bytearray) -> str:
    return ''.join([chr(ord(char) ^ byte) for char, byte in zip(str_, bytes_)])
#############################################################################
def forge_tag(message: str) -> bytearray:
    tags = [bytearray([0])]

    tags.append(Mac(message[:BYTES_IN_BLOCK*2], BYTES_IN_BLOCK*2))
    block_start_index = BYTES_IN_BLOCK*2

    while block_start_index < len(message):
        last_tag = tags[-1]
        tags.append(Mac(xor_str_with_bytes(
                                    message[block_start_index: block_start_index+BYTES_IN_BLOCK],
                                    last_tag
                        ) + message[block_start_index+BYTES_IN_BLOCK: block_start_index+BYTES_IN_BLOCK*2]
                        , BYTES_IN_BLOCK*2))
        
        block_start_index += BYTES_IN_BLOCK*2
    
    return tags[-1]

def main():
    if len(sys.argv) < 2:
        print("Usage: python forge.py <filename>")
        sys.exit(-1)
    
    f = open(sys.argv[1])
    message = f.read()
    f.close()

    Oracle_Connect()
    tag = forge_tag(message)
    print(bytes_to_hex(tag))
    Oracle_Disconnect()


if __name__ == "__main__":
    main()
