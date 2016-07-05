# -*- coding: utf-8 -*-
"""
https://codility.com/programmers/task/nailing_planks/
You are given two non-empty zero-indexed arrays A and B consisting of N integers. These arrays represent N planks. More precisely, A[K] is the start and B[K] the end of the K−th plank.

Next, you are given a non-empty zero-indexed array C consisting of M integers. This array represents M nails. More precisely, C[I] is the position where you can hammer in the I−th nail.

We say that a plank (A[K], B[K]) is nailed if there exists a nail C[I] such that A[K] ≤ C[I] ≤ B[K].

The goal is to find the minimum number of nails that must be used until all the planks are nailed. In other words, you should find a value J such that all planks will be nailed after using only the first J nails. More precisely, for every plank (A[K], B[K]) such that 0 ≤ K < N, there should exist a nail C[I] such that I < J and A[K] ≤ C[I] ≤ B[K].

For example, given arrays A, B such that:

    A[0] = 1    B[0] = 4
    A[1] = 4    B[1] = 5
    A[2] = 5    B[2] = 9
    A[3] = 8    B[3] = 10
four planks are represented: [1, 4], [4, 5], [5, 9] and [8, 10].

Given array C such that:

    C[0] = 4
    C[1] = 6
    C[2] = 7
    C[3] = 10
    C[4] = 2
if we use the following nails:

0, then planks [1, 4] and [4, 5] will both be nailed.
0, 1, then planks [1, 4], [4, 5] and [5, 9] will be nailed.
0, 1, 2, then planks [1, 4], [4, 5] and [5, 9] will be nailed.
0, 1, 2, 3, then all the planks will be nailed.
Thus, four is the minimum number of nails that, used sequentially, allow all the planks to be nailed.

Write a function:

def solution(A, B, C)
that, given two non-empty zero-indexed arrays A and B consisting of N integers and a non-empty zero-indexed array C consisting of M integers, returns the minimum number of nails that, used sequentially, allow all the planks to be nailed.

If it is not possible to nail all the planks, the function should return −1.

For example, given arrays A, B, C such that:

    A[0] = 1    B[0] = 4
    A[1] = 4    B[1] = 5
    A[2] = 5    B[2] = 9
    A[3] = 8    B[3] = 10

    C[0] = 4
    C[1] = 6
    C[2] = 7
    C[3] = 10
    C[4] = 2
the function should return 4, as explained above.

Assume that:

N and M are integers within the range [1..30,000];
each element of arrays A, B, C is an integer within the range [1..2*M];
A[K] ≤ B[K].
Complexity:

expected worst-case time complexity is O((N+M)*log(M));
expected worst-case space complexity is O(M), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.
"""

#100% stud
def bin_search(A, a):
    L = len(A)
    if L == 1:
        if A[0] >= a:
            return 0
        else:
            return -1

    step = i = L // 2
    prev_step1 = None
    prev_step2 = None
    while True:
        if step < 0 or step > L:
            return -1
        new_step = step
        i = i // 2
        if i == 0:
            i = 1
        if step > L - 1:
            step = L - 1
        cur = A[step]

        if cur < a:
            new_step += i
        elif cur > a:
            if step == prev_step2:
                return step
            new_step -= i
        else:
            return step

        prev_step2 = prev_step1
        prev_step1 = step
        step = new_step


def solution(A, B, C):
    L = len(A)
    nail_positions = {}
    for i in xrange(len(C)):
        nail = C[i]
        if nail not in nail_positions:
            nail_positions[nail] = i

    sorted_nails = sorted(list(set(C)))
    sorted_nails_len = len(sorted_nails)

    max_nail_required = None
    for i in xrange(L):
        a = A[i]
        b = B[i]
        min_nail_required = None
        start = bin_search(sorted_nails, a)
        if start == -1:
            continue
        for j in xrange(start, sorted_nails_len):
            nail = sorted_nails[j]
            if nail > b:
                break

            nail_position = nail_positions[nail]

            if nail_position <= max_nail_required:
                min_nail_required = nail_position
                break
            if min_nail_required is None:
                min_nail_required = nail_position
            else:
                min_nail_required = min(min_nail_required, nail_position)

            if min_nail_required == 0:
                break
        if min_nail_required is not None:
            if max_nail_required is None:
                max_nail_required = min_nail_required
            else:
                max_nail_required = max(min_nail_required, max_nail_required)
        else:
            return -1

    if max_nail_required is not None:
        return max_nail_required + 1

    return -1

"""
import random
for i in range(1):
    C = range(5)
    random.shuffle(C)

    A = list(range(6))
    random.shuffle(A)

    dist = list(range(10))

    B = []
    for a in A:
        d = random.choice(dist)
        b = a + d
        B.append(b)

    sol = solution(A, B, C)
    sol0 = solution0(A, B, C)
    if sol != sol0:
        print(sol, sol0, A, B, C)
"""
#A = [1, 4, 5, 8]
#B = [4, 5, 9, 10]
#C = [4, 6, 7, 10, 1]

A = [1, 3]
B = [2, 4]
C = [2, 3]

sol = solution(A, B, C)
print sol

"""
# 50%
def solution(A, B, C):
    L = len(A)
    count = 0
    nailed = set()
    nailed_count = 0
    for nail in C:
        count += 1
        for i in range(L):
            a = A[i]
            b = B[i]
            if a <= nail <= b and i not  in nailed:
                nailed.add(i)
                nailed_count += 1
        if nailed_count == L:
            return count

    return -1
"""

"""
# 62%
def solution(A, B, C):
    L = len(A)
    unnailed = {i for i in range(L)}
    count = 0
    nailed = set()
    nailed_count = 0
    for nail in C:
        count += 1
        for i in unnailed:
            a = A[i]
            b = B[i]
            if a <= nail <= b and i not  in nailed:
                nailed.add(i)
                nailed_count += 1
        unnailed = unnailed.difference(nailed)
        if nailed_count == L:
            return count

    return -1
"""



"""
# 62%
def solution(A, B, C):
    L = len(A)
    nailed = set()
    count = 0
    step = 0
    presets = {}
    for i in range(L):
        a = A[i]
        b = B[i]
        for j in range(a, b + 1):
            if j not in presets:
                presets[j] = set()
            presets[j].add(i)
    print presets
    for nail in C:
        step += 1
        preset = presets.get(nail, None)
        if preset:
            for plank in preset:
                if plank not in nailed:
                    nailed.add(plank)
                    count += 1
        if count == L:
            return step

    return -1

"""


"""
# 75%
def solution(A, B, C):
    L = len(A)
    #ends = {}
    count = 0
    step = 0
    visited = set()
    nailed = set()
    unnailed = {i for i in range(L)}



    for i in range(len(C)):
        step +=1
        nail = C[i]
        if nail in visited:
            continue
        visited.add(nail)
        new_nailed = set()
        for j in unnailed:
            a = A[j]
            b = B[j]
            #if a > nail:
            #    break
            if j not in nailed and b >= nail and a <= nail:
                count += 1
                nailed.add(j)
                new_nailed.add(j)

        unnailed = unnailed.difference(new_nailed)


        if count == L:
            return step

    return -1
"""

"""
#87 %
def solution(A, B, C):
    L = len(A)
    nail_positions = {}
    for i in xrange(len(C)):
        nail = C[i]
        if nail not in nail_positions:
            nail_positions[nail] = i

    max_nail_required = None
    for i in xrange(L):
        a = A[i]
        b = B[i]
        min_nail_required = None
        for j in xrange(a, b + 1):
            if j in nail_positions:
                nail_position = nail_positions[j]
                if nail_position <= max_nail_required:
                    min_nail_required = nail_position
                    break
                if min_nail_required is None:
                    min_nail_required = nail_position
                else:
                    min_nail_required = min(min_nail_required, nail_position)
        if min_nail_required is not None:
            if max_nail_required is None:
                max_nail_required = min_nail_required
            else:
                max_nail_required = max(min_nail_required, max_nail_required)

    if max_nail_required is not None:
        return max_nail_required + 1

    return -1
"""

