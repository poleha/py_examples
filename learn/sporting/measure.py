import time

def create_measure(timers):
    def measure(timer_name = None):
        def dec(func):
            key = timer_name if timer_name else func.__name__
            timers[key] = 0
            def wrapper(*args, **kwargs):
                start = time.time()
                res = func(*args, **kwargs)
                end = time.time()
                timers[key] += end - start
                return res
            return wrapper
        return dec
    return measure