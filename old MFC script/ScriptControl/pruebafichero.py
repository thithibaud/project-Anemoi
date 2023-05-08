import comunicacion as com

mfall=[]
mfconnected=0
airnode=""
gasnodes=[]


def identyall(nodo):
    elflow = com.Control_FlowBus('/dev/ttyUSB0')
    try:
        numser = elflow.get_serial(nodo)
        if numser=="NA":
            raise ValueError
    except ValueError:
        return "NA"
    else:
        capacity = str(elflow.get_capacity(nodo))
        unid = str(elflow.get_unit(nodo))
        setp = str(elflow.get_setpoint(nodo))
        texto = 'MF in node '+nodo+' with sr: '+numser+' and capacity: '+capacity+unid+'S.P.:'+setp+'%'
        return texto

def openconfigure():
    global mfall, mfconnected, airnodes, gasnodes
    try:
        f=open("config.txt")
    except FileNotFoundError:
        # doesn't exist
        print("NO DATA")
    else:
        # exists
        lineas=f.readlines()
        f.close()

        for linea in lineas:
            nodes=linea.replace("\n", "").split(":")
            mf=nodes[1]
            mfall.append(mf)
            mfconnected+=1

        print("NUMBER OF MASSFLOWS = "+str(mfconnected))
        airnode=str(mfall[0])
        print("AIR NODE "+identyall(airnode))

        for i in range(1,mfconnected):
            gasnodes.append(str(mfall[i]))
            print("GAS NODE "+identyall(str(gasnodes[i-1])))


openconfigure()

