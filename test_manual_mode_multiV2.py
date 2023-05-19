import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import comunicacion as com

# Create an instance of Control_FlowBus
mfc = com.Control_FlowBus('/dev/ttyUSB0')

# Create a figure and axis for the graph
fig = plt.Figure(figsize=(6, 4), dpi=100)
graph_ax = fig.add_subplot(1, 1, 1)
line, = graph_ax.plot([], [], 'b-', label='Measurement')
setpoint_line, = graph_ax.plot([], [], 'r--', label='Setpoint')
graph_ax.set_xlabel('Time')
graph_ax.set_ylabel('Measurement')
graph_ax.legend()
graph_ax.grid(True)

# Initialize the graph data
x_data = []
y_data = []
setpoint_data = []

# Function to update the measurement value and graph
def update_measurement():
    # Get the current measurement and setpoint
    measurement = mfc.get_mesure("03")
    setpoint = mfc.get_setpoint("03")

    # Update the measurement label and setpoint slider
    measurement_label.config(text=f"Measurement: {measurement}")
    setpoint_slider.set(setpoint)

    # Update the setpoint labels
    current_setpoint_label.config(text=f"Current Setpoint: {setpoint:.2f}")
    desired_setpoint_label.config(text=f"Desired Setpoint: {setpoint_slider.get():.2f}")

    # Update the graph data
    x_data.append(len(x_data) + 1)
    y_data.append(float(measurement))
    setpoint_data.append(float(setpoint))

    # Update the graph lines
    line.set_data(x_data, y_data)
    setpoint_line.set_data(x_data, setpoint_data)
    graph_ax.relim()
    graph_ax.autoscale_view()

    # Redraw the graph
    canvas.draw()

    # Schedule the next update
    root.after(100, update_measurement)

# Function to set the setpoint
def set_setpoint(setpoint):
    setpoint = float(setpoint)  # Convert setpoint to a float
    mfc.send_setpoint("03", setpoint)

# Create the main window
root = tk.Tk()
root.title("MFC Control Panel")

# Create a frame for the measurement section
measurement_frame = ttk.Frame(root, padding=10)
measurement_frame.pack()

# Create a label to display the measurement
measurement_label = ttk.Label(measurement_frame, text="Measurement: ")
measurement_label.pack()

# Create a label to display the capacity and the unit
capacity = mfc.get_capacity('03')
unit = mfc.get_unit('03')
capa_unit_label = ttk.Label(measurement_frame, text=f"capacity:{capacity}{unit}")
capa_unit_label.pack()

# Create a frame for the setpoint section
setpoint_frame = ttk.Frame(root, padding=10)
setpoint_frame.pack()

# Create a label and slider for the setpoint
setpoint_label = ttk.Label(setpoint_frame, text="Setpoint: ")
setpoint_label.pack(side=tk.LEFT)
setpoint_slider = ttk.Scale(setpoint_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=set_setpoint,length=300)
setpoint_slider.pack(side=tk.LEFT)

# Create a frame for the setpoint labels
setpoint_labels_frame = ttk.Frame(root, padding=10)
setpoint_labels_frame.pack()

# Create labels for the current and desired setpoints
current_setpoint_label = ttk.Label(setpoint_labels_frame, text="Current Setpoint: ")
current_setpoint_label.pack()

desired_setpoint_label = ttk.Label(setpoint_labels_frame, text="Desired Setpoint: ")
desired_setpoint_label.pack()

# Embed the graph in the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Start the measurement update loop
root.after(100, update_measurement)

# Start the Tkinter event loop
root.mainloop()
