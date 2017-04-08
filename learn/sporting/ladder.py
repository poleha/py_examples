# -*- coding: utf-8 -*-
"""
#Fibonacci

https://codility.com/programmers/task/ladder/
You have to climb up a ladder. The ladder has exactly N rungs, numbered from 1 to N. With each step, you can ascend by one or two rungs. More precisely:

with your first step you can stand on rung 1 or 2,
if you are on rung K, you can move to rungs K + 1 or K + 2,
finally you have to stand on rung N.
Your task is to count the number of different ways of climbing to the top of the ladder.

For example, given N = 4, you have five different ways of climbing, ascending by:

1, 1, 1 and 1 rung,
1, 1 and 2 rungs,
1, 2 and 1 rung,
2, 1 and 1 rungs, and
2 and 2 rungs.
Given N = 5, you have eight different ways of climbing, ascending by:

1, 1, 1, 1 and 1 rung,
1, 1, 1 and 2 rungs,
1, 1, 2 and 1 rung,
1, 2, 1 and 1 rung,
1, 2 and 2 rungs,
2, 1, 1 and 1 rungs,
2, 1 and 2 rungs, and
2, 2 and 1 rung.
The number of different ways can be very large, so it is sufficient to return the result modulo 2P, for a given integer P.

Write a function:

def solution(A, B)
that, given two non-empty zero-indexed arrays A and B of L integers, returns an array consisting of L integers specifying the consecutive answers; position I should contain the number of different ways of climbing the ladder with A[I] rungs modulo 2B[I].

For example, given L = 5 and:

    A[0] = 4   B[0] = 3
    A[1] = 4   B[1] = 2
    A[2] = 5   B[2] = 4
    A[3] = 5   B[3] = 3
    A[4] = 1   B[4] = 1
the function should return the sequence [5, 1, 8, 0, 1], as explained above.

Assume that:

L is an integer within the range [1..30,000];
each element of array A is an integer within the range [1..L];
each element of array B is an integer within the range [1..30].
Complexity:

expected worst-case time complexity is O(L);
expected worst-case space complexity is O(L), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.
"""


from measure import measure

# For fun via recursion
def count1(N, s=0):
    if s < N:
        res1 = count1(N, s + 1)
        res2 = count1(N, s + 2)
        return res1 + res2
    elif s == N:
        return 1
    else:
        return 0
def solution1(A, B):
    L = len(A)
    res = []
    for i in range(L):
        a = A[i]
        b = B[i]
        cur = count1(a)
        cur = int(cur % (2 ** b))
        res.append(cur)

    return res

#***********************************
from math import sqrt

# Подойдет только для малых чисел, так как на больших округление все портит
def count2(N):
    s = sqrt(5)
    a = (((1 + s) / 2) ** N - ((1 - s) / 2) ** N) / s
    return int(a)

def solution2(A, B):
    L = len(A)
    res = []
    for i in range(L):
        a = A[i]
        b = B[i]
        cur = count2(a + 1)
        cur = int(cur % (2 ** b))
        res.append(cur)

    return res

#**********************************
matrices = {}

@measure
def get_path(N):
    cur = 1
    path = []
    while N > 0:
        while cur <= N:
            nex = cur * 2
            if nex > N:
                path.append(cur)
                N -= cur
                cur = 1
            else:
                cur = nex
    return path

@measure
def multiply_matrices(A, B):
    C = []
    a11 = A[0] * B[0] + A[1] * B[2]
    a12 = A[0] * B[1] + A[1] * B[3]
    a13 = A[2] * B[0] + A[3] * B[2]
    a14 = A[2] * B[1] + A[3] * B[3]
    C.append(a11)
    C.append(a12)
    C.append(a13)
    C.append(a14)
    return C

@measure
def power_matrix(n):
    res_matrix = matrices.get(n, None)
    i = 1
    if res_matrix is None:
        matrix = [1, 1, 1, 0]
        while i < n:
            i *= 2
            matrix = multiply_matrices(matrix, matrix)
        res_matrix = matrix
        matrices[n] = matrix
    return res_matrix

@measure
def count3(N):
    path = get_path(N)
    matrix1 = power_matrix(path[0])
    for i in range(1, len(path)):
        cur_path = path[i]
        matrix2 = power_matrix(cur_path)
        matrix1 = multiply_matrices(matrix1, matrix2)
    return matrix1[2]


@measure
def solution3(A, B):
    L = len(A)
    res = []
    for i in range(L):
        a = A[i]
        b = B[i]
        cur = count3(a + 1)
        cur = int(cur % (2 ** b))
        res.append(cur)

    return res


#********************************************


def fib(N):
    a1 = 0
    a2 = 1
    res = [0, 1]
    for cur in range(N):
        a3 = a1 + a2
        a1 = a2
        a2 = a3
        res.append(a3)
    return res


def solution4(A, B):
    L = len(A)
    res = []

    mx = 0
    for i in range(L):
        a = A[i]
        mx = max(a, mx)
    f = fib(mx + 1)
    for i in range(L):
        a = A[i]
        b = B[i]
        cur = f[a + 1]
        cur = int(cur) % (2 ** b)
        res.append(cur)

    return res


A = [10] * 7
B = [2] * 7
sol1 = solution1(A, B)
sol2 = solution2(A, B)
sol3 = solution4(A, B)
print(sol1 == sol2 == sol3)

print(measure.timers)
