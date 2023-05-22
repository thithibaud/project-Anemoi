import tkinter as tk
from tkinter import ttk

def save_data():
    bottle_concentration = bottle_conc_entry.get()
    flow_concentration = flow_conc_entry.get()
    num_cycles = num_cycles_entry.get()
    start_purge_time = start_purge_entry.get()
    cycle_time = cycle_time_entry.get()
    final_purge_time = final_purge_entry.get()
    behind_cycle_time = behind_cycle_entry.get()

    with open('data.txt', 'w') as f:
        f.write(f"Bottle Concentration: {bottle_concentration}\n")
        f.write(f"Flow Concentration: {flow_concentration}\n")
        f.write(f"Number of Cycles: {num_cycles}\n")
        f.write(f"Start Purge Time: {start_purge_time}\n")
        f.write(f"Cycle Time: {cycle_time}\n")
        f.write(f"Final Purge Time: {final_purge_time}\n")
        f.write(f"Behind Cycle Time: {behind_cycle_time}\n")

    print("Data saved successfully.")

root = tk.Tk()
root.title("Data Entry")
root.geometry("400x300")
root.config(bg="white")
style = ttk.Style(root)
style.theme_use("clam")

# Bottle Concentration
bottle_conc_label = ttk.Label(root, text="Bottle Concentration:")
bottle_conc_label.pack()
bottle_conc_entry = ttk.Entry(root)
bottle_conc_entry.pack()

# Flow Concentration
flow_conc_label = ttk.Label(root, text="Flow Concentration:")
flow_conc_label.pack()
flow_conc_entry = ttk.Entry(root)
flow_conc_entry.pack()

# Number of Cycles
num_cycles_label = ttk.Label(root, text="Number of Cycles:")
num_cycles_label.pack()
num_cycles_entry = ttk.Entry(root)
num_cycles_entry.pack()

# Start Purge Time
start_purge_label = ttk.Label(root, text="Start Purge Time:")
start_purge_label.pack()
start_purge_entry = ttk.Entry(root)
start_purge_entry.pack()

# Cycle Time
cycle_time_label = ttk.Label(root, text="Cycle Time:")
cycle_time_label.pack()
cycle_time_entry = ttk.Entry(root)
cycle_time_entry.pack()

# Final Purge Time
final_purge_label = ttk.Label(root, text="Final Purge Time:")
final_purge_label.pack()
final_purge_entry = ttk.Entry(root)
final_purge_entry.pack()

# Behind Cycle Time
behind_cycle_label = ttk.Label(root, text="Behind Cycle Time:")
behind_cycle_label.pack()
behind_cycle_entry = ttk.Entry(root)
behind_cycle_entry.pack()

# Save Button
save_button = ttk.Button(root, text="Save", command=save_data)
save_button.pack()

root.mainloop()
