import tkinter as ttk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import os
import time

flow2 = sys.argv[1]
cycles2 = sys.argv[2]
stime2 = sys.argv[3]
cytime2 = sys.argv[4]
ftime2 = sys.argv[5]
bcytime2 = sys.argv[6]
mflow = sys.argv[7]

flow = int(flow2)
cycles = int(cycles2)
stime = int(stime2)
cytime = int(cytime2)
ftime = int(ftime2)
bcytime = int(bcytime2)

nombre = "Empty"
user = "Juan"

class mscript:
    def __init__(self,window):
        center(window)
        self.wind = window
        self.wind.title('SCRIPT Information')
        self.wind.protocol("WM_DELETE_WINDOW", on_closing)

        #CREATING FIRST FRAME
        infor = LabelFrame(self.wind, text = 'Script Info')
        infor.grid(row = 0, column = 0, sticky = W + E)

        if cycles != 0:
            maxValue=(stime+cytime+ftime+bcytime)*cycles

        currentValue=0

        ttk.Label(infor, text='FLOW:'+str(flow)).grid(row = 1, column = 1, sticky = W)
        ttk.Label(infor, text='CYCLES:'+str(cycles)).grid(row = 2, column = 1, sticky = W)
        ttk.Label(infor, text='START TIME:'+str(stime)).grid(row = 3, column = 1, sticky = W)
        ttk.Label(infor, text='CYCLE TIME:'+str(cytime)).grid(row = 4, column = 1, sticky = W)
        ttk.Label(infor, text='FINAL TIME:'+str(ftime)).grid(row = 5, column = 1, sticky = W)
        ttk.Label(infor, text='BETWEEN CYCLES TIME:'+str(bcytime)).grid(row = 6, column = 1, sticky = W)
        #ttk.Label(infor, text='You select AIR MF:'+str(mflow)).grid(row = 7, column = 0)

        imagen=PhotoImage(file='image/run.png')
        widget=Label(infor, image=imagen)
        widget.image = imagen
        widget.grid(row = 0, column = 0, rowspan = 7, sticky= N+S)

        lblimg = LabelFrame(self.wind, text = 'Script Progress')
        lblimg.grid(row = 9, column = 0, sticky = W + E)

        progressbar=Progressbar(lblimg,orient="horizontal",length=300,mode="determinate")
        progressbar.grid(row = 9, column = 0, columnspan = 3)

        if cycles != 0:
            progressbar["value"]=currentValue
            progressbar["maximum"]=maxValue
            divisions=maxValue


        Button = ttk.Button(lblimg, text = 'Check Script Plot', command= lambda: self.showplot(currentValue)).grid(row = 10, column = 1, sticky = W + E)

        for i in range(divisions):
            currentValue=currentValue+1
            progressbar.after(1000, self.progress(progressbar, currentValue))
            perc=(currentValue/maxValue)*100
            ttk.Label(lblimg, text=str(int(perc))+"%").grid(row = 9, column = 4)
            progressbar.update() # Force an update of the GUI

    def progress(self, progressbar, currentValue):
        progressbar["value"]=currentValue
        hora = time.strftime('%X')
        linea = hora + ',' + str(flow)
        grabar_txt(linea)

    def showplot(self, currentValue):
        index=str(currentValue)
        comanda = "python3 showplot.py "+flow2+" "+cycles2+" "+stime2+" "+cytime2+" "+ftime2+" "+bcytime2+" "+index
        os.system(comanda)

    #def updateflow(self):

    #def openvalve(self):

    #def closevalve(self):

def center(root):
    root.withdraw()
    root.update_idletasks()

    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.geometry("+%d+%d" % (x, y))

    root.deiconify()

def crear_txt():
    global nombre
    nombre = user + '_'+ time.strftime('%c') + '.txt'    #el nombre del archivo será: nombre + día año + hora
    arch = open(nombre, 'w')                                            #se abre el archivo para escritura
    fecha = time.strftime('%c')                                         #se pide la fecha y hora al sistema
    arch.write(fecha+'\n'+user+'\n')                           #la primera línea del archivo creado contendrá la fecha, nombre y apellidos
    arch.close()                                                        #se cierra el archivo

#def convertir_ppm():


def grabar_txt(linea):
    global nombre
    arch = open(nombre, 'a')
    arch.write(linea+'\n')
    arch.close()

def on_closing():
    if messagebox.askokcancel("Quit", "Are you shure if the experiment is over?"):
        os.remove(nombre)
        window.destroy()


if __name__ == '__main__':
    window = Tk()
    crear_txt()
    application = mscript(window)
    window.mainloop()
