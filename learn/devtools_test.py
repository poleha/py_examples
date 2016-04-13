# Файл devtools_test.py
# Закомментированные строки возбуждают исключение TypeError, если сценарий
# не был запущен командой “python -O”
from devtools import rangetest
# Тест вызовов функций с позиционными и именованными аргументами
@rangetest(age=(0, 120)) # persinfo = rangetest(...)(persinfo)
def persinfo(name, age):
    print('%s is %s years old' % (name, age))
@rangetest(M=(1, 12), D=(1, 31), Y=(0, 2009))
def birthday(M, D, Y):
    print('birthday = {0}/{1}/{2}'.format(M, D, Y))

persinfo('Bob', 40)
persinfo(age=40, name='Bob')
birthday(5, D=1, Y=1963)
#persinfo('Bob', 150)
#persinfo(age=150, name='Bob')
#birthday(5, D=40, Y=1963)
# Тест вызовов методов с позиционными и именованными аргументами
class Person:
    def __init__(self, name, job, pay):
        self.job = job
        self.pay = pay
            # giveRaise = rangetest(...)(giveRaise)
    @rangetest(percent=(0.0, 1.0)) # Аргумент percent передается по имени
    def giveRaise(self, percent): # или по позиции
        self.pay = int(self.pay * (1 + percent))

bob = Person('Bob Smith', 'dev', 100000)
sue = Person('Sue Jones', 'dev', 100000)
bob.giveRaise(.10)
sue.giveRaise(percent=.20)
print(bob.pay, sue.pay)
#bob.giveRaise(1.10)
#bob.giveRaise(percent=1.20)
# Тест вызовов функций с опущенными аргументами по умолчанию
@rangetest(a=(1, 10), b=(1, 10), c=(1, 10), d=(1, 10))
def omitargs(a, b=7, c=8, d=9):
    print(a, b, c, d)

omitargs(1, 2, 3, 4)
omitargs(1, 2, 3)
omitargs(1, 2, 3, d=4)
omitargs(1, d=4)
omitargs(d=4, a=1)
omitargs(1, b=2, d=4)
omitargs(d=8, c=7, a=1)
#omitargs(1, 2, 3, 11) # Недопустимое значение аргумента d
#omitargs(1, 2, 11) # Недопустимое значение аргумента c
#omitargs(1, 2, 3, d=11) # Недопустимое значение аргумента d
#omitargs(11, d=4) # Недопустимое значение аргумента a
#omitargs(d=4, a=11) # Недопустимое значение аргумента a
#omitargs(1, b=11, d=4) # Недопустимое значение аргумента b
#omitargs(d=8, c=7, a=11) # Недопустимое значение аргумента a

@rangetest(a=(1, 5), args =(2, 4))
def myf(a, *args):
    c = 3
    print(a, args[0])

myf(2, 3, 3, 4, 5)

