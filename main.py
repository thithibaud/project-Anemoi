#!/usr/bin/env python3
import tkinter as tk
import tkinter.ttk as ttk
import os
from tkinter import messagebox
from tkinter import filedialog
import sv_ttk
import csv


def gen_csv(login,passwd):
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file, dialect="excel")
        writer.writerow([login,passwd])
        os.environ["data_config_filename"]=filename
        
class CredentialGUI:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title('MinoS MassFlow Controller login')

        # Creating the frames
        self.image_frame = tk.LabelFrame(self.parent)
        self.image_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.login_frame = tk.LabelFrame(self.parent, text='Login Information')
        self.login_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Adding the image
        image = tk.PhotoImage(file='image/logominos.png')
        image_label = tk.Label(self.image_frame, image=image)
        image_label.image = image
        image_label.pack()

        # Adding the login form
        tk.Label(self.login_frame, text='User ID:').grid(row=0, column=0, sticky='w')
        self.user_id_entry = tk.Entry(self.login_frame)
        self.user_id_entry.grid(row=0, column=1)

        tk.Label(self.login_frame, text='Password:').grid(row=1, column=0, sticky='w')
        self.password_entry = tk.Entry(self.login_frame, show='*')
        self.password_entry.grid(row=1, column=1)

        self.login_button = ttk.Button(self.login_frame, text='Login', command=self.run_login_script)
        self.login_button.grid(row=2, columnspan=2, pady=10)

    def run_login_script(self):
        # Disable the login button to prevent multiple submissions
        self.login_button.config(state='disabled')

        user_id = self.user_id_entry.get()
        password = self.password_entry.get()
        if (user_id == "admin" and password == "admin"):
            #generate CSV for config data
            gen_csv(user_id,password)
            # Check if instrument are connected before running it
            if os.path.exists('/dev/ttyUSB0'):
                root.state(newstate='withdraw')
                command = f'python3 connect_mfc.py'
                os.system(command)
                root.state(newstate='normal')
            else:
                error_message = 'Error: MFC not found or connected'
                tk.messagebox.showerror('Error', error_message)
        else:
            filename = "data/MFC_data_config.csv"
            os.environ["data_config_filename"]=filename
            os.environ["user_id"]=user_id
            os.environ["password"]=password
            root.state(newstate='withdraw')
            command = f'python3 select_mode.py'
            os.system(command)
            root.state(newstate='normal')
            
        # Re-enable the login button after the script has finished running
        self.login_button.config(state='normal')


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


if __name__ == '__main__':
    root = tk.Tk()
    sv_ttk.use_light_theme()
    gui = CredentialGUI(root)
    center_window(root)
    root.resizable(False, False) 
    root.mainloop()
