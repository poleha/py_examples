def limiter(**limits):
    def dec(func):
        all_args = func.__code__.co_varnames[:func.__code__.co_argcount]
        def wrapper(*args, **kwargs):
            pos = all_args[:len(args)]
            attrs_dict = {pos[i]: args[i] for i in range(len(pos))}
            attrs_dict.update(kwargs)
            for arg, val in attrs_dict.items():
                if arg in limits and (val < limits[arg][0] or val > limits[arg][1]):
                    raise TypeError
            return func(*args, **kwargs)
        return wrapper
    return dec


@limiter(a=(1, 5), b=(2, 4))
def fun(a, b=2):
    return a + b


print(fun(5, b=4))

