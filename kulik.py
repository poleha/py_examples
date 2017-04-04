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

#****************************************************

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


#**************************************************

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

#************************************************************
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

#***********************************************************
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

#******************************************

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
#*****************************************************

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

#*******************************************
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

#********************************************
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
        self.__visited = set()
        return self.__listclass(self.__class__)

    def __listclass(self, aClass, level=0):
        if aClass in self.__visited:
            return aClass.__name__ + str(level) + ' Visited' + '\n'
        else:
            self.__visited.add(aClass)
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

#**********************************************

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

#*************************************************


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

#********************
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

#***********************
class cached_property(object):
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance.

    Optional ``name`` argument allows you to make cached properties of other
    methods. (e.g.  url = cached_property(get_absolute_url, name='url') )
    """
    def __init__(self, func, name=None):
        self.func = func
        self.__doc__ = getattr(func, '__doc__')
        self.name = name or func.__name__

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        res = instance.__dict__[self.name] = self.func(instance)
        return res

#*****************************
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

#********** stud
class Meta(type):
    @staticmethod
    def __new__(meta, classname, classbases, classattr):
        print('1Meta.__new__')
        return type.__new__(meta, classname, classbases, classattr) # Это будет instance of meta
        #return super(Meta, meta).__new__(meta, classname, classbases, classattr) # Это будет instance of meta
        #return type(classname, classbases, classattr) # Пропустим 2 и 3, что не верно. Это будет instance of type
        # Тогда при создании SubMeta будет вызван type, а не Meta. Потому и не вызовутся 2 и 3

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
        #return type(classname, classbases, classattr)  # Пропустим 6. 5 не пропустим тк видимо type при создании класса метакласс вызывает __init__, а при создании метакласса(type) не вызывает

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

#*******************************************

def tracer(func):
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        print('Количество вызовов', func.__name__, wrapper.count)
        return func(*args, **kwargs)
    wrapper.count = 0
    return wrapper

#******************************************
import os
def child():
    print('Hello from child',  os.getpid())
    os._exit(0)  # else goes back to parent loop
    #Завершаем процесс со статусом 0

def parent():
    while True:
        print('1')
        newpid = os.fork()
        print('2') #fork startst from here
        #Создали дочерний процесс, копию исходного
        if newpid == 0: #Если мы в дочернем процессе, то newpid == 0
            child()
        else:
            print('Hello from parent', os.getpid(), newpid)
        if input() == 'q': break

parent()

#*********************************
def infixToPostfix(infixexpr):
    prec = {}
    prec["^"] = 4
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    opStack = deque()
    postfixList = []
    tokenList = infixexpr.split()

    for token in tokenList:
        if token in digits + ascii_uppercase:
            postfixList.append(token)
        elif token == '(':
            opStack.append(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while opStack and prec[opStack[-1]] >= prec[token]:
                postfixList.append(opStack.pop())

            opStack.append(token)

    while opStack:
        postfixList.append(opStack.pop())
    return " ".join(postfixList)


#print(infixToPostfix("A * B + C * D"))
#print(infixToPostfix("( A + B ) * C - ( D - E ) * ( F + G )"))
#print(infixToPostfix("A * B + C"))
#print(infixToPostfix("A + B * C"))
#print(infixToPostfix("( A + B )  * C"))



def postfixEval(postfixExpr):
    operands = deque()
    expr = postfixExpr.split()


    for token in expr:
        try:
            token = int(token)
            is_operand = True
        except:
            is_operand = False

        if is_operand:
            operands.append(token)
        else:
            right = operands.pop()
            left = operands.pop()
            res = eval("{}{}{}".format(left, token, right))
            operands.append(res)
    return operands[0]

#print(postfixEval('7 8 + 3 2 + /'))
#print(postfixEval('17 10 + 3 * 9 /'))


A = infixToPostfix("5 * 3 ^ ( 4 - 2 )")
print(A)
print(postfixEval(A))

#************************


#Считаем, какие монеты использованы # stud
def dpMakeChange(coinValueList,change,minCoins,coinsUsed):
   for cents in range(change+1):
      coinCount = cents
      newCoin = 1
      for j in [c for c in coinValueList if c <= cents]:
            if minCoins[cents-j] + 1 < coinCount:
               coinCount = minCoins[cents-j]+1
               newCoin = j
      minCoins[cents] = coinCount
      coinsUsed[cents] = newCoin # То есть это последняя добавленная монета
   return minCoins[change]

def printCoins(coinsUsed,change):
   coin = change
   while coin > 0:
      thisCoin = coinsUsed[coin]
      print(thisCoin)
      coin = coin - thisCoin

def main():
    amnt = 11
    clist = [1,5,10,21,25]
    coinsUsed = [0]*(amnt+1)
    coinCount = [0]*(amnt+1)

    print("Making change for",amnt,"requires")
    print(dpMakeChange(clist,amnt,coinCount,coinsUsed),"coins")
    print("They are:")
    printCoins(coinsUsed,amnt)
    print("The used list is as follows:")
    print(coinsUsed)

main()

#**************************
# stud
def convert(n, base):
    digits = '0123456789ABCDEF'
    if n < base:
        return digits[n]
    else:
        return convert(n // base, base) + digits[n % base]

print(convert(769, 10)) #769
print(convert(10, 2)) #1010

#**********************************************
class Dog(object):
    def __init__(self):
        self.name = "Dog"

    def bark(self):
        return "woof!"


class Cat(object):
    def __init__(self):
        self.name = "Cat"

    def meow(self):
        return "meow!"


class Human(object):
    def __init__(self):
        self.name = "Human"

    def speak(self):
        return "'hello'"


class Car(object):
    def __init__(self):
        self.name = "Car"

    def make_noise(self, octane_level):
        return "vroom{0}".format("!" * octane_level)


class Adapter(object):
    """
    Adapts an object by replacing methods.
    Usage:
    dog = Dog
    dog = Adapter(dog, dict(make_noise=dog.bark))
    >>> objects = []
    >>> dog = Dog()
    >>> print(dog.__dict__)
    {'name': 'Dog'}
    >>> objects.append(Adapter(dog, make_noise=dog.bark))
    >>> print(objects[0].original_dict())
    {'name': 'Dog'}
    >>> cat = Cat()
    >>> objects.append(Adapter(cat, make_noise=cat.meow))
    >>> human = Human()
    >>> objects.append(Adapter(human, make_noise=human.speak))
    >>> car = Car()
    >>> car_noise = lambda: car.make_noise(3)
    >>> objects.append(Adapter(car, make_noise=car_noise))
    >>> for obj in objects:
    ...     print('A {} goes {}'.format(obj.name, obj.make_noise()))
    A Dog goes woof!
    A Cat goes meow!
    A Human goes 'hello'
    A Car goes vroom!!!
    """

    def __init__(self, obj, **adapted_methods):
        """We set the adapted methods in the object's dict"""
        self.obj = obj
        self.__dict__.update(adapted_methods)

    def __getattr__(self, attr):
        """All non-adapted calls are passed to the object"""
        return getattr(self.obj, attr)

    def original_dict(self):
        """Print original object dict"""
        return self.obj.__dict__


def main():
    objects = []
    dog = Dog()
    print(dog.__dict__)
    objects.append(Adapter(dog, make_noise=dog.bark))
    print(objects[0].__dict__)
    print(objects[0].original_dict())
    cat = Cat()
    objects.append(Adapter(cat, make_noise=cat.meow))
    human = Human()
    objects.append(Adapter(human, make_noise=human.speak))
    car = Car()
    objects.append(Adapter(car, make_noise=lambda: car.make_noise(3)))

    for obj in objects:
        print("A {0} goes {1}".format(obj.name, obj.make_noise()))


if __name__ == "__main__":
    main()

    ### OUTPUT ###
    # {'name': 'Dog'}
    # {'make_noise': <bound method Dog.bark of <__main__.Dog object at 0x7f631ba3fb00>>, 'obj': <__main__.Dog object at 0x7f631ba3fb00>}
    # {'name': 'Dog'}
    # A Dog goes woof!
    # A Cat goes meow!
    # A Human goes 'hello'
    # A Car goes vroom!!!

#***************************************


class Data(object):
    """ Data Store Class """

    products = {
        'milk': {'price': 1.50, 'quantity': 10},
        'eggs': {'price': 0.20, 'quantity': 100},
        'cheese': {'price': 2.00, 'quantity': 10}
    }

    def __get__(self, obj, klas):
        print("(Fetching from Data Store)")
        return {'products': self.products}


class BusinessLogic(object):
    """ Business logic holding data store instances """

    data = Data()

    def product_list(self):
        return self.data['products'].keys()

    def product_information(self, product):
        return self.data['products'].get(product, None)


class Ui(object):
    """ UI interaction class """

    def __init__(self):
        self.business_logic = BusinessLogic()

    def get_product_list(self):
        print('PRODUCT LIST:')
        for product in self.business_logic.product_list():
            print(product)
        print('')

    def get_product_information(self, product):
        product_info = self.business_logic.product_information(product)
        if product_info:
            print('PRODUCT INFORMATION:')
            print('Name: {0}, Price: {1:.2f}, Quantity: {2:}'.format(
                product.title(), product_info.get('price', 0),
                product_info.get('quantity', 0)))
        else:
            print('That product "{0}" does not exist in the records'.format(
                product))


def main():
    ui = Ui()
    ui.get_product_list()
    ui.get_product_information('cheese')
    ui.get_product_information('eggs')
    ui.get_product_information('milk')
    ui.get_product_information('arepas')

if __name__ == '__main__':
    main()

### OUTPUT ###
# PRODUCT LIST:
# (Fetching from Data Store)
# cheese
# eggs
# milk
#
# (Fetching from Data Store)
# PRODUCT INFORMATION:
# Name: Cheese, Price: 2.00, Quantity: 10
# (Fetching from Data Store)
# PRODUCT INFORMATION:
# Name: Eggs, Price: 0.20, Quantity: 100
# (Fetching from Data Store)
# PRODUCT INFORMATION:
# Name: Milk, Price: 1.50, Quantity: 10
# (Fetching from Data Store)
# That product "arepas" does not exist in the records


#**********************************************

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://ginstrom.com/scribbles/2007/10/08/design-patterns-python-style/

"""Implementation of the abstract factory pattern"""

import random


class PetShop(object):

    """A pet shop"""

    def __init__(self, animal_factory=None):
        """pet_factory is our abstract factory.  We can set it at will."""

        self.pet_factory = animal_factory

    def show_pet(self):
        """Creates and shows a pet using the abstract factory"""

        pet = self.pet_factory.get_pet()
        print("We have a lovely {}".format(pet))
        print("It says {}".format(pet.speak()))
        print("We also have {}".format(self.pet_factory.get_food()))


# Stuff that our factory makes

class Dog(object):

    def speak(self):
        return "woof"

    def __str__(self):
        return "Dog"


class Cat(object):

    def speak(self):
        return "meow"

    def __str__(self):
        return "Cat"


# Factory classes

class DogFactory(object):

    def get_pet(self):
        return Dog()

    def get_food(self):
        return "dog food"


class CatFactory(object):

    def get_pet(self):
        return Cat()

    def get_food(self):
        return "cat food"


# Create the proper family
def get_factory():
    """Let's be dynamic!"""
    return random.choice([DogFactory, CatFactory])()


# Show pets with various factories
if __name__ == "__main__":
    for i in range(3):
        shop = PetShop(get_factory())
        shop.show_pet()
        print("=" * 20)

### OUTPUT ###
# We have a lovely Dog
# It says woof
# We also have dog food
# ====================
# We have a lovely Dog
# It says woof
# We also have dog food
# ====================
# We have a lovely Cat
# It says meow
# We also have cat food
# ====================


#*******************************************

class Borg(object):
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        self.state = 'Init'

    def __str__(self):
        return self.state


class YourBorg(Borg):
    pass


if __name__ == '__main__':
    rm1 = Borg()
    rm2 = Borg()

    rm1.state = 'Idle'
    rm2.state = 'Running'

    print('rm1: {0}'.format(rm1))
    print('rm2: {0}'.format(rm2))

    rm2.state = 'Zombie'

    print('rm1: {0}'.format(rm1))
    print('rm2: {0}'.format(rm2))

    print('rm1 id: {0}'.format(id(rm1)))
    print('rm2 id: {0}'.format(id(rm2)))

    rm3 = YourBorg()

    print('rm1: {0}'.format(rm1))
    print('rm2: {0}'.format(rm2))
    print('rm3: {0}'.format(rm3))

### OUTPUT ###
# rm1: Running
# rm2: Running
# rm1: Zombie
# rm2: Zombie
# rm1 id: 140732837899224
# rm2 id: 140732837899296
# rm1: Init
# rm2: Init
# rm3: Init

#**********************************************************8
from contextlib import contextmanager
import os
import sys
import time


class Handler(object):

    def __init__(self, successor=None):
        self._successor = successor

    def handle(self, request):
        res = self._handle(request)
        if not res:
            self._successor.handle(request)

    def _handle(self, request):
        raise NotImplementedError('Must provide implementation in subclass.')


class ConcreteHandler1(Handler):

    def _handle(self, request):
        if 0 < request <= 10:
            print('request {} handled in handler 1'.format(request))
            return True


class ConcreteHandler2(Handler):

    def _handle(self, request):
        if 10 < request <= 20:
            print('request {} handled in handler 2'.format(request))
            return True


class ConcreteHandler3(Handler):

    def _handle(self, request):
        if 20 < request <= 30:
            print('request {} handled in handler 3'.format(request))
            return True


class DefaultHandler(Handler):

    def _handle(self, request):
        print('end of chain, no handler for {}'.format(request))
        return True


class Client(object):

    def __init__(self):
        self.handler = ConcreteHandler1(
            ConcreteHandler3(ConcreteHandler2(DefaultHandler())))

    def delegate(self, requests):
        for request in requests:
            self.handler.handle(request)


def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr
    return start


@coroutine
def coroutine1(target):
    while True:
        request = yield
        if 0 < request <= 10:
            print('request {} handled in coroutine 1'.format(request))
        else:
            target.send(request)


@coroutine
def coroutine2(target):
    while True:
        request = yield
        if 10 < request <= 20:
            print('request {} handled in coroutine 2'.format(request))
        else:
            target.send(request)


@coroutine
def coroutine3(target):
    while True:
        request = yield
        if 20 < request <= 30:
            print('request {} handled in coroutine 3'.format(request))
        else:
            target.send(request)


@coroutine
def default_coroutine():
    while True:
        request = yield
        print('end of chain, no coroutine for {}'.format(request))


class ClientCoroutine:

    def __init__(self):
        self.target = coroutine1(coroutine3(coroutine2(default_coroutine())))

    def delegate(self, requests):
        for request in requests:
            self.target.send(request)


def timeit(func):

    def count(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        count._time = time.time() - start
        return res
    return count


@contextmanager
def suppress_stdout():
    try:
        stdout, sys.stdout = sys.stdout, open(os.devnull, 'w')
        yield
    finally:
        sys.stdout = stdout


if __name__ == "__main__":
    client1 = Client()
    client2 = ClientCoroutine()
    requests = [2, 5, 14, 22, 18, 3, 35, 27, 20]

    client1.delegate(requests)
    print('-' * 30)
    client2.delegate(requests)

    requests *= 10000
    client1_delegate = timeit(client1.delegate)
    client2_delegate = timeit(client2.delegate)
    with suppress_stdout():
        client1_delegate(requests)
        client2_delegate(requests)
    # lets check what is faster
    print(client1_delegate._time, client2_delegate._time)

### OUTPUT ###
# request 2 handled in handler 1
# request 5 handled in handler 1
# request 14 handled in handler 2
# request 22 handled in handler 3
# request 18 handled in handler 2
# request 3 handled in handler 1
# end of chain, no handler for 35
# request 27 handled in handler 3
# request 20 handled in handler 2
# ------------------------------
# request 2 handled in coroutine 1
# request 5 handled in coroutine 1
# request 14 handled in coroutine 2
# request 22 handled in coroutine 3
# request 18 handled in coroutine 2
# request 3 handled in coroutine 1
# end of chain, no coroutine for 35
# request 27 handled in coroutine 3
# request 20 handled in coroutine 2
# (0.2369999885559082, 0.16199994087219238)