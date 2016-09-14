
#******************************
"""
Существует два основных способа реализации одновременного выпол-
нения задач в Python – ветвление процессов (forks) и порожденные по-
токи (threads) выполнения.

поскольку потоки выполняются в одном процессе, они
используют общую глобальную память процесса. Благодаря этому
потоки могут просто и  естественно взаимодействовать друг с  дру-
гом путем чтения и записи данных в глобальной памяти, доступной
всем потокам выполнения. Дочерний процесс, наоборот, копирует состояние и оно живет своей жизнью.

Для
запуска программ переносимым способом, с помощью команд оболоч-
ки, также можно использовать функции os.popen, os.system и  модуль
subprocess, с  которыми мы познакомились в  главах 2 и  3. Новейший
пакет multiprocessing предоставляет дополнительные переносимые спо-
собы запуска процессов.

функция
os.fork и модули threading, queue и multiprocessing.

"""
#Дочерние процессы(forks)
#*************************************
"""
#stud
"forks child processes until you type 'q'"

Запуск нового параллельного процесса осуществляется вызовом
функции os.fork. Поскольку эта функция создает копию вызывающей
программы, она возвращает различные значения в  каждой копии:
ноль – в дочернем процессе и числовой идентификатор ID процесса но-
вого потомка – в родительском процессе.
"""

import os
def child():
    print('Hello from child',  os.getpid())
    os._exit(0)  # else goes back to parent loop
    #Завершаем процесс со статусом 0

def parent():
    while True:
        print('1')
        newpid = os.fork()
        print('2') #fork startst from here
        #Создали дочерний процесс, копию исходного
        if newpid == 0: #Если мы в дочернем процессе, то newpid == 0
            child()
        else:
            print('Hello from parent', os.getpid(), newpid)
        if input() == 'q': break

parent()

#1
#2
#Hello from parent 12465 12466
#2
#Hello from child 12466
#*********************
"""
fork basics: start 5 copies of this program running in parallel with
the original; each copy counts up to 5 on the same stdout stream--forks
copy process memory, including file descriptors; fork doesn't currently
work on Windows without Cygwin: use os.spawnv or multiprocessing on
Windows instead; spawnv is roughly like a fork+exec combination;
"""

import os, time

def counter(count):                                    # run in new process
    for i in range(count):
        #time.sleep(1)                                  # simulate real work
        #Почему-то не работает
        print('[%s] => %s' % (os.getpid(), i))

for i in range(5):
    pid = os.fork()
    if pid != 0:
        print('Process %d spawned' % pid)              # in parent: continue
    else:
        counter(5)                                     # else in child/new process
        os._exit(0)                                    # run function and exit

print('Main process exiting.')                         # parent need not wait
#***************************************
#fork-exec.py
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

#child.py
import os, sys
print('Hello from child', os.getpid(), sys.argv[1])
print(sys.executable) #/usr/bin/python3
print(sys.argv) #['child.py', '1']
"""
Главное,
на что следует обратить внимание, – это функция os.execlp. В двух сло-
вах, эта функция замещает программу, выполняющуюся в  текущем
процессе, новой программой. Поэтому комбинация функций os.fork
и os.execlp означает запуск нового процесса и запуск новой программы
в  этом процессе. Другими словами  – запуск новой программы парал-
лельно оригинальной.
"""
"""
Всего существует восемь разновидностей функции exec,
что может вызывать затруднения в выборе, если не сделать обобщение:
os.execv(program, commandlinesequence)
Базовая «v»-форма функции exec, которой передается имя выполня-
емой программы вместе со списком или кортежем строк аргументов
командной строки, используемых при запуске программы (то есть
слов, которые обычно можно ввести в командной строке для запуска
программы).
os.execl(program, cmdargl, cmdarg2, ... cmdargN)
Базовая «l»-форма функции exec, которой передается имя выполняе-
мой программы, за которым следуют один или более аргументов ко-
мандной строки, передаваемых как отдельные аргументы функции.
Соответствует вызову функции os.execv(program, (cmdargl, cmdarg2,
...)).
os.execlp
os.execvp
Символ «р», добавленный к  именам execv и  execl, означает, что
Python станет искать каталог, где находится программа, используя
сис­темный путь поиска (то есть переменную PATH).
os.execle
os.execve
Символ «e», добавленный к  именам execv и  execl, означает, что до-
полнительный последний аргумент является словарем, содержащим
переменные окружения, которые нужно передать программе.
os.execvpe
os.execlpe
Символы «p» и «e», добавленные к базовым именам exec, означают
одновременное использование пути поиска и словаря с переменными
окружения.
"""
#*************************
#*******************************
#Параллельные потоки(threads)
"spawn threads until you type 'q'"

import _thread

def child(tid):
    print('Hello from thread', tid)

def parent():
    i = 0
    while True:
        i += 1
        _thread.start_new_thread(child, (i,))
        if input() == 'q': break

parent()
#************************************
"""
any callable can be run in a thread, since all live in same process;
add locks to synchronize prints if needed to avoid overlaps or output
dupication (see later in the chapter); all 3 threads print 4294967296
"""

import _thread, time

def action(i):                                       # function run in threads
    print(i ** 32)

class Power:
    def __init__(self, i):
        self.i = i
    def action(self):                                # bound method run in threads
        print(self.i ** 32)

_thread.start_new_thread(action, (2,))               # simple function

_thread.start_new_thread((lambda: action(2)), ())    # lambda function to defer

obj = Power(2)
_thread.start_new_thread(obj.action, ())             # bound method object

time.sleep(2)
print('Main thread exiting.')                        # don't exit too early
"""
Поскольку все потоки выполняются в рамках одного и того же
процесса, все они совместно используют один и тот же поток стандарт-
ного вывода (в терминах языка Python они совместно используют файл
sys.stdout, куда выводит текст функция print).
"""

#******************************
"""
synchronize access to stdout: because it is shared global,
thread outputs may be intermixed if not synchronized
"""

import _thread as thread, time

def counter(myId, count):                        # function run in threads
    for i in range(count):
        time.sleep(1)                            # simulate real work
        mutex.acquire()
        print('[%s] => %s' % (myId, i))          # print isn't interrupted now
        mutex.release()

mutex = thread.allocate_lock()                   # make a global lock object
for i in range(5):                               # spawn 5 threads
    thread.start_new_thread(counter, (i, 5))     # each thread loops 5 times

time.sleep(6)
print('Main thread exiting.')                    # don't exit too early
#*****************************
"""
uses mutexes to know when threads are done in parent/main thread,
instead of time.sleep; lock stdout to avoid comingled prints;
"""

import _thread as thread
stdoutmutex = thread.allocate_lock()
exitmutexes = [thread.allocate_lock() for i in range(10)]

def counter(myId, count):
    for i in range(count):
        stdoutmutex.acquire()
        print('[%s] => %s' % (myId, i))
        stdoutmutex.release()
    exitmutexes[myId].acquire()    # signal main thread

for i in range(10):
    thread.start_new_thread(counter, (i, 100))

for mutex in exitmutexes:
    while not mutex.locked(): pass
print('Main thread exiting.')
#*******
"""
uses simple shared global data (not mutexes) to know when threads
are done in parent/main thread; threads share list but not its items,
assumes list won't move in memory once it has been created initially
"""

import _thread as thread
stdoutmutex = thread.allocate_lock()
exitmutexes = [False] * 10

def counter(myId, count):
    for i in range(count):
        stdoutmutex.acquire()
        print('[%s] => %s' % (myId, i))
        stdoutmutex.release()
    exitmutexes[myId] = True  # signal main thread

for i in range(10):
    thread.start_new_thread(counter, (i, 100))

while False in exitmutexes: pass
print('Main thread exiting.')
#**************
#Самый правильный
"""
passed in mutex object shared by all threads instead of globals;
use with context manager statement for auto acquire/release;
sleep calls added to avoid busy loops and simulate real work
"""

import _thread as thread, time
stdoutmutex = thread.allocate_lock()
numthreads  = 5
exitmutexes = [thread.allocate_lock() for i in range(numthreads)]

def counter(myId, count, mutex):                     # shared object passed in
    for i in range(count):
        time.sleep(1 / (myId+1))                     # diff fractions of second
        with mutex:                                  # auto acquire/release: with
            print('[%s] => %s' % (myId, i))
    exitmutexes[myId].acquire()                      # global: signal main thread

for i in range(numthreads):
    thread.start_new_thread(counter, (i, 5, stdoutmutex))

while not all(mutex.locked() for mutex in exitmutexes): time.sleep(0.25)
print('Main thread exiting.')

#***********************
"""
Потоки, созданные модулем _thread, завершаются при завершении главного потока.
Однако при использовании альтернативного модуля threading програм-
ма не может завершиться, когда хотя бы один поток продолжает ра-
боту, если только он не был запущен, как поток-демон.
"""
#**********************************
"""
thread class instances with state and run() for thread's action;
uses higher-level Java-like threading module object join method (not
mutexes or shared global vars) to know when threads are done in main
parent thread; see library manual for more details on threading;
"""

import threading

class Mythread(threading.Thread):              # subclass Thread object
    def __init__(self, myId, count, mutex):
        self.myId  = myId
        self.count = count                     # per-thread state information
        self.mutex = mutex                     # shared objects, not globals
        threading.Thread.__init__(self)

    def run(self):                             # run provides thread logic
        for i in range(self.count):            # still sync stdout access
            with self.mutex:
                print('[%s] => %s' % (self.myId, i))

stdoutmutex = threading.Lock()                 # same as thread.allocate_lock()
threads = []
for i in range(10):
    thread = Mythread(i, 100, stdoutmutex)     # make/start 10 threads
    thread.start()                             # starts run method in a thread
    threads.append(thread)

for thread in threads:
    thread.join()                              # wait for thread exits
print('Main thread exiting.')
#************************************
"""
four different ways to run an action in a thread; all print 4294967296,
but prints should be synchronized with a mutex here to avoid overlap
"""

import threading, _thread
def action(i):
    print(i ** 32)

# subclass with state
class Mythread(threading.Thread):
    def __init__(self, i):
        self.i = i
        threading.Thread.__init__(self)
    def run(self):                                        # redefine run for action
        print(self.i ** 32)
Mythread(2).start()                                       # start invokes run()

# pass action in
thread = threading.Thread(target=(lambda: action(2)))     # run invokes target
thread.start()

# same but no lambda wrapper for state
threading.Thread(target=action, args=(2,)).start()        # callable plus its args

# basic thread module
_thread.start_new_thread(action, (2,))                    # all-function interface
#*******************************
"prints different results on different runs on Windows 7"
#На linux одинаковые

import threading, time
count = 0

def adder():
    global count
    count = count + 1             # update a shared name in global scope
    time.sleep(0.5)               # threads share object memory and global names
    count = count + 1

threads = []
for i in range(100):
    thread = threading.Thread(target=adder, args=())
    thread.start()
    threads.append(thread)

for thread in threads: thread.join()
print(count)

#Лекарство

"prints 200 each time, because shared resource access synchronized"

import threading, time
count = 0

def adder(addlock):                 # shared lock object passed in
    global count
    with addlock:
        count = count + 1           # auto acquire/release around stmt
    time.sleep(0.5)
    with addlock:
        count = count + 1           # only 1 thread updating at once

addlock = threading.Lock()
threads = []
for i in range(100):
    thread = threading.Thread(target=adder, args=(addlock,))
    thread.start()
    threads.append(thread)

for thread in threads: thread.join()
print(count)
#**************************
#queue
"producer and consumer threads communicating with a shared queue"

numconsumers = 2                  # how many consumers to start
numproducers = 4                  # how many producers to start
nummessages  = 4                  # messages per producer to put

import _thread as thread, queue, time
safeprint = thread.allocate_lock()    # else prints may overlap
dataQueue = queue.Queue()             # shared global, infinite size

def producer(idnum):
    for msgnum in range(nummessages):
        time.sleep(idnum)
        dataQueue.put('[producer id=%d, count=%d]' % (idnum, msgnum))

def consumer(idnum):
    while True:
        time.sleep(0.1)
        try:
            data = dataQueue.get(block=False)
        except queue.Empty:
            pass
        else:
            with safeprint:
                print('consumer', idnum, 'got =>', data)

if __name__ == '__main__':
    for i in range(numconsumers):
        thread.start_new_thread(consumer, (i,))
    for i in range(numproducers):
        thread.start_new_thread(producer, (i,))
    time.sleep(((numproducers-1) * nummessages) + 1)
    print('Main thread exit.')

#***
"same as queuetest.py, by queue object pass in as argument, not global"


numconsumers = 2                  # how many consumers to start
numproducers = 4                  # how many producers to start
nummessages  = 4                  # messages per producer to put

import _thread as thread, queue, time
safeprint = thread.allocate_lock()    # else prints may overlap
dataQueue = queue.Queue()             # shared global, infinite size

def producer(idnum, dataqueue):
    for msgnum in range(nummessages):
        time.sleep(idnum)
        dataqueue.put('[producer id=%d, count=%d]' % (idnum, msgnum))

def consumer(idnum, dataqueue):
    while True:
        time.sleep(0.1)
        try:
            data = dataqueue.get(block=False)
        except queue.Empty:
            pass
        else:
            with safeprint:
                print('consumer', idnum, 'got =>', data)

if __name__ == '__main__':
    for i in range(numconsumers):
        thread.start_new_thread(consumer, (i, dataQueue))
    for i in range(numproducers):
        thread.start_new_thread(producer, (i, dataQueue))
    time.sleep(((numproducers-1) * nummessages) + 1)
    print('Main thread exit.')

#*****************************
#************************
"""
Only for threading
#http://stackoverflow.com/questions/15085348/what-is-the-use-of-join-in-python-threading
without join:
+---+---+------------------                     main-thread
    |   |
    |   +...........                            child-thread(short)
    +..................................         child-thread(long)

with join
+---+---+------------------***********+###      main-thread
    |   |                             |
    |   +...........join()            |         child-thread(short)
    +......................join()......         child-thread(long)

with join and demon thread
+-+--+---+------------------***********+###     parent-thread
  |  |   |                             |
  |  |   +...........join()            |        child-thread(short)
  |  +......................join()......        child-thread(long)
  +,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,     child-thread(long+demonized)

'-' main-thread/parent-thread/main-program execution
'.' child-thread execution
'#' optional parent-thread execution after join()-blocked parent-thread could
    continue
'*' main-thread 'sleeping' in join-method, waiting for child-thread to finish
',' demonized thread - 'ignores' lifetime of other threads;
    terminates when main-programs exits; is normally meant for
    join-independent tasks
"""
#******************************************

"same as queuetest2.py, but uses threading, not _threads"
numconsumers = 2                  # how many consumers to start
numproducers = 4                  # how many producers to start
nummessages  = 4                  # messages per producer to put

import threading, queue, time, sys
safeprint = threading.Lock()          # else prints may overlap
dataQueue = queue.Queue()             # shared global, infinite size

def producer(idnum, dataqueue):
    for msgnum in range(nummessages):
        time.sleep(idnum)
        dataqueue.put('[producer id=%d, count=%d]' % (idnum, msgnum))

def consumer(idnum, dataqueue):
    while True:
        time.sleep(0.1)
        try:
            data = dataqueue.get(block=False)
        except queue.Empty:
            pass
        else:
            with safeprint:
                print('consumer', idnum, 'got =>', data)

if __name__ == '__main__':
    for i in range(numconsumers):
        thread = threading.Thread(target=consumer, args=(i, dataQueue))
        #thread.daemon = True  # Если демон, то когда завершится главный thread, он не будет дожидаться завершения этого
        thread.start()

    waitfor = []
    for i in range(numproducers):
        thread = threading.Thread(target=producer, args=(i, dataQueue))
        waitfor.append(thread)
        thread.start()

    for thread in waitfor: thread.join()    # or time.sleep() long enough here
    print('Main thread exit.')
 #***************************
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
#*******************************
"""
Например, следующий пример выведет
сообщение спустя 5.5 секунд:
>>> import sys
>>>
>>>
>>>
>>>
from threading import Timer
t = Timer(5.5, lambda: print(‘Spam!’)) # дочерний поток
t.start()
Spam!
"""
#*******************************************
"""
Завершение программ средствами модуля sys
Например, программу можно завершить раньше обычного, вызвав
функцию sys.exit:
>>> sys.exit(N) # выход с кодом завершения N, в противном случае
# программа завершится по достижении конца сценария
Интересно отметить, что в действительности эта функция просто воз-
буждает встроенное исключение SystemExit. Поэтому его можно обыч-
ным образом перехватывать, чтобы выполнить завершающие действия.
Если это исключение не перехватывать, интерпретатор завершит рабо-
ту как обычно. Например:
C:\...\PP4E\System> python
>>> import sys
>>> try:
...
sys.exit()
# смотрите также: os._exit, Tk().quit()
... except SystemExit:
...
print(‘ignoring exit’)
...
ignoring exit
>>>
"""
#******************************
def later():
    import sys
    print('Bye sys world')
    sys.exit(42)
    print('Never reached')

#if __name__ == '__main__': later()


try:
    later()
except SystemExit:
    print('Ignored')

try:
    later()
finally:
    print('Cleanup')

#Bye sys world
#Ignored
#Bye sys world
#Cleanup

#****************************
"""
При вызове функции os._exit вызывающий процесс завершается сра-
зу, не возбуждая исключения, которое можно перехватить и  игнори-
ровать.
Фактически при таком завершении процесс прекращает рабо-
ту, не выталкивая буферы потоков вывода и не вызывая обработчики,
выполняющие заключительные операции (которые можно определить
с помощью модуля atexit из стандартной биб­лиотеки), поэтому в общем
случае данная функция должна использоваться только дочерними про-
цессами, когда не требуется выполнения действий по завершению всей
программы.
"""

#********************************************

#*****************************
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

def worker():
    logging.debug('started')
    time.sleep(5)
    logging.debug('finished')


t = threading.Thread(target=worker)

#1
#t.start()
#logging.debug('finished')

#(Thread-1  ) started
#(MainThread) finished
#(Thread-1  ) finished


#2
#t.start()
#t.join() #Приостанавливаем вызывающий поток до завершения вызванного
#logging.debug('finished')

#(Thread-1  ) started
#(Thread-1  ) finished
#(MainThread) finished

#3
#t.setDaemon(True) #Основной поток не будет дожидаться завершения этого. Этот закончится с завершением основного потока
#t.start()
#logging.debug('finished')

#(Thread-1  ) started
#(MainThread) finished


#4 Нет смысла
t.setDaemon(True)
t.start()
t.join()
logging.debug('finished')

#(Thread-1  ) started
#(Thread-1  ) finished
#(MainThread) finished

#*************************************************
#parent_os.py
import os, sys
text = 'line1fssxszxazzcline2'
res = os.popen('{0} {1} {2}'.format(sys.executable, 'child_os.py', text)).read()
print(res)

#child_os.py
import sys
print(sys.argv[1])
#|||||||||||||||
#parent_fork.py
import os, time
import sys
text = 'line1\nline2\n'
pid = os.fork()
if pid == 0:
    os.execlp(sys.executable, sys.executable, 'child_fork.py', text)
    #os.popen('{0} {1} {2}'.format(sys.executable, 'child_fork.py', 'txt'))  - так нельзя, поскольку не замещает программу
    assert False, 'error starting program'
else:
    print('Child is opened pid={0}'.format(pid))
    time.sleep(1) #Иначе основной процесс завершится раньше и ничего не выведется

#child_fork.py
import sys
text = sys.argv[1]
print(text)

#|||||||||||||||

#parent_os_system.py
import os
os.system('python3 child_os_system.py ggg')
#child_os_system.py
import sys
#res = sys.stdin.read()
res = sys.argv[1]
print(res)

#||||||||||||||||
#parent_subprocess.py
import subprocess, sys
lines = ['line1\n'.encode(),'line2\n'.encode()]
pipe = subprocess.Popen((sys.executable, 'child_subprocess.py'), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
pipe.stdin.writelines(lines)
pipe.stdin.close()
code = pipe.wait()
res_line = pipe.stdout.read()
print(res_line.decode('utf8'))

#child_subprocess.py
import sys
res = sys.stdin.read()
sys.stdout.write(res)
sys.stdout.close()

#||||||||||||||||||||
#parent_subprocess2.py
import subprocess, sys
lines = ['line1\n'.encode(),'line2\n'.encode()]
code = subprocess.call((sys.executable, 'child_subprocess2.py', 'ggg'))

#child_subprocess2.py
import sys
#res = sys.stdin.read()
res = sys.argv[1]
print(res)

#||||||||||||||
#parent_thread.py
import _thread, os, time


def worker():
    res = os.popen('python3 child_thread.py ggg').read()
    print(res)

_thread.start_new_thread(worker, ())
time.sleep(2)
#child_thread.py
import sys
print(sys.argv[1])
#|||||||||||||
#parent_threading.py
import threading, os

class MyThread(threading.Thread):
    def __init__(self, command):
        self.command = command
    def run(self):
        res = os.popen(self.command).read()
        print(res)


th = MyThread('python3 child_threading.py ggg')
th.run()

#child_threading.py
import sys
print(sys.argv[1])


#*************************************************
#Comparing approaches, my

import threading
import time
from urllib.request import urlopen


urls = [
    'http://mail.ru',
    #'http://ag.ru',
   # 'http://wikipedia.org',
] * 10


start = time.time()

workers = []

class Worker(threading.Thread):
    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        conn = urlopen('http://mail.ru')
        reply = conn.read()
        self.reply = reply


for url in urls:
    worker = Worker(url)
    worker.start()
    workers.append(worker)


for worker in workers:
    worker.join()

for worker in workers:
    pass
    #print(worker.url, worker.reply)

end = time.time()

print(1, end - start)

start = time.time()
for url in urls:
    conn = urlopen('http://mail.ru')
    reply = conn.read()
    #print(reply)
end = time.time()

print(2, end - start)

#************************

import os
start = time.time()


def worker(url):
    conn = urlopen(url)
    reply = conn.read()
    #print(reply)
    end = time.time()
    #print(3, end - start)
    #print(results)
    os._exit(0)

for url in urls:
    pid = os.fork()
    if pid == 0:
        worker(url)
        assert False, 'error starting program'
    else:
        pass
        #print(pid)

time.sleep(3)



from multiprocessing import Process, Pipe #Есть очень похожий вариант с Queue https://docs.python.org/3/library/multiprocessing.html

"""
from multiprocessing import Process, Queue

def f(q):
    q.put([42, None, 'hello'])

if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    print(q.get())    # prints "[42, None, 'hello']"
    p.join()
 """


results = []

start = time.time()

def worker(url, conn):
    url_conn = urlopen(url)
    reply = url_conn.read()
    conn.send(reply[:500])
    conn.close()


parent_connections = []

for url in urls:
    parent_conn, child_conn = Pipe()
    p = Process(target=worker, args=(url, child_conn))
    p.start()
    p.join()
    parent_connections.append(parent_conn)



end = time.time()

for parent_connection in parent_connections:
    pass
    #print(parent_connection.recv())

print(4, end - start)

#1 2.0084848403930664
#2 2.026202917098999
#4 2.392305374145508