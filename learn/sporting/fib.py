from math import sqrt

s = sqrt(5)

n = 4

a = (((1 + s) / 2) ** n - ((1 - s) / 2) ** n) / s

a = int(a)
print(a)