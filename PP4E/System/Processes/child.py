import os, sys
print('Hello from child', os.getpid(), sys.argv[1])
print(sys.executable) #/usr/bin/python3
print(sys.argv) #['child.py', '1']