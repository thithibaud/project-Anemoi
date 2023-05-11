
import tkinter as ttk
from tkinter import *

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


x_values = []
y_values = []
y2_values = []
mflow = []

flow = sys.argv[1]
cycles = sys.argv[2] 
stime = sys.argv[3]
cytime = sys.argv[4]
ftime = sys.argv[5]
bcytime = sys.argv[6]
index = sys.argv[7]

flow = int(flow)
cycles = int(cycles)
stime = int(stime)
cytime = int(cytime)
ftime = int(ftime)
bcytime = int(bcytime)
index = int(index)
airflow = 25

flow1 = 0
flow2 = 0


class controlsys:
    def __init__(self):
        plt.style.use('ggplot')

        ani = FuncAnimation(plt.gcf(), self.animate, 1000)

        print(mflow)

        plt.tight_layout()
        plt.show()


    def animate(self,i):
        self.upgrade()
        x_values.append(index)
        y_values.append(flow1)
        y2_values.append(flow2)
        plt.cla()
        plt.ylim(0,120)
        plt.plot(x_values, y_values, 'b')
        plt.plot(x_values, y2_values, 'g')
    
    def upgrade(self):
        global index, flow, flow1, flow2
        if index <= stime:
            flow1 = airflow
            flow2 = 0
        elif (stime <= index)and(index <= (stime+cytime)):
            flow1 = 0
            flow2 = flow
        else:
            flow1 = airflow
            flow2 = 0
        index+=1 


if __name__ == '__main__':
    application = controlsys()