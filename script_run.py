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

# Create a frame for the buttons
buttons_frame = ttk.Frame(root, padding=5)
buttons_frame.grid(row=2, column=0)


# Create an instance of Control_FlowBus
mfc = com.Control_FlowBus('/dev/ttyUSB0')

# Variables to hold widget references
measurement_label = {}
dict_nodes = {}
array_script =[]
num_sensors = None
cancel_flag = False
script_index = 0

# Function to load CSV data and create measurement labels
def load_csv_data(filename):
    
    global num_sensors
    
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
    
    # Assigning values to variables
    num_cycles = values["Number of Cycles"]
    start_purge_time = values["Start Purge Time (in s)"]
    cycle_time = values["Cycle Time (in s)"]
    final_purge_time = values["Final Purge Time (in s)"]
    behind_cycle_time = values["Behind Cycle Time (in s)"]
    
#     print("Number of Cycles:", num_cycles)
#     print("Start Purge Time:", start_purge_time)
#     print("Cycle Time:", cycle_time)
#     print("Final Purge Time:", final_purge_time)
#     print("Behind Cycle Time:", behind_cycle_time)
    
    global array_script, num_sensors
    
    list_operations = ["Start Purge Time"]
    list_times = [start_purge_time]
    
    for n in range(0,num_cycles):
        for i in range(num_sensors-1):
            list_operations.append("Cycle Time")
            list_times.append(cycle_time)
            list_operations.append("Behind Cycle Time")
            list_times.append(behind_cycle_time)
    
    list_operations.append("Final Purge Time")
    list_times.append(final_purge_time)
    
    array_script.append(list_operations)
    array_script.append(list_times)
    print(array_script)
    print(dict_nodes)
    
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

def start_script():
    global current_operation_label, array_script, script_index
    if script_index < len(array_script[0]):
        current_operation = array_script[0][script_index]
        current_time = array_script[1][script_index]
        start_time = time.time()
        current_operation_label.config(text=f"Current Status: {current_operation}")
        loading_bar_update(current_time,start_time)
        remaining_time = (len(array_script[0]) - script_index - 1) * current_time
        total_time_remaning_label.config(text=f"Total Time Remaining: {remaining_time} seconds")
        total_operation_loading_bar.config(value=(script_index + 1) * 100 / len(array_script[0]))
        if script_index < len(array_script[0]) - 1:
            next_operation = array_script[0][script_index + 1]
            next_operation_label.config(text=f"Next Operation: {next_operation}")
        else:
            next_operation_label.config(text="Next Operation: -")
        root.update()  # Update the GUI to reflect changes
        script_index += 1
        root.after(current_time * 1000, start_script)  # Schedule the next iteration after current_time seconds

def loading_bar_update(time_current_operation, start_time):
    current_time = time.time() - start_time
    current_operation_loading_bar.config(value=current_time * 100 / time_current_operation)
    root.after(1000, lambda: loading_bar_update(time_current_operation, start_time))
    
def cancel_script():
    global cancel_flag
    cancel_flag = True

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

current_operation_label = ttk.Label(time_frame, text="Current status :")
current_operation_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

current_operation_loading_bar = ttk.Progressbar(time_frame,length=400 , mode="determinate")
current_operation_loading_bar.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

total_time_remaning_label = ttk.Label(time_frame, text="total time remaning :")
total_time_remaning_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

total_operation_loading_bar = ttk.Progressbar(time_frame,length=400 , mode="determinate")
total_operation_loading_bar.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

next_operation_label = ttk.Label(time_frame,text="Next operation :")
next_operation_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

start_button = ttk.Button(buttons_frame, text="Start", command=start_script, state="normal")
start_button.grid(row=0, column=1, padx=5, pady=5)

cancel_button = ttk.Button(buttons_frame, text="Cancel", command=cancel_script, state="disabled")
cancel_button.grid(row=0, column=2, padx=5, pady=5)

retry_button = ttk.Button(buttons_frame, text="Retry", command=start_script, state="disabled")
retry_button.grid(row=0, column=3, padx=5, pady=5)

# Start the Tkinter event loop
root.mainloop()
    
    
    