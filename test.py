import tkinter as tk

# define the available MFCs
mfc_list = {'Gas': ['SN123', 'SN234', 'SN345'], 'Air': ['SN456', 'SN567', 'SN678']}

# define the function to get the selected MFC
def get_selected_mfc():
    gas_or_air = var.get()
    serial_num = serial_num_var.get()
    selected_mfc = f"{gas_or_air} MFC with serial number {serial_num}"
    print(selected_mfc)

# create the GUI window
root = tk.Tk()
root.geometry('300x150')
root.title('MFC Selector')

# create the dropdown menu for selecting gas or air
var = tk.StringVar(root)
var.set('Gas')  # default value
dropdown = tk.OptionMenu(root, var, 'Gas', 'Air')
dropdown.pack(pady=10)

# create the dropdown menu for selecting the MFC serial number
serial_num_var = tk.StringVar(root)
serial_num_var.set(mfc_list['Gas'][0])  # default value
serial_num_dropdown = tk.OptionMenu(root, serial_num_var, *mfc_list[var.get()])
serial_num_dropdown.pack(pady=10)

# create the button to get the selected MFC
button = tk.Button(root, text='Select', command=get_selected_mfc)
button.pack(pady=10)

# run the GUI window
root.mainloop()
