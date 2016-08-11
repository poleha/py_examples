# -*- coding: utf-8 -*-
"""
https://codility.com/programmers/task/min_abs_sum/
For a given array A of N integers and a sequence S of N integers from the set {−1, 1}, we define val(A, S) as follows:

val(A, S) = |sum{ A[i]*S[i] for i = 0..N−1 }|
(Assume that the sum of zero elements equals zero.)

For a given array A, we are looking for such a sequence S that minimizes val(A,S).

Write a function:

def solution(A)
that, given an array A of N integers, computes the minimum value of val(A,S) from all possible values of val(A,S) for all possible sequences S of N integers from the set {−1, 1}.

For example, given array:

  A[0] =  1
  A[1] =  5
  A[2] =  2
  A[3] = -2
your function should return 0, since for S = [−1, 1, −1, 1], val(A, S) = 0, which is the minimum possible value.

Assume that:

N is an integer within the range [0..20,000];
each element of array A is an integer within the range [−100..100].
Complexity:

expected worst-case time complexity is O(N*max(abs(A))2);
expected worst-case space complexity is O(N+sum(abs(A))), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.
"""

from measure import measure

# stud
# Obvioulsly slow, but I love recursions
def step(A, L, i, cur):
    cur1 = cur + A[i]
    cur2 = cur - A[i]
    if i < L - 1:
        var1 = step(A, L, i + 1, cur1)
        var2 = step(A, L, i + 1, cur2)
        return min(var1, var2)
    else:
        return min(abs(cur1), abs(cur2))

@measure
def solution1(A):
    if not A:
        return 0
    L = len(A)
    var = step(A, L, 0, 0)
    return var

#*********************************************************


# Wrong approach. For example A = [3, 3, 3, 4, 5], 9 == 9
# 90%
@measure
def solution2(A):
    if not A:
        return 0
    L = len(A)
    if L == 1:
        return abs(A[0])
    B = [abs(cur) for cur in A]
    B = sorted(B, reverse=True)
    i = 0
    res = left = B[0]
    mn = None
    right = sum(B) - left
    while i < L - 1:
        i += 1
        cur = B[i]
        left += cur
        right -= cur
        if mn is None or abs(left - right) < mn:
            mn = abs(left - right)
        res = abs(abs(res) - abs(cur))
    return min(res, mn)


@measure
# 72%, correct but not fast enough
def solution3(A):
    steps = {0}
    for cur in A:
        new_steps = set()
        for step in steps:
            step1 = abs(step + cur)
            step2 = abs(step - cur)
            new_steps.add(step1)
            new_steps.add(step2)
        steps = new_steps
    return min(steps)





#A = [1, 2, 3]
#A = [1, 5, 2, -2, 1]
#A = []
A = [3, 3, 3, 4, 5] * 5
#{'solution2': 2.8848648071289062e-05, 'solution3': 0.00012493133544921875, 'solution1': 10.760171175003052}
#A = []

sol1 = solution1(A)
sol2 = solution2(A)
sol3 = solution3(A)
print sol1, sol2, sol3
print measure.timers
