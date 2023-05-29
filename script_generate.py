#!/usr/bin/env python3

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
root.title("Mass Flow Sensor script Configuration")
root.geometry("+200+200")

# Create a frame for the measurement section
measurement_frame = ttk.Frame(root, padding=5)
measurement_frame.grid(row=0, column=0)

# Create a frame for the configuration section
config_frame = ttk.Frame(root, padding=5)
config_frame.grid(row=1, column=0)

# Create a frame for the text
text_frame = ttk.Frame(root, padding=5)
text_frame.grid(row=1, column=1)

# Create a frame for the image and save button
image_frame = ttk.Frame(root, padding=5)
image_frame.grid(row=3, column=0, columnspan=2)

# Create an instance of Control_FlowBus
mfc = com.Control_FlowBus("/dev/ttyUSBPort2")

# Variables to hold widget references
measurement_label = {}
num_cycles_entry = None
start_purge_entry = None
cycle_time_entry = None
final_purge_entry = None
behind_cycle_entry = None
temperature_entry = None


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


def save_data(text_frame, text_field, run_button):
    num_cycles = num_cycles_entry.get()
    start_purge_time = start_purge_entry.get()
    cycle_time = cycle_time_entry.get()
    final_purge_time = final_purge_entry.get()
    behind_cycle_time = behind_cycle_entry.get()
    temperature = temperature_entry.get()

    saved_info = f"Number of Cycles : {num_cycles}\n"
    saved_info += f"Start Purge Time (in s): {start_purge_time}\n"
    saved_info += f"Cycle Time (in s): {cycle_time}\n"
    saved_info += f"Final Purge Time (in s): {final_purge_time}\n"
    saved_info += f"Behind Cycle Time (in s): {behind_cycle_time}\n"
    saved_info += f"Temperature (in celcius): {temperature}\n"

    # Write script in text file
    script_filename = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")),
    )
    script = open(script_filename, "w")
    script.write(saved_info)
    script.close()

    os.environ["script_filename"] = script_filename

    text_field.config(state="normal")

    # Clear the existing content of the text field
    text_field.delete("1.0", tk.END)

    # Display the saved information in the text field
    text_field.insert(tk.END, saved_info)

    text_field.config(state="disabled")

    run_button.config(state="normal")


def run_script():
    root.state(newstate="withdraw")
    command = "python3 script_run.py"
    os.system(command)
    root.state(newstate="normal")


def load_script(text_field, run_button):
    script_filename = filedialog.askopenfilename(
        defaultextension=".txt", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
    )
    if script_filename:
        os.environ["script_filename"] = script_filename

        text_field.config(state="normal")

        # Clear the existing content of the text field
        text_field.delete("1.0", tk.END)

        # Read the script content from the file
        with open(script_filename, "r") as file:
            script_content = file.read()

        # Display the script content in the text field
        text_field.insert(tk.END, script_content)

        text_field.config(state="disabled")

        run_button.config(state="normal")


# Function to load CSV data and create measurement labels
def load_csv_data(filename):
    with open(filename, "r") as file:
        reader = csv.reader(file)
        data = list(reader)
        try:
            num_sensors = int(data[4][1])  # Assuming the number is stored in row 5, column 2
        except ValueError:
            print("Invalid number of sensors in the CSV file.")

    # Create a list and dict to hold the nodes
    nodes = []
    dict_nodes = {}

    for i in range(6, 6 + num_sensors):
        nodes.append(data[i][0])
        dict_nodes[data[i][1]] = data[i][0]

    # Create the measurement labels
    for gas, node in dict_nodes.items():
        create_interface(node, gas)

    # Number of Cycles
    num_cycles_label = ttk.Label(config_frame, text="Number of Cycles:")
    num_cycles_label.grid(row=0, column=0)
    global num_cycles_entry
    num_cycles_entry = ttk.Entry(config_frame)
    num_cycles_entry.grid(row=0, column=1)

    # Start Purge Time
    start_purge_label = ttk.Label(config_frame, text="Start Purge Time (in s):")
    start_purge_label.grid(row=1, column=0)
    global start_purge_entry
    start_purge_entry = ttk.Entry(config_frame)
    start_purge_entry.grid(row=1, column=1)

    # Cycle Time
    cycle_time_label = ttk.Label(config_frame, text="Cycle Time (in s):")
    cycle_time_label.grid(row=2, column=0)
    global cycle_time_entry
    cycle_time_entry = ttk.Entry(config_frame)
    cycle_time_entry.grid(row=2, column=1)

    # Final Purge Time
    final_purge_label = ttk.Label(config_frame, text="Final Purge Time (in s):")
    final_purge_label.grid(row=4, column=0)
    global final_purge_entry
    final_purge_entry = ttk.Entry(config_frame)
    final_purge_entry.grid(row=4, column=1)

    # Behind Cycle Time
    behind_cycle_label = ttk.Label(config_frame, text="Behind Cycle Time (in s):")
    behind_cycle_label.grid(row=3, column=0)
    global behind_cycle_entry
    behind_cycle_entry = ttk.Entry(config_frame)
    behind_cycle_entry.grid(row=3, column=1)

    # Temperature
    temperature_label = ttk.Label(config_frame, text="Temperature (in celcius):")
    temperature_label.grid(row=5, column=0)
    global temperature_entry
    temperature_entry = ttk.Entry(config_frame)
    temperature_entry.grid(row=5, column=1)

    # Image title label
    image_title_label = ttk.Label(image_frame, text="Diagramme experiment:")
    image_title_label.pack()

    # Create the image label
    if num_sensors >= 3:
        image = tk.PhotoImage(file="image/diag2.png")
    else:
        image = tk.PhotoImage(file="image/diag.png")
    image_label = ttk.Label(image_frame, image=image)
    image_label.image = image  # Keep a reference to the image
    image_label.pack()

    # Text field
    text_label = ttk.Label(text_frame, text="Saved info:")
    text_label.pack()
    text_field = tk.Text(text_frame, height=10, width=40)
    text_field.config(state="disabled")
    text_field.pack()

    # Load Button
    load_button = ttk.Button(
        text_frame,
        text="Load",
        command=lambda: load_script(text_field, run_button),
    )
    load_button.pack(side=tk.LEFT)

    # Save Button
    save_button = ttk.Button(
        config_frame,
        text="Save",
        command=lambda: save_data(text_frame, text_field, run_button),
    )
    save_button.grid(row=6, column=1)

    # Run Button
    run_button = ttk.Button(text_frame, text="Run", command=lambda: run_script())
    run_button.config(state="disabled")
    run_button.pack(side=tk.LEFT)


# os variable
filename = os.environ.get("data_config_filename")
if not ((filename is not None) and os.path.exists(filename)):
    filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

if filename:
    load_csv_data(filename)

# Start the Tkinter event loop
root.mainloop()
