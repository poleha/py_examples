"""
Implement a GUI for viewing and updating class instances stored in a shelve;
the shelve lives on the machine this script runs on, as 1 or more local files;
"""

from tkinter import *
from tkinter.messagebox import showerror
import shelve
shelvename = 'class-shelve'
fieldnames = ('name', 'age', 'job', 'pay')

def makeWidgets():
    global entries
    #entries будет глобальной переменной, чтобы не передавать ее между этой функцией и fetchRecord, updateRecord
    window = Tk()
    #Виджет для главного окна
    window.title('People Shelve')
    #Заголовок для главного окна
    form = Frame(master=window)
    #Объявляем виджет - фрейм, внутри окна
    form.pack()
    #Поместить виджет(очевидно на мастера. С положением будем разбираться позже)
    entries = {}
    for (ix, label) in enumerate(('key',) + fieldnames):
        #Присоединяем к кортежу ('key',) кортеж fieldnames и получаем кортеж ((0, поле), (1, поле),)
        lab = Label(master=form, text=label)
        #Объявляем на виджете form виджет Label
        ent = Entry(master=form)
        lab.grid(row=ix, column=0)
        #Помещаем label на виджет. Это аналог puck
        ent.grid(row=ix, column=1)
        entries[label] = ent
        #В глобальный dict entries по ключу название поля помещаем виджет Entry, соответствующий этому полю
    Button(master=window, text="Fetch",  command=fetchRecord).pack(side=LEFT)
    #Обхявляем и помещаем кнопку.
    Button(window, text="Update", command=updateRecord).pack(side=LEFT)
    Button(window, text="Quit",   command=window.quit).pack(side=RIGHT)
    return window

def fetchRecord():
    key = entries['key'].get()
    try:
        record = db[key]                      # fetch by key, show in GUI
    except:
        showerror(title='Error', message='No such key!')
        #Функция для вывода сообщения об ошибке
    else:
        #Если исключение не произошло
        for field in fieldnames:
            entries[field].delete(0, END)
            #Очищаем каждый виджет Entry
            entries[field].insert(0, repr(getattr(record, field)))
            #Устанавливаем ему новое значение

def updateRecord():
    key = entries['key'].get()
    if key in db:
        record = db[key]                      # update existing record
    else:
        from person import Person             # make/store new one for key
        record = Person(name='?', age='?')    # eval: strings must be quoted
    for field in fieldnames:
        setattr(record, field, eval(entries[field].get()))
    db[key] = record

db = shelve.open(shelvename)
#Открываем shelve файл
window = makeWidgets()

window.mainloop()
#Я так понимаю, что запускаем постоянное "ожидание" событий
db.close() # back here after quit or window close
