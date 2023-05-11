#test connection 
import comunicacion as com
import os
import multiscript
#import ConfigMassflow


elflow = com.Control_FlowBus('/dev/ttyUSB0')
for i in range (0,9):
    global mflow
    i = 0
    j = 0
    node = "0" + str(i)
    answer = elflow.send_setpoint(node,0)
    if answer == b"00005":
        mflow.append(node)
        j+=1
    else:
        i+=1
    h = 1
    for h in range (0,j):
        node = mflow[h]
        number = elflow.get_serial(node)
        print(number)
##print(elflow)
##for i in range(0,9):
##    node = "0"+str(i)
##    number = elflow.get_serial(node)
##    print("node: " + node + "  SN: "+ str(number) )
##
##for i in range(10,100):
##    node = str(i)
##    number = elflow.get_serial(node)
##    print("node: " + node + "  SN: "+ str(number) )
node = "0"
number = elflow.get_serial(node)
print("node: " + node + "  SN: "+ str(number) )
