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
root.title("Mass Flow Sensor Script Running")

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

# Create an instance of Control_FlowBus
mfc = com.Control_FlowBus("/dev/ttyUSB0")

# Variables to hold widget references
measurement_label = {}
setpoint_slider = {}
measurement = {}
setpoint = {}
data_points = []  # Array to save all data points


# Function to load CSV data and create measurement labels
def load_csv_data(filename):
    with open(filename, "r") as file:
        reader = csv.reader(file)
        data = list(reader)
        try:
            num_sensors = int(data[4][1])  # Assuming the number is stored in row 5, column 2
        except ValueError:
            print("Invalid number of sensors in the CSV file.")

    # Create a list to hold the nodes
    nodes = []
    for i in range(6, 6 + num_sensors):
        nodes.append(data[i][0])

    # Create the measurement labels and setpoint sliders
    for node in nodes:
        create_interface(node)


# Function to create interface for each MFC
def create_interface(node):
    # Create a label to display the measurement
    measurement_label[node] = ttk.Label(measurement_frame, text=f"MFC {node}")
    measurement_label[node].pack()

    # Get the capacity and unit
    capacity = mfc.get_capacity(str(node))
    unit = mfc.get_unit(str(node))

    # Create a label to display the capacity and unit
    capa_unit_label = ttk.Label(measurement_frame, text=f"Capacity: {capacity} {unit}")
    capa_unit_label.pack()

    # Create a label and slider for the setpoint
    setpoint_label = ttk.Label(measurement_frame, text="Setpoint: ")
    setpoint_label.pack()

    setpoint_slider[node] = ttk.Scale(
        measurement_frame,
        from_=0,
        to=100,
        orient=tk.HORIZONTAL,
        length=200,
        command=lambda value, node=node: set_setpoint(node, value),
    )
    setpoint_slider[node].pack()


# Function to set the setpoint for an MFC
def set_setpoint(node, setpoint):
    try:
        setpoint = float(setpoint)  # Convert setpoint to a float
        mfc.send_setpoint(str(node), setpoint)
    except ValueError:
        print("Invalid setpoint value.")


# Function to start the measurement
def start_measurement():
    global data_points
    data_points = []  # Clear the data points array
    start_button.config(state="disabled")
    stop_button.config(state="normal")
    save_button.config(state="disabled")
    measurement_updates()


# Function to stop the measurement
def stop_measurement():
    start_button.config(state="normal")
    stop_button.config(state="disabled")
    save_button.config(state="normal")


# Function to update the measurement values
def measurement_updates():
    for node in measurement_label:
        update_measurement(node)
    root.after(1000, measurement_updates)


# Function to update the measurement value for a node
def update_measurement(node):
    measurement[node] = mfc.get_measurement(str(node))
    setpoint[node] = setpoint_slider[node].get()
    measurement_label[node].config(text=f"Measurement: {measurement[node]}")
    data_points.append((datetime.now(), node, measurement[node], setpoint[node]))


# Function to save the data points to a CSV file
def save_to_csv():
    # Open the save file dialog
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if filename:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Node", "Measurement", "Setpoint"])  # Write headers
            for data_point in data_points:
                writer.writerow(data_point)


# Load CSV data and create measurement labels
filename = os.environ.get("data_config_filename")
if not ((filename is not None) and os.path.exists(filename)):
    filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

if filename:
    load_csv_data(filename)

# Create the start, stop, and save buttons
start_button = ttk.Button(buttons_frame, text="Start", command=start_measurement, state="normal")
start_button.grid(row=0, column=0, padx=5, pady=5)

stop_button = ttk.Button(buttons_frame, text="Stop", command=stop_measurement, state="disabled")
stop_button.grid(row=0, column=1, padx=5, pady=5)

save_button = ttk.Button(buttons_frame, text="Save to CSV", command=save_to_csv, state="disabled")
save_button.grid(row=0, column=2, padx=5, pady=5)

# Start the Tkinter event loop
root.mainloop()
