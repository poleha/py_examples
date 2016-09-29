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