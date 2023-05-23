import csv
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import sv_ttk
import os

root = tk.Tk()
sv_ttk.use_light_theme()
root.title("Mass Flow Sensor Configuration")

def load_csv():
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
                create_interface(num_sensors)
            except ValueError:
                print("Invalid number of sensors in the CSV file.")

def create_interface(num_sensors):
    # Create a list to hold the sensor-gas mappings
    mappings = []
    # Create labels and dropdowns for each sensor
    for i in range(num_sensors):
        label = ttk.Label(root, text=f"Sensor {i+1} with SN {data[3][i]}:")
        label.grid(row=i, column=0, padx=5, pady=5)

        # gas options
        gas_options = ["SA"]  # Replace with your own gas options
        for j in range(num_sensors-1):
            gas_options.append(f"gas {j+1}")
        var = tk.StringVar(root)
        var.set(gas_options[0])  # Set default value to the first gas option
        dropdown = ttk.OptionMenu(root, var, *gas_options)
        dropdown.grid(row=i, column=1, padx=5, pady=5)

        mappings.append((data[2][i], var))  # Store the node-gas mapping

    # Save button callback function
    def ok():
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Sensor node', 'Gas'])
            for sensor, var in mappings:
                writer.writerow([sensor, var.get()])
        root.state(newstate='withdraw')
        command = 'python3 select_mode.py'
        os.system(command)
        root.state(newstate='normal')

    # Save button
    ok_button = ttk.Button(root, text="OK", command=ok)
    ok_button.grid(row=num_sensors, columnspan=2, padx=5, pady=10)

    root.mainloop()

# Example usage
load_csv()
