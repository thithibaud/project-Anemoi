import tkinter as tk
import tkinter.ttk as ttk
import sv_ttk
import os


# Create a function to run the "manual.py" script
def run_manual():
    root.state(newstate="withdraw")
    command = "python3 manual.py"
    os.system(command)
    root.state(newstate="normal")


# Create a function to run the "script.py" script
def run_script():
    root.state(newstate="withdraw")
    command = "python3 script_generate.py"
    os.system(command)
    root.state(newstate="normal")


# Create the main window
root = tk.Tk()
sv_ttk.use_light_theme()
root.title("Script Launcher")
root.geometry("+200+200")

# Create a frame for the buttons
button_frame = ttk.Frame(root)
button_frame.pack(padx=20, pady=20)

# Create the "Manual" button and add it to the frame
manual_button = ttk.Button(button_frame, text="Manual", command=run_manual)
manual_button.pack(side=tk.LEFT, padx=10)

# Create the "Script" button and add it to the frame
script_button = ttk.Button(button_frame, text="Script", command=run_script)
script_button.pack(side=tk.LEFT, padx=10)

# Start the main loop
root.mainloop()
