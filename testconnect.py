#Find and store MFCs
import comunicacion as com
import os
import multiscript


MFCs={}
j = 0

elflow = com.Control_FlowBus('/dev/ttyUSB0')

#Looking for Instrument connected from node 0 to 100
for i in range(0,9):
    node = "0"+str(i)
    number = elflow.get_serial(node)
    if str(number) != "NA":
        print("node: " + node + "  SN: "+ str(number) )
        if number in MFCs.values():
            print("An instrument has duplicated nodes")
        else:                 
            MFCs.update({ node : number })
        
        
for i in range(10,100):
    node = str(i)
    number = elflow.get_serial(node)
    if str(number) !="NA":
        print("node: " + node + "  SN: "+ str(number) )
        if number in MFCs.values():
            print("An instrument has duplicated nodes")
        else:                 
            MFCs.update({ node : number })


print(MFCs)
