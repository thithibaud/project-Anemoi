import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import sv_ttk
import threading
import comunicacion as com
import os
import csv

elflow = com.Control_FlowBus("/dev/ttyUSB0")
capacities = {}
units = {}
SNs = {}


def find_MFCs(cancel_event):
    global SNs
    total_nodes = 10
    for i in range(0, total_nodes):
        if cancel_event.is_set():
            break
        elif i <= 9:
            node = "0" + str(i)
        else:
            node = str(i)
        number = elflow.get_serial(node)
        global capacity, unit
        capacity = elflow.get_capacity(node)
        unit = elflow.get_unit(node)
        if str(number) != "NA":
            print(
                "node: "
                + node
                + "  SN: "
                + str(number)
                + " capacity: "
                + str(capacity)
                + unit
            )
            if number in SNs.values():
                print("An instrument has duplicated nodes")
            else:
                SNs.update({node: number})
                capacities.update({node: capacity})
                units.update({node: unit})

        loading_bar["value"] = (i + 1) * (100 / total_nodes)
        loading_bar.update()
        root.update()
        display_results()
    if len(SNs) == 0:
        error_message = "Error: MFC not found"
        tk.messagebox.showerror("Error", error_message)

    filename = os.environ.get("data_config_filename")
    if not ((filename is not None) and os.path.exists(filename)):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")),
        )

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file, dialect="excel")
        writer.writerow(["node then SN"])
        writer.writerow(SNs.keys())
        writer.writerow(SNs.values())
        writer.writerow(["number of MFC connected", len(SNs)])
    finish()


def display_results():
    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)
    for node, number in SNs.items():
        global capacity, unit
        result_text.insert(
            tk.END,
            "Node: "
            + node
            + "  SN: "
            + str(number)
            + " Capacity: "
            + str(capacities[node])
            + units[node]
            + "\n",
        )
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
    root.state(newstate="withdraw")
    command = "python3 select_mfc.py"
    os.system(command)
    root.state(newstate="normal")


root = tk.Tk()
sv_ttk.use_light_theme()
root.title("MFC Finder")
root.geometry("+200+200")

frame = ttk.Frame(root, padding="20")
frame.grid()

result_text = tk.Text(frame, width=50, height=10)
result_text.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

loading_bar = ttk.Progressbar(frame, length=400, mode="determinate")
loading_bar.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

loading_button = ttk.Button(frame, text="Find MFCs", command=start_loading)
loading_button.grid(row=2, column=0, padx=5, pady=5)

cancel_button = ttk.Button(
    frame, text="Cancel", command=cancel_loading, state="disabled"
)
cancel_button.grid(row=2, column=1, padx=5, pady=5)

retry_button = ttk.Button(frame, text="Retry", command=start_loading, state="disabled")
retry_button.grid(row=3, column=0, padx=5, pady=5)

ok_button = ttk.Button(frame, text="OK", command=ok, state="disabled")
ok_button.grid(row=3, column=1, padx=5, pady=5)

root.mainloop()
