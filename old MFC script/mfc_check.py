import os
import subprocess
import tkinter as tk

# Check if MFC is connected
mfc_connected = False
try:
    with open('/dev/ttyUSB0', 'r') as mfc:
        mfc_connected = True
except:
    pass

# Create GUI window
window = tk.Tk()
window.title('MFC Check')

# Define function to retry if MFC is not connected
def retry():
    window.destroy()
    os.system('python mfc_check.py')

# Display appropriate message and button based on MFC connection status
if mfc_connected:
    # Launch massflow.py if MFC is connected
    subprocess.Popen(['python', 'massflow.py'])
    message = 'MFC connected.\nLaunching massflow.py...'
else:
    # Display error message and retry button if MFC is not connected
    message = 'MFC not connected.\nPlease check the connection and try again.'
    retry_button = tk.Button(window, text='Retry', command=retry)
    retry_button.pack(pady=10)

message_label = tk.Label(window, text=message, font=('Arial', 16))
message_label.pack(pady=50)

# Run GUI window
window.mainloop()
