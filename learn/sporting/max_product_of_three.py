# -*- coding: utf-8 -*-
"""
https://codility.com/programmers/task/max_product_of_three/
A non-empty zero-indexed array A consisting of N integers is given. The product of triplet (P, Q, R) equates to A[P] * A[Q] * A[R] (0 ≤ P < Q < R < N).

For example, array A such that:

  A[0] = -3
  A[1] = 1
  A[2] = 2
  A[3] = -2
  A[4] = 5
  A[5] = 6
contains the following example triplets:

(0, 1, 2), product is −3 * 1 * 2 = −6
(1, 2, 4), product is 1 * 2 * 5 = 10
(2, 4, 5), product is 2 * 5 * 6 = 60
Your goal is to find the maximal product of any triplet.

Write a function:

def solution(A)
that, given a non-empty zero-indexed array A, returns the value of the maximal product of any triplet.

For example, given array A such that:

  A[0] = -3
  A[1] = 1
  A[2] = 2
  A[3] = -2
  A[4] = 5
  A[5] = 6
the function should return 60, as the product of triplet (2, 4, 5) is maximal.

Assume that:

N is an integer within the range [3..100,000];
each element of array A is an integer within the range [−1,000..1,000].
Complexity:

expected worst-case time complexity is O(N*log(N));
expected worst-case space complexity is O(1), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.
"""

# O(N ** 3)
def solution1(A):
    L = len(A)
    max_triplet = None
    for P in range(L - 2):
        for Q in range(P + 1, L - 1):
            for R in range(Q + 1, L):
                triplet = A[P] * A[Q] * A[R]
                if triplet > max_triplet or max_triplet is None:
                    max_triplet = triplet
    return max_triplet

def solution2(A):
    abs_a = []

    counters = {i:0 for i in A}
    for cur in A:
        counters[cur] += 1
        abs_a.append(abs(cur))

    abs_a = sorted(abs_a, reverse=True)

    L = len(abs_a)
    triplets = []
    for i in range(L - 2):
        a_p = abs_a[i]
        a_q = abs_a[i + 1]
        a_r = abs_a[i + 2]
        triplet = a_p * a_q * a_r
        triplets.append((triplet, a_p, a_q, a_r))

    for triplet, a_p, a_q, a_r in triplets:
        a_p_sign = a_q_sign = a_r_sign = -1
        if a_p in counters:
            a_p_sign = 1
        if a_q in counters:
            a_q_sign = 1
        if a_r in counters:
            a_r_sign = 1
        triplet_sign = a_p_sign * a_q_sign * a_r_sign
        if triplet > 0 and triplet_sign > 0:
            return triplet




A = [-3, 1, 2, -2, 5, 6]
#A = [-5, -6, -4, -7, -10]
sol = solution2(A)
print(sol)