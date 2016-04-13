"""
Декораторы Private и Public для объявления частных и общедоступных атрибутов.
Управляют доступом к атрибутам, хранящимся в экземпляре или наследуемым
от классов. Декоратор Private объявляет атрибуты, которые недоступны за
пределами декорируемого класса, а декоратор Public объявляет все атрибуты,
которые, наоборот, будут доступны. Внимание: в Python 3.0 эти декораторы
оказывают воздействие только на атрибуты с обычными именами – вызовы методов
перегрузки операторов с именами вида __X__, которые неявно производятся
встроенными операциями, не перехватываются методами __getattr__ и __getattribute__
в классах нового стиля.
Добавьте здесь реализации методов вида __X__ и с их помощью делегируйте выполнение
операций встроенным объектам.
"""
traceMe = True
def trace(*args):
    if traceMe: print('[' + ' '.join(map(str, args)) + ']')
def accessControl(failIf):
    def onDecorator(aClass):
        if not __debug__:
            return aClass
        class onInstance:
            #def __str__(self):
            #    return str(self.__wrapped)
            def __init__(self, *args, **kargs):
                self.__wrapped = aClass(*args, **kargs)
            def __getattr__(self, attr):
                trace('get:', attr)
                if failIf(attr):
                    raise TypeError('private attribute fetch: ' + attr)
                else:
                    return getattr(self.__wrapped, attr)
            def __setattr__(self, attr, value):
                trace('set:', attr, value)
                if attr == '_onInstance__wrapped':
                    self.__dict__[attr] = value
                elif failIf(attr):
                    raise TypeError('private attribute change: ' + attr)
                else:
                    setattr(self.__wrapped, attr, value)
        return onInstance
    return onDecorator

def Private(*attributes):
    return accessControl(failIf=(lambda attr: attr in attributes))

def Public(*attributes):
    return accessControl(failIf=(lambda attr: attr not in attributes))



@Private('age') # Person = Private('age')(Person)
class Person: # Person = onInstance с информацией о состоянии
    def __init__(self, name, age):
        self.name = name
        self.age = age # Внутри доступ к атрибутам не ограничивается

X = Person('Bob', 40)
print(X.name) # Попытки доступа снаружи проверяются
#'Bob'
X.name = 'Sue'
print(X.name)
#'Sue'
print(X.age)
X.age = 'Tom'
@Public('name')
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
X = Person('bob', 40) # X – экземпляр onInstance
print(X.name) # экземп. Person встраивается в экземп. onInstance
#'bob'
X.name = 'Sue'
print(X.name)
#'Sue'
print(X.age)
X.age = 'Tom'
