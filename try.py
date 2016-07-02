from math import ceil

A = [1, 2, 3, 4, 5]

def get_prefixed_sums(A, L):
    sums = {}
    s = 0
    for i in range(L):
        cur = A[i]
        s += cur
        sums[i] = s

    return sums

sums = get_prefixed_sums(A, len(A))

L = len(A)

mid = sum(A) / L

def bin_search(A, sums, start, mx, s=0, pos=0):
    if pos == 0:
        pos = int(ceil(mx / mid))
    end = min(start + pos, L - 1)
    sm = sums[end] - sums[start] + A[start]
    if sm == mx:
        return sm, end
    elif sm < mx:
        delta = int(ceil(mx - s) / mid)
        pos += delta
        res = bin_search(A, sums, start, mx, s, pos)
    else:
        if sm - A[end] < mx:
            return sm - A[end], pos -1
        delta = int(ceil(mx - s) / mid)
        pos -= delta
        res = bin_search(A, sums, start, mx, s, pos)
    return res


res = bin_search(A, sums, 0, 4)

print(res)



