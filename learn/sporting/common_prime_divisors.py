# -*- coding: utf-8 -*-
"""
https://codility.com/demo/results/trainingUYCYDF-9TR/
A prime is a positive integer X that has exactly two distinct divisors: 1 and X. The first few prime integers are 2, 3, 5, 7, 11 and 13.

A prime D is called a prime divisor of a positive integer P if there exists a positive integer K such that D * K = P. For example, 2 and 5 are prime divisors of 20.

You are given two positive integers N and M. The goal is to check whether the sets of prime divisors of integers N and M are exactly the same.

For example, given:

N = 15 and M = 75, the prime divisors are the same: {3, 5};
N = 10 and M = 30, the prime divisors aren't the same: {2, 5} is not equal to {2, 3, 5};
N = 9 and M = 5, the prime divisors aren't the same: {3} is not equal to {5}.
Write a function:

def solution(A, B)
that, given two non-empty zero-indexed arrays A and B of Z integers, returns the number of positions K for which the prime divisors of A[K] and B[K] are exactly the same.

For example, given:

    A[0] = 15   B[0] = 75
    A[1] = 10   B[1] = 30
    A[2] = 3    B[2] = 5
the function should return 1, because only one pair (15, 75) has the same set of prime divisors.

Assume that:

Z is an integer within the range [1..6,000];
each element of arrays A, B is an integer within the range [1..2,147,483,647].
Complexity:

expected worst-case time complexity is O(Z*log(max(A)+max(B))2);
expected worst-case space complexity is O(1), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.
"""

from measure import measure


@measure
def get_gd(u, v):
    while v:
        u, v = v, u % v
    return abs(u)


# Делим rest на общий делитель пока не получим единицу. Если не делится и rest > 1, значит мимо.
@measure
def check_gd_and_rest(gd, rest):
    while rest > 1:
        new_gd = get_gd(gd, rest)
        if new_gd > 1:
            rest = rest / new_gd
            return check_gd_and_rest(gd, rest)
        else:
            return False
    if rest > 1:
        return False
    else:
        return True


@measure
def solution(A, B):
    L = len(A)
    count = 0

    for i in range(L):
        a = A[i]
        b = B[i]
        gd = get_gd(a, b)
        rest_a = a / gd
        rest_b = b / gd

        if check_gd_and_rest(gd, rest_a) and check_gd_and_rest(gd, rest_b):
            count += 1

    return count


A = [2 * 3 * 5 * 5 * 5 * 3 * 2 * 7]
B = [2 * 3 * 5 * 3]
sol = solution(A, B)
print(sol)

print(measure.timers)
print(measure.calls)

"""

# 76%. Need ti be little faster

cached_primes = {}

@measure
def get_primes(N):
    res = cached_primes.get(N, None)
    if res is None:
        primes = [True for _ in range(N + 2)]
        i = 1
        while i * i <= N:
            i += 1
            if primes[i] == False:
                continue
            first = True
            j = i
            while j <= N:
                if first:
                    j = j * j
                    first = False
                else:
                    j += i
                if j <= N:
                    primes[j] = False
        res = set()
        for i in range(2, N + 1):
            if primes[i]:
                res.add(i)
        cached_primes[N] = res
    return res

@measure
def get_gd(a, b):
    if b > a:
        a, b = b, a
    if a == b:
        return a
    else:
        mod = a % b
        if mod == 0:
            return b
        else:
            return get_gd(b, mod)


@measure
def solution(A, B):
    L = len(A)
    count = 0
    for i in range(L):
        a = A[i]
        b = B[i]
        gd = get_gd(a, b)
        rest_a = a / gd
        rest_b = b / gd
        left_primes = get_primes(rest_a)


        left_primes_ok = True
        for left_prime in left_primes:
            if gd % left_prime != 0 and rest_a % left_prime == 0:
                left_primes_ok = False
                break


        if left_primes_ok:
            right_primes_ok = True
            right_primes = get_primes(rest_b)
            for right_prime in right_primes:
                if gd % right_prime != 0 and rest_b % right_prime == 0:
                    right_primes_ok = False
                    break


        if left_primes_ok and right_primes_ok:
            count += 1


    return count
"""

"""
# 84 %

@measure
def get_primes(N):
    primes = set()
    i = 1
    while i < N:
        i += 1
        if i in primes:
            continue
        j = i
        first = True
        if N % i == 0:
            yield i
        while j <= N:
            primes.add(j)

            if first:
                j *= j
                first = False
            else:
                j += i


@measure
def get_gd(a, b):
    if b > a:
        a, b = b, a
    if a == b:
        return a
    else:
        mod = a % b
        if mod == 0:
            return b
        else:
            return get_gd(b, mod)


@measure
def solution(A, B):
    L = len(A)
    count = 0
    for i in range(L):
        a = A[i]
        b = B[i]
        gd = get_gd(a, b)
        rest_a = a / gd
        rest_b = b / gd

        left_primes_ok = True
        for left_prime in get_primes(rest_a):
            if gd % left_prime != 0:
                left_primes_ok = False
                break


        if left_primes_ok:
            right_primes_ok = True
            for right_prime in get_primes(rest_b):
                if gd % right_prime != 0:
                    right_primes_ok = False
                    break


        if left_primes_ok and right_primes_ok:
            count += 1

    return count
"""

"""
# 69%

@measure
def get_primes(N):
    primes = set()
    i = 1
    while i < N:
        i += 1
        if i in primes:
            continue
        j = i
        first = True
        if N % i == 0:
            yield i
        while j <= N:
            primes.add(j)

            if first:
                j *= j
                first = False
            else:
                j += i


@measure
def get_gd(a, b):
    if b > a:
        a, b = b, a
    if a == b:
        return a
    else:
        mod = a % b
        if mod == 0:
            return b
        else:
            return get_gd(b, mod)


@measure
def solution(A, B):
    L = len(A)
    count = 0
    for i in range(L):
        a = A[i]
        b = B[i]
        gd = get_gd(a, b)
        rest_a = a / gd
        rest_b = b / gd

        for prime in get_primes(gd):
            if rest_a == 1 and rest_b == 1:
                break
            while rest_a > 1:
                if rest_a % prime == 0:
                    rest_a = rest_a / prime
                else:
                    break
            while rest_b > 1:
                if rest_b % prime == 0:
                    rest_b = rest_b / prime
                else:
                    break

        if rest_a == 1 and rest_b == 1:
            count += 1

    return count


"""
