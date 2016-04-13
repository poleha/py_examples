"""
L = [1, 2, 3, 4, 5]
for i in range(len(L)):
    L[i] += 10

print(L)

L = [x + 10 for x in L]
print(L)
"""


"""
[x + y for x in 'abc' for y in 'lmn']
#['al', 'am', 'an', 'bl', 'bm', 'bn', 'cl', 'cm', 'cn']
res = []
for x in 'abc':
    for y in 'lmn':
        res.append(x + y)
#['al', 'am', 'an', 'bl', 'bm', 'bn', 'cl', 'cm', 'cn']

"""

"""
lis = [1,2,3]


mlist = map(lis,lis)
print(mlist)
zmlist = zip(mlist)
#list(mlist)
print(mlist)
print(zmlist)
"""



"""
def iter_test():
    yield 1
    yield 2
    yield 3

for i in iter_test():
    print(i)
"""

"""
def gsquares(start, stop):
    for i in range(start, stop+1):
        yield i ** 2

Возвращает результат и сохраняет состояние


for i in gsquares(1, 5): # или: (x ** 2 for x in range(1, 5))
    print(i, end=' ')
"""

"""
def iter_test():
    yield 1
    yield 2
    yield 3

for i in iter_test():
    print(i)

"""
"""

class SkipIterator:
    def __init__(self, wrapped):
        self.wrapped = wrapped
        self.offset = 0
    def __next__(self):
        if self.offset >= len(self.wrapped):
            raise StopIteration
        else:
            item = self.wrapped[self.offset]
            self.offset += 2
            return item


class SkipObject:
    def __init__(self, wrapped):
        self.wrapped = wrapped
    def __iter__(self):
        return SkipIterator(self.wrapped)

if __name__ == '__main__':
    alpha = 'abcdef'
    skipper = SkipObject(alpha)
    I = iter(skipper)
    print(next(I), next(I), next(I))

    for x in skipper:
        for y in skipper:
            print(x + y, end=' ')


"""

"""
A = (1,2)
B = (3,4)
C = zip(A,B)
D = zip(*zip(A,B))

#print(list(C)) #[((1,3),(2,4)]
#print(list(D)) #[((1,2),(3,4)]
#print(type(D)) #class 'zip'

def for_map(val):
    if val<=1: return val-1
    else: return val+1

E = map(for_map, A)
#print(list(E))  #[2, 4]
#print(type(E)) #class 'map'
#print(next(E)) #0
#print(E.__next__()) #3

def for_filter(val):
    if val<=1: return True
    else: return False

F = filter(for_filter,A)
#print(list(F))  #[1]


G = list('abc');
#print(G) #['a', 'b', 'c']


"""



class Iters:
    def __init__(self, value):
        self.data = value
    def __getitem__(self, i): # Крайний случай для итераций
        print('get[%s]:' % i, end='') # А также для индексирования и срезов
        return self.data[i]
    def __iter__(self): # Предпочтительный для итераций
        print('iter=> ', end='') # Возможен только 1 активный итератор
        self.ix = 0
        return self
    def __next__(self):
        print('next:', end='')
        if self.ix == len(self.data): raise StopIteration
        item = self.data[self.ix]
        self.ix += 1
        return item
    def __contains__(self, x): # Предпочтительный для оператора 'in'
        print('contains: ', end='')
        return x in self.data

X = Iters([1, 2, 3, 4, 5]) # Создать экземпляр
print(3 in X) # Проверка на вхождение
for i in X: # Циклы
    print(i, end=' | ')

print()
print([i ** 2 for i in X]) # Другие итерационные контексты
print( list(map(bin, X)) )
I = iter(X) # Обход вручную (именно так действуют
while True: # другие итерационные контексты)
    try:
        print(next(I), end=' @ ')
    except StopIteration:
        break





























