# -*- coding: utf-8 -*-
"""
https://codility.com/programmers/task/count_semiprimes/
A prime is a positive integer X that has exactly two distinct divisors: 1 and X. The first few prime integers are 2, 3, 5, 7, 11 and 13.

A semiprime is a natural number that is the product of two (not necessarily distinct) prime numbers. The first few semiprimes are 4, 6, 9, 10, 14, 15, 21, 22, 25, 26.

You are given two non-empty zero-indexed arrays P and Q, each consisting of M integers. These arrays represent queries about the number of semiprimes within specified ranges.

Query K requires you to find the number of semiprimes within the range (P[K], Q[K]), where 1 ≤ P[K] ≤ Q[K] ≤ N.

For example, consider an integer N = 26 and arrays P, Q such that:

    P[0] = 1    Q[0] = 26
    P[1] = 4    Q[1] = 10
    P[2] = 16   Q[2] = 20
The number of semiprimes within each of these ranges is as follows:

(1, 26) is 10,
(4, 10) is 4,
(16, 20) is 0.
Write a function:

def solution(N, P, Q)
that, given an integer N and two non-empty zero-indexed arrays P and Q consisting of M integers, returns an array consisting of M elements specifying the consecutive answers to all the queries.

For example, given an integer N = 26 and arrays P, Q such that:

    P[0] = 1    Q[0] = 26
    P[1] = 4    Q[1] = 10
    P[2] = 16   Q[2] = 20
the function should return the values [10, 4, 0], as explained above.

Assume that:

N is an integer within the range [1..50,000];
M is an integer within the range [1..30,000];
each element of arrays P, Q is an integer within the range [1..N];
P[i] ≤ Q[i].
Complexity:

expected worst-case time complexity is O(N*log(log(N))+M);
expected worst-case space complexity is O(N+M), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.
"""


from measure import measure

def get_primes1(N):
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
    return primes

def get_mults1(N, primes):
    n = 2
    mult = []
    while n * n <= N:
        if N % n == 0 and primes[n]:
            res = N / n
            if primes[res]:
                mult.append((n, res))
        n += 1
    return mult

def get_semi_primes1(N):
    primes = get_primes1(N)
    semi_primes = [False] * (N + 1)
    for i in range(N + 1):
        if primes[i]:
            continue
        mults = get_mults1(i, primes)
        for n1, n2 in mults:
            if primes[n1] and primes[n2]:
                semi_primes[i] = True
                break
    return semi_primes

@measure
def solution1(N, P, Q):
    if N <= 2:
        return [0] * len(P)
    semi_primes = get_semi_primes1(N)
    counts = []
    while P:
        left = P.pop()
        right = Q.pop()
        count = 0
        for i in range(left, right + 1):
            if semi_primes[i]:
                count += 1
        counts.append(count)
    return list(reversed(counts))


#************************************************
# O(N * log(log(N)) + M)
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

def get_semi_primes2(N):
    primes = get_primes2(N)
    L = len(primes)
    semi_primes = set()
    for i in range(L):
        for j in range(i, L):
            n1 = primes[i]
            n2 = primes[j]
            res = n1 * n2
            if res <= N:
                semi_primes.add(res)
            else:
                break

    return semi_primes

@measure
def solution2(N, P, Q):
    if N <= 2:
        return [0] * len(P)
    semi_primes = get_semi_primes2(N)
    res = {0: 0, 1: 0, 2: 0, 3: 0}
    count = 0
    for i in range(4, N + 1):
        if i in semi_primes:
            count += 1
        res[i] = count

    counts = []
    while P:
        left = P.pop()
        right = Q.pop()
        left_count = res[left - 1]
        right_count = res[right]
        count = right_count - left_count
        counts.append(count)
    return list(reversed(counts))


#**********************************************




"""
P = [1]
Q = [26]
N = 26
sol = solution2(N, P, Q)
print(sol)

"""

"""

"""
P = [1] * 3000
Q = [5000] * 3000
N = 5000

sol1 = solution1(N, P, Q)

P = [1] * 3000
Q = [5000] * 3000
N = 5000


sol2 = solution2(N, P, Q)


print(sol1==sol2) #True

print(measure.timers)
# {'solution2': 0.005789995193481445, 'solution1': 0.5880820751190186}
#print(measure.calls)
