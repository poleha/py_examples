# -*- coding: utf-8 -*-
"""
https://codility.com/programmers/task/equi_leader/
A non-empty zero-indexed array A consisting of N integers is given.

The leader of this array is the value that occurs in more than half of the elements of A.

An equi leader is an index S such that 0 ≤ S < N − 1 and two sequences A[0], A[1], ..., A[S] and A[S + 1], A[S + 2], ..., A[N − 1] have leaders of the same value.

For example, given array A such that:

    A[0] = 4
    A[1] = 3
    A[2] = 4
    A[3] = 4
    A[4] = 4
    A[5] = 2
we can find two equi leaders:

0, because sequences: (4) and (3, 4, 4, 4, 2) have the same leader, whose value is 4.
2, because sequences: (4, 3, 4) and (4, 4, 2) have the same leader, whose value is 4.
The goal is to count the number of equi leaders.

Write a function:

def solution(A)
that, given a non-empty zero-indexed array A consisting of N integers, returns the number of equi leaders.

For example, given:

    A[0] = 4
    A[1] = 3
    A[2] = 4
    A[3] = 4
    A[4] = 4
    A[5] = 2
the function should return 2, as explained above.

Assume that:

N is an integer within the range [1..100,000];
each element of array A is an integer within the range [−1,000,000,000..1,000,000,000].
Complexity:

expected worst-case time complexity is O(N);
expected worst-case space complexity is O(N), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.
"""


# you can write to stdout for debugging purposes, e.g.
# print "this is a debug message"

"""

Можно еще воспользоваться мыслью, что удаляя два неодинаковых элемента последовательность сохраняет лидера, но это бред.
"""

timers = {}
from measure import create_measure
measure = create_measure(timers)

@measure()
def solution1(A):
    L = len(A)
    count = 0
    len_left = 0
    len_right = L
    counts_right = {}
    for cur in A:
        counts_right[cur] = counts_right[cur] + 1 if cur in counts_right else 1
    counts_left = {cur: 0 for cur in counts_right.keys()}

    for i in range(L):
        len_left += 1
        len_right -= 1
        cur = A[i]
        counts_left[cur] += 1
        counts_right[cur] -= 1
        if len_left <= len_right:
            min_len = len_left
            max_len = len_right
            min_counts = counts_left
            max_counts = counts_right
        else:
            min_len = len_right
            max_len = len_left
            min_counts = counts_right
            max_counts = counts_left

        for k, v in min_counts.items():
            if v > min_len / float(2):
                max_count = max_counts.get(k, 0)
                if max_count > max_len / float(2):
                    count += 1
    return count

@measure()
def solution2(A):
    L = len(A)
    count = 0
    len_left = 0
    len_right = L
    counts_right = {}
    count_candidates = set()
    for cur in A:
        counts_right[cur] = counts_right[cur] + 1 if cur in counts_right else 1
    counts_left = {cur: 0 for cur in counts_right.keys()}

    for i in range(L):
        len_left += 1
        len_right -= 1
        cur = A[i]
        counts_left[cur] += 1
        counts_right[cur] -= 1
        if counts_left[cur] > len_left / 2:
            count_candidates.add(cur)
        delete_candidates = []
        for candidate in count_candidates:
            if counts_left[candidate] <= len_left / 2:
                delete_candidates.append(candidate)
            elif counts_right[candidate] > len_right / 2:
                count += 1
        for candidate in delete_candidates:
            count_candidates.remove(candidate)
    return count



#A = [4, 3, 4, 4, 4, 2]
#sol = solution3(A)
#print(sol)


import random

for i in range(1000):
    A = []
    for j in range(400):
        cur = int(round(random.random() * 10))
        if cur == 0:
            cur = 1
        A.append(cur)
    res1 = solution1(A)
    res2 = solution2(A)
    if not (res1 == res2):
        print(A, res1, res2)
print(timers)

#{'solution2': 0.19128990173339844, 'solution3': 7.9801716804504395, 'solution1': 1.0761525630950928}