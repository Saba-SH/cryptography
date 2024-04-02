str_hex_0 = input().strip()
str_hex_1 = input().strip()

str_hex_result = hex(int(str_hex_0, 16) ^ int(str_hex_1, 16))[2:]

print(str_hex_result)
