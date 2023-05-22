import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import comunicacion as com
import os
import csv

global filename
filename = os.environ.get("data_config_filename")
if not ((filename is not None) and os.path.exists(filename)):
    filename = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])

if filename:
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        global data
        data = list(reader)
        try:
            num_sensors = int(data[4][1])  # Assuming the number is stored in row 5, column 2
        except ValueError:
            print("Invalid number of sensors in the CSV file.")


#Create an instance of Control_FlowBus
mfc = com.Control_FlowBus('/dev/ttyUSB0')

# Create a list to hold the nodes
nodes = []
for i in range(6, 6 + num_sensors):
    nodes.append(data[i][0])
print(nodes)

# Initialize the graph data
for  in nodes:
	x_data[node] = []
	y_data[node] = []
	setpoint_data[node] = []
	
def update_measurement(node):
    # Get the current measurement and setpoint
    measurement[node] = mfc.get_mesure(str(node))
    setpoint[node] = mfc.get_setpoint(str(node))

    # Update the measurement label and setpoint slider
    measurement_label[node].config(text=f"Measurement: {measurement[node]}")
    setpoint_slider[node].set(setpoint[node])

    # Update the setpoint labels
    current_setpoint_label[node].config(text=f"Current Setpoint: {setpoint[node]:.2f}")
    desired_setpoint_label[node].config(text=f"Desired Setpoint: {setpoint_slider[node].get():.2f}")

    # Update the graph data
    x_data[node].append(len(x_data[node]) + 1)
    y_data[node].append(float(measurement[node]))
    setpoint_data[node].append(float(setpoint[node]))

    # Update the graph lines
    line[node].set_data(x_data[node], y_data[node])
    setpoint_line[node].set_data(x_data[node], setpoint_data[node])
    graph_ax[node].relim()
    graph_ax[node].autoscale_view()

    # Redraw the graph
    canvas.draw()

    # Schedule the next update
    root.after(200, update_measurement,node)
def create_interface(node):
	# Create a label to display the measurement
	measurement_label = ttk.Label(measurement_frame, text="Measurement: ")
	measurement_label.pack()

	# Create a label to display the capacity and the unit
	capacity = mfc.get_capacity('03')
	unit = mfc.get_unit('03')
	capa_unit_label = ttk.Label(measurement_frame, text=f"capacity:{capacity}{unit}")
	capa_unit_label.pack()

	# Create a frame for the setpoint section
	setpoint_frame = ttk.Frame(root, padding=10)
	setpoint_frame.pack()

	# Create a label and slider for the setpoint
	setpoint_label = ttk.Label(setpoint_frame, text="Setpoint: ")
	setpoint_label.pack(side=tk.LEFT)
	setpoint_slider = ttk.Scale(setpoint_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=set_setpoint,length=300)
	setpoint_slider.pack(side=tk.LEFT)

	# Create a frame for the setpoint labels
	setpoint_labels_frame = ttk.Frame(root, padding=10)
	setpoint_labels_frame.pack()

	# Create labels for the current and desired setpoints
	current_setpoint_label = ttk.Label(setpoint_labels_frame, text="Current Setpoint: ")
	current_setpoint_label.pack()

	desired_setpoint_label = ttk.Label(setpoint_labels_frame, text="Desired Setpoint: ")
	desired_setpoint_label.pack()

# Create the main window
root = tk.Tk()
root.title("Mass Flow Sensor Configuration")

# Embed the graph in the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Start the measurement update loop
root.after(100, update_measurement)

# Start the Tkinter event loop
root.mainloop()
