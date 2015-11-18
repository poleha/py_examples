class Set:
    def __init__(self, value = []): # Конструктор
        self.data = [] # Управляет списком
        self.concat(value)
    def intersect(self, other): # other – любая последовательность
        res = [] # self – подразумеваемый объект
        for x in self.data:
            if x in other: # Выбрать общие элементы
                res.append(x)
        return Set(res) # Вернуть новый экземпляр Set
    def union(self, other): # other – любая последовательность
        res = self.data[:] # Копировать список
        for x in other: # Добавить элементы из other
            if not x in res:
                res.append(x)
        return Set(res)
    def concat(self, value): # Аргумент value: список, Set...
        for x in value: # Удалить дубликаты
            if not x in self.data:
                self.data.append(x)

a = Set()
