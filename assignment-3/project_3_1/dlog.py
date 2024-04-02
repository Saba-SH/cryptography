import math


# Find x such that g^x = h (mod p)
# 0 <= x <= max_x
def discrete_log(p, g, h, max_x):
	B = math.ceil(math.sqrt(max_x))
	
	lhs = [h]
	g_inv = pow(g, -1, p)
	for _ in range(1, B):
		lhs.append((lhs[-1] * g_inv) % p)
	lhs_dict = {e: i for i, e in enumerate(lhs)}	# h/g^x1(mod p) -> x1

	rhs = [1]
	g_B = pow(g, B, p)
	for x0 in range(B):
		if rhs[-1] in lhs_dict:
			return x0 * B + lhs_dict[rhs[-1]]
		else:
			rhs.append((rhs[-1] * g_B) % p)

def main():
	p = int(input().strip())
	g = int(input().strip())
	h = int(input().strip())
	max_x = 1 << 40 # 2^40

	dlog = discrete_log(p, g, h, max_x)
	print(dlog)

if __name__ == '__main__':
	main()
