class A:
    pass


def solution(A):
    res = set()
    for x, y, z in A:
        qr = x ** 2 + y ** 2 + z ** 2
        res.add(qr)
    return len(res)


A =  [(0, 5, 4), (0, 0, -3), (-2, 1, -6), (1, -2, 2), (1, 1, 1), (4, -4, 3)] * 100000
print(solution(A))
