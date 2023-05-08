import tkinter as ttk
from tkinter import *

import comunicacion as com
import os
import multiscript


#user=sys.argv[1]
#passwd=sys.argv[2]
mfall=[]
mfconnected=0
airnode=""
aircap=0
airunit=""
gasnodes=[]
gascap=[]
gasunit=[]
mferror=None
filemsg="WRONG DATA IN CONFIG.TXT"


class mfcontrol:
    def __init__(self,window):
        self.wind3 = window
        self.wind3.title('MassFlow Configure')

        #CREATING FIRST FRAME
        lblimg = LabelFrame(self.wind3, text = 'MF Configuration')
        lblimg.grid(row = 0, column = 0, sticky = W + E)

        #PASTE AN IMAGE
        imagen=PhotoImage(file='image/FLOWBUS.png')
        widget=Label(lblimg, image=imagen)
        widget.image = imagen
        widget.grid(row = 0, column = 0, rowspan=3,columnspan=2)

        if mferror==None:
            print(mferror)
            ttk.Label(lblimg, text='Conected Mass Flows: '+str(mfconnected)).grid(row=0,column=2)
            Label(lblimg, text= 'Avaliable AIR MF: '+str(airnode)+' Uni. '+str(aircap)+' '+airunit).grid(row = 1, column = 2)
            index=2
            if mfconnected>2:
                for i in range(0,(mfconnected-1)):
                    Label(lblimg, text= 'Avaliable GAS MF: '+str(gasnodes[i])+' Uni - '+str(gascap[i])+' '+gasunit[i]).grid(row = index, column = 2)
                    index+=1
            else:
                Label(lblimg, text= 'Avaliable GAS MF: '+str(gasnodes[0])+' Uni - '+str(gascap[0])+' '+gasunit[0]).grid(row = index, column = 2)
            #CREATING A FRAME
            frame4 = LabelFrame(self.wind3, text = 'Script Setup')
            frame4.grid(row =index+1, column = 0, sticky = W + E)

            #PASTE AN IMAGE
            imagen2=PhotoImage(file='image/script2.png')
            widget2=Label(frame4, image=imagen2)
            widget2.image = imagen2
            widget2.grid(row = 1, column = 0, rowspan = 7)

            Label(frame4, text= 'Select Bottle concentration').grid(row = 0, column = 2)

            opciones = ['1ppm', '5ppm', '10ppm', '20ppm', '100ppm', '1000ppm']

            var3 = ttk.StringVar(frame4)
            opcion = ttk.OptionMenu(frame4, var3, *opciones)
            opcion.config(width=15)
            opcion.grid(row = 0, column = 3)


            #CREATE INPUT
            Label(frame4, text = 'Flow Concentration(ppm)').grid(row = 1, column = 2)
            self.flow = Entry(frame4, bd=2)
            self.flow.focus()
            self.flow.grid(row = 1, column =  3)


            #CREATE INPUT
            Label(frame4, text = 'Number of cycles').grid(row = 2, column = 2)
            self.cycles = Entry(frame4, bd=2)
            self.cycles.grid(row = 2, column = 3)

            #CREATE INPUT
            Label(frame4, text = 'Start purge time(s)').grid(row = 3, column = 2)
            self.stime = Entry(frame4, bd=2)
            self.stime.grid(row = 3, column = 3)

            #CREATE INPUT
            Label(frame4, text = 'Cycle time(s)').grid(row = 4, column = 2)
            self.cytime = Entry(frame4, bd=2)
            self.cytime.grid(row = 4, column = 3)

            #CREATE INPUT
            Label(frame4, text = 'Final purge time(s)').grid(row = 5, column = 2)
            self.ftime = Entry(frame4, bd=2)
            self.ftime.grid(row = 5, column = 3)

            #CREATE INPUT
            Label(frame4, text = 'Behind cycle time(s)').grid(row = 6, column = 2)
            self.bcytime = Entry(frame4, bd=2)
            self.bcytime.grid(row = 6, column = 3)

            #BUTTON
            frame5 = LabelFrame(self.wind3).grid(row = 8, column = 0)
            ttk.Button(frame5, text = 'Start Mesaurements', command = lambda: self.startmesurement(var3.get(), self.flow.get(), self.cycles.get(), self.stime.get(), self.cytime.get(), self.ftime.get(), self.bcytime.get())).grid(row = 8, sticky = W + E)

        else:
            Label(lblimg, font="Helvetica 14 bold",text= filemsg).grid(row = 1, column = 2)

            frame5 = LabelFrame(self.wind3, text = 'System Error')
            frame5.grid(row =4, column = 0, sticky = W + E)

            ttk.Label(frame5,bg="red",font='Helvetica 14 bold', text = '\nCONTACT MINOS TECHNICIAN!\n').grid(row = 1, column=0, columnspan=3,padx=100)
            ttk.Button(frame5,text = 'Close', command = lambda: self.wind3.destroy()).grid(row = 2,column=0,columnspan=3)



    def startmesurement(self, bottle, flow, cycles, stime, cytime, ftime, bcytime):
        self.wind3.state(newstate='withdraw')
        multiscript.define(airnode,aircap,gasnodes,gascap,bottle,flow,cycles,stime,cytime,ftime,bcytime)
        multiscript.main()
        self.wind3.state(newstate='normal')


    def center(root):
        root.withdraw()
        root.update_idletasks()
        x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
        y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
        root.geometry("+%d+%d" % (x, y))
        root.deiconify()

    def identyall(node):
        global mferror,aircap,airunit,gascap,gasunit
        elflow = com.Control_FlowBus('/dev/ttyUSB0')
        try:
            numser = elflow.get_serial(node)
            if numser=="NA":
                raise ValueError

        except ValueError:
            mferror = True
        else:
            if node==airnode:
                aircap = int(elflow.get_capacity(node))
                airunit = str(elflow.get_unit(node))
            else:
                gascap.append(str(elflow.get_capacity(node)))
                gasunit.append(str(elflow.get_unit(node)))


    def openconfigure():
        elflow = com.Control_FlowBus('/dev/ttyUSB0')
        global mfall, mfconnected, airnode, gasnodes,mferror,filemsg
        try:
            f=open("config.txt")
        except FileNotFoundError:
            # doesn't exist
            filemsg="CONFIG.TXT NOT FOUND"
            mferror=True

        else:
            # exists
            lineas=f.readlines()
            f.close()

            for linea in lineas:
                nodes=linea.replace("\n", "").split(":")
                mf=nodes[1]
                mfall.append(mf)
                mfconnected+=1

            airnode=str(mfall[0])
            mfcontrol.identyall(airnode)

            for i in range(1,mfconnected):
                gasnodes.append(str(mfall[i]))
                mfcontrol.identyall(str(gasnodes[i-1]))


if __name__ == '__main__':
    window = ttk.Tk()
    mfcontrol.openconfigure()
    application = mfcontrol(window)
    mfcontrol.center(window)
    window.mainloop()
