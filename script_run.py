import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import sv_ttk
import comunicacion as com
import os
import csv
import time
from datetime import datetime
import pydps
import math

# Create the main window
root = tk.Tk()
sv_ttk.use_light_theme()
root.title("Mass Flow Sensor script running")
root.geometry("+200+200")

# dps Test Example
dps = pydps.dps_psu("/dev/ttyUSBPort1", 1)  # port name, slave address (in decimal)

# Create an instance of Control_FlowBus
mfc = com.Control_FlowBus("/dev/ttyUSBPort2")

# Create a frame for the measurement section
measurement_frame = ttk.Frame(root, padding=5)
measurement_frame.grid(row=0, column=0)

# Create a frame for the time section
time_frame = ttk.Frame(root, padding=5)
time_frame.grid(row=1, column=0)

# Create a frame for the text field
text_field_frame = ttk.Frame(root, padding=5)
text_field_frame.grid(row=2, column=0)

# Create a frame for the buttons
buttons_frame = ttk.Frame(root, padding=5)
buttons_frame.grid(row=3, column=0)

# Variables to hold widget references
measurement_label = {}
dict_nodes = {}
array_script = []
num_sensors = None
cancel_flag = False
script_index = 0
gas_number = 1
temperature = ""
x_data = {}
y_data = {}
setpoint_data = {}
measurement = {}
setpoint = {}
start_time = float(0)

# Adding this new variable outside any function
loading_bar_repeat = None

# set all MFCs to setpoint = 0
for node in dict_nodes:
    mfc.send_setpoint(str(node), float(00))


def load_csv_data(filename):
    global num_sensors

    with open(filename, "r") as file:
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
    
    return nodes


def load_script_data(script_filename):
    # sourcery skip: for-index-underscore, use-itertools-product
    with open(script_filename, "r") as script:
        data = script.read()
    global temperature
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
    behind_cycle_time = values["Behind Cycle Time (in s)"]
    final_purge_time = values["Final Purge Time (in s)"]
    temperature = values["Temperature (in celcius)"]

    global array_script, num_sensors

    list_operations = ["Start Purge Time"]
    list_times = [start_purge_time]

    for n in range(num_cycles):
        for i in range(num_sensors - 1):
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
    print(f"Temperature (in celcius):{temperature}")


def create_interface(node, gas):
    # Create a label to display the measurement
    measurement_label[node] = ttk.Label(measurement_frame, text=f"MFC for {gas} ")
    measurement_label[node].pack(padx=10, pady=10)

    # Get the capacity and unit
    capacity = mfc.get_capacity(str(node))
    unit = mfc.get_unit(str(node))

    # Create a label to display the capacity and unit
    capa_unit_label = ttk.Label(measurement_frame, text=f"Capacity: {capacity} {unit}")
    capa_unit_label.pack(padx=10, pady=10)


def start_script():
    global current_operation_label, array_script, script_index, cancel_flag, start_button, cancel_button, retry_button, start_time
    cancel_button.config(state="normal")
    retry_button.config(state="disabled")
    start_button.config(state="disabled")
    if script_index < len(array_script[0]) and not cancel_flag:
        current_operation = array_script[0][script_index]
        current_time = array_script[1][script_index]
        start_time = time.time()
        update_MFCs(current_operation)
        current_operation_label.config(text=f"Current Status: {current_operation}")
        loading_bar_update(current_time, start_time)
        remaining_time = (len(array_script[0]) - script_index - 1) * current_time
        total_time_remaning_label.config(text=f"Total Time Remaining: {remaining_time} seconds")
        total_operation_loading_bar.config(value=(script_index + 1) * 100 / len(array_script[0]))
        if root:
            script_index += 1
            root.after(current_time * 1000, start_script)
        if script_index < len(array_script[0]) - 1:
            next_operation = array_script[0][script_index + 1]
            next_operation_label.config(text=f"Next Operation: {next_operation}")
        else:
            next_operation_label.config(text="Next Operation: -")
        root.update()  # Update the GUI to reflect changes
    else:
        # Reset the cancel flag and enable the start button and disable the cancel button
        if loading_bar_repeat is not None and root:
            root.after_cancel(loading_bar_repeat)
        cancel_flag = False
        cancel_button.config(state="disabled")
        retry_button.config(state="normal")
        save_button.config(state="normal")  # Enable the retry and save button after operation
        # Set the current operation loading bar to 100 if the script is completed
        if script_index == len(array_script[0]):
            current_operation_loading_bar.config(value=100)


def loading_bar_update(time_current_operation, start_time):
    global loading_bar_repeat
    # Cancel the previously scheduled task
    if loading_bar_repeat is not None:
        root.after_cancel(loading_bar_repeat)
    current_time = time.time() - start_time
    current_operation_loading_bar.config(value=current_time * 100 / time_current_operation)
    # Check if the script has been cancelled or completed before scheduling the next update
    if not cancel_flag and script_index < len(array_script[0]):
        loading_bar_repeat = root.after(1000, lambda: loading_bar_update(time_current_operation, start_time))
    else:
        loading_bar_repeat = None  # Reset the reference after the task has been cancelled or completed


def cancel_script():
    global cancel_flag, start_button, cancel_button, retry_button, loading_bar_repeat
    cancel_flag = True
    loading_bar_repeat = None
    start_button.config(state="normal")  # Enable the start button
    cancel_button.config(state="disabled")  # Disable the cancel button
    retry_button.config(state="normal")  # Enable the retry button
    current_operation_label.config(text="Current Status: Cancelled")


def reset_script():
    global script_index, start_button, cancel_button, retry_button
    script_index = 0
    start_button.config(state="normal")
    cancel_button.config(state="disabled")
    retry_button.config(state="disabled")
    total_operation_loading_bar.config(value=0)
    current_operation_loading_bar.config(value=0)
    current_operation_label.config(text="Current Status: Ready")
    next_operation_label.config(text=f"Next Operation: {array_script[0][0]}")
    total_time_remaning_label.config(text=f"Total Time Remaining: {sum(array_script[1])} seconds")
    global x_data, y_data, setpoint_data
    x_data = {}
    y_data = {}
    setpoint_data = {}


def update_MFCs(current_operation):
    # sourcery skip: assign-if-exp, hoist-similar-statement-from-if, hoist-statement-from-if
    global dict_nodes, gas_number, num_sensors, temperature
    print(current_operation)
    if current_operation in [
        "Start Purge Time",
        "Behind Cycle Time",
        "Final Purge Time",
    ]:
        for gas, node in dict_nodes.items():
            if gas == "SA":
                setpoint = float(100)
                mfc.send_setpoint(str(node), setpoint)
                print(f"{gas} at node: {node} with setpoint: {mfc.get_setpoint(node)}")
            else:
                setpoint = float(00)
                mfc.send_setpoint(str(node), setpoint)
                print(f"{gas} at node: {node} with setpoint: {mfc.get_setpoint(node)}")
        update_temperature(25)
    else:
        for gas, node in dict_nodes.items():
            if gas == f"gas {gas_number}":
                setpoint = float(100)
                mfc.send_setpoint(str(node), setpoint)
                print(f"{gas} at node: {node} with setpoint: {mfc.get_setpoint(node)}")
            else:
                setpoint = float(00)
                mfc.send_setpoint(str(node), setpoint)
                print(f"{gas} at node: {node} with setpoint: {mfc.get_setpoint(node)}")
        gas_number += 1
        if gas_number >= num_sensors:
            gas_number = 1
        update_temperature(temperature)


def on_close():
    if loading_bar_repeat is not None:
        root.after_cancel(loading_bar_repeat)  # Stop the loading bar update
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)


# Function to update the current setpoint label
def update_current_measurments():
    global start_time
    for gas, node in dict_nodes.items():
        setpoint[node] = mfc.get_setpoint(str(node))
        measurement[node] = mfc.get_measurement(str(node))
        measurement_label[node].config(
            text=f"MFC for {gas}, Setpoint: {setpoint[node]},  Measurement :{measurement[node]}"
        )
        # Update time
        current_time = time.time() - start_time
        current_time = round(current_time)

        if node not in x_data:
            x_data[node] = []
            y_data[node] = []
            setpoint_data[node] = []
        x_data[node].append(current_time)
        y_data[node].append(measurement[node])
        setpoint_data[node].append(setpoint[node])
    root.after(1000, update_current_measurments)  # Update every 1 second


def update_temperature(temperature):  # sourcery skip: extract-duplicate-method
    # Function to update the temperature
    print(f"Updating temperature to {temperature} degrees Celsius")
    if temperature >= 30:
        current = 0.1303 * math.log(temperature) - 0.4116
        print(f"Current : {current}")
        dps.setVoltage(5)
        dps.setCurrent(current)
        dps.setOutput(True)
    else:
        dps.setVoltage(0)
        dps.setCurrent(0)
        dps.setOutput(False)

def save_to_csv():
    # Open save file dialog
    file = filedialog.asksaveasfile(
        parent=root,
        mode="w",
        defaultextension=".csv",
        filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")),
    )
    if file is None:  # If no file chosen, return
        return
    writer = csv.writer(file, dialect="excel")
    user_id = "login"
    try:
        user_id = os.environ["user_id"]
    except:
        print("no login saved")
    now = datetime.now()
    formated_now = now.strftime("%Y%m%dT%H%M")  # Date formated to follow ISO 8601
    writer.writerow([user_id, formated_now])  # Writing headers

    # Write headers for each node
    headers = []
    for node in nodes:
        headers.extend([f"{node} Time", f"{node} Measurement", f"{node} Setpoint"])
    writer.writerow(headers)

    # Find the maximum length of the arrays
    max_length = max(max(len(x_data[node]), len(y_data[node]), len(setpoint_data[node])) for node in nodes)

    for i in range(max_length):
        row_data = []
        for node in nodes:
            if i < len(x_data[node]):
                row_data.append(x_data[node][i])
            if i < len(y_data[node]):
                row_data.append(y_data[node][i])
            if i < len(setpoint_data[node]):
                row_data.append(setpoint_data[node][i])
        writer.writerow(row_data)

    file.close()


# os variable
# sourcery skip: assign-if-exp, introduce-default-else
filename = os.environ.get("data_config_filename")
if not ((filename is not None) and os.path.exists(filename)):
    filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

nodes = []
if filename:
    nodes = load_csv_data(filename)
# os variable
script_filename = os.environ.get("script_filename")
if not ((script_filename is not None) and os.path.exists(script_filename)):
    script_filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

if script_filename:
    load_script_data(script_filename)


current_operation_label = ttk.Label(time_frame, text="Current status:")
current_operation_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

current_operation_loading_bar = ttk.Progressbar(time_frame, length=400, mode="determinate")
current_operation_loading_bar.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

total_time_remaning_label = ttk.Label(time_frame, text="Total time remaining:")
total_time_remaning_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

total_operation_loading_bar = ttk.Progressbar(time_frame, length=400, mode="determinate")
total_operation_loading_bar.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

next_operation_label = ttk.Label(time_frame, text="Next operation:")
next_operation_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)


start_button = ttk.Button(buttons_frame, text="Start", command=start_script, state="normal")
start_button.grid(row=0, column=1, padx=5, pady=5)

cancel_button = ttk.Button(buttons_frame, text="Cancel", command=cancel_script, state="disabled")
cancel_button.grid(row=0, column=2, padx=5, pady=5)

retry_button = ttk.Button(buttons_frame, text="Retry", command=lambda: reset_script(), state="disabled")
retry_button.grid(row=0, column=3, padx=5, pady=5)

save_button = ttk.Button(
    buttons_frame, text="Save to CSV", command=lambda: save_to_csv(), state="disabled"
)
save_button.grid(row=0, column=4, padx=5, pady=5)

update_current_measurments()

# Start the Tkinter event loop
root.mainloop()
