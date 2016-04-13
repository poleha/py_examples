"""
instances = {}
def getInstance(aClass, *args, **kwargs): # Управляет глобальной таблицей
    if aClass not in instances: # Добавьте **kargs, чтобы обрабатывать
                                    # именованные аргументы
        instances[aClass] = aClass(*args) # По одному элементу словаря для
    return instances[aClass] # каждого класса

def singleton(aClass): # На этапе декорирования
    def onCall(*args): # На этапе создания экземпляра
        return getInstance(aClass, *args)
    return onCall
"""


def singleton(aClass): # На этапе декорирования
    instance = None
    def onCall(*args, **kwargs): # На этапе создания экземпляра
        nonlocal instance # nonlocal доступна в 3.0 и выше
        if instance == None:
            instance = aClass(*args, **kwargs) # По одной области видимости
        return instance # на каждый класс
    return onCall


"""

class singleton:
    def __init__(self, aClass):
        self.cls = aClass
        self.instance = None
    def __call__(self, *args, **kwargs):
        if self.instance == None:
            self.instance = self.cls(*args, **kwargs)
        return self.instance

"""

@singleton # Person = singleton(Person)
class Person: # Присвоит onCall имени Person
    def __init__(self, name, hours, rate): # onCall сохранит Person
        self.name = name
        self.hours = hours
        self.rate = rate
    def pay(self):
        return self.hours * self.rate

@singleton # Spam = singleton(Spam)
class Spam: # Присвоит onCall имени Spam
    def __init__(self, val): # onCall сохранит Spam
        self.attr = val

bob = Person('Bob', 40, 10) # В действительности вызовет onCall
print(bob.name, bob.pay())
sue = Person('Sue', 50, 20) # Тот же самый единственный объект
print(sue.name, sue.pay())
X = Spam(42) # Один экземпляр Person, один – Spam
Y = Spam(99)
print(X.attr, Y.attr)