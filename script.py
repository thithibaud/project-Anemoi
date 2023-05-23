import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import sv_ttk
import comunicacion as com
import os
import csv
import time
from datetime import datetime

# Create the main window
root = tk.Tk()
sv_ttk.use_light_theme()
root.title("Mass Flow Sensor Configuration")

def create_interface(node,gas):
    # Create a frame for the measurement section
    measurement_frame = ttk.Frame(root, padding=5)
    measurement_frame.pack()

    # Create a label to display the measurement
    measurement_label[node] = ttk.Label(measurement_frame, text=f"MFC for {gas} ")
    measurement_label[node].pack()

    # Get the capacity and unit
    capacity = mfc.get_capacity(str(node))
    unit = mfc.get_unit(str(node))

    # Create a label to display the capacity and unit
    capa_unit_label = ttk.Label(measurement_frame, text=f"Capacity: {capacity} {unit}")
    capa_unit_label.pack()

def save_data():
    num_cycles = num_cycles_entry.get()
    start_purge_time = start_purge_entry.get()
    cycle_time = cycle_time_entry.get()
    final_purge_time = final_purge_entry.get()
    behind_cycle_time = behind_cycle_entry.get()
    
#os variable
filename = os.environ.get("data_config_filename")
if not ((filename is not None) and os.path.exists(filename)):
    filename = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])

if filename:
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
        try:
            num_sensors = int(data[4][1])  # Assuming the number is stored in row 5, column 2
        except ValueError:
            print("Invalid number of sensors in the CSV file.")

#init
measurement_label = {}
# Create an instance of Control_FlowBus
mfc = com.Control_FlowBus('/dev/ttyUSB0')
# Create a list and dict to hold the nodes
nodes = []
dict_nodes = {}

for i in range(6, 6 + num_sensors):
    nodes.append(data[i][0])
    dict_nodes[data[i][1]] = data[i][0]
print(nodes)
print(dict_nodes)

# Create the measurement labels
for gas, node in dict_nodes.items():
    create_interface(node,gas)

# Number of Cycles
num_cycles_label = ttk.Label(root, text="Number of Cycles:")
num_cycles_label.pack()
num_cycles_entry = ttk.Entry(root)
num_cycles_entry.pack()

# Start Purge Time
start_purge_label = ttk.Label(root, text="Start Purge Time:")
start_purge_label.pack()
start_purge_entry = ttk.Entry(root)
start_purge_entry.pack()

# Cycle Time
cycle_time_label = ttk.Label(root, text="Cycle Time:")
cycle_time_label.pack()
cycle_time_entry = ttk.Entry(root)
cycle_time_entry.pack()

# Final Purge Time
final_purge_label = ttk.Label(root, text="Final Purge Time:")
final_purge_label.pack()
final_purge_entry = ttk.Entry(root)
final_purge_entry.pack()

# Behind Cycle Time
behind_cycle_label = ttk.Label(root, text="Behind Cycle Time:")
behind_cycle_label.pack()
behind_cycle_entry = ttk.Entry(root)
behind_cycle_entry.pack()

# Create the image label
image = tk.PhotoImage(file='image/diag.png')
image_label = ttk.Label(root,image = image)
image_label.pack()

# Save Button
save_button = ttk.Button(root, text="Save", command=save_data)
save_button.pack()

# Start the Tkinter event loop
root.mainloop()
