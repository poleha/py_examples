

S = list('()()(((')

L = len(S)


# Когда мы переворачиваем ) ошибку - смотрим, какая ошибка следующая.
# Если ), то убираем обе.
# Иначе --- Если ( или правильно, то не меняем ошибок


# Когда мы переворачиваем ( ошибку - смотрим, какая ошибка перед ней.
# Если (, то убираем обе.
# Иначе --- Если ) или правильно, то не меняем ошибок


# Когда мы переворачиваем правильную скобку ), то
# Если после нее есть ошибка ), то ошибка удалена
# Предшествующая ей правильная становится непраильной


# Когда мы переворачиваем правильную скобку (, то
# Если перед ней есть ошибка (, то ошибка удалена
# Следующая за ней правильная становится непраильной



def react_to_change(S, change_points, errors, changed_point_index0):
    change_point_index = change_points[changed_point_index0]
    change_point = S[change_point_index]
    if change_point in errors:
        if change_point == ')':
            for i in xrange(changed_point_index0 - 1, -1, -1):
                prev_change_point_index = change_points[i]
                prev_change_point = S[prev_change_point_index]
                if prev_change_point in errors and change_point == prev_change_point:
                    del change_point[i]


def rotate2(cur):
    if cur == '(':
        return ')'
    else:
        return '('

def get_closers(S, L):
    opened = []
    closed = []
    closers = {}
    next_errors = {}
    for i in xrange(L):
        cur = S[i]
        if cur == '(':
            opened.append(i)
        else:
            if opened:
                closers[opened.pop()] = i
            else:
                closed.append(i)
    errors = closed + opened
    for i in xrange(len(errors) - 1):
        #error = errors[i]
        #next_error = errors[i + 1]
        next_errors[i] = i + 1


    return set(errors), closers, next_errors


errors, closers, next_errors = get_closers(S, L)
print errors, closers, next_errors



for i in xrange(L):
    new_S = S[:]
    new_S[i] = rotate2(S[i])
    if i in errors:
        if i in next_errors:
            errors.remove(i)
            errors.remove(next_errors[i])

    else:
        if i in closers:
            errors.add




"""
for i in xrange(1, L):
    new_S = S[i:]
    if i - 1 in errors:
        errors.remove(i - 1)
    else:
        if i - 1 in closers:
            errors.add(closers[i - 1])
            del closers[i - 1]
    print new_S, errors, closers

"""