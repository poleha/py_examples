#Файл checkio тоже для перечитываения

# Управляемые аттрибуты


#***********************************************************************************************************
#***********************************************************************************************************
#***********************************************************************************************************
#Управляемые аттрибуты.Дескрипторы, property

"""
Дескрипторы атрибутов классов
Дескрипторы позволяют определить методы-
обработчики __get__, __set__ и __delete__ в отдельном классе, которые ав-
томатически вызываются при обращении к атрибуту, которому присвоен
экземпляр этого класса.
"""


#******************** stud
class MyProperty:   #https://docs.python.org/3/howto/descriptor.html#properties
    "Emulate PyProperty_Type() in Objects/descrobject.c"

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self #for MyPerson.name call
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)



class MyPerson:
    def __init__(self):
        self._name = ''

    def getter(self):
        return self._name

    def setter(self,value):
        self._name = value.title()

    def deleter(self):
        del self._name

    name = MyProperty(getter, setter, deleter)


class MyPerson2:
    def __init__(self):
        self._name = ''

    @MyProperty
    def name(self):
        return self._name

    @name.setter
    def name(self,value):
        self._name = value.title()

    @name.deleter
    def name(self):
        del self._name


person = MyPerson()
#person.setter('alex')  - без проперти
#print(person.getter()) - без проперти

person.name = 'alex'
print(person.name)
print(person.__dict__)
print(person.__class__.__dict__)
print(type(person).__dict__)




#*************************
class ExternalStorage:
    __slots__ = ("attribute_name",)
    __storage = {}

    def __init__(self, attribute_name):
        self.attribute_name = attribute_name

    def __set__(self, instance, value):
        self.__storage[id(instance), self.attribute_name] = value #tuple as dict key

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return self.__storage[id(instance), self.attribute_name]

class Point:
    __slots__ = ()
    x = ExternalStorage("x")
    y = ExternalStorage("y")

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

p1 = Point(1,2)
p2 = Point(3,4)
print(p1.x, p1.y)

#tuple as dict key
a = {}
a['123','456'] = 1
print(a)
#******************************






#*************************************** stud
class C(object):
    def __init__(self):
        self._x = None

    @MyProperty
    def x(self):
        """I'm the 'x' property."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @x.deleter
    def x(self):
        del self._x


#*************************************** stud
class Person:

    def addProperty(self, attribute):
        # create local setter and getter with a particular attribute name
        getter = lambda self: self._getProperty(attribute)
        setter = lambda self, value: self._setProperty(attribute, value)

        # construct property attribute and add it to the class
        setattr(self.__class__, attribute, property(fget=getter, \
                                                    fset=setter, \
                                                    doc="Auto-generated method"))

    def _setProperty(self, attribute, value):
        print("Setting: %s = %s" %(attribute, value))
        setattr(self, '_' + attribute, value.title())

    def _getProperty(self, attribute):
        print("Getting: %s" %attribute)
        return getattr(self, '_' + attribute)



#>>> user = Person()
#>>> user.addProperty('name')
#>>> user.addProperty('phone')
#>>> user.name = 'john smith'
#Setting: name = john smith
#>>> user.phone = '12345'
#Setting: phone = 12345
#>>> user.name
#Getting: name
#'John Smith'
#>>> user.__dict__
#{'_phone': '12345', '_name': 'John Smith'}





#***********************************************************************************************************
#***********************************************************************************************************
#***********************************************************************************************************
#Управляемые аттрибуты.getattr, getattribute


def __getattribute__(self, name):
    x = object.__getattribute__(self, 'other') # Принудительный вызов метода суперкласса
    # тут аналогов нет, так как обращение к __dict__ тоже вызывает рекурсию

def __setattr__(self, name, value):
    self.__dict__[name] = value # С использованием словаря атрибутов. Присваеваем значение ключу словаря, а не аттрибуту

def __setattr__(self, name, value):
    object.__setattr__(self, name, value) # Принудительный вызов метода суперкласса


#******************************

class Gattr:
    def __init__(self):
        self.attr = 1
    def __repr__(self):
        return 'Object {0} with attr={1}'.format(self.__class__.__name__, self.attr)
    def __getattribute__(self, item):
        print('Tracing {0}!!!!!!!!!'.format(item))
        return object.__getattribute__(self, item)
    def __add__(self, other):
        return self.attr + other
"""
ob = Gattr()
print(ob + 3) #Не протрейсится, но вызовет def __add__(self, other)
Поиск аттрибутов для встроенных операций начинается с классов. Это значит, что методы __getattr* не будут
#вызываться(а они вызываются из экземпляра). Интерпретатор будет смотреть в классе. Есть __repl__ или __add__
#или любой__*__? в классе. Нет? Тогда ищем выше и находим в object(если там есть)
print(ob)   #Не протрейсится, но вызовет метод def __repr__(self):  Поиск аттрибутов начинается с классов
print(ob.__add__(4)) #Протрейсится
"""

#***************


class Gattr:
    def __getattr__(self, item):    #Только для неопределенных ни в одной доступной зоне видимости аттрибутов
        print('tracing __getattr__', item)
        if item == 'attr':
            return 1
        else:
            raise AttributeError

class GetAttribute:
    attr = 1
    def __getattribute__(self, item):   #Для всех аттрибутов. Не вызывается при ob + 3, print(ob), см. выше.
        print('tracing __getattribute__', item)
        return object.__getattribute__(self, item)

class SetAttr:
    def __setattr__(self, key, value):      #Для всех аттрибутов
        print('tracing __setattr__')
        #object.__setattr__(self, key, value)
        self.__dict__[key] = value #Присваиваем значение не аттрибуту, а словарю


gattr = Gattr()
getattribute = GetAttribute()
setattr = SetAttr()
print(gattr.attr)
print(getattribute.attr)
setattr.attr = 1



#*********************************

"""
Два случая, когда метод не получает self
1)test
Мы переопределили функцию __getattribute__, а это она вызывает __get__ для функции(Класс 'function' имеет метод __get__)
и связывает функцию с экземпляром, что дает связанный метод
2)name
эта строчка  return object.__getattribute__(self, item) вызывает DescName.__get__. В обычном случае это метод
функции, и функция привязывается к экземпляру. Но в нашем случае этот механизм не срабатывает
3)(получает):test2, test3 вызывает обычный метод __get__ для дескпиптора, коим является класс function. Тут первым аргументом
будет self
"""

def test2(self, *args, **kwargs):
    print(self, args, kwargs)


class DescName:
    def __get__(self, instance, owner):
        return lambda *args, **kwargs : print(args, kwargs)

class Cls:
    def __getattribute__(self, item):
        if item == 'test':
            return lambda *args, **kwargs : print(args, kwargs)
        return object.__getattribute__(self, item) #Если это закомментировать, то функция name не вызовется.
                                                    #Причина в том, что это __getattribute__ вызывает __get__
    test2 = test2

    test3 = lambda self, *args, **kwargs: print(self, args, kwargs)

    name = DescName()

ob = Cls()
ob.test(1,2,3, named = 4) #(1, 2, 3) {'named': 4}
ob.name('sam', 'mike', named = 'exl') #('sam', 'mike') {'named': 'exl'}
ob.test2(3, 'hike', named = 'word') #<__main__.Cls object at 0x7fa5485dca90> (3, 'hike') {'named': 'word'}
ob.test3(4, 'super', named = 'world') #<__main__.Cls object at 0x7fa5485dca90> (4, 'super') {'named': 'world'}

#*************************************************




#1191
#For objects, the machinery is in object.__getattribute__()
#  which transforms b.x into type(b).__dict__['x'].__get__(b, type(b))

class Desc:
    def __get__(self, instance, owner=None):
        return instance._attr

#Думаю, что как-то так
class Cls:
    def __getattribute__(self, item):
        if item in type(self).__dict__: #Только тут и далее нужно учитывать все суперклассы, но идея такая
            if hasattr(type(self).__dict__[item], '__get__'):
                return type(self).__dict__[item].__get__(self, type(self))
            else:
                return type(self).__dict__[item]
        else:
            return object.__getattribute__(self, '__dict__')[item]
            #Ищем в __dict__ в экземпляре, но это вызвало бы рекурсию





class SubCls(Cls):
    def __init__(self, i_attr1):
        self.i_attr1 = i_attr1
        self._attr = 'i_attr_desc'

    c_attr = 'c_attr'


ob = SubCls('i_attr1')
ob.i_attr2 = 'i_attr2'
SubCls.i_attr_desc = Desc()

print(ob.i_attr1) #i_attr1
print(ob.i_attr2) #i_attr2
print(ob.c_attr) #c_attr
print(ob.i_attr_desc) #i_attr_desc



#**********************

class Desc:
    def __get__(self, instance, owner=None):
        return instance._attr

class A:
    def _attr(self, text):
        print(text)

attr = Desc()
A.attr = attr

ob = A()

ob.attr('1')
attr.__get__(ob)('2')
Desc.__get__(attr, ob, A)('3')


#******************
#Аналог на наследовании. Аналог чего - не ясно, так как перераскидал все. Но пусть будет так.
class PrivateExc(Exception): pass # Подробнее об исключениях позднее

class Privacy:
    def __setattr__(self, attrname, value): # Вызывается self.attrname = value
        if attrname in self.privates:
            raise PrivateExc(attrname, self)
        else:
            self.__dict__[attrname] = value # Self.attrname = value
                                            # вызовет зацикливание!
            #object.__setattr__(self, attrname, value) # Или так
    def __getattribute__(self, attrname):
        if attrname in object.__getattribute__(self, 'privates'):
            raise PrivateExc(attrname, self)
        else:
            return object.__getattribute__(self, attrname)

class Test1(Privacy):
    privates = ['age']

class Test2(Privacy):
    privates = ['name', 'pay']
    def __init__(self):
        self.__dict__['name'] = 'Tom'

x = Test1()
y = Test2()
x.name = 'Bob'
#y.name = 'Sue' # <== ошибка
y.age = 30
#x.age = 40 # <== ошибка
#y.name - ощибка
#***************************

"""
>>> class D:
... __slots__ = ['a', 'b', '__dict__'] # Добавить __dict__ в слоты
... c = 3 # Атрибуты класса действуют как обычно
... def __init__(self): self.d = 4 # Имя d будет добавлено в __dict__,
... # а не в __slots__
>>> X = D()
>>> X.d
4
>>> X.__dict__ # Некоторые объекты имеют оба атрибута, __dict__ и __slots__
{'d': 4} # getattr() может извлекать атрибуты любого типа
>>> X.__slots__
['a', 'b', '__dict__']
>>> X.c
3
>>> X.a # Все атрибуты экземпляра не определены,
AttributeError: a # пока им не будет присвоено значение
>>> X.a = 1
>>> getattr(X, 'a',), getattr(X, 'c'), getattr(X, 'd')
(1, 3, 4)


>>> for attr in list(getattr(X,'__dict__', [])) + getattr(X, '__slots__', []):
... print(attr, '=>', getattr(X, attr))

"""
#******************************

#Слоты — это список атрибутов, задаваемый в заголовке класса с помощью __slots__.
# В инстансе необходимо назначить атрибут, прежде чем пользоваться им:
class limiter(object):
    __slots__ = ['age', 'name', 'job']

x=limiter()
x.age = 20
x.attr = 1 #error



#***********************************************************************************************************
#***********************************************************************************************************
#***********************************************************************************************************
#Декораторы

#******************
def decorator(F): # F – функция или метод, не связанный с экземпляром
    def wrapper(*args, **kwargs): # для методов - экземпляр класса в args[0]
        return F(*args, **kwargs) #– вызов функции или метода
    return wrapper

@decorator
def func(x, y): # func = decorator(func)
    return x + y
print(func(5, 7)) # В действительности вызовет wrapper(5, 7)   #12

class C:
    @decorator
    def method(self, x, y): # method = decorator(method)
        return x + y # Присвоит простую функцию

X = C()
print(X.method(5, 7)) # В действительности вызовет wrapper(X, 5, 7), поскольку #12
                #X.method(5, 7) = wrapper.__get__(X)(5 , 7) = wrapper(X, 5, 7)


#************************************
# study
def decorator(cls): # На этапе декорирования @
    class Wrapper:
        def __init__(self, *args, **kwargs): # На этапе создании экземпляра
            self.wrapped = cls(*args, **kwargs)
        def __getattr__(self, item): # Вызывается при обращении к неопределенному атрибуту экземпляра
                                    # класса Wrapper, коими для
                                    #него являются все аттрибуты задекорированного класса и его экземпляров
                                    #Вызывается из __getattribute__, потому для
                                    # object не определен. Вероятно, ищется в экземпляре *
            print('Getting {0}'.format(item))
            return super(cls, self.wrapped).__getattribute__(item)
            #return super(cls, self.wrapped).__getattr__(item)    #error *

            #return object.__getattribute__(self.wrapped, item)
            #return object.__getattr__(self.wrapped, item) #error *

            #return getattr(self.wrapped, item)
            #return cls.__getattribute__(self.wrapped, item)
            #return self.wrapped.__dict__[item] #Так нельзя в общем случае, поскольку это может быть аттрибут класса
            #return self.wrapped.__getattribute__(item)

        def __setattr__(self, key, value):
            if key == 'wrapped':
                super().__setattr__(key, value)
                #object.__setattr__(self, key, value)
                #self.__dict__[key] = value  #Присваиваем значение словарю, а не аттрибуту
                #type(self).__setattr__(self, key, value) #error, unlimited recursion
                #setattr(self, key, value) #error, unlimited recursion
                #self._setattr_(key, value) #error, unlimited recursion
            else:
                self.wrapped.__dict__[key] = value
                #super(cls, self.wrapped).__setattr__(key, value)
                #object.__setattr__(self.wrapped, key, value)
                #cls.__setattr__(self.wrapped, key, value)
                #self.wrapped.__setattr__(key, value)
                #setattr(self.wrapped, key, value)
    return Wrapper

@decorator
class C: # C = decorator(C)
    def __init__(self, x, y): # Вызывается методом Wrapper.__init__
        self.attr = 'spam'


x = C(6, 7) # В действительности вызовет Wrapper(6, 7)
print(x.attr) # Вызовет Wrapper.__getattr__, выведет “spam”
x.attr2 = 2
print(x.attr2)


#**************************
#Аналогичный пример с ошибкой

class Decorator:
    def __init__(self, C): # На этапе декорирования @
        self.C = C
    def __call__(self, *args, **kwargs): # На этапе создания экземпляра
        self.wrapped = self.C(*args, **kwargs)
        return self
    def __getattr__(self, attrname): # Вызывается при обращении к атрибуту
        return getattr(self.wrapped, attrname)

@Decorator
class C: ... # C = Decorator(C), то есть мы на этом этапе создали экземпляр класса Decorator(__init__)
x = C()      #А здесь мы просто вызываем этот экземпляр(__call__)
y = C() # Затрет x! - поскольку мы вызываем тот же экземпляр и затираем его свойство wrapped
#*********************

#****************************
#Ошибка:

class decorator:
    def __init__(self, func): # func – это метод, не связанный
        print('__init__', self) # с экземпляром
        self.func = func
    def __call__(self, *args, **kwargs): # self – это экземпляр декоратора
        print('__call__', self)
        print('__call__ - args', args)
        self.func(*args, **kwargs)

class C:
    @decorator
    def method(self, x, y): # method = decorator(method)
        print('method', self)

ob = C()
ob.method(1,2)  #вызываем decorator.__call__. Очевидно, что self для него - экземпляр декоратора

#********************************
#Декратор одновременно для функции и метода(правильный вариант предыдущего, один из. Ниже еще.)
# study
class tracer:
    def __init__(self, func): # На этапе декорирования @
        self.calls = 0 # Сохраняет функцию для последующего вызова
        self.func = func
    def __call__(self, *args, **kwargs): # Вызывается при обращениях к
        self.calls += 1 # оригинальной функции
        print('call %s to %s' % (self.calls, self.func.__name__))
        return self.func(*args, **kwargs)
    def __get__(self, instance, owner): # Вызывается при обращении к атрибуту
        class wrapper:
            def __init__(self, desc, subj): # Сохраняет оба экземпляра
                self.desc = desc # Делегирует вызов дескриптору
                self.subj = subj
            def __call__(self, *args, **kwargs):
                return self.desc(self.subj, *args, **kwargs) # Вызовет tracer.__call__
            #def __call__(self2, *args, **kwargs): Можно и так, но
            #    return self(instance, *args, **kwargs) это глупость
        return wrapper(self, instance) #self - экз. tracer, instance - экз. Person
        #Получается, что мы подменяем метод на дескриптор. При вызове метода мы на самом деле будем вызывать
        #эту функцию, то есть для каждого вызова задекорированного метода мы будем создавать экземпляр оболочки.
        #При обращении к аттрибуту(вызове метода) сначала вызывается tracer__get__, потом создается wrapper
        #и уже он вызывается. При этом он возвращает Вызовет tracer.__call__
        #Проблема в том, что при обычном вызове tracer.__call__ первый параметр - экземпляр tracer, а нам нужно, чтобы
        #это был экземпляр Person. Мы при каждом вызове создаем новый экземпляр объекта-оболочки и сразу вызываем его.


#************************

#Аналог на функциях
class tracer(object):
    def __init__(self, func): # На этапе декорирования @
        self.calls = 0 # Сохраняет функцию для последующего вызова
        self.func = func
    def __call__(self, *args, **kwargs): # Вызывается при обращениях к
        self.calls += 1 # оригинальной функции
        print('call %s to %s' % (self.calls, self.func.__name__))
        return self.func(*args, **kwargs)
    def __get__(self, instance, owner): # Вызывается при обращении к методу
        def wrapper(*args, **kwargs): # Сохраняет оба экземпляра
            return self(instance, *args, **kwargs) # Вызовет __call__
        return wrapper

#*****************************
def tracer(func):
    count = 0
    def wrapper(*args, **kwargs):
        nonlocal count
        count += 1
        print('Количество вызовов', func.__name__, count)
        return func(*args, **kwargs)
    return wrapper
######
def tracer(func):
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        print('Количество вызовов', func.__name__, wrapper.count)
        return func(*args, **kwargs)
    wrapper.count = 0
    return wrapper

#***************************
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
                format = '%s %s: %.5f, %.5f' #https://docs.python.org/3.3/library/string.html#formatspec
                                            #%.5f - 5 символов после запятой. f - принципиально
                values = (label, self.func.__name__, elapsed, self.alltime)
                print(format % values)
            return result
    return Timer


@timer(trace=True, label='[MMM]==>')
def mapcall(N):
    return map((lambda x: x * 2), range(N))
#***************************


def class_decorator(aClass):
    def func(self, *args, **kwargs):
        print(self, args, kwargs)
    aClass.func = func #func имеет метод __get__ И работает как дескриптор
    return aClass

@class_decorator
class My:
    pass

ob = My()
ob.func(1, 2)    #Первый аргемент будет self, поскольку для получения аттрибута func для экземпляра мы вызываем
                #метод класса __getattribute__, который вызывает метод __get__ аттрибута, если он есть.
                #у функции определен метод __get__, возвращающий связанную функцию

#***************  stud
#МОЕ 1191
def dec_for_dec(dec):
    def new_dec(func):
        def wrapper(self, *args, **kwargs):
            @dec
            def decorated_func(*args2, **kwargs2):
                return func.__get__(self, type(self))(*args2, **kwargs2) #bound метод экземпляра ob
                #return func(self, *args2, **kwargs2)  #unbound метод класса Person
            return decorated_func(*args, **kwargs)
        return wrapper
    return new_dec


class Tester():
    @dec_for_dec(permission_required('posts.add_comment'))
    def test(self, request):
        print('test')


request = HttpRequest()
request.user = User.objects.get(pk=3)
ob = Tester()
ob.test(request)

#**********************

#*************************************** http://www.ibm.com/developerworks/library/os-pythondescriptors/ stud
def decorator_for_decorator(orig_decorator):
    def decorator_maker(*args, **kwargs):
        def decorator(func):
            #тут мы декорируем декоратор и выполняем его
            return orig_decorator(func, *args, *kwargs)
            #7)Он возвращет результат выполнения orig_decorator(func = original_func,args = 5, kwargs)
        return decorator
        #5)Она возвращает decorator_wrapper с доступом к orig_decorator = original_decorator и args = 5
    return decorator_maker
    #2)Она возвращает decorator_maker с доступом к orig_decorator = original_decorator


@decorator_for_decorator
#1)Выполням функцию decorator_for_decorator(original_decorator)
#3)Получаем original_decorator = decorator_maker
def original_decorator(func, *args, **kwargs):
    print(args, kwargs)
    return func
    #8)Так исходный декоратор получае доступ к args = 5, выводит их(тем самым декорирует функцию) и возвращает
    #func = original_func


@original_decorator(5)
#4)Выполняем decorator_maker(5)
#6)выполняем decorator_wrapper(original_func)
#9)Получаем что original_func = original_func, но мы ее задекорировали, выведя print(args) в декораторе
def original_func(a, b):
    print(a + b)


original_func(1, 2)
#******************************
"""
Файл devtools.py: декоратор функций, выполняющий проверку аргументов на
вхождение в заданный диапазон. Проверяемые аргументы передаются декоратору в
виде именованных аргументов. В фактическом вызове функции аргументы могут
передаваться как в виде позиционных, так и в виде именованных аргументов,
при этом аргументы со значениями по умолчанию могут быть опущены.
Примеры использования приводятся в файле devtools_test.py.
"""
trace = True
def rangetest(args = None, **argchecks): # Проверяемые аргументы с диапазонами #args = None - для *args, 1191
    def onDecorator(func): # onCall сохраняет func и argchecks
        if not __debug__: # True – если "python –O main.py args..."
            return func # Обертывание только при отладке; иначе возвращается оригинальная функция
        else:
            import sys
            code = func.__code__
            allargs = code.co_varnames[:code.co_argcount]   #('a', 'b')Берем все .аргум. функции.и переменные Вообще все.
                                                            #  пример ниже. Копируем в новый кортеж?
            funcname = func.__name__
            def onCall(*pargs, **kargs):
                            # Все аргументы в кортеже pargs сопоставляются с первыми N
                            # ожидаемыми аргументами по позиции
                            # Остальные либо находятся в словаре kargs, либо опущены, как
                            # аргументы со значениями по умолчанию
                positionals = list(allargs) #['a', 'b']
                given_args = pargs[len(positionals):]   #для обработки переданных *args, 1191. Все переданные аргументы, под
                                                    #которые у функции нет позиционных
                positionals = positionals[:len(pargs)]  #Получаем из всех аргументов позиционные
                                                        #Считая количество позиционных(*) аргументов, переданных функции
                if args is not None:
                    for given_arg in given_args:
                        if given_arg < args[0] or given_arg > args[1]:
                            raise TypeError('My error')

                for (argname, (low, high)) in argchecks.items():
                            # Для всех аргументов, которые должны быть проверены
                    if argname in kargs:
                            # Аргумент был передан по имени
                        if kargs[argname] < low or kargs[argname] > high:
                            errmsg = '{0} argument "{1}" not in {2}..{3}'
                            errmsg = errmsg.format(funcname, argname,
                                                    low, high)
                            raise TypeError(errmsg)
                    elif argname in positionals:
                                            # Аргумент был передан по позиции
                            position = positionals.index(argname)
                            if pargs[position] < low or pargs[position] > high:
                                errmsg = '{0} argument "{1}" not in {2}..{3}'
                                errmsg = errmsg.format(funcname, argname,
                                                                low, high)
                                raise TypeError(errmsg)
                    else:
                                                # Аргумент не был передан: предполагается, что он
                                                    # имеет значение по умолчанию
                        if trace:
                            print('Argument "{0}" defaulted'.format(argname))
                return func(*pargs, **kargs) # OK: вызвать оригинальную
                                                                                # функцию
        return onCall
    return onDecorator

@rangetest(a=(1, 5), c=(0.0, 1.0), args=(2, 5))
def func(a, b, *args, c): # func = rangetest(func)
    d = 3
    print(a + b + c)
func(1, 2, 3, 4, 5, 6, c=0.5)

#Пример сюда же
def fun(a, b, c, d=3, *args, **kwargs):
    x = 4
    return

print(fun.__code__.co_varnames) #('a', 'b', 'c', 'd', 'args', 'kwargs', 'x')
print(fun.__code__.co_argcount) #4



# Аналог с использованием аннотаций функций
def rangetest(func):
    def onCall(*pargs, **kargs):
        argchecks = func.__annotations__
        print(argchecks)
        for check in argchecks: pass # Добавьте проверку сюда
        return func(*pargs, **kargs)
    return onCall


@rangetest
def func(a:(1, 5), b, c:(0.0, 1.0)): # func = rangetest(func)
    print(a + b + c)
func(1, 2, c=3) # Вызовет onCall, аннотации в функции func

#*************************************************************
#Мой аналог
def checker(params):
    def dec(fun):
        allargs = fun.__code__.co_varnames
        argcount = fun.__code__.co_argcount
        allargs = allargs[:argcount]

        def wrapper(*args, **kwargs):
            error_count = 0
            positionals = allargs[:len(args)]
            named = allargs[len(args):]
            for i in range(len(args)):
                if positionals[i] in params:
                    min_val, max_val = params[positionals[i]]
                    print("{0} = {1} with condition ({2},{3})".format(positionals[i], args[i], min_val, max_val))
                    if min_val < args[i] < max_val:
                        print("OK")
                    else:
                        error_count+=1
                        print("Error")
            for key in named:
                if key in params and key in kwargs:
                    min_val, max_val =  params[key]
                    print("{0} = {1} with condition ({2},{3})".format(key, kwargs[key], min_val, max_val))
                    if min_val < kwargs[key] < max_val:
                        print("OK")
                    else:
                        error_count+=1
                        print("Error")
            if error_count == 0:
                return fun(*args, **kwargs)
        return wrapper
    return dec

@checker({'a': (1,3),'b':(2,6), 'c':(1,2)})
def func(a, b, c=3):
    d = 4
    print('Success')

func(2, 7, c=1.5)


#Мой аналог 2 stud:
def limiter(**limits):
    def dec(func):
        all_args = func.__code__.co_varnames[:func.__code__.co_argcount]
        def wrapper(*args, **kwargs):
            attrs_dict = {all_args[i]: args[i] for i in range(len(args))}
            attrs_dict.update(kwargs)
            for k, (left, right) in limits.items():
                if k in attrs_dict and not (left <= attrs_dict[k] <= right):
                    raise TypeError
            return func(*args, **kwargs)
        return wrapper
    return dec


@limiter(a=(1, 5), b=(2, 4))
def fun(a, b=2):
    return a + b


print(fun(1, b=2))
#**************************************************************

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
"""
Внимание!
1) При явном вызове (x.__str__(), x.__add__(n)
a) __str__ определен для object и не попадает под власть __getattr__ и не перехватывается(__getattribute__ бы помог)
б) __add__ при явном вызове перехватывает, тк __add__ не определен для object
2) При неявном вызове(print(x) или x + n) не перехватывает потому, что поиск аттрибутов для встроенных операций
#начинается с класса. А метод __getattribute__, используемый по умолчанию для получения аттрибутов,
#работает для экземпляра, также как не работает __getattr__
#То есть для решения проблемы мы должны переопределить методы перезагрузки как показано со __str___
"""
traceMe = False
def trace(*args):
    if traceMe: print('[' + ' '.join(map(str, args)) + ']')
def accessControl(failIf):
    def onDecorator(aClass):
        if not __debug__:
            return aClass
        class onInstance:
            def __str__(self):
                return str(self.__wrapped)
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

@Private('age')
class Person:
    def __init__(self):
        self.age = 42
    def __str__(self):
        return 'Person: ' + str(self.age)
    def __add__(self, yrs):
        self.age += yrs
X = Person()
X + 10 # Начнет поиск метода __add__ начиная с класса onInstance, пропуская экземпляр. Выдаст ошибку
X.__add__(10) #Вызовет onInstance.__getattr__, который вернет нам getattr(self.__wrapped, attr) этот метод

#Пояснение:
args = (0, 1, 2, 3)
print('[' + '&&'.join(map(str, args)) + ']')  #[0&&1&&2&&3]

#********************************************

def decorator(C): # На этапе декорирования @
    class Wrapper:
        def __init__(self, *args, **kwargs): # Вызывается при создании экземпляра
            self.wrapped = C(*args, **kwargs)
        def __getattr__(self, item):
            print('getting', item)
            return getattr(self.wrapped, item)
    return Wrapper




#**************************
class Wrapper:
    def __init__(self, wrapped):
        self.wrapped = wrapped
    def __getattr__(self, item):
        print('getting', item)
        return getattr(self.wrapped, item)

def decorator(C): # На этапе декорирования @
    def onCall(*args, **kwargs): # На этапе создания экземпляра
        return Wrapper(C(*args, **kwargs)) # Встраивает экземпляр в экземпляр
    return onCall
#**************************



class Decor():
    def __init__(self, func):
        self.func = func
        self.counter = 0
    def __call__(self, *args, **kwargs):
       self.counter +=1
       print(self.counter)
       return self.func(*args, **kwargs)

@Decor
def fun(a, b):
    return a + b

#***************************


# Расширение вручную – добавление новых методов в классы
class Client1:
    def __init__(self, value):
        self.value = value
    def spam(self):
        return self.value * 2


class Client2:
    value = 'ni?'

def eggsfunc(obj):
    return obj.value * 4
def hamfunc(obj, value):
    return value + 'ham'

Client1.eggs = eggsfunc
Client1.ham = hamfunc
Client2.eggs = eggsfunc
Client2.ham = hamfunc
X = Client1('Ni!')
print(X.spam())
print(X.eggs())
print(X.ham('bacon'))
Y = Client2()
print(Y.eggs())
print(Y.ham('bacon'))

#Или таким декоратором:
def decor_maker(funcs):
    def decor(aClass):
        for name, func in funcs.items():
            setattr(aClass, name, func)
        return aClass
    return decor

def eggsfunc(obj):
            return obj.value * 4
def hamfunc(obj, value):
            return value + 'ham'


# Расширение вручную – добавление новых методов в классы
@decor_maker({'eggs': eggsfunc, 'ham': hamfunc})
class Client1:



#***********************************************************************************************************
#***********************************************************************************************************
#***********************************************************************************************************
#Метаклассы
"""
Говоря техническим языком, интерпретатор следует стандартному протоколу:
в конце инструкции class после выполнения всех вложенных инструкций и со-
хранения всех созданных имен в словаре пространства имен он вызывает объ-
ект type, чтобы создать объект класса:
class = type(classname, superclasses, attributedict)
"""
#********** stud
class Meta(type):
    @staticmethod
    def __new__(meta, classname, classbases, classattr):
        print('1Meta.__new__')
        return type.__new__(meta, classname, classbases, classattr)
        #return super(Meta, meta).__new__(meta, classname, classbases, classattr)

    def __init__(submeta, classname, classbases, classattr):
        print('2Meta.__init__')

    def __call__(submeta, classname, classbases, classattr):
        print('3Meta.__call__')
        #return type.__call__(submeta, classname, classbases, classattr)
        #return super(Meta, type).__call__(submeta, classname, classbases, classattr)
        cls = submeta.__new__(submeta, classname, classbases, classattr)
        submeta.__init__(cls, classname, classbases, classattr)
        return cls


#Meta = type('Meta', (type,), {'__call__' : Meta.__call__,'__new__' : Meta.__new__,'__init__' : Meta.__init__, })
#Meta = type.__call__(type, 'Meta', (type,), {'__call__' : Meta.__call__,'__new__' : Meta.__new__,'__init__' : Meta.__init__, })

class SubMeta(type, metaclass=Meta):
    @staticmethod
    def __new__(submeta, classname, classbases, classattr):
        print('4SubMeta.__new__')
        return type.__new__(submeta, classname, classbases, classattr)
        #return super(SubMeta, submeta).__new__(submeta, classname, classbases, classattr)

    def __init__(cls, classname, classbases, classattr):
        print('5SubMeta.__init__')

    def __call__(cls,  *args, **kwargs):
        print('6SubMeta.__call__')
        #return type.__call__(cls, *args, **kwargs)
        #return super(SubMeta, cls).__call__(cls, *args, **kwargs)
        ob = cls.__new__(cls)
        cls.__init__(ob, *args, **kwargs)
        return ob



#SubMeta = type.__call__(Meta, 'Submeta', (type,), {'__call__' : SubMeta.__call__,'__new__' : SubMeta.__new__,'__init__' : SubMeta.__init__, })


class Cls(metaclass=SubMeta):
    @staticmethod
    def __new__(cls, *args, **kwargs):
        print('7Cls.__new__')
        return object.__new__(cls)
        #return super(Cls, cls).__new__(cls)
    def __init__(ob, *args, **kwargs):
        print('8Cls.__init__')
    def __call__(ob, *args, **kwargs):
        print('9Cls.__call__')



#Cls = Meta.__call__(SubMeta, 'Cls', (), {'__call__' : Cls.__call__,'__new__' : Cls.__new__,'__init__' : Cls.__init__, })
ob = Cls(1, 2)
ob(3, 4)




#__new__ класса(метакласса) вызывается для создания экземпляра(класса)
#__init__ класса(экземпляра) вызывается для инициации экземпляра(класса)
#__call__ класса(метакласса) вызывается при вызове экземпляра(класса, что ведет к созданию экземпляра)

#Правило: чтобы получить экземпляр, нужно вызвать метод __call__ метакласса, передав в него класс

#********** stud
"""
                        object     object
object      object      type       type          object
type1-------type2-------Meta-------SubMeta-------Class-------ob

ob(*args, **kwargs) = Class.__call__(ob, *args, **kwargs)

ob = Class(*args, **kwargs) = Sumbeta.__call__(Class, *args, **kwargs) (Чтобы вызвать метод класса для экземпляра, этому методу передает экземпляр)
calls:
Class.__new__(class) => ob
Class.__init__(ob, *args, **kwargs)

Class = SubMeta(classname, supers, classdict) = Meta.__call__(submeta, classname, supers, classdict)
Submeta.__new__(submeta, classname, supers, classdict) => class
Submeta.__init__(class, classname, supers, classdict)


SubMeta = Meta(classname, supers, classdict) = type2.__call__(meta, classname, supers, classdict)
Meta.__new__(meta, classname, supers, classdict)    => sumbeta
Meta.__init__(submeta, classname, supers, classdict)


Meta = type2(classname, supers, classdict) = type1.__call__(type2, classname, supers, classdict)
За кадром:
type2.__new__(type2, classname, supers, classdict)  - тут super() не сработает, тк для type super() - это object
type2.init(Meta, classname, supers, classdict)
"""
#*************************************


#Так лучше не делать, но для примера интересно. Плюс можно поместить в один класс, но будет не так наглядно
class SuperMeta:
     def __call__(self, classname, supers, classdict):
        print('In SuperMeta.call: ', classname, supers, classdict, sep='\n...')
        Class = self.__New__(classname, supers, classdict)
        self.__Init__(Class, classname, supers, classdict)
        return Class


class SubMeta(SuperMeta):
    def __New__(self, classname, supers, classdict):
        print('In SubMeta.new: ', classname, supers, classdict, sep='\n...')
        return type(classname, supers, classdict)

    def __Init__(self, Class, classname, supers, classdict):
        print('In SubMeta init:', classname, supers, classdict, sep='\n...')
        print('...init class object:', list(Class.__dict__.keys()))

class Eggs:
    pass

print('making class')
class Spam(Eggs, metaclass=SubMeta()): # Метакласс – экземпляр обычного класса
    data = 1 # Вызывается в конце инструкции
    def meth(self, arg):
        pass
#Spam = Submeta()(classname, supers, classdict) = SuperMeta.__call__(submeta, classname, supers, classdict)
                                                                        #где submeta - экземпляр SubMeta
print('making instance')
X = Spam()
print('data:', X.data)

"""
Здесь SubMeta и SuperMeta связаны наследованием, а не как класс - экземпляр.
Метакласс  - простой вызываемый объект. Мы могли бы слить эти два класса в один, просто перенеся метод __call__
как есть.
Для создания класса мы вызываем экземпляр класса SubMeta.
1)Вызывается метод __call__, унаследованный им от SuperMeta;
2)Вызывается метод __new__, унаследованный им от SubMeta, он возвращает класс;
3)Вызывается метод __init__, унаследованный им от SubMeta. Он может инициализировать класс.
self здесь всегда - экземпляр класса SubMeta.
"""


#***********************


# Простая функция также может играть роль метакласса
def MetaFunc(classname, supers, classdict):
    print('In MetaFunc: ', classname, supers, classdict, sep='\n...')
    return type(classname, supers, classdict)
class Eggs:
    pass

print('making class')
class Spam(Eggs, metaclass=MetaFunc): # В конце вызовет простую функцию
    data = 1 # Функция возвращает класс
    def meth(self, args):
        pass

print('making instance')
X = Spam()
print('data:', X.data)

#*******************

# Управление экземплярами подобно предыдущему примеру, но с помощью метакласса
def Tracer(classname, supers, classdict): # На этапе создания класса
    aClass = type(classname, supers, classdict) # Создать клиентский класс
    class Wrapper:
        def __init__(self, *args, **kargs): # На этапе создания экземпляра
            self.wrapped = aClass(*args, **kargs)
        def __getattr__(self, attrname):
            print('Trace:', attrname) # Перехватывает обращения ко
                # всем атр., кроме .wrapped
            return getattr(self.wrapped, attrname) # Делегирует обращения
    return Wrapper # обернутому объекту



class Test(metaclass=Tracer):
    def test(self):
        print(self)


ob = Test()
ob.test()
#Trace: test
#<__main__.Test object at 0x7f318fe1a9b0>
#****************************



#********************
# Фабрика метаклассов: применяет любой декоратор ко всем методам класса
#study
from types import FunctionType
from mytools import tracer, timer
def decorateAll(decorator):
    class MetaDecorate(type):
        def __new__(meta, classname, supers, classdict):
            for attr, attrval in classdict.items():
                if type(attrval) is FunctionType:
                    classdict[attr] = decorator(attrval)
            return type.__new__(meta, classname, supers, classdict)
    return MetaDecorate

class Person(metaclass=decorateAll(tracer)):# Применить произвольный декоратор
    def __init__(self, name, pay):
        self.name = name
        self.pay = pay
    def giveRaise(self, percent):
        self.pay *= (1.0 + percent)
    def lastName(self):
        return self.name.split()[-1]


#Аналог на одних декораторах
def decorateAll(decorator):
    def DecoDecorate(aClass):
        for attr, attrval in aClass.__dict__.items():
            if type(attrval) is FunctionType:
                setattr(aClass, attr, decorator(attrval)) # Не __dict__
                #aClass.__dict__[attr] = decorator(attrval) Не сработает, см ниже *
        return aClass
    return DecoDecorate

@decorateAll(tracer) # Используется декоратор класса
class Person:
    pass
#...

#Пояснение к *: aClass.__dict__[attr] = decorator(attrval) Не сработает, см ниже *
from types import MappingProxyType
d = {'a': 1, 'b': 2}
mp = MappingProxyType(d)
d['a'] = 2
#mp['a'] = 3 #error
print(mp['a']) #2
print(d['a'])   #2
#№То есть по сути __dict__ - это не словарь, а экземпляр MappingProxyType, который обертывает словарь и делает его
#read-only


#***********************************************************************************************************
#***********************************************************************************************************
#***********************************************************************************************************
#Итераторы
#Тут экземпляр будет собственным итератором, то есть мы не сделаем вложенный цикл или несколько циклов
# одновременно
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
#************************************
# Тут итератор отдельно от экземпляра, то есть для каждого итерационного контекста создается свой экземпляр итератора
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

#****************************************

def gsquares(start, stop):
    for i in range(start, stop + 1):
        yield i ** 2


for i in gsquares(1, 5): # или: (x ** 2 for x in range(1, 6))
    print(i, end=' ')


print(list(range(1, 5))) #[1, 2, 3, 4]


#*************************************

def iter_test():
    yield 1
    yield 2
    yield 3

for i in iter_test():
    print(i)
#*****************************

A = (1, 2)
B = (3, 4)
C = zip(A, B)
D = zip(*zip(A, B))

print(list(C), end='\n') #[(1, 3), (2, 4)]
print(list(D), end='\n') #[(1, 2), (3, 4)]

#******************************************
class Reverse:
    def __init__(self, data):
        self.data = data
        self.index = len(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]

for char in Reverse('12345'):
    print(char)



#**********************************

it = iter((1, 2))
it = (1, 2).__iter__()
it = (1, 2)
#<tuple_iterator object at 0x7f55482cfd68>
print(it.__next__()) #1
print(it.__next__()) #2

#*************************

#В число итерационных контекстов языка Python входят: цикл for, генераторы
#списков, встроенная функция map, оператор in проверки вхождения,
#а также встроенные функции sorted, sum, any и all. В эту категорию также
#входят встроенные функции list и tuple, строковый метод join и операции
#присваивания последовательностей – все они следуют итерационному протоколу
#(метод __next__) для обхода итерируемых объектов.

#***********************************************************************************************************
#***********************************************************************************************************
#***********************************************************************************************************
#Исключения
#TODO доделать
"""
try: # Формат 1
    statements
except [type [as value]]: # [type [, value]] в Python 2
    statements
[except [type [as value]]:
    statements]*
[else:
    statements]
[finally:
    statements]

try: # Формат 2
    statements
finally:
    statements
"""



#***********************************************************************************************************
#***********************************************************************************************************
#***********************************************************************************************************
#Рекурсии

#********** stud
def sumtree(L):
    sum = 0
    for cur in L:                # Обход элементов одного уровня
        if not isinstance(cur, list):
            sum += x           # Числа суммируются непосредственно
        else:
            sum += sumtree(cur)  # Для списков вызывается функция
    return sum



#******************************
#********** stud
def mysum(L):
    if not L:
        return 0
    else:
        return L[0] + mysum(L[1:])     # Вызывает себя саму


#******************************
# stud
class SimpleListTree:
    def __str__(self):
        self.__visited = {}
        return self.__listclass(self.__class__)

    def __listclass(self, aClass, level=0):
        if aClass in self.__visited:
            return aClass.__name__ + str(level) + ' Visited' + '\n'
        else:
            self.__visited[aClass] = True
            strabove = ''
            for c in aClass.__bases__:
                strabove += self.__listclass(c, level+1)
            return aClass.__name__ + str(level) + '\n' + strabove
            #genabove = (self.__listclass(c, level+1) for c in aClass.__bases__)
            #return 'level = {0} {1}\n{2}'.format(level, aClass.__name__, ''.join(genabove))
    """
    Эта функция получает класс. Вызывает рекурсивно себя с каждым суперклассом класса и суперклассом суперкласса,
    пока не дойдет до object, который не имеет суперклассов. Тогда просто вернет object.
    Получает для этого класса строку strabove, хранящую в себе названия всех его суперклассов вместе с уровнем.
    Выводит уровень, класс и все, что над ним(strabove).

    Механизм:
    class A(SimpleListTree):
        pass

    __listclass(A, 0)
     strabove = __listclass(ListTree, 1)
     return A0 + strabove = SimpleListTree1 + object2

     __listclass(ListTree, 1)
     strabove = __listclass(object, 2)
     return SimpleListTree1 + strabove = SimpleListTree1 + object2

     __listclass(object, 2)
     strabove = ''
     return object2


    Генератор позволяет не получать эту строку сразу, а выдавать по требованию. Смысла особого не вижу, работает
    в 2 раза медленнее. То есть для каждой функции этот genabove содержит столько элементов, сколько баз у класса
    """

#***********************

class SimpleListTree:
    def __str__(self):
        self.__visited = {}
        return self.__lt(self.__class__)

    def __lt(self, aClass, level=0):
        if aClass in self.__visited:
            return aClass.__name__ + '-visited'
        self.__visited[aClass] = True
        above = ''
        for c in aClass.__bases__:
            above += self.__lt(c, level + 1)
        return aClass.__name__ + str(level) + ',' + above
        # C + (A + (SimpleListTree + (object + '')) + (B + (object + ''))

        #above = [self.__lt(c, level+1) for c in aClass.__bases__]
        #return aClass.__name__ + str(level) + ',' + ''.join(above)


class A(SimpleListTree):
    pass

class B:
    pass

class C(A, B):
    pass

ob = C()
print(ob)
"""
[]
['object3,']
['SimpleListTree2,object3,']
['object-visited']
['A1,SimpleListTree2,object3,', 'B1,object-visited']
C0,A1,SimpleListTree2,object3,B1,object-visited
"""




#**************************
class ListTree:
    """
    Примесный класс, в котором метод __str__ просматривает все дерево классов
    и составляет список атрибутов всех объектов, находящихся в дереве выше
    self; вызывается функциями print(), str() и возвращает сконструированную
    строку со списком; во избежание конфликтов с именами атрибутов клиентских
    классов использует имена вида __X; для рекурсивного обхода суперклассов
    использует выражение-генератор; чтобы сделать подстановку значений более
    очевидной, использует метод str.format()
    """
    def __str__(self):
        self.__visited = {}
        return '<Instance of {0}, address {1}:\n{2}{3}>'.format(
                                        self.__class__.__name__,
                                        id(self),
                                        self.__attrnames(self, 0),
                                        self.__listclass(self.__class__, 4))

    def __listclass(self, aClass, indent):
        dots = '.' * indent
        if aClass in self.__visited:
            return '\n{0}<Class {1}:, address {2}: (see above)>\n'.format(
                                                            dots,
                                                            aClass.__name__,
                                                            id(aClass))
        else:
            self.__visited[aClass] = True
            genabove = (self.__listclass(c, indent+4) for c in aClass.__bases__)
            #genabove = [self.__listclass(c, indent+4) for c in aClass.__bases__] - так принципиальная разница. Разобрать.
            return '\n{0}<Class {1}, address {2}:\n{3}{4}{5}>\n'.format(
                                                            dots,
                                                            aClass.__name__,
                                                            id(aClass),
                                                            self.__attrnames(aClass, indent),
                                                            ''.join(genabove),
                                                            dots)
    def __attrnames(self, obj, indent):
        spaces = ' ' * (indent + 4)
        result = ''
        for attr in sorted(obj.__dict__):
            if attr.startswith('__') and attr.endswith('__'):
                result += spaces + '{0}=<>\n'.format(attr)
            else:
                result += spaces + '{0}={1}\n'.format(attr, getattr(obj, attr))
        return result
#*********************************


#***********************************************************************************************************
#***********************************************************************************************************
#***********************************************************************************************************
#Функции(пока нет раздела).Области видимости.


# Like kwargs but named. We cant call without naming.
def test(a, *, b, c=None):
    print(a, b, c)

test(1, b=2)
#test(1, 2) #TypeError: test() takes 1 positional argument but 2 were given


#***********************  stud
def counter(fun):
    fun.count = 0
    count = 0
    count_list = []
    def wrapper(*args, **kwargs):
        nonlocal count #won't work without it
        #nonlocal fun # changes nothing, because it is changeable object
        #nonlocal count_list # changes nothing, because it is changeable object
        fun.count += 1
        count += 1
        wrapper.count += 1
        count_list.append((args, kwargs))
        print(fun.count)
        print(count)
        print(count_list)
        return fun(*args, **kwargs)
    wrapper.count = 0
    return wrapper

@counter
def test(a, b):
    return a + b

test(1, 2)
test(3, 4)
test(5, 6)
test(7, 8)
print(test.count) #it's wrapper.count

#*****************************
a1 = 1

def fun1():
    a2 = 2
    class C1:
        a3 = 3
        print(a1, a2, a3, a4) #not a4
        def __init__(self):
            a4 = 4
            print(a1, a2, a3, a4) #not a3
            class C2:
                print(a1, a2, a3, a4) #not a3
                def __init__(self):
                    print(a1, a2, a3, a4) #not a3
        class C3:
            print(a1, a2, a3, a4) #not a3, a4
            def __init__(self):
                print(a1, a2, a3, a4) #not a3, a4

#Если класс или функция вложена в функцию, то видят все вышестоящие области.
#Если класс или функция(то есть метод) вложены в класс, то они не видят область наружного класса. Но выше - видят.
#Метод класса видит область содержащего ее класса через self.attr, type(self).attr, self.__class__.attr


#*******************************
#Каждое свойство класса записывается в его __dict__ и извлекается оттуда при обращении, при этом свойство классу
#можно присвоить и внутри и снаружи.
#Каждое свойство функии аналогично, но свойства функциям присваиваются снаружи. Все, что внутри - это локальные
#переменные функций

glob_attr = 'glob'

def fun():
    attr1 = 1 #просто переменная в области видимости
    print('fun', attr1, fun.attr2, glob_attr) #Имеет доступ к fun в глобальной области видимости
    #print(attr2) - ошибка, это свойство объекта - функции, а не переменная в области видимости
fun.attr2 = 2 #Не аналогично присвоению внутри функции. Аттрибут объекта-функции.

fun() #1,2
#print(fun.attr1) - ошибка, это просто переменная в области видимости
print('fun.__dict__', fun.__dict__) #только attr2


class cls:
    attr1 = 1
    #cls.attr1 = -ошибка, cls тут не доступен
    #global glob_attr - без этого снаружи не изменится, с этим изменится
    glob_attr = 'changed inside cls glob attr'
    #cls.attr3 = 3 ошибка, так как cls тут не доступен
    def go(self):
        print('cls.go', cls.attr1, cls.attr2, glob_attr) #а тут доступно и своество, присвоенное снаружи класс и внутр

cls.attr2 = 2 #Аналогично присовению внутри класса

ob = cls()
ob.go() #1,2

print('cls.__dict__', cls.__dict__)
#cls.__dict__ {'attr2': 2, '__doc__': None, 'go': <function cls.go at 0x7f083cf9de18>,
# 'glob_attr': 'changed inside cls glob attr', 'attr1': 1, ... еще много
print(glob_attr) #glob Не изменен


#********************************************

# Python stores default variable between calls. default only.
def test(k, l=[]):
    for i in range(k):
        l.append(i)
    return l


print(test(3))  # [0, 1, 2]
print (test(4, [1, 2, 3]))  # [1, 2, 3, 0, 1, 2, 3] # not here
print(test(1))  # [0, 1, 2, 0]



#*********************************

def outer():
    def level1():
        print('running level1')
        def level2():
            print('running level2:', level1.__name__, outer.__name__, level2.__name__)
            #функция видит все объемлющие функции и функцию в глобальной области видимости и себя
        return level2()
    return level1()

y = 1
def outer2():
    x = 1
    def inner2():
        nonlocal x
        global y
        x += 1 #будет увеличивать x в объемлющей области видимости с каждым вызовом внутренней функции
        y = 2
        print(x)
    return inner2

inner = outer2()
inner()
inner()
#print(x) #Ошибка, это переменная в локальной области видимости
print(y) #2, изменен внутри inner2

#*********************************


#***********************************************************************************************************
#***********************************************************************************************************
#***********************************************************************************************************
#Прочее

#*************************************************
#Неизменяемые по значению. Здесь x - на самом деле ссылка на неизменяемый объект 3
def test(val):
    val += 1
    print(val) #4

x = 3
test(x)
print(x) #3


#Изменяемые по ссылке.
def test(val):
    val.append(1)


x = [3]
test(x)
print(x) #[3, 1]
#*************************************************



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



#******************************
# В Python 3.0 (и 2.6 для совместимости):
def func(a, b, c, d, k=0):
    x = 1
    y = 2
code = func.__code__ # Объект с программным кодом,
print(code.co_nlocals) # принадлежащий объекту функции
#7
print(code.co_varnames) # Все имена локальных переменных
#('a', 'b', 'c', 'd', 'k', 'x', 'y')
print(code.co_varnames[:code.co_argcount]) # Первые N локальных имен – это
#('a', 'b', 'c', 'd', 'k') # ожидаемые аргументы

import sys # Для обратной совместимости
print(sys.version_info) # [0] – старший номер версии
#sys.version_info(major=3, minor=4, micro=0, releaselevel='final', serial=0)
code = func.__code__ if sys.version_info[0] == 3 else func.func_code
#******************************


#*************************************************
class Commuter: # Тип класса распространяется на результат
    def __init__(self, val):
        self.val = val

    def __add__(self, other):
        print('__add__')
        if isinstance(other, Commuter): other = other.val
        return Commuter(self.val + other)

    def __radd__(self, other):
        print('__radd__')
        return Commuter(other + self.val)

    def __str__(self):
        return '<Commuter: %s>' % self.val
x = Commuter(88)
y = Commuter(99)
print(x + 10) # Результат – другой экземпляр класса Commuter
#__add__
#<Commuter: 98>
print(10 + y)
#__radd__
z = x + y # Нет вложения: не происходит рекурсивный вызов __radd__
print(z)
#__add__
#<Commuter: 109>

#************************************************************

#Делегирование, объект-обертка
class Wrapper:
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __getattr__(self, item):
        print('Tracing {0}'.format(item))
        return getattr(self.wrapped, item)


ob = Wrapper([1,2,3])
ob.append(5)

#********************
#*********************************************
#Псевдочастные атрибуты
class C1:
    def meth1(self):
        self.__x = 88 # Теперь x - мой атрибут
    def meth2(self): print(self.__x) # Превратится в _C1__X


class C2:
    def metha(self):
        self.__x = 99 # И мой тоже
    def methb(self): print(self.__x) # Превратится в _C2__X

class C3(C1, C2): pass

ob = C3() # В I два имени X
ob.meth1(); ob.metha()
print(ob.__dict__)
#{'_C2__x': 99, '_C1__x': 88}
ob.meth2(); ob.methb()
#88
#99

#*********************************************


#>>> def f(a, *b, c=6, **d): print(a, b, c, d) # Только именованные аргументы
#...                                           # между * и **
#>>> f(1, *(2, 3), **dict(x=4, y=5))           # Распаковывание аргументов
#1 (2, 3) 6 {'y': 5, 'x': 4}
#
#>>> def f(a, *b, **d, c=6): print(a, b, c, d) # Только именованные аргументы
#SyntaxError: invalid syntax                   # должны предшествовать **!

#>>> def f(a, *b, c=6, **d): print(a, b, c, d) # Коллекции аргументов
#...



#******************************


nudge = 1
wink = 2
nudge, wink = wink, nudge # Кортежи: обмен значениями
nudge, wink               # То же, что и T = nudge; nudge = wink; wink = T
#(2, 1)


#******************************


import sys
showall = lambda x: list(map(sys.stdout.write, x)) # Функция list
                                                       # необходима в 3.0

t = showall(['spam\n', 'toast\n', 'eggs\n'])
#spam
#toast
#eggs

showall = lambda x: [sys.stdout.write(line) for line in x]

t = showall(('bright\n', 'side\n', 'of\n', 'life\n'))
#bright
#side
#of
#life

#********************
action = (lambda x: (lambda y: x + y))
act = action(99)
act(3)
#102
((lambda x: (lambda y: x + y))(99))(4)
#103
#********************
counters = (1, 2, 3)
print(list(map((lambda x: x + 3), counters)))
#[4, 5, 6]

#********************
class Test:
    def go(self, text):
        print(text)

ob = Test()
go1 = ob.go
go2 = Test.go
go2.__get__(ob, type(ob))('bound1')
go1('bound2')
go2(ob, 'unbound3')


#*******************
def unbound1(self, *args, **kwargs):
    print(self, args, kwargs)

def unbound2(self, *args, **kwargs):
    print(self, args, kwargs)


class Cls:
    meth2 = unbound2

Cls.meth1 = unbound1

ob = Cls()
ob.meth1(1, 3, named=4)
ob.meth2(1, 3, named=4)


#********************
map(pow, [1, 2, 3], [2, 3, 4]) # 1**2, 2**3, 3**4  # 1**2, 2**3, 3**4
from functools import reduce   # В 3.0 требуется выполнить импортирование
reduce((lambda x, y: x + y), [1, 2, 3, 4])
#10
reduce((lambda x, y: x * y), [1, 2, 3, 4])
#24

print(reduce(lambda x, y: max(x, y), [5, 6, 7, 2, 1, -3, 0]))
#7

print(max([1, 3, 5, 0]))
#5

#********************
import operator, functools
functools.reduce(operator.add, [2, 4, 6]) # Оператор сложения в виде ф-ции
#********************

def fun():
    yield 1
    yield 2

f = fun
i = f()
print(next(i)) #1
print(next(i)) #2
#*******************


# map(func, seqs...) на основе использования zip
def mymap(func, *seqs):
    res = []
    for args in zip(*seqs):
        res.append(func(*args))
    return res

print(mymap(abs, [-2, -1, 0, 1, 2]))
print(mymap(pow, [1, 2, 3], [2, 3, 4, 5]))

# С использованием генератора списков

def mymap(func, *seqs):
    return [func(*args) for args in zip(*seqs)]

# С использованием генераторов: yield и (...)

def mymap(func, *seqs):
    for args in zip(*seqs):
        yield func(*args)

def mymap(func, *seqs):
    return (func(*args) for args in zip(*seqs))


# Версии zip(seqs...) и map(None, seqs...) в Python 2.6

def myzip(*seqs):
    seqs = [list(S) for S in seqs]
    res = []
    while all(seqs):
        res.append(tuple(S.pop(0) for S in seqs))
    return res

def mymapPad(*seqs, pad=None):
    seqs = [list(S) for S in seqs]
    res = []
    while any(seqs):
        res.append(tuple((S.pop(0) if S else pad) for S in seqs))
    return res

S1, S2 = 'abc', 'xyz123'
print(myzip(S1, S2))
print(mymapPad(S1, S2))
print(mymapPad(S1, S2, pad=99))


# С использованием генераторов: yield

def myzip(*seqs):
    print(seqs) #((1, 2), (3, 4))
    seqs = [list(S) for S in seqs] #Превращаем кортеж кортежей в лист листов
    print(seqs) #[[1, 2], [3, 4]]
    while all(seqs):
        yield tuple(S.pop(0) for S in seqs)


print(list(myzip((1, 2), (3, 4))))
#[(1, 3), (2, 4)]

def mymapPad(*seqs, pad=None):
    seqs = [list(S) for S in seqs]
    while any(seqs):
        yield tuple((S.pop(0) if S else pad) for S in seqs)

S1, S2 = 'abc', 'xyz123'
print(list(myzip(S1, S2)))
print(list(mymapPad(S1, S2)))
print(list(mymapPad(S1, S2, pad=99)))


def myzip(*args):
    iters = list(map(iter, args)) #Если не завернуть в list, то даже при StopIteration для iters он
    # все равно будет выдавать true(то есть это будет <map object at 0x7f753ea8eb70>)
    while iters:
        res = [next(i) for i in iters]
        yield tuple(res)


# Альтернативные реализации с вычислением длин исходных последовательностей

def myzip(*seqs):
    minlen = min(len(S) for S in seqs)
    return [tuple(S[i] for S in seqs) for i in range(minlen)]

def mymapPad(*seqs, pad=None):
    maxlen = max(len(S) for S in seqs)
    index = range(maxlen)
    return [tuple((S[i] if len(S) > i else pad) for S in seqs) for i in index]
#if len(S) > i значит, что для последовательностей (1, 2), (1, 2, 3) дойдя до индекса 2 получим для первой послед
# 2 > 2, условие не выполняется, берем pad. То есть последовательность длиннее этого индекса(а значит содержит его),
#Берем по индексу, иначе pad
#**********************************


class Spam:
    SpamInstances = 0
    def __init__(self):
        Spam.SpamInstances += 1
        #type(self).SpamInstances += 1
        #self.__class__.SpamInstances += 1
        #self.SpamInstances += 1 #Так не сработает, см далее пример
    @classmethod # print_numInstances = staticmethod(print_numInstances)
    def print_numInstances(cls):
        print('Number of instances created: ', cls.SpamInstances)

ob, ob1, ob3 = Spam(), Spam(), Spam()
Spam.print_numInstances() #3
ob.print_numInstances() #3


class Spam:
    egg = 1
    def test(self, val):
        self.egg += val

#********************
ob = Spam()
ob.test(3)
print(ob.egg) #4 !!! ВНИМАНИЕ
print(Spam.egg) #1


#*********************

class ListTree:
    def __str__(self): ...
    def other(self): ...

class Super:
    def __str__(self): ...
    def other(self): ...

class Sub(ListTree, Super): # Унаследует __str__ класса ListTree, так как он
# первый в списке
    other = Super.other # Явно выбирается версия атрибута из класса Super
    def __init__(self):
        ...
        x = Sub() # Поиск сначала выполняется в Sub и только потом в ListTree/Super

#*********************************
d = {'one': 1, 'two': 2, 'three': 3}
x = d['one']
y = d.get('two')
print(x, y) #1, 2
#***********************************

#Когда несколько операций выполняются слева направо, то кажлая последующая получает результат предыдущей, если предыдущая возвращает результат
class Cls:
    def fun(self):
        return 'aaa'

ob = Cls()
print(ob.fun().title()[:1]) #A



class Cls:
    def fun(self):
        print('aaa')

ob = Cls()
print(ob.fun().title()[:1]) #'NoneType' object has no attribute 'title'

#***********************
#Наследование, MRO, super
#super(cls, instance-or-subclass).method(*args, **kw)

#corresponds more or less to

#right-method-in-the-MRO-applied-to(instance-or-subclass, *args, **kw)
#*********************************


class A:
    def test(self):
        print('A')
        super().test()

class C:
    def test(self):
        print('C')
        #super().test() - error


class B(C):
    def test(self):
        print('B')
        super().test()


class D(A, B):
    def test(self):
        print('D')
        super().test()
        #super().test(self) - error, super() returns bound method

ob = D()
ob.test()
#D
#A
#B
#C
#************************************

class A:
    def test(self):
        print('A')


class B(A):
    def test(self):
        print('B')
        super().test()

class X:
    pass

class C(A):
    def test(self):
        print('C')
        super().test()


class D(B, X, C):
    def test(self):
        print('D')
        super().test()


d = D()

d.test()

#D
#B
#C
#A - A only once, because super() is smart
#************************************


class A:
    def test(self):
        print('A')


class B(A):
    def test(self):
        print('B')
        super().test()


class C(B):
    def test(self):
        print('C')
        super().test()


class D(B, C):
    def test(self):
        print('D')
        super().test()

#TypeError: Cannot create a consistent method resolution
#order (MRO) for bases B, C

#************************************


class A:
    def t(self):
        print('a')

class B(A):
    def t(self):
        print('b')
        super().t()

class Z(B):
    def t(self):
        print('z')
        super().t()

class C(A):
    def t(self):
        print('c')
        super().t()

class X(C):
    def t(self):
        print('x')
        super().t()


class Y(X):
    def t(self):
        print('y')
        super().t()

class D(Z, Y):
    def t(self):
        print('d')
        super().t()

d = D()
d.t()

#d
#z
#b
#y
#x
#c
#a



#********************************************


class A:
    def test(self):
        print('A')


class B(A):
    def test(self):
        print('B')
        super(B, self).test()


class C(A):
    def test(self):
        print('C')
        super(C, self).test()

class D(B, C):
    def test(self):
        print('D')
        super(D, self).test()

d = D()
d.test()

#Если есть общий суперкласс, то прежде, чем прийти к нему, обходим нижние классы
#D
#B
#C
#A

#

class A:
    def test(self):
        print('A')

class A1:
    def test(self):
        print('A1')


class B(A1):
    def test(self):
        print('B')
        super(B, self).test()


class C(A):
    def test(self):
        print('C')
        super(C, self).test()

class D(B, C):
    def test(self):
        print('D')
        super(D, self).test()

d = D()
d.test()


#D
#B
#A1



#***************************************
class parent(object):
    def __init__(self): self.__f = 2

    def get(self):
        return self.__f

class child(parent):
    def __init__(self):
        self.__f = 1
        parent.__init__(self)

    def cget(self):
        return self.__f

c = child()
print(c.get()) #2
print(c.cget()) #1
print(c.__dict__) # {'_child__f': 1, '_parent__f': 2}

#******************************************
class A:
    @classmethod
    def test(cls):
        print('from A', cls.__name__)

class B(A):
    @classmethod
    def test(cls):
        print('from B', cls.__name__)

class C(B):
    @classmethod
    def test(cls):
        print('from C', cls.__name__)


ob = C()
super(C, C).test()
#from B C
super(B, C).test()
#from A, C
#super(A, C).test()
#error, object does not have test method
#************************************

class A:
    def test(self):
        print('from A', self)

class B(A):
    def test(self):
        print('from B', self)

class C(B):
    def test(self):
        print('from C', self)

ob = C()
super(C, ob).test()
#from B <__main__.C object at 0x7fddc5410048>
super(B, ob).test()
#from A <__main__.C object at 0x7fddc5410048>
#super(A, ob).test()
#error, object does not have test method

print(super(C, C).test) ##<function B.test at 0x7f8dc5b7ce18>  - unbound method
print(super(B, C).test) #<function A.test at 0x7f8500b202f0> - unbound method, поскольку test - не classmethod

super(C, C).test(ob) # unbound method
#super(C, B).test(ob) #  obj must be an instance or subtype of type, error
super(B, C).test(ob) #from A <__main__.C object at 0x7fda70180908>


#unbound super != unbound method
super(C).__get__(ob).test()

#**********************
#usage of unbound super
class B(object):
    a = 1

class C(B):
    pass

class D(C):
    sup = super(C)

d = D()
print(d.sup.a) #1
print(D.sup.__get__(d).a) #1
#*******************  unbound super
# study


class A:
    @classmethod
    def class_test(cls):
        print("class A")

    def test(self):
        print("A")


class B(A):
    @classmethod
    def class_test(cls):
        print("class B")
        cls.__super.__get__(cls).class_test()  #сработает только так, поскольку протокол дескриптора работает только для
                                                # instance.desc_instance

    def test(self):
        print("B")
        self.__super.test()

B._B__super = super(B)

class Meta(type):
    pass


class C(A, metaclass=Meta):
    @classmethod
    def class_test(cls):
        print("class C")
        cls._super.class_test()


Meta._super = super(C)


ob = B()
ob.test()
#B
#A
B.class_test()
#class B
#class A
C.class_test()
#class C
#class A


#**************************** median
#study
data = [1, 4, 5, 6, 2]
checkio = lambda d: (lambda t, n: t[n] + t[-n-1])(sorted(d), len(d)//2)/2
#checkio - это функция, которая возвращает результат выполнения другой функции с полученным аргументом, деленный на 2


print(checkio(data)) #4.0
print(5//2) # 2
print(sorted(data)) #[1, 2, 4, 5, 6]
print(sorted(data)[2]) # 4
print(sorted(data)[-3]) # 4

#********************************


"""
Атрибуты механизма интроспекции
#__class, __dict__, __code__(для функций)

Методы перегрузки операторов
__str__, __add__

Методы обработки обращений к атрибутам
__getattr__, __setattr__ и __getattribute__


Свойства классов
property


Дескрипторы атрибутов классов
Дескрипторы позволяют определить методы-
обработчики __get__, __set__ и __delete__ в отдельном классе, которые ав-
томатически вызываются при обращении к атрибуту, которому присвоен
экземпляр этого класса.

Декораторы функций и классов
"""

"""
Объектная модель
>>> type(‘spam’)
<class ‘str’>
>>> type(str)
<class ‘type’>
>>> isinstance(‘spam’, object) # То же относится и к встроенным типам
True # (классам)
>>> isinstance(str, object)
True
Фактически сам класс type наследует класс object, а класс object наследует
класс type(не так. object не наследует класс type, а является его экземпляром) , даже при том,
что оба они являются совершенно различными объектами, – циклическая связь, венчающая объектную модель и вытекающая из
того факта, что типы являются классами, которые генерируют другие классы:
>>> type(type) # Все классы – это типы, и наоборот
<class ‘type’>
>>> type(object)
<class ‘type’>
>>> isinstance(type, object) # Все классы наследуют object, даже класс type
x является экземпляром A, A является субклассом B => x является экземпляром B
type( то есть x) является экземпляром type(то есть A), type( то есть A) является субклассом object( то есть B) => type( то есть x) является экземпляром object( то есть B)

True
>>> isinstance(object, type) # Типы создают классы, и type является классом
Очевидно, object - это экземпляр type
True
>>> type is object
False

print(object.__class__) #<class 'type'> object являтся экземпряром type
print(object.__bases__) #() object не имеет базовых классов, то есть он класс высшего уровня
print(type.__class__)   #<class 'type'> type является экземпляром класса type
print(type.__bases__) #(<class 'object'>,)  type является подклассом object

type
class: type  метакласс, то есть type это экземпляр type
base: object    суперкласс

object
class: type  метакласс, то есть object это экземпляр type
base: -


То есть type является экземпляром класса type и субклассом object
А object является экземпляром класса type и классом высшего уровня
Любой класс, например str, является субклассом класса object и экземпляром класса type.
"""

#date, time
import pytz, datetime
tz = pytz.timezone('Europe/Moscow')

dat = datetime.datetime.now()
dat_tz = datetime.datetime.now(tz=tz)   #(1)
now = datetime.datetime.utcnow()
now_utc = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)   #То же, что и (1), но быстрее и с другой таймзоной. Это делает timezone.now()


new_york_tz = pytz.timezone("America/New_York")
new_york = new_york_tz.normalize(now_utc.astimezone(new_york_tz))


print(dat)      #2014-11-11 15:12:53.355327
print(dat_tz)   #2014-11-11 15:12:53.355371+03:00
print(now)      #2014-11-11 12:12:53.355435
print(now_utc)  #2014-11-11 12:12:53.355438+00:00 - это рекомендуется писать в ДБ
print(new_york) #2014-11-11 07:12:53.355438-05:00

print(dat - now) #2:59:59.999919  # не учитывает tz, непременимо
print(now_utc - dat_tz) #0:00:00.000059  умно учитывает tz
print(now_utc - new_york) #0:00:00 - то есть это два одинаковых значения, но с разными часовыми поясами

#*************************
#study

def partial(func, *args, **keywords):
    """New function with partial application of the given arguments
    and keywords.
    """
    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*(args + fargs), **newkeywords)
    newfunc.func = func #Не ясно, зачем это. Ничего не меняет.
    newfunc.args = args #Не ясно, зачем это. Ничего не меняет.
    newfunc.keywords = keywords #Не ясно, зачем это. Ничего не меняет.
    return newfunc

WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__qualname__', '__doc__',
                       '__annotations__')

WRAPPER_UPDATES = ('__dict__',)

def update_wrapper(wrapper,
                   wrapped,
                   assigned = WRAPPER_ASSIGNMENTS,
                   updated = WRAPPER_UPDATES):
    """Update a wrapper function to look like the wrapped function

       wrapper is the function to be updated
       wrapped is the original function
       assigned is a tuple naming the attributes assigned directly
       from the wrapped function to the wrapper function (defaults to
       functools.WRAPPER_ASSIGNMENTS)
       updated is a tuple naming the attributes of the wrapper that
       are updated with the corresponding attribute from the wrapped
       function (defaults to functools.WRAPPER_UPDATES)
    """
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
        else:
            setattr(wrapper, attr, value)
    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
    # Issue #17482: set __wrapped__ last so we don't inadvertently copy it
    # from the wrapped function when updating __dict__
    wrapper.__wrapped__ = wrapped
    # Return the wrapper so this can be used as a decorator via partial()
    return wrapper



def wraps(wrapped,
          assigned = WRAPPER_ASSIGNMENTS,
          updated = WRAPPER_UPDATES):
    """Decorator factory to apply update_wrapper() to a wrapper function

       Returns a decorator that invokes update_wrapper() with the decorated
       function as the wrapper argument and the arguments to wraps() as the
       remaining arguments. Default arguments are as for update_wrapper().
       This is a convenience function to simplify applying partial() to
       update_wrapper().
    """
    return partial(update_wrapper, wrapped=wrapped,
                   assigned=assigned, updated=updated)

#fun2 начинает выглядеть как fun1
def fun1():
    print('1')

@wraps(fun1)
def fun2():
    print('2')

print(fun1) #<function fun1 at 0x7f6dbe58cea0>
print(fun2) #function fun1 at 0x7f6dbe5990d0>
fun1() #1
fun2() #2


#************************************
#study доразобрать при следующем проходе.
class Promise(object):
    """
    This is just a base class for the proxy class created in
    the closure of the lazy function. It can be used to recognize
    promises in code.
    """
    pass

def lazy(func, *resultclasses): #На этапе декорирования
    """
    Turns any callable into a lazy evaluated callable. You need to give result
    classes or types -- at least one is needed so that the automatic forcing of
    the lazy evaluation code is triggered. Results are not memoized; the
    function is evaluated on every access.
    """
    #Результирующие классы - это классы, которые готовы лениво получать результат выполнения func
    #Мы сохраним все их методы(ссылки на них) в словаре __dispatch класса __proxy__.

    @total_ordering #Разобрать
    class __proxy__(Promise):
        """
        Encapsulate a function call and act as a proxy for methods that are
        called on the result of that function. The function is not evaluated
        until one of the methods on the result is called.
        """
        __dispatch = None

        def __init__(self, args, kw): #На этапе вызова функции
            #4) Экземпляр класса __proxy__ сохраняет полученные функцией аргументы
            self.__args = args
            self.__kw = kw
            if self.__dispatch is None:
                self.__prepare_class__()
            #5) И если еще не инициирован, вызывает метод _proxy__prepare_class().
            #Что характерно, self.__prepare_class__() - это экземпляр именно класса, а не экземпляра
            #Это работает, поскольку класс для каждого вызова lazy создается заново

            #Первый вызов функции вызывает инициацию класса, то есть сохранение всех методов результирующих классов
            #(ссылок на них) в словаре __dispatch класса __proxy__
            #Каждый последующий вызов функции не вызывает инициацию класса, а создает новый экземпляр __proxy__,
            # хранящий полученный args и kw
            # Результатом вызова функции является экземпляр класса __proxy__, хранящий args и kw
            # Вместо каждого метода класса __proxy__, присутствующего у результирующих классов, мы получаем ссылку на
            #метод __wrapper__, который передает результат выполнения функции в метод класса, сохраненный
            # в словаре __dispatch класса __proxy__  по ссылке

        def __reduce__(self):
            return (
                _lazy_proxy_unpickle,
                (func, self.__args, self.__kw) + resultclasses
            )

        @classmethod
        def __prepare_class__(cls):
            #6) Этот метод готовит класс __proxy__ для дальнейшей работы. Не экземпляр, а именно класс.
            cls.__dispatch = {}
            for resultclass in resultclasses:
                #7) Перебираем результирующие классы. Для теста я задал просто str
                cls.__dispatch[resultclass] = {}
                for type_ in reversed(resultclass.mro()):
                    #8) resultclass.mro() [<class 'str'>, <class 'object'>], то есть получаем каждый суперкласс
                    #для нашего результирующего класса
                    #reversed(resultclass.mro()) <list_reverseiterator object at 0x7fd4894fd4a8>
                    for (k, v) in type_.__dict__.items():
                        # All __promise__ return the same wrapper method, but
                        # they also do setup, inserting the method into the
                        # dispatch dict.
                        #9) Перебираем каждый метод и свойство данного класса или суперкласса, начиная с самого верхнего
                        meth = cls.__promise__(resultclass, k, v)
                        #10) Вызываем метод класса __promise__, передавая туда класс-результат(str), не суперкласс
                        #И имя свойства(k) и его значение(v).
                        if hasattr(cls, k):
                            continue
                        setattr(cls, k, meth)
                        #14) Если данного метода(например find) нет у класса __promise__, то добавляем его.
                        #То есть у класса __promise__ появляется метод find класса str.
            cls._delegate_bytes = bytes in resultclasses
            cls._delegate_text = six.text_type in resultclasses
            #15) Проверяем, есть ли среди результирующих классов bytes и str
            assert not (cls._delegate_bytes and cls._delegate_text), "Cannot call lazy() with both bytes and text return types."
            #16) Если не(оба условия выполняются одновременно), вызвать исключение
            #17) В зависимости от версии питона установить в качестве __str__ или __unicode__ метод __proxy__
            #__text_cast для str и __bytes_cast для bytes
            if cls._delegate_text:
                if six.PY3:
                    cls.__str__ = cls.__text_cast
                else:
                    cls.__unicode__ = cls.__text_cast
            elif cls._delegate_bytes:
                if six.PY3:
                    cls.__bytes__ = cls.__bytes_cast
                else:
                    cls.__str__ = cls.__bytes_cast

        @classmethod
        def __promise__(cls, klass, funcname, method):
            # Builds a wrapper around some magic method and registers that
            # magic method for the given type and method name.
            def __wrapper__(self, *args, **kw): #При вызове каждого метода результирующего класса (str)
                # Automatically triggers the evaluation of a lazy value and
                # applies the given magic method of the result type.
                #18) Результат res -  это результат выполнения исходной функции test с ее аргументами, которые сохранены
                #в экземпляре __promise__. В нашем случае строка 'aaaa'
                res = func(*self.__args, **self.__kw)
                for t in type(res).mro():
                    #19) Перебираем все суперклассы(включая сам класс) класса type('aaaa') = str, начиная с нижнего
                    if t in self.__dispatch:
                        #20) Если для этого суперкласса есть запись в словаре __dispatch(а у нас есть только для str)
                        #Возвражаем результат выполнения метода, записанного в словаре __dispatch, то есть
                        #в нашем случае метода find класса str, ссылка на который записана в словаре __dispatch
                        #cls.__dispatch[str]['find'] = str.find
                        return self.__dispatch[t][funcname](res, *args, **kw)
                raise TypeError("Lazy object returned unexpected type.")

            #11) Если для этого результирующего класса(не суперкласса), в эксперементе - str еще нет
            #__dispatch[klass]
            if klass not in cls.__dispatch:
                cls.__dispatch[klass] = {}
            cls.__dispatch[klass][funcname] = method
            #12) Добавляем __proxy__.__dispatch[str]['find'] = unbound метод find класса str
            #13) Возвращает вместо метода (каждого, но, например, find)  __wrapper__, каждый раз один и тот же,
            # но добавляет данный метод (find) в словарь __dispatch
            #Получается, что поскольку мы идем от самого верхнего суперкласса, последним и итоговым методом будет
            #Самый нижний
            return __wrapper__

        def __text_cast(self):
            return func(*self.__args, **self.__kw)

        def __bytes_cast(self):
            return bytes(func(*self.__args, **self.__kw))

        def __cast(self):
            if self._delegate_bytes:
                return self.__bytes_cast()
            elif self._delegate_text:
                return self.__text_cast()
            else:
                return func(*self.__args, **self.__kw)

        def __ne__(self, other):
            if isinstance(other, Promise):
                other = other.__cast()
            return self.__cast() != other

        def __eq__(self, other):
            if isinstance(other, Promise):
                other = other.__cast()
            return self.__cast() == other

        def __lt__(self, other):
            if isinstance(other, Promise):
                other = other.__cast()
            return self.__cast() < other

        def __hash__(self):
            return hash(self.__cast())

        def __mod__(self, rhs):
            if self._delegate_bytes and six.PY2:
                return bytes(self) % rhs
            elif self._delegate_text:
                return six.text_type(self) % rhs
            return self.__cast() % rhs

        def __deepcopy__(self, memo):
            # Instances of this class are effectively immutable. It's just a
            # collection of functions. So we don't need to do anything
            # complicated for copying.
            memo[id(self)] = self
            return self

    @wraps(func)
    def __wrapper__(*args, **kw):
        # Creates the proxy object, instead of the actual value.
        return __proxy__(args, kw)
        #2)На этапе вызова функции
        # Вместо функции test вызывается функция __wrapper__, которая получает аргументы, полученные функцией
        #3)Эта функция возвращает экземпляр класса __proxy__,

    return __wrapper__
    #1)Вместо фунции test мы получаем эту функцию, замаскированную под test


def _lazy_proxy_unpickle(func, args, kwargs, *resultclasses):
    return lazy(func, *resultclasses)(*args, **kwargs)



class MyStr(str):
    pass


def test(text):
    text += 'aaa'
    return text



lazy_test = lazy(test, str)
a = lazy_test('aaaaa')



test = lazy(test, str)
a = test('a')
print(a.find('a')) #0

class Test:
    def fun(self, var):
        return var

Test.fun = lazy(Test.fun, str)
ob = Test()
prox2 = ob.fun('baaaaa')
print(prox2.find('a')) #1

#******************
#Простой аналог lazy, мой

def lazy(fun):
    class proxy:
        def __init__(self, args, kwargs):
            self.args = args
            self.kwargs = kwargs

        def __getattr__(self, item):
            res = fun(*self.args, **self.kwargs)
            bound_fun = getattr(res, item)
            return bound_fun

    def wrapper(*args, **kwargs):
        return proxy(args, kwargs)

    return wrapper


class MyStr(str):
    pass

def test(val):
    return MyStr(val)


lazytest = lazy(test)

prox1 = lazytest('baaaaaa')

print(prox1.find('a'))

#***************


a1 = 'abc'
a2 = 'abc'
print(a1 == a2) #True
print(a1 is a2) #True

l1 = [1, 2, 3]
l2 = [1, 2, 3]
print(l1 == l2) #True
print(l1 is l2) #False
#***********************
#Ссылки
x = [1, 2]
y = [3, 4, x]
x.append(3)
print(y) #[3, 4, [1, 2, 3]]

z = y.copy() #Поверхностно
print(z) #[3, 4, [1, 2, 3]]
print(z[2] == x) #True
print(z[2] is x) #True

from copy import deepcopy
m = deepcopy(y) #Глубоко
print(m[2] == x) #True
print(m[2] is x) #False

n = y[:]
print(n[2] == x) #True
print(n[2] is x) #True

l1 = [1, 2]
l2 = l1
l1 = l1 + [1] #Новый объект
print(l1) #[1, 2, 1]
print(l2) #[1, 2]


l1 = [1, 2]
l2 = l1
l1 += [1] #Тот же объект
print(l1) #[1, 2, 1]
print(l2) #[1, 2, 1]

l1 = [1, 2]
l2 = l1
l1[1] = 3 #Меняем тот же объект
print(l1) #[1, 3]
print(l2) #[1, 3]

l1 = None #Объект [1 , 3] не изменился, просто l1 перестала на него ссылаться
print(l1) #None
print(l2) #[1, 3]

t1 = 'abc'
t2 = t1 #Обе ссылаются на тот же объект 'abc', но он не изменяемый
t1[0] = 'x' #TypeError: 'str' object does not support item assignment

#**********************************

#**************************************
#Singleton with metaclass
class Singleton(type):

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__call__(*args, **kwargs)
        else:
            cls._instance.__init__(*args, **kwargs)
        return cls._instance

class C(metaclass=Singleton):
    def __init__(self, name):
        self.name = name


ob1 = C('name1')
print(ob1.name)
ob2 = C('name2')

print(ob1, ob2)
print(ob1.name, ob2.name)




#Simple singleton
class Singleton:
    __instance = None

    @staticmethod
    def __new__(cls, *args, **kwargs):
        print(args, kwargs)
        #('name1',) {'x': 3}
        #('name2',) {}
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)  #without args or kwargs
        return cls.__instance

    def __init__(self, name, x=2):
        self.name = name


ob1 = Singleton('name1', x=3)
print(ob1.name)
ob2 = Singleton('name2')

print(ob1, ob2)
print(ob1.name, ob2.name)


#singleton decorator
class singleton:

    def __init__(self, aClass): #on decorate
        self.aClass = aClass
        self.__instance = None

    def __call__(self, *args, **kwargs): #on instance create
        if self.__instance is None:
            self.__instance = self.aClass(*args, **kwargs)
        else:
            #self.aClass.__init__(self.__instance, *args, **kwargs)
            self.__instance.__init__(*args, **kwargs)

        return self.__instance

@singleton
class C:
    def __init__(self, name):
        self.name = name


ob1 = C('name1')
print(ob1.name)
ob2 = C('name2')

print(ob1, ob2)
print(ob1.name, ob2.name)

#************************************
#Sort with key, функтор
#*************
#sort with key example
sort_list = ['aaaaa', 'cc', 'bbb']

def sort_by_length(input_str):
        return len(input_str) # Ключом является длина каждой строки, сортируем по длине

sort_list.sort(key=sort_by_length)
print(sort_list) #['cc', 'bbb', 'aaaaa']


class SortKey:  #Функтор

    def __init__(self, *attribute_names):
        self.attribute_names = attribute_names

    def __call__(self, instance):
        values = []
        for attribute_name in self.attribute_names:
            values.append(getattr(instance, attribute_name))
        return values

def sort_by_length(person):
        return len(person.forename)

class Person:

    def __init__(self, forename, surname, email):
        self.forename = forename
        self.surname = surname
        self.email = email

people = []
p = Person('Petrov', '', '')
people.append(p)
p = Person('Sidorov', '', '')
people.append(p)
p = Person(u'Ivanov', '', '')
people.append(p)
for p in people:
    print(p.forename)
#Petrov
#Sidorov
#Ivanov
people.sort(key=SortKey("forename"))
for p in people:
    print(p.forename)
#Ivanov
#Petrov
#Sidorov

people.sort(key=sort_by_length)
for p in people:
    print(p.forename)
#Ivanov
#Petrov
#Sidorov
#********************
class MySequence:
    def __init__(self, start=0, step=1):
        self.start = start
        self.step = step
        self.changed = {}
    def __getitem__(self, key):
        return self.start + key*self.step
    def __setitem__(self, key, value):
        self.changed[key] = value

s = MySequence(1, 2)
print(s[0])
#1
s[0] = 2
print(s[0])
#1
print(s.changed)
#{0: 2}
print(s[1])
#3
print(s[100])
#201

#*****************
#Многопоточность https://www.ibm.com/developerworks/ru/library/l-python_part_9/
#http://pymotw.com/2/threading/

#subprocess
#parent.py  works with child.py

#В питоне есть стандартный модуль subprocess, который упрощает управление другими программами, передавая им опции
# командной строки и организуя обмен данными через каналы (pipe). Мы рассмотрим пример, в котором пользователь з
# апускает программу из командной строки, которая в свою очередь запустит несколько дочерних программ.
#  В данном примере два скрипта – рarent.py и child.py.
# Запускается parent.py. Child.py выступает в роли аргумента command, который передается в запускаемый процесс.
#  У этого процесса есть стандартный вход, куда мы передаем два аргумента – поисковое слово и имя файла.
# Мы запустим два экземпляра программы child.py,
# каждый экземпляр будет искать слово word в своем файле – это будут файлы исходников самих программ.
# Запись на стандартный вход осуществляет модуль subprocess.
# Каждый процесс пишет результат своего поиска в консоль.
# В главном процессе мы ждем, пока все child не закончат свою работу.

# parent_subprocess.py
import os
import subprocess
import sys

child = os.path.join(os.path.dirname(__file__), "child_subprocess.py")

word = 'word'
file = ['parent_subprocess.py', 'child_subprocess.py']

pipes = []
for i in range(0, 2):
    command = [sys.executable, child]
    #['/home/kulik/virtualenvs/main/main/bin/python3.4', '/home/kulik/Copy/projects/kulik/child.py']
    pipe = subprocess.Popen(command, stdin=subprocess.PIPE)
    pipes.append(pipe)
    pipe.stdin.write(word.encode("utf8") + b"\n") #Передавать через pipe можем только байты
    pipe.stdin.write(file[i].encode("utf8") + b"\n")
    #Передали параметры
    pipe.stdin.close()

while pipes:
    pipe = pipes.pop()
    pipe.wait() #Ждем заавершения подпроцесса, возвращаем код

# child_subprocess.py
import sys
#Считали параметры
word = sys.stdin.readline().rstrip() #Но получакем уже строки
filename = sys.stdin.readline().rstrip()

try:
    with open(filename, "r") as fh:
        while True:
            current = fh.readline()
            if not current:
                break
            if word in current:
                print("find: {0} {1}".format(filename, word))
except:
    pass

#**************************
#http://pymotw.com/2/threading/
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

def daemon():
    logging.debug('Starting')
    time.sleep(2)
    logging.debug('Exiting')

d = threading.Thread(name='daemon', target=daemon)
d.setDaemon(True)

def non_daemon():
    logging.debug('Starting')
    logging.debug('Exiting')

t = threading.Thread(name='non-daemon', target=non_daemon)

d.start()
t.start()

d.join(1) #if == 3, we'll see Exiting
print('d.isAlive()', d.isAlive())
t.join()

#(daemon    ) Starting
#(non-daemon) Starting
#(non-daemon) Exiting
#d.isAlive() True
#*******************************
import random
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

def worker():
    """thread worker function"""
    #t = threading.currentThread()
    #Получаем текущий поток
    pause = random.randint(1, 5)
    logging.debug('sleeping %s', pause)
    time.sleep(pause)
    logging.debug('ending')

for i in range(3):
    t = threading.Thread(target=worker)
    #Объявляем поток, выполняющий функцию worker
    t.setDaemon(True)
    #Объявляем этот поток демоном, то есть другие не дожидаются его завершения
    t.start()

main_thread = threading.current_thread()
#Получаем основной поток

for t in threading.enumerate():
    if t is main_thread:
        #Перечисляем все потоки,основной пропускаем
        continue
    logging.debug('joining %s', t.getName())
    t.join()
    #Говорим, что мы приостанавливаем вызывающий поток и дожидаемся завершения вызывающего потока. Если убрать setDaemon, то и так дождемся.
    #Но только для threading. _thread не дожидается.
#*******************
"""
Для управления потоками существуют методы:
start() – дает потоку жизнь.
run() –этот метод представляет действия, которые должны быть выполнены в потоке.
join([timeout]) – поток, который вызывает этот метод, приостанавливается, ожидая завершения потока, чей метод вызван. Параметр timeout (число с плавающей точкой) позволяет указать время ожидания (в секундах), по истечении которого приостановленный поток продолжает свою работу независимо от завершения потока, чей метод join был вызван. Вызывать join() некоторого потока можно много раз. Поток не может вызвать метод join() самого себя. Также нельзя ожидать завершения еще не запущенного потока.
getName() – возвращает имя потока.
setName(name) – присваивает потоку имя name.
isAlive() – возвращает истину, если поток работает (метод run() уже вызван).
isDaemon() – возвращает истину, если поток имеет признак демона.
setDaemon(daemonic) – устанавливает признак daemonic того, что поток является демоном.
activeCount() – возвращает количество активных в настоящий момент экземпляров класса Thread. Фактически это len(threading.enumerate()).
currentThread() – возвращает текущий объект-поток, т.е. соответствующий потоку управления, который вызвал эту функцию.
enumerate() – возвращает список активных потоков.

"""

#************************
import threading
import time

L = list(range(20))

def worker(L):
    while len(L) > 0:
        print(threading.current_thread().getName())
        print(L.pop())
        time.sleep(1)

def counter(L):
    while len(L) > 0:
        time.sleep(5)
        print('len', len(L))


for k in range(3):
    t = threading.Thread(target=worker, args=(L,))
    #t.setDaemon(True) #Если не сделать join, то основной поток не дожидается его завершения. Бессмысленно.
    t.start()
    #t.join() #Если сделать join здесь, то первый же поток присоединится к основному и мы будем дожидаться его
    # завершения

c = threading.Thread(target=counter, args=(L,), name='counter')
#c.setDaemon(True)
c.start()


main = threading.current_thread()

for t in threading.enumerate():
    if t is main:
        continue
    #t.join() #Не обязательно, так как все равно будем дожидаться завершения всех процессов, а живость главного нам не важна#*********************

#**************************************************
import threading
import time
class ClockThread(threading.Thread):
    def __init__(self, interval):
        threading.Thread.__init__(self)
        self.daemon = True
        self.interval = interval
    def run(self):
        while True:
            print("The time is %s" % time.ctime())
            time.sleep(self.interval)

t = ClockThread(5)
t.start()
t.join() #На самом деле демонизировать и join излишне...

#The time is Sat Jan  3 14:58:00 2015
#The time is Sat Jan  3 14:58:05 2015
#The time is Sat Jan  3 14:58:10 2015
#...
#**********************************************

#*************************
"""
Timer Threads
One example of a reason to subclass Thread is provided by Timer, also included in threading. A Timer starts its work
after a delay, and can be canceled at any point within that delay time period.
Notice that the second timer is never run, and the first timer appears to run after the rest of the main program
is done. Since it is not a daemon thread, it is joined implicitly when the main thread is done.
"""

import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

def delayed():
    logging.debug('worker running')
    return

t1 = threading.Timer(3, delayed)
t1.setName('t1')
t2 = threading.Timer(3, delayed)
t2.setName('t2')

logging.debug('starting timers')
t1.start()
t2.start()

logging.debug('waiting before canceling %s', t2.getName())
time.sleep(2)
logging.debug('canceling %s', t2.getName())
t2.cancel()
logging.debug('done')
#*********************************

"""
Signaling Between Threads
Although the point of using multiple threads is to spin separate operations off to run concurrently,
there are times when it is important to be able to synchronize the operations in two or more threads.
A simple way to communicate between threads is using Event objects. An Event manages an internal flag that callers
can either set() or clear(). Other threads can wait() for the flag to be set(), effectively blocking progress until
allowed to continue.

The wait() method takes an argument representing the number of seconds to wait for the event before timing out.
 It returns a boolean indicating whether or not the event is set, so the caller knows why wait() returned.
The isSet() method can be used separately on the event without fear of blocking.

"""

import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

def wait_for_event(e):
    """Wait for the event to be set before doing anything"""
    logging.debug('wait_for_event starting')
    event_is_set = e.wait()
    logging.debug('event set: %s', event_is_set)

def wait_for_event_timeout(e, t):
    """Wait t seconds and then timeout"""
    while not e.isSet():
        logging.debug('wait_for_event_timeout starting')
        event_is_set = e.wait(t)
        logging.debug('event set: %s', event_is_set)
        if event_is_set:
            logging.debug('processing event')
        else:
            logging.debug('doing other work')


e = threading.Event()
t1 = threading.Thread(name='block',
                      target=wait_for_event,
                      args=(e,))
t1.start()

t2 = threading.Thread(name='non-block',
                      target=wait_for_event_timeout,
                      args=(e, 2))
t2.start()

logging.debug('Waiting before calling Event.set()')
time.sleep(3)
e.set()
logging.debug('Event is set')

"""
(block     ) wait_for_event starting
(non-block ) wait_for_event_timeout starting
(MainThread) Waiting before calling Event.set()
(non-block ) event set: False
(non-block ) doing other work
(non-block ) wait_for_event_timeout starting
(MainThread) Event is set
(block     ) event set: True
(non-block ) event set: True
(non-block ) processing event
"""
#*******************************
"""
Controlling Access to Resources
In addition to synchronizing the operations of threads, it is also important to be able to control access to
shared resources to prevent corruption or missed data. Python’s built-in data structures (lists, dictionaries, etc.)
are thread-safe as a side-effect of having atomic byte-codes for manipulating them (the GIL is not released in the
middle of an update). Other data structures implemented in Python, or simpler types like integers and floats,
don’t have that protection.
To guard against simultaneous access to an object, use a Lock object.
In this example, the worker() function increments a Counter instance, which manages a Lock to prevent two
 threads from changing its internal state at the same time.
If the Lock was not used, there is a possibility of missing a change to the value attribute.

"""
import logging
import random
import threading
import time

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

class Counter:
    def __init__(self, start=0):
        self.lock = threading.Lock()
        #create a new lock object
        self.value = start
    def increment(self):
        logging.debug('Waiting for lock')
        self.lock.acquire()
        #lock object
        try:
            logging.debug('Acquired lock')
            self.value = self.value + 1
        finally:
            self.lock.release()
            #unlock object

def worker(c):
    for i in range(2):
        pause = random.random()
        logging.debug('Sleeping %0.02f', pause)
        time.sleep(pause)
        c.increment()
    logging.debug('Done')

counter = Counter()
for i in range(2):
    t = threading.Thread(target=worker, args=(counter,))
    t.start()

logging.debug('Waiting for worker threads')
main_thread = threading.currentThread()
for t in threading.enumerate():
    if t is not main_thread:
        t.join()
logging.debug('Counter: %d', counter.value)

"""
(Thread-1  ) Sleeping 0.39
(Thread-2  ) Sleeping 0.61
(MainThread) Waiting for worker threads
(Thread-1  ) Waiting for lock
(Thread-1  ) Acquired lock
(Thread-1  ) Sleeping 0.48
(Thread-2  ) Waiting for lock
(Thread-2  ) Acquired lock
(Thread-2  ) Sleeping 0.03
(Thread-2  ) Waiting for lock
(Thread-2  ) Acquired lock
(Thread-2  ) Done
(Thread-1  ) Waiting for lock
(Thread-1  ) Acquired lock
(Thread-1  ) Done
(MainThread) Counter: 4
"""
#*****************************************
"""
To find out whether another thread has acquired the lock without holding up the current thread,
pass False for the blocking argument to acquire(). In the next example, worker() tries to acquire the lock
three separate times, and counts how many attempts it has to make to do so. In the mean time, lock_holder()
cycles between holding and releasing the lock, with short pauses in each state used to simulate load.
"""
import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

def lock_holder(lock):
    logging.debug('Starting')
    while True:
        lock.acquire()
        try:
            logging.debug('Holding')
            time.sleep(0.5)
        finally:
            logging.debug('Not holding')
            lock.release()
        time.sleep(0.5)
    return

def worker(lock):
    logging.debug('Starting')
    num_tries = 0
    num_acquires = 0
    while num_acquires < 3:
        time.sleep(0.5)
        logging.debug('Trying to acquire')
        have_it = lock.acquire(0)
        try:
            num_tries += 1
            if have_it:
                logging.debug('Iteration %d: Acquired',  num_tries)
                num_acquires += 1
            else:
                logging.debug('Iteration %d: Not acquired', num_tries)
        finally:
            if have_it:
                lock.release()
    logging.debug('Done after %d iterations', num_tries)


lock = threading.Lock()

holder = threading.Thread(target=lock_holder, args=(lock,), name='LockHolder')
holder.setDaemon(True)
holder.start()

worker = threading.Thread(target=worker, args=(lock,), name='Worker')
worker.start()
#****************************
"""
Normal Lock objects cannot be acquired more than once, even by the same thread.
This can introduce undesirable side-effects if a lock is accessed by more than one function in the same call chain.
In this case, since both functions are using the same global lock, and one calls the other, the second acquisition
fails and would have blocked using the default arguments to acquire().
In a situation where separate code from the same thread needs to “re-acquire” the lock, use an RLock instead.
"""
import threading

lock = threading.Lock()

print('First try :', lock.acquire())
print('Second try:', lock.acquire(0)) #Тут без 0 зависнет, тк будет дожидаться освобождения замка


lock = threading.RLock()

print('First try :', lock.acquire())
print('Second try:', lock.acquire(0))

#First try : True
#Second try: False
#First try : True
#Second try: True

# #*********************

import threading
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

def worker_with(lock):
    with lock:
        logging.debug('Lock acquired via with')

def worker_no_with(lock):
    lock.acquire()
    try:
        logging.debug('Lock acquired directly')
    finally:
        lock.release()

lock = threading.Lock()
w = threading.Thread(target=worker_with, args=(lock,))
nw = threading.Thread(target=worker_no_with, args=(lock,))

w.start()
nw.start()
#******************************
"""
Synchronizing Threads
In addition to using Events, another way of synchronizing threads is through using a Condition object.
Because the Condition uses a Lock, it can be tied to a shared resource. This allows threads to wait for the
    resource to be updated. In this example, the consumer() threads wait() for the Condition to be set before
    continuing. The producer() thread is responsible for setting the condition and notifying the other threads that
    they can continue.
"""
import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )

def consumer(cond):
    """wait for the condition and use the resource"""
    logging.debug('Starting consumer thread')
    t = threading.currentThread()
    with cond:
        cond.wait()
        logging.debug('Resource is available to consumer')

def producer(cond):
    """set up the resource to be used by the consumer"""
    logging.debug('Starting producer thread')
    with cond:
        logging.debug('Making resource available')
        cond.notifyAll()

condition = threading.Condition()
c1 = threading.Thread(name='c1', target=consumer, args=(condition,))
c2 = threading.Thread(name='c2', target=consumer, args=(condition,))
p = threading.Thread(name='p', target=producer, args=(condition,))

c1.start()
time.sleep(2)
c2.start()
time.sleep(2)
p.start()
#*******************************
"""
Limiting Concurrent Access to Resources¶

Sometimes it is useful to allow more than one worker access to a resource at a time, while
    still limiting the overall number. For example, a connection pool might support a fixed number of
    simultaneous connections, or a network application might support a fixed number of concurrent downloads.
    A Semaphore is one way to manage those connections.

 In this example, the ActivePool class simply serves as a convenient way to track which threads are able to run at
 a given moment. A real resource pool would allocate a connection or some other value to the newly active thread,
 and reclaim the value when the thread is done.
  Here it is just used to hold the names of the active threads to show that only five are running concurrently.
"""
import logging
import random
import threading
import time

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )

class ActivePool(object):
    def __init__(self):
        super(ActivePool, self).__init__()
        self.active = []
        self.lock = threading.Lock()
    def makeActive(self, name):
        with self.lock:
            self.active.append(name)
            logging.debug('Running: %s', self.active)
    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)
            logging.debug('Running: %s', self.active)

def worker(s, pool):
    logging.debug('Waiting to join the pool')
    with s:
        name = threading.currentThread().getName()
        pool.makeActive(name)
        time.sleep(0.1)
        pool.makeInactive(name)

pool = ActivePool()
s = threading.Semaphore(2)
for i in range(4):
    t = threading.Thread(target=worker, name=str(i), args=(s, pool))
    t.start()
#***********************************************
"""
Thread-specific Data

While some resources need to be locked so multiple threads can use them,
 others need to be protected so that they are hidden from view in threads that do not “own” them.
 The local() function creates an object capable of hiding values from view in separate threads.
"""
import random
import threading
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

def show_value(data):
    try:
        val = data.value
    except AttributeError:
        logging.debug('No value yet')
    else:
        logging.debug('value=%s', val)


def worker(data):
    show_value(data)
    data.value = random.randint(1, 100)
    show_value(data)

local_data = threading.local()
show_value(local_data)
local_data.value = 1000
show_value(local_data)

for i in range(2):
    t = threading.Thread(target=worker, args=(local_data,))
    t.start()
#***************************************
"""
To initialize the settings so all threads start with the same value, use a
subclass and set the attributes in __init__().
"""
import random
import threading
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )


def show_value(data):
    try:
        val = data.value
    except AttributeError:
        logging.debug('No value yet')
    else:
        logging.debug('value=%s', val)

def worker(data):
    show_value(data)
    data.value = random.randint(1, 100)
    show_value(data)

class MyLocal(threading.local):
    def __init__(self, value):
        logging.debug('Initializing %r', self)
        self.value = value

local_data = MyLocal(1000)
show_value(local_data)

for i in range(2):
    t = threading.Thread(target=worker, args=(local_data,))
    t.start()

#То есть каждый thread получает свой экземпляр, который там инициализируется
#(MainThread) Initializing <__main__.MyLocal object at 0x7f40566ab588>
#(MainThread) value=1000
#(Thread-1  ) Initializing <__main__.MyLocal object at 0x7f40566ab588>
#(Thread-1  ) value=1000
#(Thread-1  ) value=65
#(Thread-2  ) Initializing <__main__.MyLocal object at 0x7f40566ab588>
#(Thread-2  ) value=1000
#(Thread-2  ) value=85



#***************************
#Thread-local data is data whose values are thread specific.
# To manage thread-local data, just create an instance of local (or a subclass) and store attributes on it:
import threading
import time

local = threading.local()

local.x = 'main'


def worker(val):
    local.x = val
    time.sleep(1)
    print(local.x)

m = threading.current_thread()

for i in range(2):
    t = threading.Thread(target=worker, args=(i,))
    t.setDaemon(True)
    t.start()

for t in threading.enumerate():
    if t is m:
        continue
    t.join()

print(local.x)

#0
#1
#main

#******************************
names = ['name', 'age', 'pay', 'job']
values = ['Sue Jones', 45, 40000, 'hdw']
print(list(zip(names, values)))
#[('name', 'Sue Jones'), ('age', 45), ('pay', 40000), ('job', 'hdw')]
sue = dict(zip(names, values))
print(sue)
#{'job': 'hdw', 'pay': 40000, 'age': 45, 'name': 'Sue Jones'}
#*****************************************

bob = dict(name='Bob Smith', age=42, pay=30000, job='dev')


bob = {'pay': 30000, 'job': 'dev', 'age': 42, 'name': 'Bob Smith'}
sue = {'job': 'hdw', 'pay': 40000, 'age': 45, 'name': 'Sue Jones'}

people = [bob, sue]

names = [person['name'] for person in people]
print(names) #['Bob Smith', 'Sue Jones']

salary = sum([person['pay'] for person in people])
print(salary)  #70000

names = [(lambda p: p['name'])(person) for person in people]
print(names)  #['Bob Smith', 'Sue Jones']

names_map = map(lambda p: p['name'], people)
print(names_map) #<map object at 0x7f8f8caa3a20>
print(list(names_map))  #['Bob Smith', 'Sue Jones']


print([rec['name'] for rec in people if rec['age'] >= 45])
#['Sue Jones']
# SQL-подобный
# запрос
print([(rec['age'] ** 2 if rec['age'] >= 45 else rec['age']) for rec in people])
#[42, 2025]


G = (rec['name'] for rec in people if rec['age'] >= 45)
print(next(G))
#'Sue Jones'
G = ((rec['age'] ** 2 if rec['age'] >= 45 else rec['age'])
for rec in people)
print(G.__next__())
#42

#*******************************************
import sys

def read_stdin(ob, f):
    sys.stdin = ob
    line = input()
    while line is not None:
        f(line)
        try:
            line = input()
        except:
            line = None

with open(__file__) as file:
    read_stdin(file, lambda ob: print(ob))

#****************************
import pickle, glob
for filename in glob.glob('*.pkl'):         # for 'bob','sue','tom'
    recfile = open(filename, 'rb')
    record  = pickle.load(recfile)
    print(filename, '=>\n  ', record)

suefile = open('sue.pkl', 'rb')
print(pickle.load(suefile)['name'])         # fetch sue's name

#*******************************************
from urllib.request import urlopen
conn = urlopen('http://anekdot.ru')
reply = conn.read()
print(reply)

#************************************
D = {'say': 5, 'get': 'shrubbery'}
S = '%(say)s => %(get)s' % D
print(S)

#******************************
rowhtml  = '<tr><th>%s<td><input type=text name=%s value="%%(%s)s">\n'
rowshtml = ''
for fieldname in ('A', 'B', 'C', 'D'):
    rowshtml += (rowhtml % ((fieldname,) * 3))

print(rowshtml)
#<tr><th>A<td><input type=text name=A value="%(A)s">
#<tr><th>B<td><input type=text name=B value="%(B)s">
#<tr><th>C<td><input type=text name=C value="%(C)s">
#<tr><th>D<td><input type=text name=D value="%(D)s">

rowshtml = rowshtml % {'A': 1, 'B': 2, 'C': 3, 'D': 4}
print(rowshtml)
#<tr><th>A<td><input type=text name=A value="1">
#<tr><th>B<td><input type=text name=B value="2">
#<tr><th>C<td><input type=text name=C value="3">
#<tr><th>D<td><input type=text name=D value="4">

#*******************
from person import Person
bob = Person('Bob', 35)
print('%(name)s, %(age)s' % bob.__dict__ )# выражение: ключи __dict__)
#'Bob, 35'
print('{0.name} => {0.age}'.format(bob)) # метод: синтаксис атрибутов
#'Bob => 35'


#******************
import sys
dir(sys)
sys.__doc__
print(sys.__doc__)
help(sys)


#*************************************
"""
split and interactively page a string or file of text
"""

def more(text, numlines=15):
    lines = text.splitlines()                # like split('\n') but no '' at end
    while lines:
        chunk = lines[:numlines]
        lines = lines[numlines:]
        for line in chunk: print(line)
        if lines and input('More?') not in ['y', 'Y']: break

if __name__ == '__main__':
    import sys                               # when run, not imported
    more(open(sys.argv[1]).read(), 10)       # page contents of file on cmdline

#*******************
#>>> mystr = ‘xxaaxxaa’
#>>> ‘SPAM’.join(mystr.split(‘aa’)) # усложненная версия str.replace!
#‘xxSPAMxxSPAM’

#*******************
#open(‘file’).read()  #Весь файл в строку
#open(‘file’).read(N) #Следующие n байт в строку
#open(‘file’).readlines() #Весь файл в массив строк
#open(‘file’).readline() #След строку до символа \n


#*****************************
#>>> os.path.split(r’C:\temp\data.txt’)
#(‘C:\\temp’, ‘data.txt’)
#>>> os.path.join(r’C:\temp’, ‘output.txt’)
#‘C:\\temp\\output.txt’
#>>> name = r’C:\temp\data.txt’
# пути в Windows
#>>> os.path.dirname(name), os.path.basename(name)
#(‘C:\\temp’, ‘data.txt’)
#>>> name = ‘/home/lutz/temp/data.txt’
## пути в стиле Unix
#>>> os.path.dirname(name), os.path.basename(name)
#(‘/home/lutz/temp’, ‘data.txt’)
#>>> os.path.splitext(r’C:\PP4thEd\Examples\PP4E\PyDemos.pyw’)
#(‘C:\\PP4thEd\\Examples\\PP4E\\PyDemos’, ‘.pyw’)


#************************************
import os
os.system('ls') # Сразу выведет список каталогов
print(os.path.exists(r'try2.py')) #True


text = os.popen(r'cat try2.py').readlines() #Как массив строк
for line in text:
    print(line)

text = open('try2.py').readlines()
for line in text:
    print(line)


res = os.popen('python3 try.py').read() #Целиком
print(res)

import subprocess
#Аналог os.system. shell=True означает использовать для запуска оболочку. Можно также указать какую
subprocess.call(r'cat try2.py', shell=True)

#Примерный аналог os.popen. shell=True означает использовать для запуска оболочку. Можно также указать какую
import subprocess
pipe = subprocess.Popen(r'cat try2.py', stdout=subprocess.PIPE, shell=True)
res = pipe.communicate()
print(isinstance(res, tuple)) #True
print(res)
#(b"import subprocess\npipe = subprocess.Popen(r'cat try2.py', stdout=subprocess.PIPE, shell=True)\nres =
#  pipe.communicate()\nprint(isinstance(res, tuple)) #True\nprint(res)\ncode = pipe.returncode\nprint(code)", None)
code = pipe.returncode
print(code) #0


import subprocess
pipe = subprocess.Popen(r'cat try2.py', stdout=subprocess.PIPE, shell=True)
pipe.wait()
res = pipe.stdout.read()
print(res)
#b'import subprocess\npipe = subprocess.Popen(r\'cat try2.py\', stdout=subprocess.PIPE, shell=True)\npipe.wa
# it()\nres = pipe.stdout.read()\nprint(res)\n#(b"import subprocess\\npipe = subprocess.Popen(r\'cat try2.py\',
# stdout=subprocess.PIPE, shell=True)\\nres =\n#  pipe.communicate()\\nprint(isinstance(res, tuple)) #True\\nprint(res)\\nc
# ode = pipe.returncode\\nprint(code)", None)\ncode = pipe.returncode\nprint(code) #0'
code = pipe.returncode
print(code) #0


pipe = subprocess.Popen(r'python3 try.py', stdout=subprocess.PIPE, shell=True)
pipe.stdout.read()
#b’The Meaning of Life\r\n’
pipe.wait()
# 0

#Прямая замена os.open
from subprocess import Popen, PIPE
Popen('python3 try.py', stdout=PIPE).communicate()[0]
#b’The Meaning of Life\r\n’

import os
os.popen('python3 try.py').read()
#‘The Meaning of Life\n’

#**************************
import sys
print('hello stdout world')
#hello stdout world
sys.stdout.write('hello stdout world' + '\n')
#hello stdout world
#19
print(input('hello stdin world>'))
#hello stdin world>spam
#'spam'
print('hello stdin world>')
print(sys.stdin.readline()) #Читаем одну линию из потока, не все. Иначе это будет бесконечный ввод.
#hello stdin world>
#eggs
#'eggs'


#*******************
"read numbers till eof and show squares"

def interact():
    print('Hello stream world')                     # print sends to sys.stdout
    while True:
        try:
            reply = input('Enter a number>')        # input reads sys.stdin
        except EOFError:
            break                                   # raises an except on eof
        else:                                       # input given as a string
            num = int(reply)
            print("%d squared is %d" % (num, num ** 2))
    print('Bye')

if __name__ == '__main__':
    interact()                                      # when run, not imported

    #C:\...\PP4E\System\Streams> python teststreams.py < input.txt > output.txt
    #Получит в качестве input данные  input.txt, выведет в output.txt

#*************************************
#Вывод одного сценария Python всегда можно отправить на ввод другого:
#C:\...\PP4E\System\Streams> type writer.py
#print(“Help! Help! I’m being repressed!”)
#print(42)
#C:\...\PP4E\System\Streams> type reader.py
#print(‘Got this: “%s”’ % input())
#import sys
#data = sys.stdin.readline()[:-1]
#print(‘The meaning of life is’, data, int(data) * 2)
#C:\...\PP4E\System\Streams> python writer.py
#Help! Help! I’m being repressed!
#42
#C:\...\PP4E\System\Streams> python writer.py | python reader.py
#Got this: “Help! Help! I’m being repressed!”
#The meaning of life is 42 84

#*****************
import sys                                  # or sorted(sys.stdin)
lines = sys.stdin.readlines()               # sort stdin input lines,
#lines = list(sys.stdin)
#Ждем бесконечно окончания ввода. Работает при вводе файла python3 sorter.py < data.txt
lines.sort()                                # send result to stdout
for line in lines: print(line, end='')      # for further processing
#************************
import sys
sum = 0
while True:
    try:
        line = input() #Тут читаем линии построчно. Тоже сработает для открытия файла.
        print(line)
    except EOFError:
        break
    else:
        sum += int(line)
print(sum)
#**********************
import sys
sum = 0
while True:
    line = sys.stdin.readline()
    if not line: break
    sum += int(line)
print(sum)
#**************
import sys
sum = 0
for line in sys.stdin: sum += int(line)
print(sum)
#****************
import sys
print(sum(int(line) for line in sys.stdin))
#****************
import sys
for line in sorted(sys.stdin): print(line, end='')

#*************************
"""
file-like objects that save standard output text in a string and provide
standard input text from a string; redirect runs a passed-in function
with its output and input streams reset to these file-like class objects;
"""

import sys                                      # get built-in modules

class Output:                                   # simulated output file
    def __init__(self):
        self.text = ''                          # empty string when created
    def write(self, string):                    # add a string of bytes
        self.text += string
    def writelines(self, lines):                # add each line in a list
        for line in lines: self.write(line)

class Input:                                    # simulated input file
    def __init__(self, input=''):               # default argument
        self.text = input                       # save string when created
    def read(self, size=None):                  # optional argument
        if size == None:                        # read N bytes, or all
            res, self.text = self.text, ''
        else:
            res, self.text = self.text[:size], self.text[size:]
        return res
    def readline(self):
        eoln = self.text.find('\n')             # find offset of next eoln
        if eoln == -1:                          # slice off through eoln
            res, self.text = self.text, ''
        else:
            res, self.text = self.text[:eoln+1], self.text[eoln+1:]
        return res

def redirect(function, pargs, kargs, input):    # redirect stdin/out
    savestreams = sys.stdin, sys.stdout         # run a function object
    sys.stdin   = Input(input)                  # return stdout text
    sys.stdout  = Output()
    try:
        result = function(*pargs, **kargs)      # run function with args
        output = sys.stdout.text
    finally:
        sys.stdin, sys.stdout = savestreams     # restore if exc or not
    return (result, output)                     # return result if no exc

#***************
#>>> from io import StringIO
#>>> buff = StringIO()
#>>> print(42, file=buff)
#>>> print(‘spam’, file=buff)
#>>> print(buff.getvalue())
#42
#spam

#************************
#reader.py
#print('Got this: "%s"' % input())
#import sys
#data = sys.stdin.readline()[:-1]
#print('The meaning of life is', data, int(data) * 2)

#writer.py
#print("Help! Help! I'm being repressed!")
#print(42)

"""
import os
p1 = os.popen('python3 writer.py', 'r')
p2 = os.popen('python3 reader.py', 'w')
p2.write( p1.read() )
#36
X = p2.close()
#Got this: “Help! Help! I'm being repressed!”
#The meaning of life is 42 84
print(X)
#None
"""


from subprocess import Popen, PIPE
p1 = Popen('python3 writer.py', stdout=PIPE, shell=True)
p2 = Popen('python3 reader.py', stdin=p1.stdout, stdout=PIPE, shell=True)
output = p2.communicate()[0]
print(output)
#b'Got this: “Help! Help! I\'m being repressed!”\r\nThe meaning of life is 42 84\r\n'
print(p2.returncode)
#0
#*******************

"""
>>> file.seek(0)
# перейти в начало файла
>>> file.read()
# прочитать в строку файл целиком
‘Hello file world!\nBye file world.\n’
>>> file.seek(0)
>>> file.readlines()
[‘Hello file world!\n’, ‘Bye
>>> file.seek(0)
>>> file.readline()
‘Hello file world!\n’
>>> file.readline()
‘Bye file world.\n’
>>> file.readline()
‘’
>>> file.seek(0)
# прочитать N (или оставшиеся) символы/байты
>>> file.read(1), file.read(8) # конец файла – возвращается пустая строка
(‘H’, ‘ello fil’)
"""

#***************************************
#Файл имеет свой итератор
"""
>>> file = open(‘data.txt’)
>>> for line in file:
...
print(line, end=’’)
...
Hello file world!
Bye file world.

>>> for line in open(‘data.txt’): # еще короче: временный объект файла
...
print(line, end=’’)
# будет закрыт при утилизации автоматически
...
Hello file world!
Bye file world.
"""

"""

Имеется также возможность запретить преобразование символов кон-
ца строки в текстовом режиме с помощью дополнительных аргументов
функции open, которые мы не будем рассматривать здесь. Подробности
ищите в  описании аргумента newline в  справочной документации по
функции open, но, в двух словах: если в этом аргументе передать пустую
строку, это предотвратит преобразование символов конца строки и со-
хранит остальные особенности поведения текстового режима


>>> open(‘data.txt’).readlines()
[‘Hello file world!\n’, ‘Bye file world.\n’] # всегда читает строки
>>> list(open(‘data.txt’))
[‘Hello file world!\n’, ‘Bye # выполняет обход строк
file world.\n’]
>>> lines = [line.rstrip() for line in open(‘data.txt’)] # генераторы

>>> lines
[‘Hello file world!’, ‘Bye
file world.’]
>>> lines = [line.upper() for line in open(‘data.txt’)] # произв. действия
>>> lines
[‘HELLO FILE WORLD!\n’, ‘BYE FILE WORLD.\n’]
>>> list(map(str.split, open(‘data.txt’)))
# применение функции
[[‘Hello’, ‘file’, ‘world!’], [‘Bye’, ‘file’, ‘world.’]]
>>> line = ‘Hello file world!\n’
>>> line in open(‘data.txt’)
True
# проверка на вхождение
"""
#*******************************************
"""
>>> data = ‘sp\xe4m’
>>> data
‘sp ä m’
>>> 0xe4, bin(0xe4), chr(0xe4)
(228, ‘0b11100100’, ‘ ä ’)

>>> data.encode(‘latin1’)
b’sp\xe4m’ # 8-битовые символы: ascii + дополнительные
>>> data.encode(‘utf8’)
b’sp\xc3\xa4m’ # 2 байта отводится только
# для специальных символов
>>> data.encode(‘ascii’)
# кодирование в ascii невозможно
UnicodeEncodeError: ‘ascii’ codec can’t encode character ‘\xe4’ in position 2:
ordinal not in range(128)

>>> data.encode(‘utf16’)
# по 2 байта на символ плюс преамбула
b’\xff\xfes\x00p\x00\xe4\x00m\x00’
>>> data.encode(‘cp500’)
b’\xa2\x97C\x94’
# кодировка ebcdic: двоичное представление
# строки существенно отличается
>>> open(‘data.txt’, ‘w’, encoding=’latin1’).write(data)
4
>>> open(‘data.txt’, ‘r’, encoding=’latin1’).read()
‘sp ä m’
>>> open(‘data.txt’, ‘rb’).read()
b’sp\xe4m’

>>> open(‘data.txt’, ‘w’, encoding=’utf8’).write(data) # кодировка utf8
4
>>> open(‘data.txt’, ‘r’, encoding=’utf8’).read() # декодирование: отменяет
# кодирование
‘sp ä m’
>>> open(‘data.txt’, ‘rb’).read()
# преобразование
b’sp\xc3\xa4m’

>>> open(‘data.txt’, ‘w’, encoding=’ascii’).write(data)
UnicodeEncodeError: ‘ascii’ codec can’t encode character ‘\xe4’ in position 2:
ordinal not in range(128)
(UnicodeEncodeError: кодек ‘ascii’ не может преобразовать символ ‘\xe4’
в позиции 2: число выходит за пределы range(128) )
>>> open(r’C:\Python31\python.exe’, ‘r’).read()
UnicodeDecodeError: ‘charmap’ codec can’t decode byte 0x90 in position 2:
character maps to <undefined>
(UnicodeDecodeError: кодек ‘charmap’ не может преобразовать байт 0x90
в позиции 2: символ отображается в символ <undefined>

>>> open(‘data.txt’, ‘w’, encoding=’cp500’).writelines([‘spam\n’, ‘ham\n’])
>>> open(‘data.txt’, ‘r’, encoding=’cp500’).readlines()
[‘spam\n’, ‘ham\n’]
>>> open(‘data.txt’, ‘r’).readlines()
UnicodeDecodeError: ‘charmap’ codec can’t decode byte 0x81 in position 2:
character maps to <undefined>
(UnicodeDecodeError: кодек ‘charmap’ не может преобразовать байт 0x81 в позиции
2: символ отображается в символ <undefined> )
>>> open(‘data.txt’, ‘rb’).readlines()
[b’\xa2\x97\x81\x94\r%\x88\x81\x94\r%’]
>>> open(‘data.txt’, ‘rb’).read()
b’\xa2\x97\x81\x94\r%\x88\x81\x94\r%’
"""


"""
Ниже демонстрируется действие механизма преобразования символов
конца строки в Python 3.1 в Windows – объект файла, открытого в тек-
стовом режиме, выполняет преобразование символов конца строки
и обеспечивает переносимость наших сценариев:
>>> open(‘temp.txt’, ‘w’).write(‘shrubbery\n’) # запись в текстовом режиме:
10
# \n -> \r\n
>>> open(‘temp.txt’, ‘rb’).read()
# чтение двоичных данных:
b’shrubbery\r\n’
# фактические байты из файла
>>> open(‘temp.txt’, ‘r’).read()
# проверка чтением: \r\n -> \n
‘shrubbery\n’

#Двоичный режим записывает как есть
>>> data = b’a\0b\rc\r\nd’
>>> len(data)
8
>>> open(‘temp.bin’, ‘wb’).write(data)
8
>>> open(‘temp.bin’, ‘rb’).read()
b’a\x00b\rc\r\nd’
# 4 байта, 4 обычных символа
# запись двоичных данных как есть
# чтение двоичных данных:
# без преобразования

"""

"""
from io import BytesIO, StringIO

data_str = 'sp\xe4m'
data_bytes = data_str.encode(encoding='utf-8') #Кодировку можно не указывать
print(data_str) #späm
print(data_bytes) #b'sp\xc3\xa4m'
print(data_bytes.decode(encoding='utf-8')) #späm, Кодировку можно не указывать

io_bytes = BytesIO(data_bytes)
io_str = StringIO(data_str)

print(io_bytes.read()) #b'sp\xc3\xa4m'
print(io_str.read()) #späm

"""

#raw string. Escape спецсимволы
from io import BytesIO

st = 'abcd\ndefg'
print(st)
#abcd
#defg
b_file = BytesIO(st.encode())
print(b_file.read())
#b'abcd\ndefg'

raw_st = r'abcd\ndefg'
print(raw_st)
#abcd\ndefg
b_file = BytesIO(raw_st.encode())
raw_str_as_bytes = b_file.read()
print(raw_str_as_bytes) #$b'abcd\\ndefg'
print(raw_str_as_bytes.decode()) #abcd\ndefg

#************************************
"""
Допустимо только для байтов, поскольку символы юникода могут занимать несколько байтов
Для демонстрации создадим файл в  режиме “w+b” (эквивалент режи-
ма “wb+”) и запишем в него некоторые данные – этот режим позволяет
читать из файла и писать в него и создает новый пустой файл, если он
существовал прежде (это относится ко всем режимам “w”).
>>> records = [bytes([char] * 8) for char in b’spam’]
>>> records
[b’ssssssss’, b’pppppppp’, b’aaaaaaaa’, b’mmmmmmmm’]
>>> file = open(‘random.bin’, ‘w+b’)
>>> for rec in records:
...
size = file.write(rec)
...
>>> file.flush()
>>> pos = file.seek(0)
>>> print(file.read())
b’ssssssssppppppppaaaaaaaammmmmmmm’
# запиcать четыре записи
# bytes означает двоичный режим
# прочитать файл целиком

Теперь повторно откроем файл в режиме “r+b” – он также позволяет чи-
тать из файла и писать в него, но не очищает файл при открытии.
c:\temp> python
>>> file = open(‘random.bin’, ‘r+b’)
>>> print(file.read())
b’ssssssssppppppppaaaaaaaammmmmmmm’
>>>
>>>
>>>
>>>
>>>
record = b’X’ * 8
file.seek(0)
file.write(record)
file.seek(len(record) * 2)
file.write(b’Y’ * 8)
>>> file.seek(8)
>>> file.read(len(record))
b’pppppppp’
>>> file.read(len(record))
b’YYYYYYYY’
# прочитать файл целиком
# изменить первую запись
# изменить третью запись
# извлечь вторую запись
# извлечь следующую (третью) запись
>>> file.seek(0)
>>> file.read()
b’XXXXXXXXppppppppYYYYYYYYmmmmmmmm’ # прочитать файл целиком
c:\temp> type random.bin
XXXXXXXXppppppppYYYYYYYYmmmmmmmm # посмотреть файл за пределами Python

"""
#********************************
from io import StringIO
import sys

file = StringIO()
existing = sys.stdout
sys.stdout = file
sys.stdout.write('abc')
print('def')
sys.stdout = existing
file.seek(0)
print(file.read())
#abcdef
"""
>>> from io import StringIO
>>> buff = StringIO()
>>> print(42, file=buff)
>>> print(‘spam’, file=buff)
>>> print(buff.getvalue())
42
spam
>>> from redirect import Output
>>> buff = Output()
>>> print(43, file=buff)
>>> print(‘eggs’, file=buff)
>>> print(buff.text)
43
eggs
"""
#********************************
"""
>>> import sys
>>> for stream in (sys.stdin, sys.stdout, sys.stderr):
...
print(stream.fileno())
...
0
1
2
>>> sys.stdout.write(‘Hello stdio world\n’)
Hello stdio world
18
>>> import os
>>> os.write(1, b’Hello descriptor world\n’)
Hello descriptor world
23
# записать с помощью метода
# объекта файла
# записать с помощью модуля os

"""
#************************************
"""
file = open(r’C:\temp\spam.txt’, ‘w’) # создать внешний файл, объект
# записать с помощью объекта файла
file.write(‘Hello stdio file\n’)
file.flush()
# или сразу - функции os.write
fd = file.fileno()
# получить дескриптор из объекта
>>>
3
>>>
>>>
>>>
import os
os.write(fd, b’Hello descriptor file\n’) # записать с помощью модуля os
file.close()
C:\temp> type spam.txt
Hello stdio file
Hello descriptor file
# строки, записанные
# двумя способами
"""
#****************************************
"""
>>> fdfile = os.open(r’C:\temp\spam.txt’, (os.O_RDWR | os.O_BINARY))
>>> os.read(fdfile, 20)
b’Hello stdio file\r\nHe’
# вернуться в начало файла
>>> os.lseek(fdfile, 0, 0)
>>> os.read(fdfile, 100)
# в двоичном режиме сохраняются “\r\n”
b’Hello stdio file\r\nHello descriptor file\n’
>>> os.lseek(fdfile, 0, 0)
>>> os.write(fdfile, b’HELLO’) # перезаписать первые 5 байтов
5
C:\temp> type spam.txt
HELLO stdio file
Hello descriptor file
"""

#**************************************
"""

>>> fdfile = os.open(r’C:\temp\spam.txt’, (os.O_RDWR | os.O_BINARY))
>>> fdfile
3
>>> objfile = os.fdopen(fdfile, ‘rb’)
>>> objfile.read()
b’Jello stdio file\r\nHello descriptor file\n’
"""
#************************
"""
C:\...\PP4E\System> python
>>> import os
>>> fdfile = os.open(r’C:\temp\spam.txt’, (os.O_RDWR | os.O_BINARY))
>>> fdfile
3
>>> objfile = open(fdfile, ‘r’, encoding=’latin1’, closefd=False)
>>> objfile.read()
‘Jello stdio file\nHello descriptor file\n’
>>> objfile = os.fdopen(fdfile, ‘r’, encoding=’latin1’, closefd=True)
>>> objfile.seek(0)
>>> objfile.read()
‘Jello stdio file\nHello descriptor file\n’
"""
#**********************
#>>> os.chmod(‘spam.txt’, 0o777)
# разрешить доступ всем пользователям
#*******************************
"""
>>> os.rename(r’C:\temp\spam.txt’, r’C:\temp\eggs.txt’) # откуда, куда
>>> os.remove(r’C:\temp\spam.txt’)
# удалить файл?
WindowsError: [Error 2] The system cannot find the file specified: ‘C:\\
temp\\...’
"""
#*********************************
# построчное сканирование
# вызов объекта функции
def scanner(name, function):
    file = open(name, 'r')
    while True:
        line = file.readline()
        if not line: break
        function(line)
    file.close()

#Можно так, выгоднее, эффективнее
def scanner(name, function):
    for line in open(name, 'r'):
        function(line)

#Можно так для небольших файлов
#Цикл for замещается вызовом функции map или генератором,
#и Python сам закрывает файл на этапе сборки мусора или при выходе из
#сценария (в процессе обработки во всех реализациях создается список
#результатов, однако такое неэкономное расходование ресурсов вполне
#допустимо, за исключением очень больших файлов):
def scanner(name, function):
    list(map(function, open(name, 'r')))

def scanner(name, function):
    [function(line) for line in open(name, 'r')]

def scanner(name, function):
    list(function(line) for line in open(name, 'r'))
#******************************
import sys

def filter_files(name, function):         # filter file through function
    input  = open(name, 'r')              # create file objects
    output = open(name + '.out', 'w')     # explicit output file too
    for line in input:
        output.write(function(line))      # write the modified line
    input.close()
    output.close()                        # output has a '.out' suffix

def filter_stream(function):              # no explicit files
    while True:                           # use standard streams
        line = sys.stdin.readline()       # or: input()
        if not line: break
        print(function(line), end='')     # or: sys.stdout.write()

if __name__ == '__main__':
    filter_stream(lambda line: line)      # copy stdin to stdout if run



"""
def filter_files(name, function):
    with open(name, 'r') as input, open(name + '.out', 'w') as output:
        for line in input:
            output.write(function(line))      # write the modified line
"""

"""
def filter_stream(function):
    for line in sys.stdin:
        print(function(line), end='')
"""
"""
C:\...\PP4E\System\Filetools> filters.py < hillbillies.txt
*Granny
+Jethro
*Elly May
+”Uncle Jed”

>>> from filters import filter_files
>>> filter_files(‘hillbillies.txt’, str.upper)
>>> print(open(‘hillbillies.txt.out’).read())
*GRANNY
+JETHRO
*ELLY MAY
+”UNCLE JED”
"""
#*****************************************
#>>> glob.glob(‘*’)
#[‘parts’, ‘PP3E’, ‘random.bin’, ‘spam.txt’, ‘temp.bin’, ‘temp.txt’]

#>>> for path in glob.glob(r’PP3E\Examples\PP3E\*\s*.py’): print(path)


#**************************************
"""
>>> os.popen(‘dir /b parts’).readlines()
[‘part0001\n’, ‘part0002\n’, ‘part0003\n’, ‘part0004\n’]
>>> glob.glob(r’parts\*’)
[‘parts\\part0001’, ‘parts\\part0002’, ‘parts\\part0003’, ‘parts\\part0004’]
>>> os.listdir(‘parts’)
[‘part0001’, ‘part0002’, ‘part0003’, ‘part0004’]

#В предыдущем примере отмечалось, что функция glob возвращает пол-
#ные имена файлов с  путями, а  функция listdir возвращает простые
#базовые имена файлов.
"""
#****************************
"list file tree with os.walk"

import sys, os

def lister(root):                                           # for a root dir
    for (thisdir, subshere, fileshere) in os.walk(root):    # generate dirs in tree
        print('[' + thisdir + ']')
        for fname in fileshere:                             # print files in this dir
            path = os.path.join(thisdir, fname)             # add dir name prefix
            print(path)

if __name__ == '__main__':
    lister(sys.argv[1])                                     # dir name in cmdline

"""
>>> gen = os.walk(r’C:\temp\test’)
>>> gen.__next__()
(‘C:\\temp\\test’, [‘parts’], [‘random.bin’, ‘spam.txt’, ‘temp.bin’, ‘temp.
txt’])
>>> gen.__next__()
(‘C:\\temp\\test\\parts’, [], [‘part0001’, ‘part0002’, ‘part0003’, ‘part0004’])
>>> gen.__next__()
Traceback (most recent call last):
File “<stdin>”, line 1, in <module>
StopIteration
"""
#***************************
# list files in dir tree by recursion

import sys, os

def mylister(currdir):
    print('[' + currdir + ']')
    for file in os.listdir(currdir):              # list files here
        path = os.path.join(currdir, file)        # add dir path back
        if not os.path.isdir(path):
            print(path)
        else:
            mylister(path)                        # recur into subdirs

if __name__ == '__main__':
    mylister(sys.argv[1])                         # dir name in cmdline

#*****************
"""
C:\...\PP4E\System\Filetools> python
>>> import os
>>> os.listdir(‘.’)[:4]
[‘bigext-tree.py’, ‘bigpy-dir.py’, ‘bigpy-path.py’, ‘bigpy-tree.py’]
>>> os.listdir(b’.’)[:4]
[b’bigext-tree.py’, b’bigpy-dir.py’, b’bigpy-path.py’, b’bigpy-tree.py’]
"""
#*****************************
"""
Важно помнить, что Юникод может выполнять применительно к фай-
лам две различные задачи: кодирование содержимого файлов и  коди-
рование имен файлов. Интерпретатор Python определяет настройки по
умолчанию для этих двух операций в двух различных атрибутах; для
Windows 7:
>>> import sys
>>> sys.getdefaultencoding()
‘utf-8’
>>> sys.getfilesystemencoding()
‘mbcs’

Эти настройки позволяют явно указывать используемые кодиров-
ки – кодировка для содержимого используется операциями чтения из
файлов и  записи в  файлы, а  кодировка для имен файлов использует-
ся при работе с именами файлов, до передачи данных. Кроме того, ис-
пользование строк байтов bytes для передачи имен файлов различным
инструментам позволяет обойти проблему несовместимости со схемой
кодирования, используемой файловой сис­темой, а  открытие файлов
в двоичном режиме позволяет подавить ошибки декодирования их со-
держимого
"""


#**************************
#Casino
import random

def play():
    result = random.choice((0, 1))
    if result == 1:
        return True
    else:
        return False

class Game:
    money = 10000
    start = 5
    min_money = money
    def __init__(self):
        self.bet = self.start

    def play(self):
        self.bet *= 2
        #bet = self.bet
        win = play()
        if win:
            Game.money += self.bet
            self.bet = Game.start
        else:
            Game.money -= self.bet
        Game.min_money = min(Game.money, Game.min_money)
        #print(self.money, bet)

games = {}
for i in range(10):
    games[i] = Game()

for i in range(365 * 5):
    for key in games:
        games[key].play()

print(Game.min_money)
print(Game.money)

#***********************************

#Extended slice

#  s[i:j:k]	slice of s from i to j with step k
x = '0123456789'
print(x[::-1])
#9876543210
print(x[::-2])
#97531
print(x[::3])
#0369

print(x[0:3:2])
#02
l = list(x)
l[0:3:2] = ['P', 'P']
print(l)
#['P', '1', 'P', '3', '4', '5', '6', '7', '8', '9']
#*****************

from collections import defaultdict

d = defaultdict(lambda: 'missing', {'key1': 1, 'key2': 2})

print(d['key1']) #1
print(d['key3']) #'missing'

d1 = {'key1': 1, 'key2': 2}

for k in range(0, 10):
    d1.setdefault('key{0}'.format(k), 'missing')

print(d1['key1']) #1
print(d1['key3']) #'missing'
#***********************
s = set([1, 2, 3, 1])
#s = {1, 2, 3, 1} Аналог
fs = frozenset([1, 2, 3, 1])

print(s == fs) #True

print(s)
#{1, 2, 3}
print(fs)
#frozenset({1, 2,

s.add(4)
s.remove(1)
#fs.add(4) AttributeError: 'frozenset' object has no attribute 'add'
#fs.remove(1) AttributeError: 'frozenset' object has no attribute 'remove'


d = {}
d[fs] = True
#d[s] = True #TypeError: unhashable type: 'set'
#*****************************************

from collections import defaultdict
s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
d = defaultdict(list)
for k, v in s:
    d[k].append(v)
print(list(d.items()))
#[('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]
print(d) #defaultdict(<class 'list'>, {'red': [1], 'blue': [2, 4], 'yellow': [1, 3]})
#*******************************
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(11, y=22)     # instantiate with positional or keyword arguments
print(p[0] + p[1])             # indexable like the plain tuple (11, 22)
#33
x, y = p                # unpack like a regular tuple
print(x, y)
#(11, 22)
print(p.x + p.y)               # fields also accessible by name
#33
print(p)                       # readable __repr__ with a name=value style
#Point(x=11, y=22)
p = Point(1, 2, 3) #TypeError: __new__() takes 3 positional arguments but 4 were given
#*****************************
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
#Point = namedtuple('Point', 'x, y')
#Point = namedtuple('Point', 'x y')
p = Point(11, y=22)     # instantiate with positional or keyword arguments
print(p[0] + p[1])             # indexable like the plain tuple (11, 22)
#33
x, y = p                # unpack like a regular tuple
print(x, y)
#(11, 22)
print(p.x + p.y)               # fields also accessible by name
#33
print(p)                       # readable __repr__ with a name=value style
#Point(x=11, y=22)
#p = Point(1, 2, 3) #TypeError: __new__() takes 3 positional arguments but 4 were given

#************************************
#https://docs.python.org/3/library/collections.html
"""
This module implements specialized container datatypes providing alternatives to Python’s general purpose built-in containers, dict, list, set, and tuple.

namedtuple()	factory function for creating tuple subclasses with named fields
deque	list-like container with fast appends and pops on either end
ChainMap	dict-like class for creating a single view of multiple mappings
Counter	dict subclass for counting hashable objects
OrderedDict	dict subclass that remembers the order entries were added
defaultdict	dict subclass that calls a factory function to supply missing values
UserDict	wrapper around dictionary objects for easier dict subclassing
UserList	wrapper around list objects for easier list subclassing
UserString	wrapper around string objects for easier string subclassing
"""

#ChainMap objects


#*********************************

from collections import ChainMap

m0 = ChainMap({'level0': 0})
m1 = m0.new_child({'level1': 1})
m2 = m1.new_child({'level2': 2})

print(m2)
#ChainMap({'level2': 2}, {'level1': 1}, {'level0': 0})

print(m1)
#ChainMap({'level1': 1}, {'level0': 0})

print(m0)
#ChainMap({'level0': 0})

print(m2.maps)
#[{'level2': 2}, {'level1': 1}, {'level0': 0}]\


#****************************************** ChainMap
from collections import ChainMap

d1 = {'name': 'd1'}
d2 = {'name': 'd2'}
d3 = {'name': 'd3'}
d4 = {'name': 'd4'}

c = ChainMap(d1)        # Create root context
d = c.new_child(d2)     # Create nested child context
e = c.new_child(d3)     # Child of c, independent from d
f = e.new_child(d4)

print(e.maps[0])             # Current context dictionary -- like Python's locals() # {'name': 'd3'}
print(e.maps[-1])            # Root context -- like Python's globals() #    {'name': 'd1'}
print(e.parents)             # Enclosing context chain -- like Python's nonlocals # ChainMap({'name': 'd1'})
print(f)                    # ChainMap({'name': 'd4'}, {'name': 'd3'}, {'name': 'd1'})
print(c)                    # ChainMap({'name': 'd1'})
print(e)                    # ChainMap({'name': 'd3'}, {'name': 'd1'})

#******************************
import builtins
loc = locals()
glob = globals()
bins = vars(builtins)
pylookup = ChainMap(loc, glob, bins)
print(pylookup)

#******************************
class DeepChainMap(ChainMap):
    'Variant of ChainMap that allows direct updates to inner scopes'

def __setitem__(self, key, value):
    for mapping in self.maps:
        if key in mapping:
            mapping[key] = value
            return
    self.maps[0][key] = value

def __delitem__(self, key):
    for mapping in self.maps:
        if key in mapping:
            del mapping[key]
            return
    raise KeyError(key)

d = DeepChainMap({'zebra': 'black'}, {'elephant': 'blue'}, {'lion': 'yellow'})
d['lion'] = 'orange'         # update an existing key two levels down
d['snake'] = 'red'           # new keys get added to the topmost dict
del d['elephant']            # remove an existing key one level down
DeepChainMap({'zebra': 'black', 'snake': 'red'}, {}, {'lion': 'orange'})

#Counter
#https://docs.python.org/3/library/collections.html#collections.Counter
from collections import Counter
cnt = Counter(['red', 'blue', 'red', 'green', 'blue', 'blue'])
print(cnt)
#Counter({'blue': 3, 'red': 2, 'green': 1})

"""
>>> # Find the ten most common words in Hamlet
>>> import re
>>> words = re.findall(r'\w+', open('hamlet.txt').read().lower())
>>> Counter(words).most_common(10)
[('the', 1143), ('and', 966), ('to', 762), ('of', 669), ('i', 631),
 ('you', 554),  ('a', 546), ('my', 514), ('hamlet', 471), ('in', 451)]
"""
#*********************
from collections import Counter

c = Counter('hello world')
print(c.elements())
print(list(c.elements()))
#<itertools.chain object at 0x7f90ffe35f60>
#['d', 'w', 'l', 'l', 'l', 'r', 'o', 'o', 'e', ' ', 'h']

print(c.most_common(3))
#[('l', 3), ('o', 2), ('r', 1)]

c.subtract('low')
print(c.most_common(3))
#[('l', 2), (' ', 1), ('o', 1)]

c.update('low')
print(c.most_common(3))
#[('l', 3), ('o', 2), ('h', 1)]

n = 3
print(c.most_common()[:-n-1:-1]) #Least common
#[('w', 1), ('h', 1), ('r', 1)]

d = +c ## remove zero and negative counts
print(d)

#*************************************************
#deque
#https://docs.python.org/3/library/collections.html#deque-objects
#class collections.deque([iterable[, maxlen]])
"""
>>> from collections import deque
>>> d = deque('ghi')                 # make a new deque with three items
>>> for elem in d:                   # iterate over the deque's elements
...     print(elem.upper())
G
H
I

>>> d.append('j')                    # add a new entry to the right side
>>> d.appendleft('f')                # add a new entry to the left side
>>> d                                # show the representation of the deque
deque(['f', 'g', 'h', 'i', 'j'])

>>> d.pop()                          # return and remove the rightmost item
'j'
>>> d.popleft()                      # return and remove the leftmost item
'f'
>>> list(d)                          # list the contents of the deque
['g', 'h', 'i']
>>> d[0]                             # peek at leftmost item
'g'
>>> d[-1]                            # peek at rightmost item
'i'

>>> list(reversed(d))                # list the contents of a deque in reverse
['i', 'h', 'g']
>>> 'h' in d                         # search the deque
True
>>> d.extend('jkl')                  # add multiple elements at once
>>> d
deque(['g', 'h', 'i', 'j', 'k', 'l'])
>>> d.rotate(1)                      # right rotation
>>> d
deque(['l', 'g', 'h', 'i', 'j', 'k'])
>>> d.rotate(-1)                     # left rotation
>>> d
deque(['g', 'h', 'i', 'j', 'k', 'l'])

>>> deque(reversed(d))               # make a new deque in reverse order
deque(['l', 'k', 'j', 'i', 'h', 'g'])
>>> d.clear()                        # empty the deque
>>> d.pop()                          # cannot pop from an empty deque
Traceback (most recent call last):
    File "<pyshell#6>", line 1, in -toplevel-
        d.pop()
IndexError: pop from an empty deque

>>> d.extendleft('abc')              # extendleft() reverses the input order
>>> d
deque(['c', 'b', 'a'])
"""

#*********************************
#try2.py
from collections import deque
def tail(filename, n=10):
    'Return the last n lines of a file'
    with open(filename) as f:
        return deque(f, n)

x = tail('try2.py', 2)
print(x)
#deque(["x = tail('try2.py', 2)\n", 'print(x)'], maxlen=2)
#********************************
from collections import deque
d = deque(['1', '2', '3'], 3)
d.append('4')
print(d)
#deque(['2', '3', '4'], maxlen=3
#*****************************


"""
>>> from collections import deque
>>> d = deque('ghi')                 # make a new deque with three items
>>> for elem in d:                   # iterate over the deque's elements
...     print(elem.upper())
G
H
I

>>> d.append('j')                    # add a new entry to the right side
>>> d.appendleft('f')                # add a new entry to the left side
>>> d                                # show the representation of the deque
deque(['f', 'g', 'h', 'i', 'j'])

>>> d.pop()                          # return and remove the rightmost item
'j'
>>> d.popleft()                      # return and remove the leftmost item
'f'
>>> list(d)                          # list the contents of the deque
['g', 'h', 'i']
>>> d[0]                             # peek at leftmost item
'g'
>>> d[-1]                            # peek at rightmost item
'i'

>>> list(reversed(d))                # list the contents of a deque in reverse
['i', 'h', 'g']
>>> 'h' in d                         # search the deque
True
>>> d.extend('jkl')                  # add multiple elements at once
>>> d
deque(['g', 'h', 'i', 'j', 'k', 'l'])
>>> d.rotate(1)                      # right rotation
>>> d
deque(['l', 'g', 'h', 'i', 'j', 'k'])
>>> d.rotate(-1)                     # left rotation
>>> d
deque(['g', 'h', 'i', 'j', 'k', 'l'])

>>> deque(reversed(d))               # make a new deque in reverse order
deque(['l', 'k', 'j', 'i', 'h', 'g'])
>>> d.clear()                        # empty the deque
>>> d.pop()                          # cannot pop from an empty deque
Traceback (most recent call last):
    File "<pyshell#6>", line 1, in -toplevel-
        d.pop()
IndexError: pop from an empty deque

>>> d.extendleft('abc')              # extendleft() reverses the input order
>>> d
deque(['c', 'b', 'a'])
"""


#**************************************
from collections import ChainMap
import os, argparse

defaults = {'color': 'red', 'user': 'guest', 'test': 'default'}

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user')
parser.add_argument('-c', '--color')
parser.add_argument('-t', '--test')
namespace = parser.parse_args(['--user', 'Alex', '-c', 'Green'])
print(namespace) #Namespace(color='Green', test=None, user='Alex'

command_line_args = {k: v for k, v in vars(namespace).items() if v}
print(command_line_args) #{'user': 'Alex', 'color': 'Green'}
combined = ChainMap(command_line_args, os.environ, defaults)
print(combined['color'])
print(combined['user'])
print(combined['test'])
#Green
#Alex
#default
#********************************************
from collections import namedtuple
class Point(namedtuple('Point', 'x y')):
    __slots__ = ()
    @property
    def hypot(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    def __str__(self):
        return 'Point: x=%6.3f  y=%6.3f  hypot=%6.3f' % (self.x, self.y, self.hypot)

for p in Point(3, 4), Point(14, 5/7):
    print(p)
#Point: x= 3.000  y= 4.000  hypot= 5.000
#Point: x=14.000  y= 0.714  hypot=14.018

#++++++++++++
Point3D = namedtuple('Point3D', Point._fields + ('z',))
p3d = Point3D(1, 2, 3)
print(p3d)
#Point3D(x=1, y=2, z=3)
#++++++++++++

Account = namedtuple('Account', 'owner balance transaction_count')
default_account = Account('<owner name>', 0.0, 0)
johns_account = default_account._replace(owner='John')
janes_account = default_account._replace(owner='Jane')
print(johns_account)
#Account(owner='John', balance=0.0, transaction_count=0)
print(janes_account)
#Account(owner='Jane', balance=0.0, transaction_count=0)
#++++++++++++

Status = namedtuple('Status', 'open pending closed')._make(range(3))
Status.open, Status.pending, Status.closed
#(0, 1, 2)

#++++++++++++

from enum import Enum
class Status(Enum):
    open, pending, closed = range(3)

st = Status(1)
print(st) #Status.pending

#***********************
from collections import OrderedDict
# regular unsorted dictionary
d = {'banana': 3, 'apple':4, 'pear': 1, 'orange': 2}

# dictionary sorted by key
print(OrderedDict(sorted(d.items(), key=lambda t: t[0])))
#OrderedDict([('apple', 4), ('banana', 3), ('orange', 2), ('pear', 1)])


# dictionary sorted by value
print(OrderedDict(sorted(d.items(), key=lambda t: t[1])))
#OrderedDict([('pear', 1), ('orange', 2), ('banana', 3), ('apple', 4)])

# dictionary sorted by length of the key string
print(OrderedDict(sorted(d.items(), key=lambda t: len(t[0]))))
#OrderedDict([('pear', 1), ('apple', 4), ('orange', 2), ('banana', 3)])
#**************************************
from functools import reduce
value = ['1', '2', '3']
allowed = ['1', '3']
res = reduce(str.__add__, map(lambda x: (("0", x)[int(x in allowed)]), value), "")
print(res)
#103
#*******************************************
#Удобнее, чем subclass dict. data - обернутый dict. Есть еще UserList и UserString, но там все аналогично.
from collections import UserDict

class MyDict(UserDict):
    def sum(self):
        return sum(self.data.values())

d = {'a': 1, 'b': 2}
md = MyDict(d)
print(md)
print(md.sum())

#***************************
L = [1, 2, 3, 4, 5]

res = (elem > 3 for elem in L)
res1 = [elem > 3 for elem in L]
print(res) #<generator object <genexpr> at 0x7fd2999c69d8>
print(res1) #[False, False, False, True, True]

print(any(elem > 3 for elem in L)) #True
print(any((elem > 3 for elem in L))) #True
print(all([elem > 3 for elem in L])) #False


#***************************
print([x + y for x in 'abc' for y in 'lmn'])
#['al', 'am', 'an', 'bl', 'bm', 'bn', 'cl', 'cm', 'cn']

res = []
for x in 'abc':
    for y in 'lmn':
        res.append(x + y)
print(res)

#['al', 'am', 'an', 'bl', 'bm', 'bn', 'cl', 'cm', 'cn']
#**********************************
"""
>>> [x for x in range(5) if x % 2 == 0]
[0, 2, 4]
>>> list(filter((lambda x: x % 2 == 0), range(5)))
[0, 2, 4]
>>>
>>>
...
...
...
>>>
[0,
res = []
for x in range(5):
if x % 2 == 0:
res.append(x)
res
2, 4]
"""
#******************************
print(list(map((lambda x: x**2), filter((lambda x: x % 2 == 0), range(10)))))
#[0, 4, 16, 36, 64]
#*************************************
#stud
def gen():
    for i in range(10):
        X = yield i
        print('X =', X)

G = gen()
print(next(G))
#0
print(next(G))
#X = None
#1
print(G.send(222))
#X = 222
#2
#***********************
l = [[1, 3], [2, 3], [4, 5], 6]

f1 = [inner for elem in l if isinstance(elem, list) for inner in elem]
print(f1)
#[1, 3, 2, 3, 4, 5]



k = [x + y for x in 'abc' for y in 'def' if x != 'a']
print(k)
#['bd', 'be', 'bf', 'cd', 'ce', 'cf']

k = [x + y for x in 'abc' if x != 'a' for y in 'def']
print(k)

#['bd', 'be', 'bf', 'cd', 'ce', 'cf']
k = [x + y if x != 'a' else x for x in 'abc' for y in 'def']
print(k)
#['bd', 'be', 'bf', 'cd', 'ce', 'cf']


#******************************************
#stud my
class Catalog:

    def meth1(self):
        print('meth1')

    def meth2(self):
        print('meth2')

    methods = {'method1': meth1, 'method2': meth2}

    def __init__(self, meth):
        self.meth = self.methods[meth]

    def call_meth(self):
        return self.meth.__get__(self, Catalog)()

c1 = Catalog('method1')


c1.call_meth()
#'meth1'

#operator.itemgetter stud
class itemgetter:
    """
    Return a callable object that fetches the given item(s) from its operand.
    After f = itemgetter(2), the call f(r) returns r[2].
    After g = itemgetter(2, 5, 3), the call g(r) returns (r[2], r[5], r[3])
    """
    def __init__(self, item, *items):
        if not items:
            def func(obj):
                return obj[item]
            self._call = func
        else:
            items = (item,) + items
            def func(obj):
                return tuple(obj[i] for i in items)
            self._call = func

    def __call__(self, obj):
        return self._call(obj)

r = {2: 'x'}

f = itemgetter(2)
print(f(r)) #x

r = {2: 'x', 3: 'y'}

f = itemgetter(2, 3)
print(f(r)) #('x', 'y')


#*************************
#Первые 127 символов у ut8-8 и ascii совпадают
s = 'az'


b = s.encode('utf-8')

for x in b:
    print(x)

b = s.encode('ascii')

for x in b:
    print(x)

#97
#122

#97
#122

#*********************************************
s = 'aя'

b = s.encode('utf-8')

for x in b:
    print(x)
#97
#209
#143

#На киррилический символ 2 байта

#***************************

s = 'aя'


b = s.encode('ascii')

#UnicodeEncodeError: 'ascii' codec can't encode character '\u044f' in position 1: ordinal not in range(128)
#Эта кодировка ascii использует первые 127 значений.

#********************************************************

# Naive encoding and decoding. Should find 20 vinutes to improve.

table = {
    'ʠ': '02A0',
    'ʛ': '029B'
}



reversed_table = {v: k for k, v in table.items()}

def get_bytes_count(number):
    # В зависимости от номера символу выделяется определенное количество байт
    return 2

def encode(s):
    number = table[s]  # Можно еще number = ord(c]
    length = get_bytes_count(number)
    i = int(number, 16)
    b = "{0:b}".format(i)
    if length == 2:
        first_byte = '110'
        second_byte = '10'
        right = b[-6:]
        left = b[:-6]
        second_byte += right

        zeros = 5 - len(left)
        left = '0' * zeros + left
        first_byte += left
        return first_byte, second_byte


encoded = encode('ʛ')
print(encoded)

test = 'ʛ'.encode()
for b in test:
    print("{0:b}".format(b))


def decode(b):
    first_byte = b[0]
    if first_byte[:3] == '110':
        second_byte = b[1]
        binary_number = first_byte[3:] + second_byte[2:]
        int_number = int(binary_number, 2)
        hex_number = hex(int_number).upper()
        hex_number = hex_number[0] + hex_number[2:]
        return reversed_table[hex_number]

print(decode(encoded))

#*************************************************


s = b'Alex' #Bytes representation of a string

for b in s:
    print(b, end=' ') # 65 108 101 120

ba = bytearray(s)

ba.append(100)
print(ba) #bytearray(b'Alexd')

#**********************************************


import binascii


print(ord('A')) # 65 Номер в таблице utf - 8 по порядку в десятичной
print(binascii.hexlify(b'A'))  # b'41' hex representation

print(hex(65)) # 0x41
print(int('41',16)) #65

print(binascii.unhexlify('41')) #b'A'

k = binascii.hexlify(b'Alex')
print(k) #416c6578

m = int(k, 16)
l = hex(m)
print(l) #0x416c6578



a = 0x8F7A93
print(a) #9403027

k = bin(a)
print(k) #0b100011110111101010010011
print(type(k)) #<class 'str'>


#****************************************



x = 1e200
y = x * x
print(y) # inf

z = y / y
print(z) # nan


x = 10**200
print(x) #100000000000000000000000000000000000000000000000000000000000000000.......
y = (x + 0.5) * x # Без 0.5 будет ок
print(y) #inf

#z = x * x + 0.5 OverflowError: int too large to convert to float


#*********************

x = 0x100 #octal, 16, hex
print(x) #256

y = 0o100 # 8, octal
print(y) #64

z = 0b100 #binary
print(z) #4

#***************************


print(0b110 & 0b001) # 0
print(0b111 & 0b111) #7, то есть 111


print(0b110 | 0b001) #7
print(bin(7)) #0b111

print(0b110 ^ 0b001) # Только 0 1 или 1 0, Xor... Результат 7

print(~ 0b001) # Not, -2

"""
1 is 0000 00001
~ 0000 00001 is 1111 1110, which is -2
https://ru.wikipedia.org/wiki/Дополнительный_код_(представление_числа)
"""

print(bin(-2)) #-0b10
print(int('0b001', 2)) #1]
print(~ 1) #-2
print(~ 0b0110) #-7
print(bin(-7)) #-0b111


# Shifting


k = 0b100
print(k) #4
k = k << 1
print(k) #8, 0100 => 1000

k = k >> 2
print(k) #2 1000 =? 0010


#setting and clearing

x = 0b1010101
mask = 0b0100000


x = x | mask
print(bin(x)) #0b1110101

mask = 0b0010000
mask = ~mask
print(bin(mask)) #-0b10001 or 1101111, so remove only one byte
x = x & mask
print(bin(x)) #0b1100101

#*********************************
# Boolean flags

X = 0x01
Y = 0x02
Z = 0x04
#Thats is 0b0xyz with x, y, z having values in (0,1)  : X = 0x01, Y = 0x02, Z = 0x04

T = 0x03
print(bin(T)) #'0b11'
print(T & X) # 1
print(T & Y) # 2
print(T & Z) # 0

T = 0b101
print(T & X) # 1
print(T & Y) # 0
print(T & Z) # 4

#***********************************************
print(b'abc' == 'abc'.encode()) #True

#*******************************************

import struct
import binascii

values = (1, b'ab', 2.7)
s = struct.Struct('I 2s f') # Integer, 2 strings, float
packed_data = s.pack(*values)

print('Original values:', values)
print('Format string  :', s.format)
print('Uses           :', s.size, 'bytes')
print('Packed Value   :', binascii.hexlify(packed_data))

#Original values: (1, b'ab', 2.7)
#Format string  : b'I 2s f'
#Uses           : 12 bytes
#Packed Value   : b'0100000061620000cdcc2c40' # Это не utf-8, а шестнадцатиричное представление, потому
# превратить в байты через binascii.unhexlify. Обычно расчет на utf-8 (b'abc' == 'abc'.encode())

unpacked = s.unpack(packed_data)
print(unpacked) # (1, b'ab', 2.700000047683716)


packed_data = binascii.unhexlify('0100000061620000cdcc2c40')

s = struct.Struct('I 2s f')
unpacked_data = s.unpack(packed_data)
print('Unpacked Values:', unpacked_data)


#********************