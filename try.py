#Аналоги
def counter(func):
    def new_func(*args, **kwargs):
        new_func.count +=1
        print(func)
        return func(*args, **kwargs)
    new_func.count = 0
    return new_func

class counter:
    def __init__(self, func):
        self.func = func
        self. count = 0
    def __call__(self, *args, **kwargs):
        self.count += 1
        self.func(*args, **kwargs)

@counter
def mfun(a):
    print(a)

mfun('123')
mfun('234')
print(mfun.count)
