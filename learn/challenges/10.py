# http://www.pythonchallenge.com/pc/return/bull.html

def las(n):
    if n == 1:
        return '1'
    else:
        prev = str(las(n - 1))
        res = ''
        prev_char = char = prev[0]
        counter = 1
        for i in range(1, len(prev)):
            char = prev[i]
            counter += 1
            if prev_char != char:
                res += str(counter - 1) + prev_char
                counter = 1

            prev_char = char
        if counter:
            res += str(counter) + char
    return res


print(len(las(31))) #5808
