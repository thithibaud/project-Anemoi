
# Import the propar module
import propar

# Connect to the local instrument, when no settings provided
# defaults to locally connected instrument (address=0x80, baudrate=38400)
instrument = propar.instrument('/dev/ttyUSB0')

# Measure and setpoint in output units.
instrument.writeParameter(206, 0.0)
print(instrument.readParameter(205), instrument.readParameter(129)) # fMeasure, Capacity Unit

# Measure and setpoint scaled to 0-32000 = 0-100%
instrument.writeParameter(9, 16000)
print(instrument.readParameter(8))

# Measure and setpoint as property (also 0-32000)
instrument.setpoint = 0
print(instrument.measure)

# Most parameters can also be read by their FlowDDE number,
# for example the user tag parameter.
instrument.writeParameter(115, "Hello World!")
print(instrument.readParameter(115))
for i in range(0, 200):
    try:
        print(instrument.readParameter(i))

# Connect to an instrument by specifying the channel number to connect to
flow = propar.instrument('/dev/ttyUSB0', channel=1)
pressure = propar.instrument('/dev/ttyUSB0', channel=2)

# Alternatively, pass channel to parameter functions
instrument = propar.instrument('/dev/ttyUSB0')
p_upstream = instrument.readParameter(205, channel=2)
print(instrument.readParameter(105))
print(p_upstream)
print(flow.readParameter(105))
print(pressure.readParameter(105))

el_flow = propar.instrument('/dev/ttyUSB0', 3)
cori_flow = propar.instrument('/dev/ttyUSB0', 4)
es_flow   = propar.instrument('/dev/ttyUSB0', 5)
print(el_flow.readParameter(105))
print(cori_flow.readParameter(102))
print(es_flow.readParameter(93))

# Connect to the local instrument.
el_flow = propar.instrument('/dev/ttyUSB0')

# Use the get_nodes function of the master of the instrument to get a list of instruments on the network
nodes = el_flow.master.get_nodes()

# Display the list of nodes
for node in nodes:
  print(node)
