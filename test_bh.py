from bronkhorst import *

##mfc = Bronkhorst
##
##print (mfc)
##print (mfc.read_serial(00))
##
##from bronkhorst import Bronkhorst

# Create an instance of the Bronkhorst class
mfc = Bronkhorst('/dev/ttyUSB0', 100)

# Call the read_serial() method to retrieve the serial number
serial_number = mfc.read_serial()

# Print the serial number
print("Serial number:", serial_number)
