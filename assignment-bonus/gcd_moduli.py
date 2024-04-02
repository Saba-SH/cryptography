import gmpy2
import random 


def pow2(n):
    return 2 ** (n.bit_length() - 1)


def one_pair(Ns, gcds_with_rest):
    assert len(Ns) == len(gcds_with_rest)

    for i in range(len(Ns)):
        N = Ns[i]
        if gcds_with_rest[i] not in (1, Ns[i]):
            a = int(str(N))
            g = int(str(gcds_with_rest[i]))

            for ii in range(len(Ns)):
                if ii != i and Ns[ii] % g == 0:
                    b = Ns[ii]
                    break

            return ((a, g, a//g), (b, g, b//g))
        
    return None


def gcd_with_rest(lst):
    n = len(lst)

    if n == 2:
        return [gmpy2.gcd(lst[0], lst[1]), gmpy2.gcd(lst[0], lst[1])]
    
    prods = [gmpy2.mul(lst[i], lst[i + 1]) for i in range(0, n, 2)]
    
    rs = gcd_with_rest(prods)

    res = []

    for i in range(n):
        if i % 2 == 0:
            res.append(gmpy2.gcd(lst[i], gmpy2.mul(rs[i//2], lst[i+1])))
        else:
            res.append(gmpy2.gcd(gmpy2.gcd(lst[i], gmpy2.mul(rs[i//2], lst[i-1]))))

    return res


def main():
    Ns = []

    a = int(input())
    for _ in range(a):
        Ns.append(gmpy2.mpz(int(input(), 16)))

    p = pow2(len(Ns))

    if p != len(Ns):
        Ns = random.sample(Ns, p)

    gcds = gcd_with_rest(Ns)

    # for i in range(len(Ns)):
    #     print(f"{Ns[i]}: {gcds[i]}")

    pair = one_pair(Ns, gcds)
    
    if pair is not None:
        print(pair[0][0])
        print(pair[0][1])
        print(pair[0][2])
        print()
        print(pair[1][0])
        print(pair[1][1])
        print(pair[1][2])
    else:
        print(None)


if __name__ == "__main__":
    main()
