class Node:
    def __init__(self,initdata):
        self.data = initdata
        self.next = None

    def getData(self):
        return self.data

    def getNext(self):
        return self.next

    def setData(self,newdata):
        self.data = newdata

    def setNext(self,newnext):
        self.next = newnext


class UnorderedList:

    def __init__(self):
        self.head = None
        self.tail = None

    def isEmpty(self):
        return self.head is None

    def add(self,item):
        temp = Node(item)
        temp.setNext(self.head)
        self.head = temp

        if self.tail is None:
            self.tail = temp

    """
    O(n)
    def append(self, item):
        previous = None
        current = self.head
        while current != None:
            previous = current
            current = current.getNext()

        node = Node(item)
        if previous is None:
            current.next = node
        else:
            previous.next = node
    """

    # O(1)
    def append(self, item):
        node = Node(item)
        self.tail.next = node
        self.tail = node
        #print(self.tail.getData(), self.tail.getNext().getData())



    def size(self):
        current = self.head
        count = 0
        while current != None:
            count = count + 1
            current = current.getNext()

        return count

    def search(self,item):
        current = self.head
        found = False
        while current != None and not found:
            if current.getData() == item:
                found = True
            else:
                current = current.getNext()

        return found

    def remove(self,item):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.getData() == item:
                found = True
            else:
                previous = current
                current = current.getNext()

        if previous is None:
            self.head = current.getNext()
        else:
            previous.setNext(current.getNext())

        if self.tail == current:
            if previous:
                self.tail = previous
            else:
                self.tail = self.head

mylist = UnorderedList()

mylist.add(31)
mylist.add(77)
mylist.add(17)
mylist.add(93)
mylist.add(26)
mylist.add(54)

print(mylist.size())
print(mylist.search(93))
print(mylist.search(100))

mylist.add(100)
print(mylist.search(100))
print(mylist.size())

mylist.remove(54)
print(mylist.size())
mylist.remove(93)
print(mylist.size())
mylist.remove(31)
print(mylist.size())
print(mylist.search(93))
mylist.append(1024)
print(mylist.search(1024))