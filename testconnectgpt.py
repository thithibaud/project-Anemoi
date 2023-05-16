import propar

# Connect to the local instrument, when no settings provided
# defaults to locally connected instrument (address=0x80, baudrate=38400)
instrument = propar.instrument('/dev/ttyUSB0')

# Measure and setpoint in output units.
instrument.writeParameter(100, 0)
print(instrument.readParameter(100))
for i in range(1,255):
    print(instrument.readParameter(i))
    print(i)
