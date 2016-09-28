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