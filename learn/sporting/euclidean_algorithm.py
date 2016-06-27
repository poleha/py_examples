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
#Iterative binary algorithm
def gcd_bin(u, v):
    u, v = abs(u), abs(v)  # u >= 0, v >= 0
    if u < v:
        u, v = v, u  # u >= v >= 0
    if v == 0:
        return u

    # u >= v > 0
    k = 1
    while u & 1 == 0 and v & 1 == 0:  # u, v - even
        u >>= 1 # 12 6
        v >>= 1 # 10  5
        k <<= 1 # 2  4  ... 8 ... 16
        # Делим на 2, на 4, на 8 и так далее, пока не получим нечетное. к - это число, на которое разделили

    t = -v if u & 1 else u # u & 1 - нечет, odd
    # Если u(большее) четно, то t = u, иначе t = -v
    while t:
        while t & 1 == 0: # Пока четно
            t >>= 1 #Делим на 2 нацело пока не получим нечетного

        # Если делили u
        if t > 0:
            u = t

        # Если делили v
        else:
            v = -t
        t = u - v
        # Находим результат вычитания. Тут деленным на 2 до нечетного может быть левая или правая часть


        print(u, v, t)
        #(3, 5, -2)
        #(3, 1, 2)
        #(1, 1, 0)
    return u * k

sol = gcd_bin(24, 20)
print(sol)