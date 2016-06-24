# -*- coding: utf-8 -*-
"""
https://codility.com/programmers/task/max_profit/
A zero-indexed array A consisting of N integers is given. It contains daily prices of a stock share for a period of N consecutive days. If a single share was bought on day P and sold on day Q, where 0 ≤ P ≤ Q < N, then the profit of such transaction is equal to A[Q] − A[P], provided that A[Q] ≥ A[P]. Otherwise, the transaction brings loss of A[P] − A[Q].

For example, consider the following array A consisting of six elements such that:

  A[0] = 23171
  A[1] = 21011
  A[2] = 21123
  A[3] = 21366
  A[4] = 21013
  A[5] = 21367
If a share was bought on day 0 and sold on day 2, a loss of 2048 would occur because A[2] − A[0] = 21123 − 23171 = −2048. If a share was bought on day 4 and sold on day 5, a profit of 354 would occur because A[5] − A[4] = 21367 − 21013 = 354. Maximum possible profit was 356. It would occur if a share was bought on day 1 and sold on day 5.

Write a function,

def solution(A)
that, given a zero-indexed array A consisting of N integers containing daily prices of a stock share for a period of N consecutive days, returns the maximum possible profit from one transaction during this period. The function should return 0 if it was impossible to gain any profit.

For example, given array A consisting of six elements such that:

  A[0] = 23171
  A[1] = 21011
  A[2] = 21123
  A[3] = 21366
  A[4] = 21013
  A[5] = 21367
the function should return 356, as explained above.

Assume that:

N is an integer within the range [0..400,000];
each element of array A is an integer within the range [0..200,000].
Complexity:

expected worst-case time complexity is O(N);
expected worst-case space complexity is O(1), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.
"""

from measure import measure


# O(N ** 2)
@measure
def solution1(A):
    L = len(A)
    max_profit = 0
    for i in range(L - 1):
        for j in range(i, L):
            profit = A[j] - A[i]
            if profit > max_profit:
                max_profit = profit
    return max_profit


#O(N**2), но в 6 раз быстрее, чем 1
@measure
def solution2(A):
    L = len(A)
    mins = []
    maxs = []
    max_delta = 0
    for i in range(L):
        cur = A[i]
        nex = A[i + 1] if i < L - 1 else cur
        pre = A[i - 1] if i > 0 else nex
        if cur <= pre and cur <= nex:
            mins.append(i)
        elif cur >= nex and cur >= pre:
            maxs.append(i)
    for mn in mins:
        for mx in maxs:
            if mn <= mx:
                cur_delta = A[mx] - A[mn]
                if cur_delta > max_delta:
                    max_delta = cur_delta
    return max_delta

# O(N)
@measure
def solution3(A):
    L = len(A)
    mn = 0
    max_delta = 0
    for i in range(L):
        cur = A[i]
        nex = A[i + 1] if i < L - 1 else cur
        pre = A[i - 1] if i > 0 else nex
        if cur <= pre and cur <= nex:
            if A[i] < A[mn]:
                mn = i
        elif cur >= nex and cur >= pre:
            cur_delta = A[i] - A[mn]
            if cur_delta > max_delta:
                max_delta = cur_delta
    return max_delta



A = [23171, 21011, 21123, 21366, 21013, 21367] * 1000

sol1 = solution1(A)
sol2 = solution2(A)
sol3 = solution3(A)
print(sol1, sol2, sol3, sol1==sol2==sol3, measure.timers)
#(2160, 2160, 2160, True, {'solution2': 0.1962110996246338, 'solution3': 0.001104116439819336, 'solution1': 1.1574699878692627})