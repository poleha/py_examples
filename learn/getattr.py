class GetAttr:
    eggs = 88 # eggs – атрибут класса, spam – атрибут экземпляра
    def __init__(self):
        self.spam = 77
    def __len__(self): # Реализация операции len, иначе __getattr__
        print('__len__: 42') # будет вызываться с именем __len__
        return 42
    def __getattr__(self, attr): # Возвращает реализацию __str__ по запросу,
        print('getattr: ' + attr) # иначе – функцию-заглушку
        if attr == '__str__':
            return lambda *args: '[Getattr str]'
        else:
            return lambda *args: None


class GetAttribute: # object – требуется в 2.6, подразумевается в 3.0
    eggs = 88 # В 2.6 для всех классов автоматически
    def __init__(self): # выполняется условие isinstance(object)
        self.spam = 77 # Но мы вынуждены наследовать object, чтобы
    def __len__(self): # обрести инструменты, присущие классам нового
        print('__len__: 42') # стиля, включая __getattribute__, и некоторые
        return 42 # атрибуты по умолчанию, с именами вида __X__
    def __getattribute__(self, attr):
        print('getattribute: ' + attr)
        if attr == '__str__':
            return lambda *args: '[GetAttribute str]'
        else:
            return lambda *args: None

for Class in GetAttr, GetAttribute:
    print('\n' + Class.__name__.ljust(50, '='))
    X = Class()
    X.eggs # Атрибут класса
    X.spam # Атрибут экземпляра
    X.other # Отсутствующий атрибут
    len(X) # Метод __len__ определен явно
    try: # Классы нового стиля должны поддерживать [], +, вызов:
        X[0] # __getitem__?
    except:
        print('fail []')
    try:
        X + 99 # __add__?
    except:
        print('fail +')
    try:
        X() # __call__? (неявный вызов, встроенная операция)
    except:
        print('fail ()')
    X.__call__() # __call__? (явный вызов, нет унаследованного метода)
    print(X.__str__()) # __str__? (явный вызов, унаследован от type)
    print(X) # __str__? (неявный вызов, встроенная операция)
