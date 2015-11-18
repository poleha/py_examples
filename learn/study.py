"""
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<ЗАДАЧИ
https://docs.djangoproject.com/en/1.7/topics/class-based-views/generic-editing/
Переделать на правильные формы

***
class classonlymethod(classmethod):
***

TemplateResponse

**
post.models
  def save(self, *args, **kwargs):
        # For automatic slug generation.
        if not self.slug:
            self.slug = slugify(self.title)[:50]

        return super(Post, self).save(*args, **kwargs)
**


**
settings.py
**
модуль allauth
**
Еще раз про property


descriptors
http://users.rcn.com/python/download/Descriptor.htm

Разобрать, как это работает:
#from django.template import RequestContext, loader
django.template - template system, это приложение. Оно содержит в себе модуль loader и класс RequestContext

Разобрать код
class ModelBase(type): в base.py

if __name__ == "__main__":

packages
https://www.djangopackages.com

authentification
https://www.djangopackages.com/packages/p/django-tastypie/


Наследование шаблонов
http://habrahabr.ru/post/23132/
**********************************************************************



 ЗАДАЧИ>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Книга Learning Python 4-е издание
[461-468]
[505-509]

*******************
Функции
Глава 6 - ссылки
a = a[:] - копирование объекта

lambda?
yield?
global?
nonlocal?
*******************

Кортеж, список, словарь


*********************
Итераторы

*********************

Книга Learning Python 4-е издание>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


Проверка существования переменной
http://webonrails.ru/post/274/
Проверка существования ключа в словаре способ #1

if key in dictname:
   # key exists in dictname

Проверка существования переменной в локальной видимости

if 'myVar' in locals():
  # myVar exists

Проверка существования переменной в глобальной видимости

if 'myVar' in globals():
  # myVar exists

Проверка существования переменной используя исключения

try:
    myVar
except NameError:
    myVar = None

Проверка существования ключа в словаре способ #2

try:
    dictname['key']
except KeyError:
    dictname['key'] = None

Проверка существования индекса в списке

try:
    dictname['1']
except IndexError:
    dictname['1'] = None

Проверка наличия метода, свойства в объекте

if hasattr(obj, 'attr_name'):
  # obj.attr_name exists

<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<ДЕКОРАТОРЫ

Декораторы — это, по сути, просто своеобразные «обёртки», которые дают нам возможность делать что-либо до и
после того, что сделает декорируемая функция, не изменяя её.
http://habrahabr.ru/post/141411/
http://habrahabr.ru/post/141501/

def makebold(fn):
    def wrapped():
        return "<b>" + fn() + "</b>"
    return wrapped

def makeitalic(fn):
    def wrapped():
        return "<i>" + fn() + "</i>"
    return wrapped

@makebold
@makeitalic
def hello():
    return "hello habr"

print hello() ## выведет <b><i>hello habr</i></b>


Программируем декоратор decorator

def my_decorator(func_to_wrap):
    def decorated_function():
        print("addition_before")
        func_to_wrap()
        print ("addition_after")

    return decorated_function

@my_decorator
def stand_alone_function():
    print("stand_alone")

#my_decorator(stand_alone_function)() - аналог

stand_alone_function()


#****
И еще пример декоратора, функция - счетчик количества вызовов функции


def counter(func): #сам декоратор
    def wrapper(*args,**kwargs):    #обертка. Декоратор возвращает именно ее. Вопрос: где декоратор берет
    #  *args,**kwargs, если они - часть функции func. Ответ простой. Как видно из примера без конструкции @
    # fun = counter(fun), где counter(fun) возвращает wrapper. То есть fun это уже ссылка на функцию wrapper
        print(args)                 #выводим аргументы, переданные обертке при выполнении обертки
        wrapper.count = wrapper.count + 1   #к свойству обертки при выполнении обертки прибавляется 1
        return func(*args,**kwargs) #возвращаем исходную функцию со всеми аргументами
    wrapper.count = 0 # при единственном вызове декоратора присваиваем обертке свойство count = 0
    return wrapper  #возвращаем обертку


@counter
def fun(x):
    print(x)

fun("a")
fun("b")
fun("c")
print(fun.count)



def fun(x):
    print(x)
fun = counter(fun)

fun("a")
fun("b")
fun("c")
fun("d")
print(fun.count)
#***

def decorator_maker_with_arguments(decorator_arg1, decorator_arg2):

    print("Я создаю декораторы! И я получил следующие аргументы:", decorator_arg1, decorator_arg2)

    def my_decorator(func):
        print("Я - декоратор. И ты всё же смог передать мне эти аргументы:", decorator_arg1, decorator_arg2)

        # Не перепутайте аргументы декораторов с аргументами функций!
        def wrapped(function_arg1, function_arg2) :
            print("Я - обёртка вокруг декорируемой функции.\n"
                  "И я имею доступ ко всем аргументам: \n"
                  "\t- и декоратора: {0} {1}\n"
                  "\t- и функции: {2} {3}\n"
                  "Теперь я могу передать нужные аргументы дальше"
                  .format(decorator_arg1, decorator_arg2,
                          function_arg1, function_arg2))
            return func(function_arg1, function_arg2)

        return wrapped

    return my_decorator


@decorator_maker_with_arguments("Леонард", "Шелдон")
def decorated_function_with_arguments(function_arg1, function_arg2):
    print ("Я - декорируемая функция и я знаю только о своих аргументах: {0}"
           " {1}".format(function_arg1, function_arg2))

decorated_function_with_arguments("Раджеш", "Говард")

#Иначе говоря
#fun1 = my_decorator(func)
#my_decorator(func) имеет доступ к переменным вызвавшей ее функции decorator_arg1, decorator_arg2
#fun2 = wrapped(function_arg1, function_arg2), но она имеет доступ к к переменным вызвавшей ее функции
#decorator_arg1, decorator_arg2
#fun2(function_arg1, function_arg2) имеет тоступ как к своим аргументам, так и к аргументам вывзавшей ее функции
# выведет:
# Я создаю декораторы! И я получил следующие аргументы: Леонард Шелдон
# Я - декоратор. И ты всё же смог передать мне эти аргументы: Леонард Шелдон
# Я - обёртка вокруг декорируемой функции.
# И я имею доступ ко всем аргументам:
#   - и декоратора: Леонард Шелдон
#   - и функции: Раджеш Говард
# Теперь я могу передать нужные аргументы дальше
# Я - декорируемая функция и я знаю только о своих аргументах: Раджеш Говард

#****


#Напишем самостоятельно конструктор декоратора с агрументами

def decorator_maker(maker_arg):
    def decorator(func):
        def wrapper(function_arg):
            print(maker_arg)
            func(function_arg)
        return wrapper
    return decorator

#@decorator_maker("maker_arg") - alt
fun1 = decorator_maker("maker_arg") #фактически это значит, что fun1 ссылается на decorator(func), но этот
#decorator(func) имеет доступ к maker_arg.

def simple_func(function_arg):
    print(function_arg)

fun2 = fun1(simple_func) # выполняем декоратор, поучая функцию wrapper, имеющую аргументы maker_arg. Profit.
fun2("func_arg") # выполняем функцию fun2("func_arg"), которая ссылается на wrapper, имеющий доступ к maker_arg


#simple_func("func_arg") - alt




****************************8
#А попробуем обернуть декоратором декоратор
#Сам писал!
#1191

def decorator_for_decorator(orig_decorator):
    def decorator_maker(*args,**kwargs):
        def decorator_wrapper(func):
            #тут мы декорируем декоратор и выполняем его
            return orig_decorator(func,args,kwargs)
            #7)Он возвращет результат выполнения orig_decorator(func = original_func,args = 5, kwargs)
        return decorator_wrapper
        #5)Она возвращает decorator_wrapper с доступом к orig_decorator = original_decorator и args = 5
    return decorator_maker
    #2)Она возвращает decorator_maker с доступом к orig_decorator = original_decorator


@decorator_for_decorator
#1)Выполням функцию decorator_for_decorator(original_decorator)
#3)Получаем original_decorator = decorator_maker
def original_decorator(func,*args,**kwargs):
    print(args)
    return func
    #8)Так исходный декоратор получае доступ к args = 5, выводит их(тем самым декорирует функцию) и возвращает
    #func = original_func


@original_decorator(5)
#4)Выполняем decorator_maker(5)
#6)выполняем decorator_wrapper(original_func)
#9)Получаем что original_func = original_func, но мы ее задекорировали, выведя print(args) в декораторе
def original_func(a,b):
    print(a+b)


original_func(1,2)

ДЕКОРАТОРЫ>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

"""


"""

***********************************************************************




<<<<<<<<<<<<<СПИСОК КЛАССОВ
**
class Model(**kwargs)
https://docs.djangoproject.com/en/1.7/ref/models/instances/#django.db.models.Model
https://docs.djangoproject.com/en/1.7/topics/db/models/
A model is the single, definitive source of information about your data. It contains
the essential fields and behaviors of the data you’re storing. Generally, each model maps to a single database table.
**



**
class QuerySet([model=None, query=None, using=None])
https://docs.djangoproject.com/en/1.7/ref/models/querysets/#django.db.models.query.QuerySet
Набор моделей, выдаваемый, как правило, менеджером модели методами типа filter, exclude
**

**
class Manager - класс для создания запросов. Имеет методы filter, exclude. Основной источкик QuerySet
https://docs.djangoproject.com/en/1.7/topics/db/managers/#django.db.models.Manager
**


**
class RelatedManager
https://docs.djangoproject.com/en/1.7/ref/models/relations/,
через который можно получить разные QuerySets подчиненных моделей, в зависимости от
        фильтра, порядка итд
**


**
class django.views.generic.detail.DetailView
https://docs.djangoproject.com/en/1.7/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView
While this view is executing, self.object will contain the object that the view is operating upon
**

**
django.views.generic.list.ListView
https://docs.djangoproject.com/en/1.7/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView
A page representing a list of objects.
**

**
class HttpResponse
https://docs.djangoproject.com/en/1.7/ref/request-response/#django.http.HttpResponse
In contrast to HttpRequest objects, which are created automatically by Django,
HttpResponse objects are your responsibility. Each view you write is responsible for instantiating, populating
and returning an HttpResponse.
Это то, что создают view. html, выводимый на страницу
**

**
class HttpRequest
https://docs.djangoproject.com/en/1.7/ref/request-response/#django.http.HttpRequest
Параметры запроса
Например
HttpRequest.GET
HttpRequest.POST
**

**
class HttpResponseRedirect
 Always return an HttpResponseRedirect after successfully dealing
 with POST data. This prevents data from being posted twice if a
 user hits the Back button.
Возвращаем код 302(страница изменена) после обработки post-даты
**

**
class django.template.Context
Context как правило получает словарь, который передает в template system
**

**
А RequestContext - это суб-класс django.template.Context, отличается тем, что
1) Принимает HttpRequest в качестве первого параметра;
2) The second difference is that it automatically populates the context with a few variables,
according to your TEMPLATE_CONTEXT_PROCESSORS setting.
По умолчанию это кортеж:
("django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.tz",
"django.contrib.messages.context_processors.messages")

То есть этот класс не просто выдает текст, а передает в template system еще дополнительные переменные
**


**
class django.http.Http404
When you return an error such as HttpResponseNotFound, you’re responsible for defining the HTML of the resulting error page:

return HttpResponseNotFound('<h1>Page not found</h1>')
For convenience, and because it’s a good idea to have a consistent 404 error page across your site,
Django provides an Http404 exception. If you raise Http404 at any point in a view function, Django will catch it
and return the standard error page for your application, along with an HTTP error code 404.
**

СПИСОК КЛАССОВ>>>>>>>>>>>>>>>>>>>>>>>



**********************************************************************
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<ДОКУМЕНТАЦИЯ

full api reference
https://docs.djangoproject.com/en/1.7/ref/

Модели
https://docs.djangoproject.com/en/1.7/topics/db/models/



Поля
https://docs.djangoproject.com/en/1.7/ref/models/fields/#django.db.models.DateTimeField

Создание запросов
https://docs.djangoproject.com/en/1.7/topics/db/queries/

QuerySet
https://docs.djangoproject.com/en/1.7/ref/models/querysets/#django.db.models.query.QuerySet


Manager
https://docs.djangoproject.com/en/1.7/topics/db/managers/#django.db.models.Manager


Предопределенные view(class based)
!!!!!!!!!!!!!!!!!!!!!https://docs.djangoproject.com/en/1.7/topics/class-based-views/intro/
https://docs.djangoproject.com/en/1.7/ref/class-based-views/base/#django.views.generic.base.View.as_view
https://docs.djangoproject.com/en/1.7/topics/class-based-views/generic-display/
https://docs.djangoproject.com/en/1.7/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView

Shortcuts
https://docs.djangoproject.com/en/1.7/topics/http/shortcuts/

Request and Response objects
https://docs.djangoproject.com/en/1.7/ref/request-response/#django.http.HttpResponse
https://docs.djangoproject.com/en/1.7/ref/request-response/#module-django.http

*************************************************************
Template system
https://docs.djangoproject.com/en/1.7/ref/templates/api/#django.template.RequestContext  - для программистов
+https://docs.djangoproject.com/en/1.7/topics/templates/ - просто
http://www.djangobook.com/en/2.0/chapter04.html#cn317

https://docs.djangoproject.com/en/1.7/ref/templates/builtins/#ref-templates-builtins-filters - фильтры
https://docs.djangoproject.com/en/1.7/ref/templates/builtins/#ref-templates-builtins-tags  -tags
http://habrahabr.ru/post/23132/ - шаблоны джанго, наследование
http://habrahabr.ru/blog/php/38628.html -фрагментарное кеширование

*************************************************************
urls.py
https://docs.djangoproject.com/en/1.7/ref/urls/
*************************************************************
admin docs
https://docs.djangoproject.com/en/1.7/ref/contrib/admin/
https://docs.djangoproject.com/en/1.7/ref/contrib/admin/admindocs/
*************************************************************
Users
https://docs.djangoproject.com/en/1.7/topics/auth/default/
https://docs.djangoproject.com/en/1.7/ref/contrib/auth/#django.contrib.auth.models.User
***********************************************************
Защита форм от взлома
https://docs.djangoproject.com/en/1.7/ref/contrib/csrf/
***************************************************************

ДОКУМЕНТАЦИЯ>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

"""


"""
#!/usr/bin/env python
import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kulik.settings")

import django
django.setup()
"""
"""
from polls.models import Question, Choice
q = Question.objects
#c = q.choice_set.all() # Returns all Entry objects related to Blog.
#print(c)
print(q.__class__)

#q.entry_set is a Manager that returns QuerySets.

z =  Question.objects.get(id=1).choice_set #.filter(choice_text__contains=' ')
print(z.__class__)
"""

"""
#*****************************************************
Объект передается по ссылке, а переменная по значению(не совсем так, но суть в том, что переменная не меняется)
class A():
    def __init__(self):
        self.k = 1

def change_val(ob):
    ob.k = 2
z = A()

change_val(z)
print(z.k)  #2

a=1
def change_var(var):
    var = 2

change_var(a)
print(a)    #1


a=1
def change_var():
    global a
    a=2

change_var(a)
print(a)    #2
#**************************************************************************************
"""

#***************************
"""
Свойства и методы метода класса
"""
"""
class A():
    class_attr_a = "class_attr_a"
    class_attr_a_only = "class_attr_a_only"
    def __init__(self):
        self.lost_attr_a = "LA"
        self.attr_a = "attr_a"

class B(A):
    class_attr_a = "class_attr_b"
    class_attr_b = "class_attr_b"
    def __init__(self):
        self.attr_a = "attr_a_b"
        self.attr_b = "attr_b"

    def fun(self):
        print("fun")
    fun.fun_attr = "fun_attr"

ob = B()
print(ob.attr_a)    #attr_a_b - __init__ суперкласса не вызываестся, если был переопределен
#print(ob.lost_attr_a) error, нужен super()
print(ob.class_attr_a)  #class_attr_b  - был переопределен в __init__класса B
print(ob.class_attr_b)  #class_attr_b - занятно, что аттрибуты класса доступны экземпляру
print(ob.fun.fun_attr) #fun_attr - это свойство метода класса, Доступно и для экземпляра
#print(A.attr_a) error назначен экземпляру, а не классу
print(B.class_attr_a) #class_attr_b свойство класса переопределено
print(B.class_attr_b) #class_attr_b
print(B.class_attr_a_only) #class_attr_a_only  не переопределенное свойство суперкласса доступно
print(ob.fun.fun_attr)  #fun_attr
ob.fun() #fun
B.fun(ob) #fun
"""
#****************************************
"""
super
Вызывает функцию суперкласса
class A():
    def __init__(self):
        self.attr_a = 'attr_a'
    def func(self):
        print("func_a")

class B(A):
    def __init__(self):
        super().__init__()  #позволяет не заменить фнкцию, а дополнить. То есть вызывает функцию суперкласса
        self.attr_b = 'attr_b'
    def func(self):
        super().func()
        print("func_b")

ob = B()
print(ob.attr_a) #without super() error
print(ob.attr_b)

ob.func()
#func_a
#func_b

"""
"""
Ссылка на объект. Оба обе ссылки(ob1 и ob2) ссылаются на один объект.
Когда мы удаляем одну из ссылок, вторая остается.
class A():
    pass

ob1 = A()
ob2 = ob1

ob1.attr = 1;
ob2.attr = 2;
print(ob2.attr) #2
print(ob1.attr) #2
del ob1
print(ob2.attr) #2
#print(ob1.attr) - error
"""


#Метакласы
#********************
# Использование type
"""
def print_atrr():
    print('Ить')

MyClass = type('MyClass',(),{'print_attr':print_atrr})
MyClass.print_attr()
"""
#********************
#Аттрибут __metaclass__ так по умолчанию
"""
class MyClass(metaclass = type):
    pass

ob = MyClass()
print(ob)
"""
#**************
#Атрибут метакласс, расширенное использование, функция
"""
def metaclass_creator(cls,accessors,attribs):
    print(cls)
    return type(cls,accessors,attribs)



class MyClass(metaclass=metaclass_creator):
    bar  = 'bip'

ob = MyClass()
print(ob)
"""


"""
Выучить, переписать и в 1191
http://stackoverflow.com/questions/100003/what-is-a-metaclass-in-python/6581949#6581949
# remember that `type` is actually a class like `str` and `int`
# so you can inherit from it
class UpperAttrMetaclass(type):
      # __new__ is the method called before __init__
    # it's the method that creates the object and returns it
    # while __init__ just initializes the object passed as parameter
    # you rarely use __new__, except when you want to control how the object
    # is created.
    # here the created object is the class, and we want to customize it
    # so we override __new__
    # you can do some stuff in __init__ too if you wish
    # some advanced use involves overriding __call__ as well, but we won't
    # see this
    def __new__(upperattr_metaclass, future_class_name,
                future_class_parents, future_class_attr):
        uppercase_attr = {}
        for name, val in future_class_attr.items():
            if not name.startswith('__'):
                uppercase_attr[name.upper()] = val
            else:
                uppercase_attr[name] = val

        #return type(future_class_name, future_class_parents, uppercase_attr)
        return type.__new__(upperattr_metaclass, future_class_name,
                            future_class_parents, uppercase_attr)
      #return super(UpperAttrMetaclass, cls).__new__(cls, clsname, bases, uppercase_attr)

class MyClass(metaclass = UpperAttrMetaclass):
    spam = 'bar'


"""



"""
Упаковка, распаковка
class Parent():
    def test(self,a,b,c,d,arg1,arg2,*args,**kwargs): #
        print('Hi, this is Parent',self.__class__,a,b,c,arg1)



class Child(Parent):
    def test(self,*args,**kwargs):
        print('Hi, this is Child',self.__class__,args,kwargs)
        super().test(*args,**kwargs)



#Когда мы объявляем функцию, которая принимает *args и **kwargs, мы говорим о том, что эта функция примет любое
#количество позиционных и именных элементов.
#1) Когда мы передаем *кортеж в качестве аргумента функции, это значит что этот кортеж будет распакован функцией в
#позиционные переменные. Когда мы передаем в *словарь больше аргументов, чем требует функция, лишние аргументы остаются
#нераспакованы
#2) Когда мы передает **словарь в качестве аргумента функции, это значит, что словарь будет распакован в именные переменные,
#если они есть в функции. Если в функции их нет, то они так и останутся нераспакованными, в словаре
#3) Когда мы передаем в *словарь больше аргументов, чем требует функция, лишние аргументы остаются нераспакованы
ob = Child()
ob.test(1,2,3,4,5,arg1=14,arg2=15,k=3)
"""






#****************************************
from functools import wraps, update_wrapper, WRAPPER_ASSIGNMENTS
from django.utils import six
from django.utils.decorators import available_attrs
from functools import wraps
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.utils.decorators import available_attrs
from django.utils.encoding import force_str
from django.utils.six.moves.urllib.parse import urlparse
from django.shortcuts import resolve_url
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest


def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """
    #Наконец-то получаем декоратор. Его возвращаем. В него будет передана наша функция
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func)) #применяем update_wrapper чтобы функция
        # def dummy(*args, **kwargs): выглядела как... непонятно
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            # urlparse chokes on lazy objects in Python 3, force to str
            resolved_login_url = force_str(
                resolve_url(login_url or settings.LOGIN_URL))
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator
    #Декоратор вернули, но потом его сразу же получает декоратор декоратора method_decorator. Цель -
    #Сделать, чтобы декоратор понимал первый аргумент self

def permission_required(perm, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    #Это декоратор-мейкер.

    def check_perms(user):
        #Эта функция проверяет, есть ли у пользователя определенные полномочия
        if not isinstance(perm, (list, tuple)):
            perms = (perm, )
        else:
            perms = perm
        # First check if the user has the permission (even anon users)
        if user.has_perms(perms):
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return user_passes_test(check_perms, login_url=login_url)
    #Декоратор-мейкер возвращает результат выполнения другого декоратор-мейкера, передав в него определенную тут же
    #функцию check_perms


def method_decorator(decorator):
    """
    Converts a function decorator into a method decorator
    """
    # 'func' is a function at the time it is passed to _dec, but will eventually
    # be a method of the class it is defined it.
    def _dec(func):
        def _wrapper(self, *args, **kwargs):
            @decorator
            def bound_func(*args2, **kwargs2):
                return func.__get__(self, type(self))(*args2, **kwargs2)
        # bound_func has the signature that 'decorator' expects i.e.  no
        # 'self' argument, but it is a closure over self so it can call
        # 'func' correctly.
            return bound_func(*args, **kwargs)
        # In case 'decorator' adds attributes to the function it decorates, we
        # want to copy those. We don't have access to bound_func in this scope,
        # but we can cheat by using it on a dummy function.

        @decorator
        def dummy(*args, **kwargs):
            pass
        update_wrapper(_wrapper, dummy)
        # Need to preserve any existing attributes of 'func', including the name.
        update_wrapper(_wrapper, func)

        return _wrapper

    update_wrapper(_dec, decorator, assigned=available_attrs(decorator))
    #Change the name to aid debugging.
    if hasattr(decorator, '__name__'):
        _dec.__name__ = 'method_decorator(%s)' % decorator.__name__
    else:
        _dec.__name__ = 'method_decorator(%s)' % decorator.__class__.__name__
    return _dec
#Обернули исходный декоратор decorator, чтобы он превратился в def _dec(func):

#МОЕ 1191
def dec_for_dec(dec):
    def func_wrapper(func):
        def new_func(self,*args,**kwargs):
            @dec
            def decorated_func(*args2,**kwargs2):
                return func.__get__(self,type(self))(*args2,**kwargs2)
            return decorated_func(*args,**kwargs)
        return new_func
    return func_wrapper


class Tester():
    @dec_for_dec(permission_required('posts.add_comment'))
    def test(self,request):
        print('test')


request = HttpRequest()
request.user = User.objects.get(pk=3)
ob = Tester()
ob.test(request)
#****************************************




#**************************************************<<<<<<<<<<<<<<<<Дескрипорты
#http://www.ibm.com/developerworks/library/os-pythondescriptors/
#Способ 1:
"""
class Descriptor(object):

    def __init__(self):
        self._name = ''

    #Получается, что любое свойство класса - это экземпляр класса-дескриптора
    #

    def __get__(self, instance, owner):
        print("Getting: %s" % self._name)
        #self - name, экземпляр класса Descriptor
        #instance - user, экземпляр класса Person
        #owner - класс Person
        return self._name       #вариант - instance, тогда свойство будет храниться в

    def __set__(self, instance, name):
        #self - name, экземпляр класса Descriptor
        #instance - user, экземпляр класса Person
        #name - {str}'john smith', значение, присваиваемое сеттером
        print("Setting: %s" % name)
        self._name = name.title()   #функция для превращения первой буквы каждого слова в заглавную

    def __delete__(self, instance):
        #self - name, экземпляр класса Descriptor
        #instance - user, экземпляр класса Person
        print("Deleting: %s" %self._name)
        del self._name

class Person(object):
    name = Descriptor()

"""
#Способ 2
"""

class Person(object):
    def __init__(self):
        self._name = ''

    def fget(self):
        print("Getting: %s" % self._name)
        return self._name

    def fset(self, value):
        print("Setting: %s" % value)
        self._name = value.title()

    def fdel(self):
        print("Deleting: %s" %self._name)
        del self._name
    name = property(fget, fset, fdel, "I'm the property.")
    #Мы фактически говорим, что name = экземпляр класса-дескриптора property, с соответствующими функциями. То есть это
    #не функции - методы класса Person, это как бы функции для дескриптора
"""

#Способ 3, с декоратором
"""
class Person(object):

    def __init__(self):
        self._name = ''

    @property
    def name(self):
        print("Getting: %s" % self._name)
        return self._name

    @name.setter
    def name(self, value):
        print("Setting: %s" % value)
        self._name = value.title()

    @name.deleter
    def name(self):
        print(">Deleting: %s" % self._name)
        del self._name
"""
"""
user = Person()
user.name = 'john smith'
print(user.name)
del user.name
"""

#И еще пример, использование data descriptor
"""
class Person(object):

    def addProperty(self, attribute):
        # create local setter and getter with a particular attribute name
        getter = lambda self: self._getProperty(attribute)
        #getter = лямбда - функция, получающая экземпляр класса и возвращающая self._getProperty(attribute)
        setter = lambda self, value: self._setProperty(attribute, value)

        # construct property attribute and add it to the class
        setattr(self.__class__, attribute, property(fget=getter, \
                                                    fset=setter, \
                                                    doc="Auto-generated method"))
        #Создаем аттрибут - свойство, который создаст аттрибут с именем attribute и значением property

    def _setProperty(self, attribute, value):
        print("Setting: %s = %s" %(attribute, value))
        setattr(self, '_' + attribute, value.title())
        #функция получает имя аттрибута и значение и устанавливает этому аттрибуту это значение
        #То есть мы добавим объекту user аттрибут _attribute и установим ему значение = value.title()

    def _getProperty(self, attribute):
        print("Getting: %s" %attribute)
        return getattr(self, '_' + attribute)
"""


#***************************************************Дескрипторы>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#***************************************<<<<<<<<<<____свойства и методы
#__dict__

#Special method names
#https://docs.python.org/3.3/reference/datamodel.html#customization

#Special Attributes
#https://docs.python.org/3.3/library/stdtypes.html#special-attributes
"""
The implementation adds a few special read-only attributes to several object types, where they are relevant. Some of these are not reported by the dir() built-in function.

object.__dict__
A dictionary or other mapping object used to store an object’s (writable) attributes.

instance.__class__
The class to which a class instance belongs.

class.__bases__
The tuple of base classes of a class object.

class.__name__
The name of the class or type.

class.__qualname__
The qualified name of the class or type.

New in version 3.3.

class.__mro__
This attribute is a tuple of classes that are considered when looking for base classes during method resolution.

class.mro()
This method can be overridden by a metaclass to customize the method resolution order for its instances. It is called at class instantiation, and its result is stored in __mro__.

class.__subclasses__()

"""

#******************************************____свойства и методы>>>>>>>>>>>>>>>>>>>


#Как работает класс Property, упрощенная схема(моя)
#Оригинал тут https://docs.python.org/3/howto/descriptor.html
#1191
#For objects, the machinery is in object.__getattribute__() which transforms b.x into type(b).__dict__['x'].__get__(b, type(b))

class MyProperty(object):

    def __init__(self,getter=None,setter=None,deleter=None):
        self.getter = getter
        self.setter = setter
        self.deleter = deleter

    def __get__(self, instance, owner=None):    #self - экземпляр дескриптора, instance - объект, которому при
        #надлежит экземпляр
        return self.getter(instance)

    def __set__(self, instance, value):
        return self.setter(instance,value)

    def __delete__(self,instance):
        return self.deleter(instance)



class MyPerson(object):
    def __init__(self):
        self._name = ''

    def getter(self):
        return self._name

    def setter(self,value):
        self._name = value.title()

    def deleter(self):
        del self._name

    name = MyProperty(getter,setter,deleter)


person = MyPerson()
#person.setter('alex')  - без проперти
#print(person.getter()) - без проперти

person.name = 'alex'
print(person.name)
print(person.__dict__)
print(person.__class__.__dict__)
print(type(person).__dict__)




























