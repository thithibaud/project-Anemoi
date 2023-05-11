import propar

# Connect to the local instrument, when no settings provided
# defaults to locally connected instrument (address=0x80, baudrate=38400)
instrument = propar.instrument('/dev/ttyUSB0')

# Measure and setpoint in output units.
instrument.writeParameter(206, 1.1)
print(instrument.readParameter(206))
##for i in range(1,255):
##    print(instrument.readParameter(i))
##    print(i)