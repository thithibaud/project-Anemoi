from pymodbus.client.sync import ModbusSerialClient

# Create a Modbus client
client = ModbusSerialClient(method='rtu', port='/dev/ttyUSB0', baudrate=38400)

# Open the connection
connection = client.connect()

# Check if the connection is successful
if connection:
    print("MFC is connected!")

    # Read the serial number from the MFC
    result = client.read_holding_registers(address=92, count=20, unit=1)

    if result.isError():
        print("Failed to read serial number from MFC.")
    else:
        # Extract the serial number from the result
        serial_number = "".join([chr(i) for i in result.registers])

        # Print the serial number
        print("Serial Number: ", serial_number)

else:
    print("Connection failed.")

# Close the connection
client.close()


