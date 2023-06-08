#!/usr/bin/env python3


from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import sv_ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import comunicacion as com
import os
import csv
import time

os.environ["QT_LOGGING_RULES"] = "qt5ct.debug=false"

# Create the main window
root = tk.Tk()
sv_ttk.use_light_theme()
root.title("Mass Flow Sensor Configuration")
root.geometry("+200+1")
# os variable
filename = os.environ.get("data_config_filename")
if filename is None or not os.path.exists(filename):
    filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

if filename:
    with open(filename, "r") as file:
        reader = csv.reader(file)
        data = list(reader)
        try:
            num_sensors = int(data[4][1])  # Assuming the number is stored in row 5, column 2
        except ValueError:
            print("Invalid number of sensors in the CSV file.")

# Create an instance of Control_FlowBus
mfc = com.Control_FlowBus("/dev/ttyUSBPort2")

# Create a list to hold the nodes
nodes = []
nodes.extend(data[i][0] for i in range(6, 6 + num_sensors))
print(nodes)

# Initialize the graph data
x_data = {}
y_data = {}
setpoint_data = {}
measurement = {}
setpoint = {}
measurement_label = {}
setpoint_slider = {}
current_setpoint_label = {}
desired_setpoint_label = {}
setpoint_input_entry = {}
start_time = None

# Initialize a flag for measurement updates
running = False


def start_measurement():
    global running, start_time
    running = True
    start_button.config(state="disabled")
    stop_button.config(state="normal")
    reset_button.config(state="disabled")
    save_button.config(state="disabled")
    start_time = time.time()
    measurement_updates()


def stop_measurement():
    global running
    running = False
    reset_setpoints()
    start_button.config(state="disabled")
    stop_button.config(state="disabled")
    reset_button.config(state="normal")
    save_button.config(state="normal")


def reset_measurement():
    global x_data, y_data, setpoint_data
    x_data = {}
    y_data = {}
    setpoint_data = {}
    for node in nodes:
        line[node].set_data([], [])
        setpoint_line[node].set_data([], [])
    ax1.relim()  # Recalculate limits
    ax1.autoscale_view(True, True, True)  # Autoscale the view
    canvas.draw()
    start_button.config(state="normal")
    stop_button.config(state="disabled")
    reset_button.config(state="disabled")
    save_button.config(state="disabled")


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


def measurement_updates():
    if running:
        for node in nodes:
            update_measurement((node,))  # node is passed as a single-element tuple
        root.after(1000, measurement_updates)


def update_measurement(node):
    if isinstance(node, tuple):
        node = node[0]
    # Get the current measurement and setpoint
    measurement[node] = mfc.get_measurement(str(node))
    setpoint[node] = mfc.get_setpoint(str(node))

    try:
        # Convert measurement and setpoint to float
        measurement_float = float(measurement[node])
        setpoint_float = float(setpoint[node])

        # Update the measurement label and setpoint slider
        measurement_label[node].config(text=f"Measurement: {measurement_float}")
        setpoint_slider[node].set(setpoint_float)

        # Update the setpoint labels
        current_setpoint_label[node].config(text=f"Current Setpoint: {setpoint_float:.2f}")
        desired_setpoint_label[node].config(text=f"Desired Setpoint: {setpoint_slider[node].get():.2f}")

        # Update time
        current_time = time.time() - start_time
        current_time = round(current_time)
        # Update the graph data
        if node not in x_data:
            x_data[node] = []
            y_data[node] = []
            setpoint_data[node] = []
        x_data[node].append(current_time)
        y_data[node].append(measurement_float)
        setpoint_data[node].append(setpoint_float)

        # Update the graph lines
        line[node].set_data(x_data[node], y_data[node])
        setpoint_line[node].set_data(x_data[node], setpoint_data[node])

        # Recalculate limits
        ax1.relim()
        ax2.relim()

        # Autoscale the view
        ax1.autoscale_view(True, True, True)
        ax2.autoscale_view(True, True, True)

        # Redraw the graph
        canvas.draw()
    except ValueError:
        print(f"Invalid measurement or setpoint value for node {node}")


def set_setpoint(node, setpoint):
    try:
        setpoint = float(setpoint)  # Convert setpoint to a float
        mfc.send_setpoint(str(node), setpoint)
    except ValueError:
        print("Invalid setpoint value.")


def set_setpoint_button(node, setpoint):
    try:
        setpoint = float(setpoint)  # Convert setpoint to a float
        mfc.send_setpoint(str(node), setpoint)
    except ValueError:
        print("Invalid setpoint value.")
    else:
        setpoint_input_entry[node].delete(0, tk.END)  # Clear the entry field if the setpoint was valid


def reset_setpoints():
    for node in nodes:
        set_setpoint(node, 0)  # Reset the setpoint to zero


def create_interface(node):
    # Create a frame for the measurement section
    measurement_frame = ttk.Frame(root, padding=3)
    measurement_frame.pack()

    # Get the capacity, unit and SN
    capacity = mfc.get_capacity(str(node))
    unit = mfc.get_unit(str(node))
    SN = mfc.get_serial(str(node))

    # Create a label to display the SN and node
    SN_node_label = ttk.Label(measurement_frame, text=f"MFC with SN: {SN} and node {node}")
    SN_node_label.pack()

    # Create labels for the desired setpoints
    desired_setpoint_label[node] = ttk.Label(measurement_frame, text="Desired Setpoint: ")
    desired_setpoint_label[node].pack()

    # Create a frame for the setpoint section
    setpoint_frame = ttk.Frame(root, padding=3)
    setpoint_frame.pack()

    # Create a label and slider for the setpoint
    setpoint_label = ttk.Label(setpoint_frame, text="Setpoint: ")
    setpoint_label.pack(side=tk.LEFT)
    setpoint_slider[node] = ttk.Scale(
        setpoint_frame,
        from_=0,
        to=100,
        orient=tk.HORIZONTAL,
        length=500,
        command=lambda value, node=node: set_setpoint(node, value),
    )
    setpoint_slider[node].pack(side=tk.LEFT)

    # Create a frame for the setpoint labels
    setpoint_labels_frame = ttk.Frame(root, padding=3)
    setpoint_labels_frame.pack()

    # Create a frame for the setpoint input
    setpoint_input_frame = ttk.Frame(root, padding=3)
    setpoint_input_frame.pack()

    # Create a label and entry for the setpoint input
    setpoint_input_label = ttk.Label(setpoint_input_frame, text="Input Setpoint: ")
    setpoint_input_label.pack(side=tk.LEFT)

    # Create the entry widget and store it in the dictionary
    setpoint_input_entry[node] = ttk.Entry(setpoint_input_frame)
    setpoint_input_entry[node].pack(side=tk.LEFT)

    # Create a button to set the setpoint to the input value
    setpoint_input_button = ttk.Button(
        setpoint_input_frame,
        text="Set",
        command=lambda: set_setpoint_button(node, setpoint_input_entry[node].get()),
    )
    setpoint_input_button.pack(side=tk.LEFT)

    # Create labels for the current setpoints
    current_setpoint_label[node] = ttk.Label(setpoint_labels_frame, text="Current Setpoint: ")
    current_setpoint_label[node].pack()

    # Create a label to display the measurement
    measurement_label[node] = ttk.Label(setpoint_labels_frame, text="Measurement: ")
    measurement_label[node].pack()


##    # Add the graph lines to the legend
##    ax.legend()


# Create a figure and two y-axes for the graph
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()  # Create a twin y-axis sharing the same x-axis with ax1

ax1.grid(True)  # Add grid to the plot

# Create the measurement labels and setpoint sliders
line = {}
setpoint_line = {}
for node in nodes:
    (line[node],) = ax1.plot([], [], label=f"Sensor {node}")
    (setpoint_line[node],) = ax2.plot([], [], label=f"Setpoint {node}", linestyle="--")

# Set labels for axes
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Measurement", color="tab:blue")
ax2.set_ylabel("Setpoint", color="tab:orange")

# Set colors for labels and ticks
ax1.tick_params(axis="y", labelcolor="tab:blue")
ax2.tick_params(axis="y", labelcolor="tab:orange")

# Add legends to each axis
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")


# Create the measurement labels and setpoint sliders
for node in nodes:
    create_interface(node)

# Embed the graph in the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Create a frame for the buttons
button_frame = ttk.Frame(root)
button_frame.pack(side=tk.BOTTOM)

# Create the start, stop,reset buttons and save button
start_button = ttk.Button(button_frame, text="Start", command=start_measurement, state="normal")
start_button.pack(side=tk.LEFT)

stop_button = ttk.Button(button_frame, text="Stop", command=stop_measurement, state="disabled")
stop_button.pack(side=tk.LEFT)

reset_button = ttk.Button(button_frame, text="Reset", command=reset_measurement, state="disabled")
reset_button.pack(side=tk.LEFT)

save_button = ttk.Button(button_frame, text="Save as CSV", command=save_to_csv, state="disabled")
save_button.pack(side=tk.LEFT)

# Schedule the start of the measurement update loop
root.after(1000, measurement_updates)

# Start the Tkinter event loop
root.mainloop()
