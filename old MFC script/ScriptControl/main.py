#!/usr/bin/env python3
from tkinter import ttk
from tkinter import *
from PIL.ImageTk import PhotoImage
from PIL import Image
from tkinter import filedialog
import os


class Principal:
    def __init__(self,window):
        self.wind = window
        self.wind.title('MinoS MassFlow Controller')

        #CREATING FIRST FRAME
        lblimg=LabelFrame(self.wind)
        lblimg.grid(row=0, column=2)

        #PASTE AN IMAGE
        imagen=PhotoImage(file='image/logominos.png')
        widget=Label(lblimg, image=imagen)
        widget.image = imagen
        widget.grid(row=0, column=2)


        #CREATING A FRAME
        frame=LabelFrame(self.wind, text='Insert your ID and PSWD')
        frame.grid(row=1, column=0, columnspan=3, pady=20)


        #CREATE INPUT
        ttk.Label(frame, text='UserID: ').grid(row=2, column=0)
        self.name=Entry(frame)
        self.name.focus()
        self.name.grid(row=2, column=1)

        #CREATE PSWD
        ttk.Label(frame, text = 'Password: ').grid(row=3, column=0)
        self.passwd=Entry(frame, show='*')
        self.passwd.grid(row=3, column=1)

        #BUTTON
        ttk.Button(frame, text='Login', command=lambda: self.Script(self.name.get(), self.passwd.get())).grid(row=4, columnspan=2, sticky=W+E)


    def Script(self,userpassat,passpassat):
        window.state(newstate='withdraw')
        comanda = 'python3 massflow.py '+userpassat+' '+passpassat
        os.system(comanda)
        window.state(newstate='normal')


def center(root):
    root.withdraw()
    root.update_idletasks()

    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.geometry("+%d+%d" % (x, y))

    root.deiconify()


if __name__ == '__main__':
    window=Tk()
    application = Principal(window)
    center(window)
    window.mainloop()
