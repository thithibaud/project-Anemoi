import tkinter as tk
import os

# Create a function to run the "manual.py" script
def run_manual():
    os.system('python manual.py')

# Create a function to run the "script.py" script
def run_script():
    os.system('python script.py')

# Create the main window
root = tk.Tk()
root.title("Script Launcher")

# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.pack(padx=20, pady=20)

# Create the "Manual" button and add it to the frame
manual_button = tk.Button(button_frame, text="Manual", command=run_manual)
manual_button.pack(side=tk.LEFT, padx=10)

# Create the "Script" button and add it to the frame
script_button = tk.Button(button_frame, text="Script", command=run_script)
script_button.pack(side=tk.LEFT, padx=10)

# Start the main loop
root.mainloop()
