# -*- coding: utf-8 -*-
"""
https://codility.com/programmers/task/number_of_disc_intersections/
We draw N discs on a plane. The discs are numbered from 0 to N − 1. A zero-indexed array A of N non-negative integers, specifying the radiuses of the discs, is given. The J-th disc is drawn with its center at (J, 0) and radius A[J].

We say that the J-th disc and K-th disc intersect if J ≠ K and the J-th and K-th discs have at least one common point (assuming that the discs contain their borders).

The figure below shows discs drawn for N = 6 and A as follows:

  A[0] = 1
  A[1] = 5
  A[2] = 2
  A[3] = 1
  A[4] = 4
  A[5] = 0


There are eleven (unordered) pairs of discs that intersect, namely:

discs 1 and 4 intersect, and both intersect with all the other discs;
disc 2 also intersects with discs 0 and 3.
Write a function:

def solution(A)
that, given an array A describing N discs as explained above, returns the number of (unordered) pairs of intersecting discs. The function should return −1 if the number of intersecting pairs exceeds 10,000,000.

Given array A shown above, the function should return 11, as explained above.

Assume that:

N is an integer within the range [0..100,000];
each element of array A is an integer within the range [0..2,147,483,647].
Complexity:

expected worst-case time complexity is O(N*log(N));
expected worst-case space complexity is O(N), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.
"""

MAX_INT = 10000000

# O(N ** 2)
def solution1(A):
    N = len(A)
    count = 0
    for i in range(N - 1):
        for j in range(i + 1, N):
            d = j - i
            if A[j] + A[i] >= d:
                count += 1
    if count > MAX_INT:
        return -1
    return count

# O(N*log(N));
def solution(A):
    N = len(A)
    if N <= 1:
        return 0
    count = 0
    starts = {}
    ends = {}
    keys = set()
    mn = None
    mx = None
    for i in range(N):
        cur = A[i]
        left = i - cur
        right = i + cur
        if left not in starts:
            starts[left] = set()
        if right not in ends:
            ends[right] = set()
        starts[left].add(i)
        ends[right].add(i)
        keys.add(left)
        keys.add(right)
        if left < mn or mn is None:
            mn = left
        if right > mx or mx is None:
            mx = right

    active = set()
    #keys = sorted(set(starts.keys() + ends.keys()))
    for i in sorted(keys):
        to_add = starts.get(i, set())
        to_remove = ends.get(i, set())
        len_active = len(active)
        len_to_add = len(to_add)

        count += len_active * len_to_add
        if len_to_add > 1:
            # If we add more than one, we should take into acctount additions intrrsections
            # For example we add 1,2,3,4 sectors
            # we have 1,2  1,3  1,4
            #         2,3  2, 4
            #         3,4
            # So sum of ar. progression
            n = len_to_add - 1
            addition = (1 + n) * n / 2
            count += addition

        if count > MAX_INT:
            return -1

        active.update(to_add)
        active.difference_update(to_remove)

    return count


A = [1, 5, 2, 1, 4, 0]
#A = [1, 2147483647, 0]

sol = solution(A)
print(sol)


