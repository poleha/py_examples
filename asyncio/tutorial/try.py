import collections
import sys
import types


class Trampoline:
            """Manage communications between coroutines"""

            running = False

            def __init__(self):
                self.queue = collections.deque()

            def add(self, coroutine):
                """Request that a coroutine be executed"""
                self.schedule(coroutine)

            def run(self):
                result = None
                self.running = True
                try:
                    while self.running and self.queue:
                        func = self.queue.popleft()
                        result = func()
                    return result
                finally:
                    self.running = False

            def stop(self):
                self.running = False

            def schedule(self, coroutine, stack=(), val=None, *exc):
                def resume():
                    value = val
                    try:
                        if exc:
                            value = coroutine.throw(value,*exc)
                        else:
                            value = coroutine.send(value)
                    except:
                        if stack:
                            # send the error back to the "caller"
                            self.schedule(
                                stack[0], stack[1], *sys.exc_info()
                            )
                        else:
                            # Nothing left in this pseudothread to
                            # handle it, let it propagate to the
                            # run loop
                            raise

                    if isinstance(value, types.GeneratorType):
                        # Yielded to a specific coroutine, push the
                        # current one on the stack, and call the new
                        # one with no args
                        self.schedule(value, (coroutine, stack))

                    elif stack:
                        # Yielded a result, pop the stack and send the
                        # value to the caller
                        self.schedule(stack[0], stack[1], value)

                    # else: this pseudothread has ended

                self.queue.append(resume)
loop = Trampoline()

def test1():
    print(5)
    yield 5

def test2():
    yield test1()

t = test2()

loop.schedule(t)

loop.run()