# -*- coding: utf-8 -*-
#Greatest common divisor by subtraction.
def gcd(a, b):
    if a == b:
        print('a == b', a, b)
        return a
    if a > b:
        print('a > b', a, b)
        return gcd(a - b, b)
    else:
        print('a < b', a, b)
        return gcd(a, b - a)

#('a > b', 24, 9)
#('a > b', 15, 9)
#('a < b', 6, 9)
#('a > b', 6, 3)
#('a == b', 3, 3)


sol = gcd(24, 9)
print(sol)

print('*' * 10)
#**********************************************
#Greatest common divisor by division.
def gcd(a, b):
    if a % b == 0:
        print('a % b == 0', a, b)
        return b
    else:
        print('else', a, b)
        return gcd(b, a % b)


#('else', 24, 9)
#('else', 9, 6)
#('a % b == 0', 6, 3)

sol = gcd(24, 9)
print(sol)

print('*' * 10)
#**********************************
#Recursive Euclid algorithm

def gcd(u, v):
    return gcd(v, u % v) if v else abs(u)

sol = gcd(24, 9)
print(sol)

print('*' * 10)


#*******************************
#Iterative Euclid algorithm

def gcd_iter(u, v):
    while v:
        u, v = v, u % v
    return abs(u)



# *****************************************
# binary GCD algorithm (my)
# https://en.wikipedia.org/wiki/Binary_GCD_algorithm
"""
The algorithm reduces the problem of finding the GCD by repeatedly applying these identities:

gcd(0, v) = v, because everything divides zero, and v is the largest number that divides v. Similarly, gcd(u, 0) = u. gcd(0, 0) is not typically defined, but it is convenient to set gcd(0, 0) = 0.
If u and v are both even, then gcd(u, v) = 2·gcd(u/2, v/2), because 2 is a common divisor.
If u is even and v is odd, then gcd(u, v) = gcd(u/2, v), because 2 is not a common divisor. Similarly, if u is odd and v is even, then gcd(u, v) = gcd(u, v/2).
If u and v are both odd, and u ≥ v, then gcd(u, v) = gcd((u − v)/2, v). If both are odd and u < v, then gcd(u, v) = gcd((v − u)/2, u). These are combinations of one step of the simple Euclidean algorithm, which uses subtraction at each step, and an application of step 3 above. The division by 2 results in an integer because the difference of two odd numbers is even.[3]
Repeat steps 2–4 until u = v, or (one more step) until u = 0. In either case, the GCD is 2kv, where k is the number of common factors of 2 found in step 2.
The algorithm requires O(n2)[4] worst-case time, where n is the number of bits in the larger of the two numbers. Although each step reduces at least one of the operands by at least a factor of 2, the subtract and shift operations take linear time for very large integers (although they're still quite fast in practice, requiring about one operation per word of the representation).


"""
def eq(a, b, k=1):
    if a == 0:
        return k * b
    if b == 0:
        return k * a
    if a == b:
        return k * a

    a = abs(a)
    b = abs(b)

    if b > a:
        a, b = b, a

    while a & 1 == 0 and b & 1 == 0:
        a = a / 2
        b = b / 2
        k *= 2

    if a & 1 == 0 and b & 1 == 1:
        return eq(a / 2, b, k)
    elif a & 1 == 1 and b & 1 == 0:
        return eq(a, b / 2, k)
    else: # a & 1 == 1 and b & 1 == 1
        return  eq((a - b) / 2, b, k)