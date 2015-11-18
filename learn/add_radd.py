class Commuter: # Тип класса распространяется на результат
    def __init__(self, val):
        self.val = val
    def __add__(self, other):
        if isinstance(other, Commuter): other = other.val
        return Commuter(self.val + other)
    def __radd__(self, other):
        return Commuter(other + self.val)
    def __str__(self):
        return '<Commuter: %s>' % self.val
x = Commuter(88)
y = Commuter(99)
print(x + 10) # Результат – другой экземпляр класса Commuter
#<Commuter: 98>
print(10 + y)
#<Commuter: 109>
z = x + y # Нет вложения: не происходит рекурсивный вызов __radd__
print(z)
