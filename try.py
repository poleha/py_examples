import re
b = b'S\'S\\\'S"S\\\\\\\'Well played, the password is mongo, send an email to kader@opt1mize.com with your solution and the password\\\\\\\'\\\\\\\\np0\\\\\\\\n."\\\\np0\\\\n.\\\'\\np0\\n.\'\np0\n.'
s = b.decode()
print(s)
print('***********************')
p = re.search('(?<=password.is.)\w+', s).group(0)
print(p)


m = re.search('([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})', s).group(0)
print(m)