import csv
import tkinter as tk
from tkinter import filedialog
import os

def load_csv():
    global filename
    filename = os.environ.get("data_config_filename")
    if not os.path.exists('filename'):
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
    root = tk.Tk()
    root.title("Mass Flow Sensor Configuration")

    # Create a list to hold the sensor-gas mappings
    mappings = []
    # Create labels and dropdowns for each sensor
    for i in range(num_sensors):
        label = tk.Label(root, text=f"Sensor {i+1} with SN {data[3][i]}:")
        label.grid(row=i, column=0, padx=5, pady=5)

        # gas options
        gas_options = ["SA"]  # Replace with your own gas options
        for j in range(num_sensors-1):
            gas_options.append(f"gas {j+1}")
        var = tk.StringVar(root)
        var.set(gas_options[0])  # Set default value to the first gas option
        dropdown = tk.OptionMenu(root, var, *gas_options)
        dropdown.grid(row=i, column=1, padx=5, pady=5)

        mappings.append((i+1, var))  # Store the sensor-gas mapping

    # Save button callback function
    def save_mappings():
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Sensor', 'Gas'])
            for sensor, var in mappings:
                writer.writerow([sensor, var.get()])
        root.destroy()

    # Save button
    save_button = tk.Button(root, text="Save Mappings", command=save_mappings)
    save_button.grid(row=num_sensors, columnspan=2, padx=5, pady=10)

    root.mainloop()

# Example usage
load_csv()
