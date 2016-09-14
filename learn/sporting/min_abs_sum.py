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


# Wrong approach. For example A = [3, 3, 3, 4, 5], 9 == 9. Gives wrong answer
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


#********************************
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

#********************************

# stud
def step4(A, n):
    if n == 0:
        return {A[0]}
    else:
        res = set()
        for a in step4(A, n - 1):
            res.add(abs(a - A[n]))
            res.add(abs(a + A[n]))
        return res

@measure
def solution4(A):
    if not A:
        return 0
    L = len(A)
    return min(step4(A, L - 1))


#***********************************

#81
@measure
def solution5(A):
    counts = {}
    for cur in A:
        if cur == 0:
            continue
        cur = abs(cur)
        counts[cur] = 1 if cur not in counts else counts[cur] + 1

    results = []
    for key in counts.keys():
        count = counts[key]
        start = 0 if count % 2 == 0 else key
        end = key * count
        step = key * 2
        results.append((start, end, step))

    final_results = {0}
    for start, end, step in results:
        new_final_results = set()
        for item in xrange(start, end + 1, step):
            for final_result in final_results:
                var1 = abs(final_result + item)
                var2 = abs(final_result - item)
                new_final_results.add(var1)
                new_final_results.add(var2)
        final_results = new_final_results

    return min(final_results)


#Obviously super slow
@measure
def solution6(A):
    L = len(A)
    n = 0
    for i in xrange(L):
        n += 2 ** i

    B = [abs(a) for a in A]
    S = sum(B)
    res = S
    bin_n = '{0:b}'.format(n)
    bin_n_len = len(bin_n)

    for i in xrange(n + 1):
        bn = '{0:b}'.format(i)
        cur_l = len(bn)
        if cur_l < bin_n:
            bn = '0' * (bin_n_len - cur_l) + bn
        cur_s = S
        for j in xrange(len(bn)):
            sym = bn[j]
            if sym == '1':
                cur_s -= B[j] * 2
        res = min(res, abs(cur_s))

    return res




def solution7(A):

    pass



#A = [1, 7, 6]
#print(sum([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]))
#A = [1, 2, 3]
#A = [1, 5, 2, -2, 1]
#A = [1]
#A = [2, 4, 6, 8, 14, 15]
#A = [11, 13, 14, 10, 12]
#print(sum(A))
#A = [2] * 6
#A = [3, 3, 3]
A = [1000, 1, 1, 1, 1, 1, 1] * 3
#A = [3, 3, 3, 4, 5] * 2

#{'solution2': 2.8848648071289062e-05, 'solution3': 0.00012493133544921875, 'solution1': 10.760171175003052}
#A = []

#sol1 = solution1(A)
#sol2 = solution2(A)
sol3 = solution3(A)
#sol4 = solution4(A)
#sol5 = solution5(A)
sol7 = solution7(A)
#print sol2, sol3, sol4, sol5
print sol7, sol3
print measure.timers
