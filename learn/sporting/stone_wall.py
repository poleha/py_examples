# -*- coding: utf-8 -*-
"""
https://codility.com/programmers/task/stone_wall/
Solution to this task can be found at our blog.

You are going to build a stone wall. The wall should be straight and N meters long, and its thickness should be constant; however, it should have different heights in different places. The height of the wall is specified by a zero-indexed array H of N positive integers. H[I] is the height of the wall from I to I+1 meters to the right of its left end. In particular, H[0] is the height of the wall's left end and H[N−1] is the height of the wall's right end.

The wall should be built of cuboid stone blocks (that is, all sides of such blocks are rectangular). Your task is to compute the minimum number of blocks needed to build the wall.

Write a function:

def solution(H)
that, given a zero-indexed array H of N positive integers specifying the height of the wall, returns the minimum number of blocks needed to build it.

For example, given array H containing N = 9 integers:

  H[0] = 8    H[1] = 8    H[2] = 5
  H[3] = 7    H[4] = 9    H[5] = 8
  H[6] = 7    H[7] = 4    H[8] = 8
the function should return 7. The figure shows one possible arrangement of seven blocks.



Assume that:

N is an integer within the range [1..100,000];
each element of array H is an integer within the range [1..1,000,000,000].
Complexity:

expected worst-case time complexity is O(N);
expected worst-case space complexity is O(N), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.
"""

timers = {}
from measure import create_measure

measure = create_measure(timers)

#Doesn't work on  #A = [1, 1000000000, 1]
@measure()
def solution1(H):
    if not H:
        return 0
    cur_max = H[0]
    not_count = set()
    count = 0

    for cur in H:
        if cur < cur_max:
            for i in range(cur + 1, cur_max + 1):
                if i in not_count:
                    not_count.remove(i)
        cur_max = cur
        if cur not in not_count:
            count += 1
        not_count.add(cur)
    return count


#O(N)
@measure()
def solution2(H):
    if not H:
        return 0
    cur_max = H[0]
    not_count = set()
    count = 0

    for cur in H:
        L = len(not_count)
        if cur_max - cur > L:
            if cur < cur_max:
                new_not_count = set()
                while not_count:
                    cur_not_count = not_count.pop()
                    if cur_not_count <= cur:
                        new_not_count.add(cur_not_count)
                not_count = new_not_count
        else:
            for i in range(cur + 1, cur_max + 1):
                if i in not_count:
                    not_count.remove(i)

        cur_max = cur
        if cur not in not_count:
            count += 1
            not_count.add(cur)
    return count

# Это их решение
@measure()
def solution3(H):
    N = len(H)
    stones = 0
    stack = [0] * N
    stack_num = 0

    for i in range(N):
        # Суть тут в том, что номера в stack идут строго по возрастанию, как же иначе...
        # И если мы встречаем меньше, мы откатываемся назад до... Возможно, что и до 1.
        while stack_num > 0 and stack[stack_num - 1] > H[i]:
            stack_num -= 1
        if stack_num > 0 and stack[stack_num - 1] == H[i]:
            pass
        # Мы откатились и смотрим, кто остался наверху стека. Это самый больой номер.
        # Если мы его уже встречали, не считаем.
        # Иначе движемся вправо на 1 и ставим текущий самым большим
        else:
            stones += 1
            stack[stack_num] = H[i]
            stack_num += 1
    return stones

A = [1, 2, 3, 1]
#A = [3, 1, 1, 3]
#A = [1, 1000000000, 1]
#A = [8, 8, 5, 7, 9, 8, 7, 4, 8]
sol = solution3(A)
print(sol)

import random

for i in range(1000):
    A = []
    for j in range(400):
        cur = int(round(random.random() * 400))
        if cur == 0:
            cur = 1
        A.append(cur)
    res1 = solution1(A)
    res2 = solution2(A)
    res3 = solution3(A)
    if not res1 == res2 == res3:
        print(A, res1, res2, res3)



print(timers)
#{'solution2': 0.3388378620147705, 'solution3': 0.12395262718200684, 'solution1': 1.362870693206787}