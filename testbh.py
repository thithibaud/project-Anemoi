import serial.tools.list_ports
import bronkhorst

def get_bronkhorst_controllers():
    # Get a list of all available serial ports
    ports = list(serial.tools.list_ports.comports())
    
    # Create an empty list to hold the Bronkhorst controllers
    controllers = []
    print(ports)
    # Iterate over all available serial ports
    for port in ports:
        try:
            # Try to connect to the port
            ser = serial.Serial(port.device, baudrate=38400, timeout=0.6)
            
            # Try to create a Bronkhorst controller object
            controller = bronkhorst.MassFlowController(ser)
            
            # If successful, add the controller to the list
            controllers.append(controller)
            print(controller)
            print(test)
            # Close the connection to the port
            ser.close()
        except:
            # If unsuccessful, continue to the next port
            continue
    
    # Return the list of Bronkhorst controllers
    return controllers
get_bronkhorst_controllers()
print(get_bronkhorst_controllers)
bronkhorst.MassFlowController("/dev/ttyUSB0")
