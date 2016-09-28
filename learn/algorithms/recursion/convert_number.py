# stud
def convert(n, base):
    digits = '0123456789ABCDEF'
    if n < base:
        return digits[n]
    else:
        return convert(n // base, base) + digits[n % base]

print(convert(769, 10)) #769
print(convert(10, 2)) #1010



