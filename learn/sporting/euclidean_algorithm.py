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