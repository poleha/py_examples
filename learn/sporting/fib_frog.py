# -*- coding: utf-8 -*-
"""
https://codility.com/programmers/task/fib_frog/
The Fibonacci sequence is defined using the following recursive formula:

    F(0) = 0
    F(1) = 1
    F(M) = F(M - 1) + F(M - 2) if M >= 2
A small frog wants to get to the other side of a river. The frog is initially located at one bank of the river (position −1) and wants to get to the other bank (position N). The frog can jump over any distance F(K), where F(K) is the K-th Fibonacci number. Luckily, there are many leaves on the river, and the frog can jump between the leaves, but only in the direction of the bank at position N.

The leaves on the river are represented in a zero-indexed array A consisting of N integers. Consecutive elements of array A represent consecutive positions from 0 to N − 1 on the river. Array A contains only 0s and/or 1s:

0 represents a position without a leaf;
1 represents a position containing a leaf.
The goal is to count the minimum number of jumps in which the frog can get to the other side of the river (from position −1 to position N). The frog can jump between positions −1 and N (the banks of the river) and every position containing a leaf.

For example, consider array A such that:

    A[0] = 0
    A[1] = 0
    A[2] = 0
    A[3] = 1
    A[4] = 1
    A[5] = 0
    A[6] = 1
    A[7] = 0
    A[8] = 0
    A[9] = 0
    A[10] = 0
The frog can make three jumps of length F(5) = 5, F(3) = 2 and F(5) = 5.

Write a function:

def solution(A)
that, given a zero-indexed array A consisting of N integers, returns the minimum number of jumps by which the frog can get to the other side of the river. If the frog cannot reach the other side of the river, the function should return −1.

For example, given:

    A[0] = 0
    A[1] = 0
    A[2] = 0
    A[3] = 1
    A[4] = 1
    A[5] = 0
    A[6] = 1
    A[7] = 0
    A[8] = 0
    A[9] = 0
    A[10] = 0
the function should return 3, as explained above.

Assume that:

N is an integer within the range [0..100,000];
each element of array A is an integer that can have one of the following values: 0, 1.
Complexity:

expected worst-case time complexity is O(N*log(N));
expected worst-case space complexity is O(N), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.
"""

#*************************** stud
# We can also check here if current count > than the one we already have return False
# But that's slow anyway
from measure import measure, MeasureBlock


def get_fib(n):
    res = {0, 1}
    a1 = 0
    a2 = 1
    while a2 < n:
        a3 = a1 + a2
        res.add(a3)
        a1 = a2
        a2 = a3
    return res


@measure
def solution1(A):
    L = len(A)
    f = get_fib(L + 1)
    if L + 1 in f:
        return 1
    def step(A, pos=-1, count=0):
        if pos == L:
            return count
        n = 0
        counts = []
        for i in range(pos + 1, L + 1):
            n += 1
            if A[i] == 1 and n in f:
                step_count = step(A, i, count + 1)
                if step_count:
                    counts.append(step_count)
        if counts:
            return min(counts)
        else:
            return False

    count = step(A + [1])
    if count:
        return count
    else:
        return -1


#************************************


@measure
def solution2(A):
    A.append(1)
    L = len(A)
    f = get_fib(L + 1)
    if L in f:
        return 1
    steps = {0: 0}
    for i in range(L):
        n = i + 1
        cur = A[i]
        if cur == 1:
            keys = list(steps.keys())
            for step in keys:
                steps_from_step = n - step
                if steps_from_step in f:
                    saved_count = steps.get(n, float('inf'))
                    current_count = steps[step] + 1
                    count = min(saved_count, current_count)
                    steps[n] = count
    count = steps.get(L, None)
    if count:
        return count
    else:
        return -1

#********************************


mb1 = MeasureBlock('mb1')
mb2 = MeasureBlock('mb2')
mb3 = MeasureBlock('mb3')
mb4 = MeasureBlock('mb4')
mb5 = MeasureBlock('mb5')



def get_fib_list(n):
    res = []
    a1 = 0
    a2 = 1
    while a2 < n:
        a3 = a1 + a2
        res.append(a3)
        a1 = a2
        a2 = a3
    return res


@measure
def solution3(A):
    A.append(1)
    L = len(A)
    f = get_fib_list(L + 1)
    steps = set()
    for i in range(L):
        n = i + 1
        cur = A[i]
        if cur == 1:
            steps.add(n)

    cur_steps = {0}
    for i in range(1, L + 1):
        new_steps = set()
        for step in cur_steps:
            for n in f:
                new_step = step + n
                if new_step > L:
                    break
                if new_step in steps:
                    if new_step == L:
                        return i
                    new_steps.add(new_step)
        cur_steps = new_steps

    return -1



#f = get_fib(1000000)


#A = [1]
#A = [1, 1, 0, 0, 0]
#A = [0, 0, 0]
#A = [0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0] * 1000
#A = [1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0] * 1000
A = []
#sol1 = solution1(A)
sol2 = solution2(A)
#A = [0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0] * 1000
#A = [1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0] * 1000
A = []
sol3 = solution3(A)
print(sol2, sol3)


#sol1 = solution1(A)
#print(sol1)

print(measure.timers)
#print(str(mb1), str(mb2), str(mb3), str(mb4), str(mb5))