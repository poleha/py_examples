# Get two lists. Find the missing from first in second in in second from first. Find the common part.

timers = {}
from measure import create_measure
measure = create_measure(timers)

@measure()
def compare_arrays(a1, a2):
    miss1 = set() # pressent in a2 only
    miss2 = set() # present in a1 only
    both = set()

    a1_set = set()
    a2_set = set(a2)

    for cur in a1:
        if cur in a2_set:
            both.add(cur)
            a2_set.remove(cur)
        else:
            miss2.add(cur)
        a1_set.add(cur)

    for cur in a2_set:
        if cur in a1_set:
            both.add(cur)
        else:
            miss1.add(cur)


    return miss1, miss2, both






A1 = [7, 1, 2, 4, 8, 8]
A2 = [2, 3, 5, 7, 1, 2, 3, 4, 5, 6]

print(compare_arrays(A1, A2))

print(timers)