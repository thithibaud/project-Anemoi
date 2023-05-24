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
root.title("Mass Flow Sensor script running")

# Create a frame for the measurement section
measurement_frame = ttk.Frame(root, padding=5)
measurement_frame.grid(row=0, column=0)

# Create a frame for the time section
time_frame = ttk.Frame(root, padding=5)
time_frame.grid(row=1, column=0)

# Create an instance of Control_FlowBus
mfc = com.Control_FlowBus('/dev/ttyUSB0')

# Variables to hold widget references
measurement_label = {}
num_cycles_entry = None
start_purge_entry = None
cycle_time_entry = None
final_purge_entry = None
behind_cycle_entry = None
dict_nodes = {}
# Function to load CSV data and create measurement labels
def load_csv_data(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
        try:
            num_sensors = int(data[4][1])  # Assuming the number is stored in row 5, column 2
        except ValueError:
            print("Invalid number of sensors in the CSV file.")

    # Create a list and dict to hold the nodes
    nodes = []
    global dict_nodes

    for i in range(6, 6 + num_sensors):
        nodes.append(data[i][0])
        dict_nodes[data[i][1]] = data[i][0]

    # Create the measurement labels
    for gas, node in dict_nodes.items():
        create_interface(node, gas)

def load_script_data(script_filename):
    script = open(script_filename, "r")
    data = script.read()
    script.close()

    # Extracting values from the script
    lines = data.split("\n")
    values = {}
    for line in lines:
        if line.strip():
            key, value = line.split(":")
            values[key.strip()] = int(value.strip())
    
    global num_cycles, start_purge_time, cycle_time, final_purge_time, behind_cycle_time
    
    # Assigning values to variables
    num_cycles = values["Number of Cycles"]
    start_purge_time = values["Start Purge Time (in s)"]
    cycle_time = values["Cycle Time (in s)"]
    final_purge_time = values["Final Purge Time (in s)"]
    behind_cycle_time = values["Behind Cycle Time (in s)"]

def create_interface(node, gas):
    # Create a label to display the measurement
    measurement_label[node] = ttk.Label(measurement_frame, text=f"MFC for {gas} ")
    measurement_label[node].pack()

    # Get the capacity and unit
    capacity = mfc.get_capacity(str(node))
    unit = mfc.get_unit(str(node))

    # Create a label to display the capacity and unit
    capa_unit_label = ttk.Label(measurement_frame, text=f"Capacity: {capacity} {unit}")
    capa_unit_label.pack()

# os variable
filename = os.environ.get("data_config_filename")
if not ((filename is not None) and os.path.exists(filename)):
    filename = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])

if filename:
    load_csv_data(filename)
# os variable
script_filename = os.environ.get("script_filename")
if not ((script_filename is not None) and os.path.exists(script_filename)):
    script_filename = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])

if script_filename:
    load_script_data(script_filename)    

# Start the Tkinter event loop
root.mainloop()
    
    
    