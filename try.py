import time
"""

res = 1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111 ** 4000

start = time.time()


end = time.time()
timer = end - start

res = 2

def get_int(s, l):
    s = bin(s)
    s = s.lstrip('-0b')
    right = s[-l:]
    #right = ''.join(right)
    return int(right, 2)



num = get_int(res, 19)

res = 0#int(str(res)[-6:])

print(num, res)
print(timer)




a = 100000
b = bin(a)
b = b.lstrip('-0b')
print(b) #11000011010100000

a = 999999
b = bin(a)
b = b.lstrip('-0b')
print(b) #11110100001000111111

"""


a = 1111111111111111111111111111234567
b = 11111111111111111111111111111111111234567

c = a * b
print(c)

a = 1234567
b = 1234567

c = a * b
print(c)