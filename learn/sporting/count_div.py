"""
https://codility.com/programmers/task/count_div/
Write a function:

def solution(A, B, K)
that, given three integers A, B and K, returns the number of integers within the range [A..B] that are divisible by K, i.e.:

{ i : A ≤ i ≤ B, i mod K = 0 }
For example, for A = 6, B = 11 and K = 2, your function should return 3, because there are three numbers divisible by 2 within the range [6..11], namely 6, 8 and 10.

Assume that:

A and B are integers within the range [0..2,000,000,000];
K is an integer within the range [1..2,000,000,000];
A ≤ B.
Complexity:

expected worst-case time complexity is O(1);
expected worst-case space complexity is O(1).
"""

# O(n)
def solution1(A, B, K):
    count = 0
    for i in range(A, B + 1):
        if i % K == 0:
            count += 1
    return count


#***************
# O(1)
from math import ceil, floor

def solution(A, B, K):
    if A == B:
        if A % K == 0:
            return 1
        else:
            return 0
    if A > B:
        return 0

    l = B - A + 1
    n = ceil(A / floor(K))
    if n == 0:
        n = 1
    first_in = K * n
    # Находим самое левое потенциальное вхождение
    offset = first_in - A
    l = l - offset
    # Смещаем длину на него, чтобы первым был кратный K символ
    res = int(ceil(l / float(K)))
    # Например было 1, 2, 3, 4, 5, 6, 7, 8
    # l = 8
    # first_in = 3
    # offset = 2
    # остается фактически 3, 4, 5, 6, 7, 8
    # Число вхождений тут - округленное в большую сторону деление l / K
    # Поскольку в текущей картине видим что кусочки длиной K 3,4,5    6,7,8 Дают длину 6. При увеличении хоть на
    # 1 длина будет 7 деление будет 3 и начало след кусочка войдет
    if A == 0:
        res += 1
    return res

A = 0
B = 2
K = 2

import os
sol = solution(A, B, K)
#print(sol)
#os._exit(0)

for A in range(0, 100):
    for B in range(0, 100):
        for K in range(1, 100):

            try:
                sol = solution(A, B, K)
                sol1 = solution1(A, B, K)
                if sol1 != sol:
                    print A, B, K, sol1, sol
                    os._exit(0)
            except:
                pass



