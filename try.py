class A:
    def test(self):
        print('A')
        super().test()

class C:
    def test(self):
        print('C')
        #super().test() - error


class B(C):
    def test(self):
        print('B')
        super().test()


class D(A, B):
    def test(self):
        print('D')
        super().test()
        #super().test(self) - error, super() returns bound method

ob = D()
ob.test()

print('*****************')


class A:
    def test(self):
        print('A')


class B(A):
    def test(self):
        print('B')
        super(B, self).test()


class C(A):
    def test(self):
        print('C')
        super(C, self).test()

class D(B, C):
    def test(self):
        print('D')
        super(D, self).test()

d = D()
d.test()