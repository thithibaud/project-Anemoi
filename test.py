import tkinter as tk
from tkinter import ttk

def update_options(*args):
    selected_option = var1.get()
    menu1['menu'].delete(0, 'end')
    menu2['menu'].delete(0, 'end')
    for option in options:
        if option != selected_option:
            menu1['menu'].add_command(label=option, command=tk._setit(var1, option))
            menu2['menu'].add_command(label=option, command=tk._setit(var2, option))

root = tk.Tk()
root.title("Dropdown Menus")

# Define the options
options = ['Option 1', 'Option 2', 'Option 3', 'Option 4']

# Create the variables to store the selected values
var1 = tk.StringVar(root)
var2 = tk.StringVar(root)

# Set the initial values
var1.set(options[0])
var2.set(options[0])

# Create the first dropdown menu
label1 = ttk.Label(root, text="Menu 1:")
label1.pack()
menu1 = ttk.OptionMenu(root, var1, *options, command=update_options)
menu1.pack()

# Create the second dropdown menu
label2 = ttk.Label(root, text="Menu 2:")
label2.pack()
menu2 = ttk.OptionMenu(root, var2, *options, command=update_options)
menu2.pack()

root.mainloop()
