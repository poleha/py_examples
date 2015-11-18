#reader.py
#print('Got this: "%s"' % input())
#import sys
#data = sys.stdin.readline()[:-1]
#print('The meaning of life is', data, int(data) * 2)

#writer.py
#print("Help! Help! I'm being repressed!")
#print(42)

"""
import os
p1 = os.popen('python3 writer.py', 'r')
p2 = os.popen('python3 reader.py', 'w')
p2.write( p1.read() )
#36
X = p2.close()
#Got this: “Help! Help! I'm being repressed!”
#The meaning of life is 42 84
print(X)
#None
"""


from subprocess import Popen, PIPE
p1 = Popen('python3 writer.py', stdout=PIPE, shell=True)
p2 = Popen('python3 reader.py', stdin=p1.stdout, stdout=PIPE, shell=True)
output = p2.communicate()[0]
print(output)
#b'Got this: “Help! Help! I\'m being repressed!”\r\nThe meaning of life is 42 84\r\n'Стандартные потоки ввода-вывода
#203
print(p2.returncode)
#0