class Root:
    def method_from_root(self):
        print('Root')

class Alpha(Root):
    def method_from_root(self):
        print('Alpha')
        super().method_from_root()


class Beta(Root):
    def method_from_root(self):
        print('Beta')
        super().method_from_root()



class Gamma(Alpha, Beta):
    def method_from_root(self):
        print('Gamma')
        super().method_from_root()



g = Gamma()

g.method_from_root()

