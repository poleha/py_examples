# -*- coding: utf-8 -*-
"""
https://codility.com/programmers/task/count_non_divisible/
You are given a non-empty zero-indexed array A consisting of N integers.

For each number A[i] such that 0 ≤ i < N, we want to count the number of elements of the array that are not the divisors of A[i]. We say that these elements are non-divisors.

For example, consider integer N = 5 and array A such that:

    A[0] = 3
    A[1] = 1
    A[2] = 2
    A[3] = 3
    A[4] = 6
For the following elements:

A[0] = 3, the non-divisors are: 2, 6,
A[1] = 1, the non-divisors are: 3, 2, 3, 6,
A[2] = 2, the non-divisors are: 3, 3, 6,
A[3] = 3, the non-divisors are: 2, 6,
A[4] = 6, there aren't any non-divisors.
Write a function:

def solution(A)
that, given a non-empty zero-indexed array A consisting of N integers, returns a sequence of integers representing the amount of non-divisors.

The sequence should be returned as:

a structure Results (in C), or
a vector of integers (in C++), or
a record Results (in Pascal), or
an array of integers (in any other programming language).
For example, given:

    A[0] = 3
    A[1] = 1
    A[2] = 2
    A[3] = 3
    A[4] = 6
the function should return [2, 4, 3, 2, 0], as explained above.

Assume that:

N is an integer within the range [1..50,000];
each element of array A is an integer within the range [1..2 * N].
Complexity:

expected worst-case time complexity is O(N*log(N));
expected worst-case space complexity is O(N), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.
"""

from measure import measure
import random

# O(N ** 2)
@measure
def solution1(A):
    res = []
    for cur in A:
        count = 0
        for comp in A:
            if cur % comp != 0:
                count += 1
        res.append(count)
    return res

#*****************************************

# O(N ** 2) A little bit faster(way faster on repeated numbers)
from math import ceil
@measure
def solution2(A):
    L = len(A)
    B = sorted(A)
    res = []
    visited = {}
    counts = {}
    for cur in A:
        counts[cur] = counts[cur] + 1 if cur in counts else 1
    for cur in A:
        count = visited.get(cur, None)
        if count is None:
            count = 0
            left = L
            for comp in B:
                if comp > ceil(cur / 2):
                    minus = counts.get(cur, 0)
                    left -= minus
                    count += left
                    break
                elif cur % comp != 0:
                    count += 1
                left -= 1
            res.append(count)
            visited[cur] = count
        else:
            res.append(count)
    return res

#********************************

from math import sqrt, ceil


def get_divisors(N):
    n = int(ceil(sqrt(N)))
    divs = set()
    for i in range(1, n + 1):
        if N % i != 0:
            continue
        res = N / i
        divs.add(i)
        divs.add(res)
    return divs

@measure
def solution3(A):
    L = len(A)
    counts = {}
    divs = {}
    for cur in A:
        counts[cur] = counts[cur] + 1 if cur in counts else 1
        if cur not in divs:
            divs[cur] = get_divisors(cur)

    res_dict = {}
    for cur in A:
        left = L
        if cur in res_dict:
            continue
        for div in divs[cur]:
            count = counts.get(div, 0)
            left -= count
        res_dict[cur] = left

    res = []
    for cur in A:
        res.append(res_dict[cur])
    return res





"""
A = [3, 1, 2,3, 6, 4]
sol2 = solution2(A)
sol3 = solution3(A)
print(sol2, sol3)

"""
A = list(range(1, 10000))
random.shuffle(A)
sol1= solution1(A)
sol2 = solution2(A)
sol3 = solution3(A)
print(sol1 == sol2 == sol3)
print(measure.timers)










