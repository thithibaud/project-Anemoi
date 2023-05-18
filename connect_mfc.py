import tkinter as tk
from tkinter import ttk
import threading
import comunicacion as com
import os
import csv

MFCs = {}
elflow = com.Control_FlowBus('/dev/ttyUSB0')
#os.environ["data_config_filename"]= "MFC_data_config_20230517T1620_test.csv"

def find_MFCs(cancel_event):
    global MFCs
    total_nodes = 10
    for i in range(0, total_nodes):
        if cancel_event.is_set():
            break
        elif (i <=9):
            node = "0" + str(i)
        else:
            node = str(i)
        number = elflow.get_serial(node)
        if str(number) != "NA":
            print("node: " + node + "  SN: " + str(number))
            if number in MFCs.values():
                print("An instrument has duplicated nodes")
            else:
                MFCs.update({node: number})

        loading_bar["value"] = (i+1) * (100 / total_nodes)
        loading_bar.update()
        root.update()
        display_results()

    filename = os.environ.get("data_config_filename")
    with open(filename, "a",  newline="") as file:
        writer = csv.writer(file, dialect="excel")
        writer.writerow(["node then SN"])
        writer.writerow(MFCs.keys())
        writer.writerow(MFCs.values())
        writer.writerow(["number of MFC connected",len(MFCs)])
    finish()
    

def display_results():
    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)
    for node, number in MFCs.items():
        result_text.insert(tk.END, "Node: " + node + "  SN: " + str(number) + "\n")
    result_text.config(state="disabled")

def start_loading():
    loading_button.config(state="disabled")
    cancel_button.config(state="normal")
    retry_button.config(state="disabled")
    ok_button.config(state="disabled")
    loading_bar["value"] = 0
    cancel_event = threading.Event()
    threading.Thread(target=find_MFCs, args=(cancel_event,)).start()

def cancel_loading():
    cancel_button.config(state="disabled")
    loading_button.config(state="normal")
    retry_button.config(state="normal")
    ok_button.config(state="normal")
    loading_bar["value"] = 0
    MFCs.clear()
    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)

def finish():
    root.update()
    loading_button.config(state="disabled")
    cancel_button.config(state="disabled")
    retry_button.config(state="normal")
    ok_button.config(state="normal")

def ok():
    root.state(newstate='withdraw')
    command = 'python3 select_mfc.py'
    os.system(command)
    root.state(newstate='normal')

root = tk.Tk()
root.title("MFC Finder")

frame = ttk.Frame(root, padding="20")
frame.grid()

result_text = tk.Text(frame, width=40, height=10)
result_text.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

loading_bar = ttk.Progressbar(frame,length=300 , mode="determinate")
loading_bar.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

loading_button = ttk.Button(frame, text="Find MFCs", command=start_loading)
loading_button.grid(row=2, column=0, padx=5, pady=5)

cancel_button = ttk.Button(frame, text="Cancel", command=cancel_loading, state="disabled")
cancel_button.grid(row=2, column=1, padx=5, pady=5)

retry_button = ttk.Button(frame, text="Retry", command=cancel_loading, state="disabled")
retry_button.grid(row=3, column=0, padx=5, pady=5)

ok_button = ttk.Button(frame, text="OK", command=ok, state="disabled")
ok_button.grid(row=3, column=1, padx=5, pady=5)

root.mainloop()