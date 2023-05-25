import tkinter as tk
from tkinter import ttk
import comunicacion as com
import time
elflow= com.Control_FlowBus('/dev/ttyUSB0')
while True:
	print(elflow.get_measurement("03"))
	print(elflow.get_setpoint("03"))
	print(elflow.get_serial("03"))
	print(elflow.get_capacity("03"))
	print(elflow.get_unit("03"))
	time.sleep(2)
