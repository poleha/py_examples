def get_primes(N):
    primes = []
    visited = set()
    i = 1
    while i < N:
        i += 1
        if i in visited:
            continue
        j = i
        first = True
        primes.append(i)
        while j <= N:
            visited.add(j)

            if first:
                j *= j
                first = False
            else:
                j += i
    return primes









for j in get_primes(25):
    print(j)



