
def eq(a, b):

    k = 1
    while a & 1 == 0 and b & 1 == 0:
        a >>= 1
        b >>= 1
        k <<= 1
    print(a, b, k)

    t = a if a & 1 == 0 else -b

    while t:
        while t & 1 == 0:
            t >>= 1
        if t > 0:
            a = t
        else:
            b = -t
        t = a - b
    return a * k


sol = eq(24, 9)
print(sol)