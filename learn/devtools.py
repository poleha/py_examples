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
            return func # Обертывание только при отладке; иначе
        else: # возвращается оригинальная функция
            import sys
            code = func.__code__
            allargs = code.co_varnames[:code.co_argcount]   #Берем все аргументы функции. Копируем в новый кортеж

            funcname = func.__name__
            def onCall(*pargs, **kargs):
                            # Все аргументы в кортеже pargs сопоставляются с первыми N
                            # ожидаемыми аргументами по позиции
                            # Остальные либо находятся в словаре kargs, либо опущены, как
                            # аргументы со значениями по умолчанию
                positionals = list(allargs)
                given_args = pargs[len(allargs):]   #для обработки переданных *args, 1191
                positionals = positionals[:len(pargs)]  #Получаем из всех аргументов позиционные
                                                        #Считая количество позиционных(*) аргументов, переданных функции
                if not args == None:
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

#Вообще же вот два случая
"""
# С использованием декоратора с аргументами
def rangetest(**argchecks):
    def onDecorator(func):
        def onCall(*pargs, **kargs):
            print(argchecks)
            for check in argchecks: pass # Добавьте проверку сюда
            return func(*pargs, **kargs)
        return onCall
    return onDecorator
@rangetest(a=(1, 5), c=(0.0, 1.0))
def func(a, b, c): # func = rangetest(...)(func)
    print(a + b + c)
func(1, 2, c=3) # Вызовет onCall, argchecks – в области
#видимости объемлющей функции



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
"""