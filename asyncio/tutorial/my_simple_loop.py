import types
from collections import deque

class Loop:
    def __init__(self):
        self.q = deque()
        self.running = False

    def run(self):
        self.running = True
        while self.running and self.q:
            task = self.q.popleft()
            res = task()
        return res

    def schedule(self, coroutine, stack=(), val=None):
        def resume():
            res = coroutine.send(val)
            if isinstance(res, types.GeneratorType):
                self.schedule(coroutine=res, stack=(coroutine, stack))
            elif stack:
                self.schedule(stack[0], stack=stack[1], val=res)
        self.q.append(resume)

"""
def coroutine(func):
    def wrapper(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr
    return wrapper
"""

def sub_sub_task():
    while True:
        yield 5


def sub_task():
    res = yield from sub_sub_task()
    yield res

def task():
    res = yield sub_task()
    print(res)
    yield res

def simple_task():
    print('simple_task')
    yield

loop = Loop()

loop.schedule(task())
loop.schedule(simple_task())

loop.run()

"""
def test(x):
    y = yield x
    yield y

cr = test(5)
#Получает x как функция, ничего не выполняет
print(cr.__next__())
#возвращает x
print(cr.send(6))
#получает y и с первым yield и возвращает со вторым
"""