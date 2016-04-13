class ListInstance:
    """
    Примесный класс, реализующий получение форматированной строки при вызове
    функций print() и str() с экземпляром в виде аргумента, через наследование
    метода __str__, реализованного здесь; отображает только атрибуты
    экземпляра; self – экземпляр самого нижнего класса в дереве наследования;
    во избежание конфликтов с именами атрибутов клиентских классов использует
    имена вида __X
    """
    def __str__(self):
        return '<Instance of %s, address %s:\n%s>' % (
                            self.__class__.__name__, # Имя клиентского класса
                            id(self), # Адрес экземпляра
                            self.__attrnames()) # Список пар name=value
    def __attrnames(self):
        result = ''
        for attr in sorted(self.__dict__): # Словарь атрибутов
            result += '\tname %s=%s\n' % (attr, self.__dict__ [attr])
        return result

class ListInherited:
    """
    Использует функцию dir() для получения списка атрибутов самого экземпляра
    и атрибутов, унаследованных экземпляром от его классов; в Python 3.0
    выводится больше имен атрибутов, чем в 2.6, потому что классы нового стиля
    в конечном итоге наследуют суперкласс object; метод getattr() позволяет
    получить значения унаследованных атрибутов, отсутствующих в self.__dict__;
    реализует метод __str__, а не __repr__, потому что в противном случае
    данная реализация может попасть в бесконечный цикл при выводе связанных
    методов!
    """
    def __str__(self):
        return '<Instance of %s, address %s:\n%s>' % (
                            self.__class__.__name__, # Имя класса экземпляра
                            id(self), # Адрес экземпляра
                            self.__attrnames()) # Список пар name=value
    def __attrnames(self):
        result = ''
        for attr in dir(self): # Передать экземпляр функции dir()
            if attr[:2] == '__' and attr[-2:] == '__': # Пропустить
                result += '\tname %s=<>\n' % attr # внутренние имена
            else:
                result += '\tname %s=%s\n' % (attr, getattr(self, attr))
        return result


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
            genabove = (self.__listclass(c, indent+4)
                            for c in aClass.__bases__)
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


class Cl(ListTree, ListInstance):
    pass

ob = Cl()
ob.tester = 'teeesssttteeerr'
print(ob)