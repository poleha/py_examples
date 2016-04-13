"forks child processes until you type 'q'"
"""
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
        newpid = os.fork()
        #Создали дочерний процесс, копию исходного
        if newpid == 0: #Если мы в дочернем процессе, то newpid == 0
            child()
        else:
            print('Hello from parent', os.getpid(), newpid)
        if input() == 'q': break

parent()
