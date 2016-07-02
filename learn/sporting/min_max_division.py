# -*- coding: utf-8 -*-
"""
You are given integers K, M and a non-empty zero-indexed array A consisting of N integers. Every element of the array is not greater than M.

You should divide this array into K blocks of consecutive elements. The size of the block is any integer between 0 and N. Every element of the array should belong to some block.

The sum of the block from X to Y equals A[X] + A[X + 1] + ... + A[Y]. The sum of empty block equals 0.

The large sum is the maximal sum of any block.

For example, you are given integers K = 3, M = 5 and array A such that:

  A[0] = 2
  A[1] = 1
  A[2] = 5
  A[3] = 1
  A[4] = 2
  A[5] = 2
  A[6] = 2
The array can be divided, for example, into the following blocks:

[2, 1, 5, 1, 2, 2, 2], [], [] with a large sum of 15;
[2], [1, 5, 1, 2], [2, 2] with a large sum of 9;
[2, 1, 5], [], [1, 2, 2, 2] with a large sum of 8;
[2, 1], [5, 1], [2, 2, 2] with a large sum of 6.
The goal is to minimize the large sum. In the above example, 6 is the minimal large sum.

Write a function:

def solution(K, M, A)
that, given integers K, M and a non-empty zero-indexed array A consisting of N integers, returns the minimal large sum.

For example, given K = 3, M = 5 and array A such that:

  A[0] = 2
  A[1] = 1
  A[2] = 5
  A[3] = 1
  A[4] = 2
  A[5] = 2
  A[6] = 2
the function should return 6, as explained above.

Assume that:

N and K are integers within the range [1..100,000];
M is an integer within the range [0..10,000];
each element of array A is an integer within the range [0..M].
Complexity:

expected worst-case time complexity is O(N*log(N+M));
expected worst-case space complexity is O(1), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.
"""


# you can write to stdout for debugging purposes, e.g.
# print "this is a debug message"

def solution(K, M, A):
    if M == 0:
        return 0

    L = len(A)
    if L == 0:
        return 0

    if L <= K:
        return max(A)
    if K == 1:
        return sum(A)


    s = sum(A)
    a = s // K

    max_sum = float('inf')
    i = M // 2
    step = i
    visited = set()
    while True:
        step = step // 2
        if step == 0:
            step = 1
        cur_sum = 0
        cur_max_sum = 0
        slice_count = 1
        if i in visited:
            break
        for cur in A:
            if cur_sum + cur <= a + i:
                cur_sum += cur
            else:
                slice_count += 1
                cur_sum = cur
                if slice_count > K:
                    break
            cur_max_sum = max(cur_sum, cur_max_sum)

        if slice_count <= K:
            visited.add(i)
            i -= step
            max_sum = min(max_sum, cur_max_sum)
        else:
            i += step

    return max_sum


#A = [3, 4, 5, 6, 7, 8, 7, 3, 5, 5]
#K = 3
#M = 8



A = [3, 5]
K = 5
M = 3




sol = solution(K, M, A)
print(sol)



"""

#83

def solution(K, M, A):
    if M == 0:
        return 0
    s = sum(A)
    a = s // K
    for i in range(M + 1):
        cur_sum = 0
        cur_max_sum = 0
        slice_count = 1
        for cur in A:
            if cur_sum + cur <= a + i:
                cur_sum += cur
            else:
                slice_count += 1
                cur_sum = cur
                if slice_count > K:
                    break
            cur_max_sum = max(cur_sum, cur_max_sum)

        if slice_count <= K:
            return cur_max_sum

"""

"""
# 91



from math import ceil

def get_prefixed_sums(A, L):
    sums = {}
    s = 0
    for i in range(L):
        cur = A[i]
        s += cur
        sums[i] = s

    return sums


def solution(K, M, A):
    M = max(A)
    A = [cur for cur in A if cur > 0]
    if M == 0:
        return 0
    L = len(A)
    if L == 0:
        return 0

    if L <= K:
        return max(A)
    if K == 1:
        return sum(A)

    sums = get_prefixed_sums(A, L)

    def bin_search(start, step, current_step):
        current_step = current_step if current_step > 0 else 1
        end = start + step + current_step

        if end >= L:
            if start == L - 1:
                return A[start], start
            else:
                end = L - 1
                s = sums[end] - sums[start] + A[start]
                if s <= mx:
                    return s, end

        s = sums[end] - sums[start] + A[start]
        if end == start:
            return s, end
        if s == mx:
            return s, end
        elif s < mx:
            step += current_step
            res = bin_search(start, step, int(ceil(current_step / float(2))))
        elif s > mx:
            if s - A[end] <= mx:
                return s - A[end], end - 1
            step -= current_step
            res = bin_search(start, step, int(ceil(current_step / float(2))))
        return res

    s = sums[L - 1]
    a = s // K
    initial_step = int(ceil(L / K) / 2)

    for i in range(M + 1):
        cur_max_sum = 0
        slice_count = 1
        pos = -1
        mx = a + i

        while pos < L and slice_count <= K:
            if pos == L - 1:
                s, pos = A[pos], L
            else:
                s, pos = bin_search(pos + 1, initial_step, int(ceil(initial_step / float(2))))
            slice_count += 1
            cur_max_sum = max(cur_max_sum, s)

        if pos == L - 1:
            slice_count -= 1

        if slice_count <= K:
            return cur_max_sum



"""