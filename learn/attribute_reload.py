class Reloader():
    def __init__(self, attr1):
        self.attr1 = attr1


    def __getitem__(self, index): # Вызывается при индексировании или
        print('getitem:', index) # извлечении среза
        return self.data[index] #

class Indexer:
    data = [5, 6, 7, 8, 9]
    def __getitem__(self, index): # Вызывается при индексировании или
        print('getitem:', index) # извлечении среза
        return self.data[index] # Выполняет индексирование
        # или извлекает срез

    def __setitem__(self, index, value): # Реализует присваивание
                                             # по индексу или по срезу
        self.data[index] = value # Приcваивание по индексу или по срезу

class C:
    def __index__(self):
        return 255


class stepper:
    def __getitem__(self, i):
        return self.data[i]


class Squares:
    def __init__(self, start, stop): # Сохранить состояние при создании
        self.value = start - 1
        self.stop = stop
    def __iter__(self): # Возвращает итератор в iter()
        return self
    def __next__(self): # Возвращает квадрат в каждой итерации
        if self.value == self.stop: # Также вызывается функцией next
            raise StopIteration
        self.value += 1
        return self.value ** 2




if __name__ == '__main__':
    """
    X = Indexer()
    X[0] # При индексировании __getitem__
    X[1]
    X[-1]

    X = C()
    hex(X)
    print(('C' * 256)[X])

    X = stepper() # X -
    X.data = "Spam"
    X[1]
    for item in X:
        print(item, end=' ')
    """
    for i in Squares(1, 5): # for вызывает iter(), который вызывает __iter__()
        print(i, end=' ') # на каждой итерации вызывается __next__()
