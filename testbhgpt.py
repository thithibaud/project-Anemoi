from bronkhorst import Bronkhorst
import binascii


bh = Bronkhorst('/dev/ttyUSB0', 00)
serial_number = bh.read_serial().encode('utf-8')  # Encode the command string to bytes
print("Serial number:", serial_number.decode('utf-8'))

