def is_polindrom(s):
    if len(s) <= 1:
        return True
    else:
        left = s[0]
        right = s[-1]
        rest = s[1: -1]
        if left != right:
            return False
        else:
            return is_polindrom(rest)


print(is_polindrom('aba'))