"""
class empty:
    def __getattr__(self, attrname):        #Только для несуществующих аттрибутов
        if attrname == 'age':
            return 40
        else:
            raise AttributeError(attrname)

X = empty()
print(X.age)
print(X.name)
"""

class accesscontrol:
    def __setattr__(self, attr, value):
        if attr == 'age':
            self.__dict__[attr] = value #если вызвать напрямую, будет бесконечный цикл
        else:
            raise AttributeError(attr + ' not allowed')

X = accesscontrol()
X.age = 40 # Вызовет метод __setattr__
print(X.age)
X.name = 'mel'