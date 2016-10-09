class Spam:
    egg = 1
    def test(self, val):
        self.egg += val

ob = Spam()
ob.test(3)
print(ob.egg) #4 !!! ВНИМАНИЕ
print(Spam.egg) #1