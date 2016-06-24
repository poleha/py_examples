# -*- coding: utf-8 -*-
"""
https://codility.com/programmers/task/max_double_slice_sum/
A non-empty zero-indexed array A consisting of N integers is given.

A triplet (X, Y, Z), such that 0 ≤ X < Y < Z < N, is called a double slice.

The sum of double slice (X, Y, Z) is the total of A[X + 1] + A[X + 2] + ... + A[Y − 1] + A[Y + 1] + A[Y + 2] + ... + A[Z − 1].

For example, array A such that:

    A[0] = 3
    A[1] = 2
    A[2] = 6
    A[3] = -1
    A[4] = 4
    A[5] = 5
    A[6] = -1
    A[7] = 2
contains the following example double slices:

double slice (0, 3, 6), sum is 2 + 6 + 4 + 5 = 17,
double slice (0, 3, 7), sum is 2 + 6 + 4 + 5 − 1 = 16,
double slice (3, 4, 5), sum is 0.
The goal is to find the maximal sum of any double slice.

Write a function:

def solution(A)
that, given a non-empty zero-indexed array A consisting of N integers, returns the maximal sum of any double slice.

For example, given:

    A[0] = 3
    A[1] = 2
    A[2] = 6
    A[3] = -1
    A[4] = 4
    A[5] = 5
    A[6] = -1
    A[7] = 2
the function should return 17, because no double slice of array A has a sum of greater than 17.

Assume that:

N is an integer within the range [3..100,000];
each element of array A is an integer within the range [−10,000..10,000].
Complexity:

expected worst-case time complexity is O(N);
expected worst-case space complexity is O(N), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.
"""

from measure import measure

# O(N ** 4) or O(N ** 3)
def count_sum(A, X, Y, Z):
    s = 0
    for i in range(X + 1, Z):
        if i == Y:
            continue
        cur = A[i]
        s += cur
    return s

@measure
def solution1(A):
    L = len(A)
    max_sum = None
    for X in range(L - 2):
        for Y in range(X + 1, L - 1):
            for Z in range(Y + 1, L):
                cur_sum = count_sum(A, X, Y, Z)
                if max_sum is None or cur_sum > max_sum:
                    max_sum = cur_sum
    return max_sum

#*************************************
# O(N)
def get_nearest_max(A, reversed=False):
    L = len(A)
    maximums = {}
    cur_max = 0
    if reversed:
        r = range(L - 1, -1, -1)
    else:
        r = range(L)
    prev = 0
    for i in r:
        cur = A[i]
        cur_max = max(0, cur_max + prev)
        maximums[i] = cur_max
        prev = cur
    return maximums

@measure
def solution2(A):
    B = A[1: -1]
    L = len(B)
    left_maximums = get_nearest_max(B)
    right_maximums = get_nearest_max(B, True)

    mx = 0
    for i in range(L):
        cur_max = left_maximums[i] + right_maximums[i]
        mx = max(mx, cur_max)

    return mx
A = [5, 4, -4, -3, 2, 3, 4]
"""
sol1 = solution1(A)
sol2 = solution2(A)
print(sol1, sol2)
"""
import math, random
for k in range(1000):
    A = []
    for n in range(30):
        s = random.choice((-1, 1))
        A.append(int(s * math.ceil(random.random() * 50)))
    s1 = solution1(A)
    s2 = solution2(A)
    dif = s1 - s2
    if dif != 0:
        print(A, s1, s2)

print(measure.timers)
#{'solution2': 0.02226710319519043, 'solution1': 5.231168508529663}