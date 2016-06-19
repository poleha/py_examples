# -*- coding: utf-8 -*-
"""
https://codility.com/programmers/task/min_avg_two_slice/
A non-empty zero-indexed array A consisting of N integers is given. A pair of integers (P, Q), such that 0 ≤ P < Q < N, is called a slice of array A (notice that the slice contains at least two elements). The average of a slice (P, Q) is the sum of A[P] + A[P + 1] + ... + A[Q] divided by the length of the slice. To be precise, the average equals (A[P] + A[P + 1] + ... + A[Q]) / (Q − P + 1).

For example, array A such that:

    A[0] = 4
    A[1] = 2
    A[2] = 2
    A[3] = 5
    A[4] = 1
    A[5] = 5
    A[6] = 8
contains the following example slices:

slice (1, 2), whose average is (2 + 2) / 2 = 2;
slice (3, 4), whose average is (5 + 1) / 2 = 3;
slice (1, 4), whose average is (2 + 2 + 5 + 1) / 4 = 2.5.
The goal is to find the starting position of a slice whose average is minimal.

Write a function:

def solution(A)
that, given a non-empty zero-indexed array A consisting of N integers, returns the starting position of the slice with the minimal average. If there is more than one slice with a minimal average, you should return the smallest starting position of such a slice.

For example, given array A such that:

    A[0] = 4
    A[1] = 2
    A[2] = 2
    A[3] = 5
    A[4] = 1
    A[5] = 5
    A[6] = 8
the function should return 1, as explained above.

Assume that:

N is an integer within the range [2..100,000];
each element of array A is an integer within the range [−10,000..10,000].
Complexity:

expected worst-case time complexity is O(N);
expected worst-case space complexity is O(N), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.
"""

import os

# O(N ** 3)
def solution1(A):
    L = len(A)
    min_average = None
    min_start = None
    for start in range(L - 1): # Start position
        for length in range(2, L + 1 - start): # Length
            cur_slice = A[start: start + length]
            average = sum(cur_slice) / float(length)
            if min_average is None or average < min_average:
                min_average = average
                min_start = start
    return min_start

# O(N ** 2)
def solution2(A):
    L = len(A)
    min_average = None
    min_start = None
    for start in range(L - 1): # Start position
        cur_sum = A[start] + A[start + 1]
        average = cur_sum / float(2)
        if min_average is None or average < min_average:
            min_average = average
            min_start = start

        for length in range(3, L + 1 - start): # Length
            cur = A[start + length - 1]
            cur_sum += cur
            average = cur_sum / float(length)
            if min_average is None or average < min_average:
                min_average = average
                min_start = start
    return min_start

#**************************
"""
def prefix_sums(A):
    L = len(A)
    P = [0] * (L + 1)
    for i in range(1, L + 1):
        P[i] = P[i - 1] + A[i - 1]
    return P
"""

# Фокус а том, чтобы заметить, что самое меньшая средняя последовательность может быть длиной не более 3. Если более,
# то она превращается в последовательность из 2, меньшую. Нашел по сути методом тыка. То есть сделал простое решение
# и оно мне показало минимальные последовательности
#O (N)
def solution3(A):
    L = len(A)
    min_average = None
    min_start = None
    for i in range(0, L - 1):
        average2 = (A[i] + A[i + 1]) / float(2)
        average3 = (A[i] + A[i + 1] + A[i + 2]) / float(3) if (i + 2) < L else average2
        average = min(average2, average3)
        if min_average is None or average < min_average:
            min_average = average
            min_start = i
    return min_start







A = [4, -2, 2, -3, 2, 4, 2, 2]
#A = [2,2,2]
#A = [10, 10, -1, 2, 4, -1, 2, -1]
#res1 = solution1(A)
res = solution3(A)
#print(res)
#os._exit(0)


import random

for L in range(2, 100):
    A = []
    for i in range(8):
        s = round(random.random() * 2)
        s = -1 if s == 0 else 1
        cur = int(s * round(random.random() * 5))
        A.append(cur)
    res1 = solution1(A)
    res2 = solution2(A)
    res3 = solution3(A)
    if res1 != res3:
        print(A, res1, res2, res3)



