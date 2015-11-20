class A:
    def test(self):
        print('A')


class B(A):
    def test(self):
        print('B')
        super().test()


class C(B):
    def test(self):
        print('C')
        super().test()


class D(B, C):
    def test(self):
        print('D')
        super().test()

#TypeError: Cannot create a consistent method resolution
#order (MRO) for bases B, C