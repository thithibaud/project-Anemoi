import tkinter as tk
from tkinter import ttk
from tkinter import *
        #DESPLEGALBE
##var = ttk.StringVar(lblimg)
##opcion = ttk.OptionMenu(lblimg, var, *mfall)
##opcion.config(width=20)
##opcion.grid(row = 1, column = 3)
##
##var2 = ttk.StringVar(lblimg)
##opcion2 = ttk.OptionMenu(lblimg, var2, *mfall)
##opcion2.config(width=20)
##opcion2.grid(row = 2, column = 3)

def identify():
        global mflow
        i = 0
        j = 0
        elflow = mf.Control_FlowBus('/dev/ttyUSB0')
        for i in range (0,6):
            nodo = '0'+str(i)
            respuesta = elflow.send_setpoint(nodo, 0)
            if respuesta == b'00005':
                mflow.append(nodo)
                j+=1
            else:
                i+=1
        mfcontrol.identyall(j)

def identyall(j):
            global mfall
            i=1
            for i in range (0,j):
                    nodo = mflow[i]
                    elflow = mf.Control_FlowBus('/dev/ttyUSB0')
                    numser = elflow.get_serial(nodo)
                    capacity = str(elflow.get_capacity(nodo))
                    unid = str(elflow.get_unit(nodo))
                    setp = str(elflow.get_setpoint(nodo))
                    texto = 'MF en nodo '+nodo+' con sr: '+numser+' y capacidad: '+capacity+unid+'S.P.:'+setp+'%'
                    mfall.append(texto)
                    print(mfall)

def Checked(self, var, var2):#,var,var2):
        windowchk = Toplevel(window)
        mfcontrol.center(windowchk)
        windowchk.title('Check connection')
        windowchk.geometry('575x90')

        mfcontrol.center(windowchk)

        op1 = var
        op2 = var2

        ttk.Label(windowchk, text='You select AIR MF:').grid(row = 1, column = 0)
        ttk.Label(windowchk, textvariable= op1).grid(row = 1, column = 1)
        ttk.Label(windowchk, text= 'You select GAS MF:').grid(row = 2, column = 0)
        ttk.Label(windowchk, textvariable= op2).grid(row = 2, column = 1)

        ttk.Button(windowchk, text = 'Close', command = lambda: windowchk.destroy()).grid(row = 3, column = 0, columnspan = 2, sticky = W + E)


mfcontrol.identify() #PRINCIPAL PER FER LA DETECCIÓ

