# classtree.py
"""
Выполняет обход дерева наследования снизу вверх, используя ссылки на пространства
имен, и отображает суперклассы с отступами
"""
def classtree(cls, indent):
    print('.' * indent + cls.__name__) # Вывести имя класса
    for supercls in cls.__bases__: # Рекурсивный обход всех суперклассов
        classtree(supercls, indent+3) # Каждый суперкласс может быть посещен
                                        # более одного раза
def instancetree(inst):
    print('Tree of', inst) # Показать экземпляр
    classtree(inst.__class__, 3) # Взойти к его классу

def selftest():
    class A: pass
    class B(A): pass
    class C(A): pass
    class D(B,C): pass
    class E: pass
    class F(D,E): pass
    instancetree(B())
    instancetree(F())
if __name__ == '__main__': selftest()
