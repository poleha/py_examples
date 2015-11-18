#!/usr/bin/env python
import os
import sys
from django.utils import timezone
from datetime import date

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kulik.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

from discount.models import Product
products = Product.objects.all()[:15]

from tkinter import *
from tkinter.messagebox import showinfo
"""
window = Tk()
window.title('Window')
frame = Frame(master=window)
frame.pack()
for product in products:
    label = Label(master=frame, text=product.title)
    label.pack()

window.mainloop()
"""


class ProductsGUI(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for product in products:
            #label = Label(master=self, text=product.title)
            #label.pack()
            button = Button(master=self, text=product.title, command=(lambda product=product: self.show_body(product)))
            button.pack()
    def show_body(self, product):
        #showinfo(title=product.title, message=product.body)
        popup = Toplevel()
        Label(popup, text=product.title).pack(side=LEFT)
        popup.title(product.title)
        frame = ProductGUI(product, master=popup)
        frame.pack()


class ProductGUI(Frame):
    def __init__(self, product, *args, **kwargs):
        super().__init__(*args, **kwargs)
        body = Entry(master=self)
        body.insert(0, product.body)
        body.pack()
        button = Button(master=self, text='Save', command=(lambda: self.save(body.get())))
        button.pack()
        self.product = product

    def save(self, body):
        if not self.product._body_rendered == body:
            self.product.body = body
            self.product.save()
            showinfo(message='Changed')
            self.master.destroy()
        else:
            showinfo(message='Not changed')


window = Tk()
frame = ProductsGUI(master=window)
frame.pack()
#window
window.mainloop()