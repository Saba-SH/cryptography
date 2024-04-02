def ascii_to_int(m):
    val = ""
    for x in m:
        val += hex(ord(x))[2:]
    return int("0x" + val,16)

def ascii_to_bin(m):
    val = ""
    for x in m:
        val += bin(ord(x))[2:].zfill(8)
    return val

def lowest_divisor(n: int) -> int:
    for d in range(2, int(n**0.5 + 1)):
        if n % d == 0:
            return d
    
    return n
