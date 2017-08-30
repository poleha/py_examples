# -*- coding: utf-8 -*-
"""
https://codility.com/programmers/task/chocolates_by_numbers/
Two positive integers N and M are given. Integer N represents the number of chocolates
arranged in a circle, numbered from 0 to N − 1.

You start to eat the chocolates. After eating a chocolate you leave only a wrapper.

You begin with eating chocolate number 0. Then you omit the next M − 1 chocolates or
wrappers on the circle, and eat the following one.

More precisely, if you ate chocolate number X, then you will next eat the chocolate with
number (X + M) modulo N (remainder of division).

You stop eating when you encounter an empty wrapper.

For example, given integers N = 10 and M = 4. You will eat the following chocolates:
0, 4, 8, 2, 6.

The goal is to count the number of chocolates that you will eat, following the above rules.

Write a function:

def solution(N, M)
that, given two positive integers N and M, returns the number of chocolates that you will
eat.

For example, given integers N = 10 and M = 4. the function should return 5,
as explained above.

"""
from measure import measure

# Too long
@measure
def solution1(N, M):
    visited = set()
    i = 0
    while True:
        if i in visited:
            return len(visited)
        visited.add(i)
        i += M
        if i >= N:
            i = i % N


#*****************

def get_greatest_divisor(a, b):
    if b > a:
        a, b = b, a

    m = a % b
    if m == 0:
        return b
    else:
        return get_greatest_divisor(b, m)


@measure
def solution2(N, M):
    gd = get_greatest_divisor(N, M)
    return N / gd


N = 10 ** 8
M = 235

sol1 = solution1(N, M)
sol2 = solution2(N, M)
print(sol1, sol2)
print(measure.timers)
#{'solution2': 5.9604644775390625e-06, 'solution1': 4.3866589069366455}



