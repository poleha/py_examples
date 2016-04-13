"starts programs until you type 'q'"

import os

parm = 0
while True:
    parm += 1
    pid = os.fork()
    if pid == 0:                                             # copy process
        os.execlp('python3', 'python3', 'child.py', str(parm)) # overlay program
        assert False, 'error starting program'               # shouldn't return
        #Второй параметр для формирования sys.executable. В этом случае может быть любой текст.
    else:
        print('Child is', pid)
        if input() == 'q': break
