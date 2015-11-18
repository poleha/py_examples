class Wrapper:
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __getattr__(self, item):
        print('Tracing', item)
        return getattr(self.wrapped, item)


ob = Wrapper([1,2,3])
ob.append(5)
