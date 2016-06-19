import random
import math
#A = [3, 5, 7, 6, 3]
#A = [4, 5, 5, 1, 1]
#A = [3, 5, 7, 6]
#A = [3, 5, 3, 5, 3, 8]

"""
https://codility.com/programmers/task/count_bounded_slices/
An integer K and a non-empty zero-indexed array A consisting of N integers are given.

A pair of integers (P, Q), such that 0 ≤ P ≤ Q < N, is called a slice of array A.

A bounded slice is a slice in which the difference between the maximum and minimum values in the slice is less than or equal to K. More precisely it is a slice, such that max(A[P], A[P + 1], ..., A[Q]) − min(A[P], A[P + 1], ..., A[Q]) ≤ K.

The goal is to calculate the number of bounded slices.

For example, consider K = 2 and array A such that:

    A[0] = 3
    A[1] = 5
    A[2] = 7
    A[3] = 6
    A[4] = 3
There are exactly nine bounded slices: (0, 0), (0, 1), (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3), (4, 4).

Write a function:

def solution(K, A)

that, given an integer K and a non-empty zero-indexed array A of N integers, returns the number of bounded slices of array A.

If the number of bounded slices is greater than 1,000,000,000, the function should return 1,000,000,000.

For example, given:

    A[0] = 3
    A[1] = 5
    A[2] = 7
    A[3] = 6
    A[4] = 3
the function should return 9, as explained above.

Assume that:

N is an integer within the range [1..100,000];
K is an integer within the range [0..1,000,000,000];
each element of array A is an integer within the range [−1,000,000,000..1,000,000,000].
Complexity:

expected worst-case time complexity is O(N);
expected worst-case space complexity is O(N), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.

Первое мое. Второе - их золотое, но не работает.
"""

maxINT = 1000000000

def solution1(K, A):
    count = 0
    N = len(A)
    for i in range(N):
        j = i
        min = max = A[i]
        while max - min <= K:
            count += 1
            if count == maxINT:
                return count
            j += 1
            if j >= N:
                break
            cur = A[j]
            if cur < min: min = cur
            if cur > max: max = cur
    return count




def solution2(K, A):
    N = len(A)

    maxQ = [0] * (N + 1)
    posmaxQ = [0] * (N + 1)
    minQ = [0] * (N + 1)
    posminQ = [0] * (N + 1)

    firstMax, lastMax = 0, -1
    firstMin, lastMin = 0, -1
    j, result = 0, 0

    for i in range(N):
        while (j < N):
            # added new maximum element
            while (lastMax >= firstMax and maxQ[lastMax] <= A[j]):
                lastMax -= 1
                lastMax += 1
                maxQ[lastMax] = A[j]
                posmaxQ[lastMax] = j
            # added new minimum element
            while (lastMin >= firstMin and minQ[lastMin] >= A[j]):
                lastMin -= 1
                lastMin += 1
                minQ[lastMin] = A[j]
                posminQ[lastMin] = j
            if (maxQ[firstMax] - minQ[firstMin] <= K):
                j += 1
            else:
                break
        result += (j - i)
        if result >= maxINT:
            return maxINT
        if posminQ[firstMin] == i:
            firstMin += 1
        if posmaxQ[firstMax] == i:
            firstMax += 1
    return result


l = [3, 2, 1, 1]
N = 1

s1 = solution1(N, l)
s2 = solution2(N, l)
dif = s1 - s2
if dif != 0:
    print(N, l, s1, s2, dif)

"""
for k in range(10000):
    l = []
    N = math.ceil(random.random() * 10)
    for n in range(4):
        s = 1 #random.choice((-1, 1))
        l.append(s * math.ceil(random.random() * 10))
    s1 = solution1(N, l)
    s2 = solution2(N, l)
    dif = s1 - s2
    if dif != 0:
        print(N, l, s1, s2, dif)

"""