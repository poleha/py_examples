import time
def timer(label='', trace=True): # Аргументы декоратора: сохраняются
    class Timer:
        def __init__(self, func): # На этапе декорирования сохраняется
            self.func = func # декорируемая функция
            self.alltime = 0
        def __call__(self, *args, **kargs): # При вызове: вызывается оригинал
            start = time.clock()
            result = self.func(*args, **kargs)
            elapsed = time.clock() - start
            self.alltime += elapsed
            if trace:
                format = '%s %s: %.5f, %.5f'
                values = (label, self.func.__name__, elapsed, self.alltime)
                print(format % values)
            return result

        def __get__(self, instance, owner):
            def wrapper(*args, **kwargs):
                    return self(instance, *args, **kwargs)
            return wrapper

    return Timer



def tracer(func): # Вместо класса с методом __call__ используется функция
    calls = 0 # Иначе “self” будет представлять экземпляр декоратора!
    def onCall(*args, **kwargs):
        nonlocal calls
        calls += 1
        print('call %s to %s' % (calls, func.__name__))
        return func(*args, **kwargs)
    return onCall

"""
def timer(label='', trace=True): # Аргументы декоратора: сохраняются
def onDecorator(func): # На этапе декорирования сохраняется функция
def onCall(*args, **kargs): # При вызове: вызывается оригинал
start = time.clock() # Информация в области видимости +
result = func(*args, **kargs) # атрибуты функции
elapsed = time.clock() - start
onCall.alltime += elapsed
if trace:
format = '%s%s: %.5f, %.5f'
values = (label, func.__name__, elapsed, onCall.alltime)
print(format % values)
return result
onCall.alltime = 0
return onCall
return onDecorator
"""





if __name__ == '__main__':
    @timer()
    def listcomp(N):
        return [x * 2 for x in range(N)]
    @timer()
    def mapcall(N):
        return list(map((lambda x: x * 2), range(N)))

    result = listcomp(5) # Хронометраж данного вызова, всех вызовов,
    listcomp(50000) # возвращаемое значение
    listcomp(500000)
    listcomp(1000000)
    print(result)
    print('')
    result = mapcall(5)
    mapcall(50000)
    mapcall(500000)
    mapcall(1000000)
    print(result)
    class Cl:
        @timer()
        def go(self, a, b):
            print(a + b)

    ob = Cl()
    ob.go(1,2)