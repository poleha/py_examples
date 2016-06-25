# -*- coding: utf-8 -*-
"""
https://codility.com/media/train/9-Sieve.pdf
"""

# Lets find all prime numbers (простые) from 2 to N


from measure import measure

@measure
def get_primes1(N):
    A = set(range(2, N + 1))
    firsts = set()
    n = 2
    while n * n < N:
        n = min(A)
        first = True
        cur = n
        firsts.add(n)
        while cur <= N:
            if cur in A:
                A.remove(cur)
            if first:
                cur = cur * cur
                first = False
            else:
                cur += n

    A.update(firsts)
    return A

@measure
def get_primes2(N):
    primes = [True] * (N + 1)
    A = list(range(2, N + 1))
    i = 0
    while i * i <= N:
        n = A[i]
        first = True
        cur = n
        while cur <= N:
            if not first:
                primes[cur] = False
            if first:
                cur = n * n
                first = False
            else:
                cur += n
        i += 1
    res_primes = []
    for i in range(2, N + 1):
        if primes[i] == True:
            res_primes.append(i)

    return res_primes


N = 2000000

sol1 = get_primes1(N)
sol2 = get_primes2(N)
print(len(sol1) == len(sol2)) # True
print(measure.timers)
#{'get_primes2': 1.642176866531372, 'get_primes1': 3.84108304977417}
