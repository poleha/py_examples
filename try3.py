from io import StringIO

file = StringIO()

file.write('11111\n')
file.write('22222\n')
file.write('33333\n')
file.seek(0)

for line in file:
    print(line.strip())
