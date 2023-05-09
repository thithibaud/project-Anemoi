#!/usr/bin/env python3
import tkinter as tk
import tkinter.ttk as ttk
import os
from tkinter import messagebox

class CredentialGUI:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title('MinoS MassFlow Controller Login')

        # Creating the frames
        self.image_frame = tk.LabelFrame(self.parent, bg='#ffffff', highlightbackground='#cccccc', highlightcolor='#cccccc', highlightthickness=1, padx=10, pady=10)
        self.image_frame.grid(row=0, column=0, columnspan=2)

        self.login_frame = tk.LabelFrame(self.parent, text='Login Information', font=('Helvetica', 12), fg='#333333', bg='#ffffff', highlightbackground='#cccccc', highlightcolor='#cccccc', highlightthickness=1, padx=10, pady=10)
        self.login_frame.grid(row=1, column=0, columnspan=2)

        # Adding the image
        image = tk.PhotoImage(file='image/logominos.png')
        image_label = tk.Label(self.image_frame, image=image, bg='#ffffff')
        image_label.image = image
        image_label.pack(padx=10, pady=10)

        # Adding the login form
        tk.Label(self.login_frame, text='User ID:', font=('Helvetica', 12), fg='#333333', bg='#ffffff').grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.user_id_entry = tk.Entry(self.login_frame, font=('Helvetica', 12), bg='#f0f0f0', fg='#333333', highlightbackground='#cccccc', highlightcolor='#cccccc', highlightthickness=1)
        self.user_id_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.login_frame, text='Password:', font=('Helvetica', 12), fg='#333333', bg='#ffffff').grid(row=1, column=0, sticky='w', padx=10, pady=10)
        self.password_entry = tk.Entry(self.login_frame, show='*', font=('Helvetica', 12), bg='#f0f0f0', fg='#333333', highlightbackground='#cccccc', highlightcolor='#cccccc', highlightthickness=1)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        self.login_button = ttk.Button(self.login_frame, text='Login', command=self.run_login_script)
        self.login_button.grid(row=2, columnspan=2, pady=10)

    def run_login_script(self):

                                    
