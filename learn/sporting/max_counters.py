"""
https://codility.com/programmers/task/max_counters/
You are given N counters, initially set to 0, and you have two possible operations on them:

increase(X) − counter X is increased by 1,
max counter − all counters are set to the maximum value of any counter.
A non-empty zero-indexed array A of M integers is given. This array represents consecutive operations:

if A[K] = X, such that 1 ≤ X ≤ N, then operation K is increase(X),
if A[K] = N + 1 then operation K is max counter.
For example, given integer N = 5 and array A such that:

    A[0] = 3
    A[1] = 4
    A[2] = 4
    A[3] = 6
    A[4] = 1
    A[5] = 4
    A[6] = 4
the values of the counters after each consecutive operation will be:

    (0, 0, 1, 0, 0)
    (0, 0, 1, 1, 0)
    (0, 0, 1, 2, 0)
    (2, 2, 2, 2, 2)
    (3, 2, 2, 2, 2)
    (3, 2, 2, 3, 2)
    (3, 2, 2, 4, 2)
The goal is to calculate the value of every counter after all operations.

Write a function:

def solution(N, A)
that, given an integer N and a non-empty zero-indexed array A consisting of M integers, returns a sequence of integers representing the values of the counters.

The sequence should be returned as:

a structure Results (in C), or
a vector of integers (in C++), or
a record Results (in Pascal), or
an array of integers (in any other programming language).
For example, given:

    A[0] = 3
    A[1] = 4
    A[2] = 4
    A[3] = 6
    A[4] = 1
    A[5] = 4
    A[6] = 4
the function should return [3, 2, 2, 4, 2], as explained above.

Assume that:

N and M are integers within the range [1..100,000];
each element of array A is an integer within the range [1..N + 1].
Complexity:

expected worst-case time complexity is O(N+M);
expected worst-case space complexity is O(N), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.
"""
from measure import create_measure
timers = {}
measure = create_measure(timers)


"""
#slow O(N*M)
@measure()
def solution1(N, A):
    c = {k:0 for k in range(1, N + 1)}
    l = len(A)
    m = 0
    for i in range(l):
        x = A[i]
        if x == N + 1:
            for k in c:
                c[k] = m
        else:
            for j in range(1, N + 1):
                if 1 <= x <= N and x == j:
                    c[j] = c[j] + 1
                    if c[j] > m:
                        m = c[j]
    return list(c.values())

#slow O(N*M) but way faster than solution1
@measure()
def solution2(N, A):
    c = {k:0 for k in range(1, N + 1)}
    l = len(A)
    prev_m = 0
    new_m = 0
    max_counter = False
    for i in range(l):
        x = A[i]
        if x == N + 1:
            max_counter = True
        else:
            for j in range(1, N + 1):
                if max_counter:
                    c[j] = prev_m
                if 1 <= x <= N and x == j:
                    c[j] = c[j] + 1
                    if c[j] > new_m:
                        new_m = c[j]
            prev_m = new_m
            max_counter = False

    if max_counter:
        for k in c:
            c[k] = new_m

    return list(c.values())

#slow O(N*M) but faster than solution2
@measure()
def solution3(N, A):
    c = {k:0 for k in range(1, N + 1)}
    l = len(A)
    m = 0
    for i in range(l):
        cur = A[i]
        if cur in c:
            c[cur] += 1
            if c[cur] > m:
                m = c[cur]
        elif cur == N + 1:
            for k in c:
                c[k] = m

    return list(c.values())


A = [3,4,4,6,1,4,4]
sol1  = solution1(5, A)
sol2 = solution2(5, A)
sol3 = solution3(5, A)
print(sol1 == sol2 == sol3, timers)

"""

"""
Фактически вместо dict у нас c_num - хранящий текущие значения и c - что изменено в них.
"""
# O(N + M)
def solution(N, A):
    c_num = 0 # Все значения
    c = {} # changed
    l = len(A)
    m = 0
    for i in range(l):
        cur = A[i]
        if 1 <= cur <= N:
            c[cur] = c[cur] + 1 if cur in c else c_num + 1
            if c[cur] > m:
                m = c[cur]
        elif cur == N + 1:
            c = {}
            c_num = m
    res = []
    for i in range(1, N + 1):
        if i not in c:
            res.append(c_num)
        else:
            res.append(c[i])
    return res


A = [3,4,4,6,1,4,4]
sol  = solution(5, A)
print(sol, timers)

