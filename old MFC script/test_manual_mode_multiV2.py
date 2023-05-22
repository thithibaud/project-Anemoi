import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import comunicacion as com

# Create instances of Control_FlowBus for each MFC
mfc_03 = com.Control_FlowBus('/dev/ttyUSB0')
mfc_04 = com.Control_FlowBus('/dev/ttyUSB0')
mfc_05 = com.Control_FlowBus('/dev/ttyUSB0')

# Create a figure and axis for the graph
fig = plt.Figure(figsize=(6, 4), dpi=100)
graph_ax = fig.add_subplot(1, 1, 1)
lines = {}  # Dictionary to store the graph lines for each MFC
graph_ax.set_xlabel('Time')
graph_ax.set_ylabel('Measurement')

# Initialize the graph data for each MFC
graph_data = {
    "03": {"x": [], "y": []},
    "04": {"x": [], "y": []},
    "05": {"x": [], "y": []}
}

# Create a dictionary to store the setpoint values for each MFC
setpoint_values = {
    "03": 50,
    "04": 50,
    "05": 50
}

# Function to update the measurement value and graph for a specific MFC
def update_measurement(node):
    # Check if the node exists in the graph_data dictionary
    if node not in graph_data:
        graph_data[node] = {"x": [], "y": []}
    measurement = mfc.get_mesure(node)

    # Update the measurement label for the MFC
    measurement_label = measurement_labels[node]
    measurement_label.config(text=f"Measurement ({node}): {measurement}")

    # Update the graph data for the MFC
    graph_data[node]["x"].append(len(graph_data[node]["x"]) + 1)
    graph_data[node]["y"].append(float(measurement))

    # Update the graph line for the MFC
    lines[node].set_data(graph_data[node]["x"], graph_data[node]["y"])
    graph_ax.relim()
    graph_ax.autoscale_view()

    # Redraw the graph
    canvas.draw()

    # Schedule the next update for the MFC
    root.after(500, update_measurement, node)

# Function to handle setpoint changes
def set_setpoint(node):
    # Get the setpoint value from the setpoint_values dictionary
    setpoint = setpoint_values[node]

    # Update the setpoint for the MFC
    if node == "03":
        mfc_03.send_setpoint(node, setpoint)
    elif node == "04":
        mfc_04.send_setpoint(node, setpoint)
    elif node == "05":
        mfc_05.send_setpoint(node, setpoint)

# Function to update the setpoint value in the setpoint_values dictionary
def update_setpoint(node, value):
    setpoint_values[node] = value

# Create the main window
root = tk.Tk()
root.title("MFC Control")

# Create a frame for the measurement section
measurement_frame = ttk.Frame(root, padding=10)
measurement_frame.pack()

# Create measurement labels for each MFC
measurement_labels = {}
for node in ["03", "04", "05"]:
    label = ttk.Label(measurement_frame, text=f"Measurement ({node}):")
    label.pack()
    measurement_labels[node] = label

# Create a frame for the setpoint section
setpoint_frame = ttk.Frame(root, padding=10)
setpoint_frame.pack()

# Create setpoint sliders and labels for each MFC
setpoint_sliders = {}
setpoint_labels = {}
for node in ["03", "04", "05"]:
    slider_label = ttk.Label(setpoint_frame, text=f"Setpoint ({node}):")
    slider_label.pack()

    slider = ttk.Scale(setpoint_frame, from_=0, to=100, length=200, orient="horizontal",
                       command=lambda value, node=node: update_setpoint(node, int(value)))
    slider.set(setpoint_values[node])
    slider.pack()

    setpoint_sliders[node] = slider

    setpoint_label = ttk.Label(setpoint_frame, text=f"Current Setpoint ({node}):")
    setpoint_label.pack()
    setpoint_labels[node] = setpoint_label

    # Bind the set_setpoint function to the slider's release event
    slider.bind("<ButtonRelease-1>", lambda event, node=node: set_setpoint(node))

# Create a frame for the graph
graph_frame = ttk.Frame(root, padding=10)
graph_frame.pack()

# Create a canvas for the graph
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack()

# Start the measurement update loop for each MFC
root.after(1000, update_measurement, "03")
root.after(1000, update_measurement, "04")
root.after(1000, update_measurement, "05")

# Start the Tkinter event loop
root.mainloop()
