# Подкласс встроенного типа/класса list.
# Отображает диапазон 1..N на 0..N-1; вызывает встроенную версию.
class MyList(list):
    def __getitem__(self, offset):
        print('(indexing %s at %s)' % (self, offset))
        return list.__getitem__(self, offset - 1)

if __name__ == '__main__':
    print(list('abc'))
    x = MyList('abc') # __init__ наследуется из списка
    print(x) # __repr__ наследуется из списка
    print(x[1]) # MyList.__getitem__
    print(x[3]) # Изменяет поведение метода суперкласса
    x.append('spam'); print(x) # Атрибуты, унаследованные от суперкласса list
    x.reverse(); print(x)