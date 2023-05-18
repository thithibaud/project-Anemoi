import tkinter as tk
from tkinter import ttk
from comunicacion import Control_FlowBus  # Import the Control_FlowBus class from your Comunicacion module

class MFCInterface(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("MFC Interface")

        # Create an instance of Control_FlowBus
        self.mfc = Control_FlowBus('/dev/ttyUSB0')  

        # Create and configure the widgets
        self.measure_label = ttk.Label(self, text="Measure:")
        self.measure_value = ttk.Label(self, text="")
        self.setpoint_label = ttk.Label(self, text="Setpoint:")
        self.setpoint_entry = ttk.Entry(self, width=10)
        self.setpoint_button = ttk.Button(self, text="Set", command=self.set_setpoint)

        # Layout the widgets using the grid geometry manager
        self.measure_label.grid(row=0, column=0, padx=5, pady=5)
        self.measure_value.grid(row=0, column=1, padx=5, pady=5)
        self.setpoint_label.grid(row=1, column=0, padx=5, pady=5)
        self.setpoint_entry.grid(row=1, column=1, padx=5, pady=5)
        self.setpoint_button.grid(row=1, column=2, padx=5, pady=5)

        # Start a thread to update the measure value periodically
        self.update_measure()

    def update_measure(self):
        # Get the measure from the MFC
        measure = self.mfc.get_mesure('03')  # Replace '01' with the desired node number

        # Update the measure value label
        self.measure_value.config(text=measure)

        # Schedule the next update after 1 second (adjust the interval as needed)
        self.after(1000, self.update_measure)

    def set_setpoint(self):
        # Get the setpoint value from the entry widget
        setpoint = int(self.setpoint_entry.get())

        # Send the setpoint to the MFC
        self.mfc.send_setpoint('01', setpoint)  # Replace '01' with the desired node number

        # Clear the setpoint entry
        self.setpoint_entry.delete(0, tk.END)

# Create an instance of the MFCInterface class and start the Tkinter event loop
interface = MFCInterface()
interface.mainloop()
