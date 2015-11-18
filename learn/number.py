class Number:
    def __init__(self, start): # Вызов Number(start)
        self.data = start
    def __sub__(self, other): # Выражение: экземпляр - other
        return Number(self.data - other) # Результат – новый экземпляр

if __name__=='__main__':
    X = Number(5) # Number.__init__(X, 5)
    Y = X - 2 # Number.__sub__(X, 2)
    Y.data # Y - новый экземпляр класса Number
    #3
