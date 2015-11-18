#1)Свойства:
class CardHolder:
    acctlen = 8 # Данные класса
    retireage = 59.5
    def __init__(self, acct, name, age, addr):
        self.acct = acct # Данные экземпляра
        self.name = name # Эти операции вызывают методы записи свойств
        self.age = age # К именам вида __X добавляется имя класса
        self.addr = addr # addr – неуправляемый атрибут
                        # remain – не имеет фактических данных
    def getName(self):
        return self.__name
    def setName(self, value):
        value = value.lower().replace(' ', '_')
        self.__name = value
    name = property(getName, setName)
    def getAge(self):
        return self.__age
    def setAge(self, value):
        if value < 0 or value > 150:
            raise ValueError('invalid age')
        else:
            self.__age = value
    age = property(getAge, setAge)
    def getAcct(self):
        return self.__acct[:-3] + '***'
    def setAcct(self, value):
        value = value.replace('-', '')
        if len(value) != self.acctlen:
            raise TypeError('invald acct number')
        else:
            self.__acct = value
    acct = property(getAcct, setAcct)
    def remainGet(self): # Можно было бы реализовать как
        return self.retireage - self.age # метод, если нигде не используется
    remain = property(remainGet) # как атрибут

#2)Дескрипторы
class CardHolder:
    acctlen = 8 # Данные класса
    retireage = 59.5
    def __init__(self, acct, name, age, addr):
        self.acct = acct # Данные экземпляра
        self.name = name # Эти операции вызывают методы __set__
        self.age = age # Имена вида __X не требуются в дескрипторах
        self.addr = addr # addr – неуправляемый атрибут
                # remain – не имеет фактических данных
    class Name:
        def __get__(self, instance, owner): # Класс имен: локальный для
            return instance.__name # CardHolder
        def __set__(self, instance, value):
            value = value.lower().replace(' ', '_')
            instance.__name = value
    name = Name()
    class Age:
        def __get__(self, instance, owner):
            return instance.__age # Данные дескриптора
        def __set__(self, instance, value):
            if value < 0 or value > 150:
                raise ValueError('invalid age')
            else:
                instance.__age = value
    age = Age()
    class Acct:
        def __get__(self, instance, owner):
            return instance.__acct[:-3] + '***'
        def __set__(self, instance, value):
            value = value.replace('-', '')
            if len(value) != instance.acctlen: # Данные экземпляра
                raise TypeError('invald acct number')
            else:
                instance.__acct = value
    acct = Acct()
    class Remain:
        def __get__(self, instance, owner):
            return instance.retireage - instance.age # Вызовет Age.__get__
        def __set__(self, instance, value):
            raise TypeError('cannot set remain') # При необходимости здесь
    remain = Remain() # можно реализовать операцию
                        #присваивания

#3)getattr(только при обращении к неопределенным аттрибутам)
class CardHolder:
    acctlen = 8 # Данные класса
    retireage = 59.5
    def __init__(self, acct, name, age, addr):
        self.acct = acct # Данные экземпляра
        self.name = name # Эти операции вызывают метод __setattr__
        self.age = age # _acct не искажается: проверяемое имя
        self.addr = addr # addr – неуправляемый атрибут
                        # remain – не имеет фактических данных
    def __getattr__(self, name):
        if name == 'acct': # Вызывается для неопределенных атрибутов
            return self._acct[:-3] + '***' # name, age, addr - определены
        elif name == 'remain':
            return self.retireage - self.age # Не вызывает __getattr__
        else:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name == 'name': # Вызывается всеми операциями присваивания
            value = value.lower().replace(' ', '_') # addr сохраняется непоср.
        elif name == 'age': # acct изменено на _acct
            if value < 0 or value > 150:
                raise ValueError('invalid age')
        elif name == 'acct':
            name = '_acct'
            value = value.replace('-', '')
            if len(value) != self.acctlen:
                raise TypeError('invald acct number')
        elif name == 'remain':
            raise TypeError('cannot set remain')
        self.__dict__[name] = value # Предотвращение зацикливания
        #object.__setattr__(self, name, value) #или так





#4)getattribute(при обращении ко всем аттрибутам. Исключение:
"""при неявном вызове методов пере-
грузки операторов встроенными операциями ни один из методов управления
доступом к атрибутам не участвует в этом процессе: поиск таких атрибутов ин-
терпретатор выполняет в классах, полностью пропуская этап поиска в экзем-
плярах.
"""
class CardHolder:
    acctlen = 8 # Данные класса
    retireage = 59.5
    def __init__(self, acct, name, age, addr):
        self.acct = acct # Данные экземпляра
        self.name = name # Эти операции вызывают метод __setattr__
        self.age = age # acct не искажается: проверяемое имя
        self.addr = addr # addr – неуправляемый атрибут
                        # remain – не имеет фактических данных
    def __getattribute__(self, name):
        superget = object.__getattribute__ # Не зацикливается: на уровень выше
        if name == 'acct': # Вызывается для всех атрибутов
            return superget(self, 'acct')[:-3] + '***'
        elif name == 'remain':
            return superget(self, 'retireage') - superget(self, 'age')
        else:
            return superget(self, name) # name, age, addr: сохраняются
    def __setattr__(self, name, value):
        if name == 'name': # Вызывается всеми операциями присваивания
            value = value.lower().replace(' ', '_') # addr сохраняется непоср.
        elif name == 'age':
            if value < 0 or value > 150:
                raise ValueError('invalid age')
        elif name == 'acct':
            value = value.replace('-', '')
            if len(value) != self.acctlen:
                raise TypeError('invald acct number')
        elif name == 'remain':
            raise TypeError('cannot set remain')
        self.__dict__[name] = value # Предотвращение зацикливания, исх. имена
        #object.__setattr__(self, name, value) #или так


bob = CardHolder('1234-5678', 'Bob Smith', 40, '123 main st')
print(bob.acct, bob.name, bob.age, bob.remain, bob.addr, sep=' / ')
bob.name = 'Bob Q. Smith'
bob.age = 50
bob.acct = '23-45-67-89'
sue = CardHolder('5678-12-34', 'Sue Jones', 35, '124 main st')
print(bob.acct, bob.name, bob.age, bob.remain, bob.addr, sep=' / ')
print(sue.acct, sue.name, sue.age, sue.remain, sue.addr, sep=' / ')

try:
    sue.age = 200
except:
    print('Bad age for Sue')
try:
    sue.remain = 5
except:
    print("Can't set sue.remain")
try:
    sue.acct = '1234567'
except:
    print('Bad acct for Sue')