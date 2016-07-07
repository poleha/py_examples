# -*- coding: utf-8 -*-
"""
https://codility.com/programmers/task/count_triangles/
A zero-indexed array A consisting of N integers is given. A triplet (P, Q, R) is triangular if it is possible to build a triangle with sides of lengths A[P], A[Q] and A[R]. In other words, triplet (P, Q, R) is triangular if 0 ≤ P < Q < R < N and:

A[P] + A[Q] > A[R],
A[Q] + A[R] > A[P],
A[R] + A[P] > A[Q].
For example, consider array A such that:

  A[0] = 10    A[1] = 2    A[2] = 5
  A[3] = 1     A[4] = 8    A[5] = 12
There are four triangular triplets that can be constructed from elements of this array, namely (0, 2, 4), (0, 2, 5), (0, 4, 5), and (2, 4, 5).

Write a function:

def solution(A)
that, given a zero-indexed array A consisting of N integers, returns the number of triangular triplets in this array.

For example, given array A such that:

  A[0] = 10    A[1] = 2    A[2] = 5
  A[3] = 1     A[4] = 8    A[5] = 12
the function should return 4, as explained above.

Assume that:

N is an integer within the range [0..1,000];
each element of array A is an integer within the range [1..1,000,000,000].
Complexity:

expected worst-case time complexity is O(N2);
expected worst-case space complexity is O(N), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.

"""

from measure import measure

# O(N ** 3), 63 %
def is_triangular(A, i, j, k):
    a = A[i]
    b = A[j]
    c = A[k]

    return a < b + c and b < a + c and c < a + b

@measure
def solution1(A):
    L = len(A)
    count = 0
    for i in xrange(L - 2):
        for j in xrange(i + 1, L - 1):
            for k in xrange(j + 1, L):
                if is_triangular(A, i, j, k):
                    count += 1
                    print(A[i], A[j], A[k])
    return count


#****************************************

@measure
def solution2(A):
    L = len(A)
    A = sorted(A, reverse=True)
    count = 0
    for i in xrange(L - 2):
        base = A[i]
        for back in range(i + 1, L - 1):
            tail = A[back]
            forward = back + 1
            while forward < L:
                head = A[forward]
                if tail + head > base:
                    count += 1
                    forward += 1
                else:
                    break
    return count



@measure
def solution3(A):
    L = len(A)
    A = sorted(A)
    count = 0
    i = L - 1
    end = L - 1
    while i > 1:
        base = A[i]
        back = 0
        while back < i - 1:
            forward = back + 1
            tail = A[back]
            while forward <= end:
                head = A[forward]
                if tail + head > base:
                    count += (i - forward)
                    end = forward + 1
                    #print base, tail, head, 'ok'
                    break
                else:
                    forward += 1
                    #print base, tail, head, 'wrong'
            back += 1
        i -= 1
    return count


@measure
def solution4(A):
    L = len(A)
    A = sorted(A)
    count = 0
    i = L - 1
    while i > 1:
        base = A[i]
        skip = False
        back = 0
        while back < i - 1:
            tail = A[back]
            if not skip:
                forward = back + 1
            while forward < i:
                head = A[forward]
                if base >= tail + head:
                    forward +=1
                else:
                    a = forward - back
                    print base, tail, head, a
                    skip = True
                    count += forward - back
                    break
            if skip:
                break

            back +=1
        i -= 1


    return count




#A =  list(range(400))
A  = [1, 2, 3, 4, 5, 6, 9, 10]
sol1 = solution1(A)
print('***************')
sol2 = solution2(A)
sol3 = solution3(A)
sol4 = solution4(A)

print(sol2, sol3, sol4)
print(measure.timers)