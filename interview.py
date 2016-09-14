"""
def f(x, l=[]):
    for i in range(x):
        l.append(i * i)
    print(l)


f(2)
#[0, 1]

f(3, [3, 2, 1])
#[3, 2, 1, 0, 1, 4]

f(3)
#[0, 1, 2, 4] 0 * 0, 1 * 1, 2 * 2
"""

class A(object):
    def go(self):
        print("go A go!")
    def stop(self):
        print("stop A stop!")
    def pause(self):
        raise Exception("Not Implemented")

class B(A):
    def go(self):
        super(B, self).go()
        print("go B go!")

class C(A):
    def go(self):
        super(C, self).go()
        print("go C go!")
    def stop(self):
        super(C, self).stop()
        print("stop C stop!")

class D(B,C):
    def go(self):
        super(D, self).go()
        print("go D go!")
    def stop(self):
        super(D, self).stop()
        print("stop D stop!")
    def pause(self):
        print("wait D wait!")

class E(B,C): pass

a = A()
b = B()
c = C()
d = D()
e = E()

a.pause()


#d.go()
print('*****4')
# go A go!
# go C go!
# go B go!
# go D go!

"""


class LinkedList(object):
    def __init__(self, num, ref=None):
        self.num = num
        self.ref = ref

    def get_sum(self):

        current_node = self
        s = current_node.num
        while current_node.ref:
            current_node = current_node.ref
            s += current_node.num

        return s

    def add_element(self, node):
        current_node = self
        while current_node.ref:
            current_node = current_node.ref

        current_node.ref = node


node1 = LinkedList(10)
node2 = LinkedList(9, node1)
node3 = LinkedList(8, node2)
node4 = LinkedList(7, node3)

node5 = LinkedList(6)

print(node1.get_sum())
print(node2.get_sum())
print(node3.get_sum())
print(node4.get_sum())

node4.add_element(node5)



print(node4.get_sum())



"""

"""
Параллелизм
Как сохранить целостность многопрточно
https://docs.python.org/2/library/threading.html
https://docs.python.org/3/library/multiprocessing.html


"""





