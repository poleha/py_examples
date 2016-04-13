"""
the threading module refuses to let the program exit if any non-daemon
child threads are still running; we don't need to time.sleep() here,
but do need extra handling if we want program exit in this case.

really, we should .join() here to wait for child threads anyhow; as
coded, the main thread's exit message appears before child thread output;
"""

import threading, time
printalone = threading.Lock()

def counter(myId, count):
    for i in range(count):
        time.sleep(1)   
        with printalone:     
            print('[%s] => %s' % (myId, i))

for i in range(5):                        
    threading.Thread(target=counter, args=(i, 5)).start()

print('Main thread exiting.')

"""
Main thread exiting.
[0] => 0
[2] => 0
[1] => 0
[3] => 0
[4] => 0
[0] => 1
[2] => 1
[1] => 1
[3] => 1
[4] => 1
[0] => 2
[3] => 2
[4] => 2
[2] => 2
[1] => 2
[0] => 3
[2] => 3
[4] => 3
[1] => 3
[3] => 3
[0] => 4
[2] => 4
[1] => 4
[3] => 4
[4] => 4
"""