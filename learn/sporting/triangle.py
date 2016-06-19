# -*- coding: utf-8 -*-
"""
https://codility.com/programmers/task/triangle/
A zero-indexed array A consisting of N integers is given. A triplet (P, Q, R) is triangular if 0 ≤ P < Q < R < N and:

A[P] + A[Q] > A[R],
A[Q] + A[R] > A[P],
A[R] + A[P] > A[Q].
For example, consider array A such that:

  A[0] = 10    A[1] = 2    A[2] = 5
  A[3] = 1     A[4] = 8    A[5] = 20
Triplet (0, 2, 4) is triangular.

Write a function:

def solution(A)
that, given a zero-indexed array A consisting of N integers, returns 1 if there exists a triangular triplet for this array and returns 0 otherwise.

For example, given array A such that:

  A[0] = 10    A[1] = 2    A[2] = 5
  A[3] = 1     A[4] = 8    A[5] = 20
the function should return 1, as explained above. Given array A such that:

  A[0] = 10    A[1] = 50    A[2] = 5
  A[3] = 1
the function should return 0.

Assume that:

N is an integer within the range [0..100,000];
each element of array A is an integer within the range [−2,147,483,648..2,147,483,647].
Complexity:

expected worst-case time complexity is O(N*log(N));
expected worst-case space complexity is O(N), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.
"""

def check(A, P, Q, R):
    return A[P] + A[Q] > A[R] and A[Q] + A[R] > A[P] and A[R] + A[P] > A[Q]

# O(N ** 3)
def solution1(A):
    l = len(A)
    for P in range(l - 2):
        for Q in range(P + 1, l - 1):
            for R in range(Q + 1, l):
                if check(A, P, Q, R):
                    return 1
    return 0

# O(N*log(N))
# Раз ни один элемент не может быть больше двух других, то когда мы отсотируем, проверяем первые 3 по порядку.
# Если да - вернули 1. Если нет, то далее перебирать R смысла нет. Представит три числа, a1, a2, a3 отсорт.
# Суть в разнице между первым, вторым и третим. Двигая второе и третье вправо, мы будем увеличивать разницу.
def solution(A):
    A = sorted(A)
    l = len(A)
    for P in range(0, l - 2):
        if check(A, P, P + 1, P + 2):
            return 1
    return 0


#A = [10, 2, 5, 1, 8, 20]
A = [10, 50, 5, 1]
sol = solution(A)
print(sol)