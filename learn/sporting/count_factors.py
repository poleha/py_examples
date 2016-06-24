# -*- coding: utf-8 -*-
"""
https://codility.com/programmers/task/count_factors/
A positive integer D is a factor of a positive integer N if there exists an integer M such that N = D * M.

For example, 6 is a factor of 24, because M = 4 satisfies the above condition (24 = 6 * 4).

Write a function:

def solution(N)
that, given a positive integer N, returns the number of its factors.

For example, given N = 24, the function should return 8, because 24 has 8 factors, namely 1, 2, 3, 4, 6, 8, 12, 24. There are no other factors of 24.

Assume that:

N is an integer within the range [1..2,147,483,647].
Complexity:

expected worst-case time complexity is O(sqrt(N));
expected worst-case space complexity is O(1).
"""

from measure import measure

# O(N)
@measure
def solution1(N):
    count = 0
    for i in range(1, N + 1):
        if N % i == 0:
            count += 1
    return count


#**********************************
#O(sqrt(N))
from math import ceil, sqrt

@measure
def solution2(N):
    count = 0
    visited = set()
    n = int(ceil(sqrt(N)))
    for i in range(1, n + 1):
        if N % i == 0:
            res = N / i
            if res not in visited:
                count += 1
                visited.add(res)
            if i not in visited:
                count += 1
                visited.add(i)
    return count


#********************************
#O(sqrt(N))
@measure
def solution3(N):
    visited = set()
    n = int(ceil(sqrt(N)))
    for i in range(1, n + 1):
        if N % i == 0:
            res = N / i
            visited.add(res)
            visited.add(i)
    return len(visited)


"""
sol1 = solution1(4)
sol2 = solution2(4)
print(sol1, sol2)
"""

for N in range(30000):

    sol1 = solution1(N)
    sol2 = solution2(N)
    sol3 = solution3(N)
    if not (sol1 == sol2 == sol3):
        print (N, sol1, sol2, sol3)

print(measure.timers)
#{'solution2': 0.2852447032928467, 'solution3': 0.24821782112121582, 'solution1': 24.65558910369873}