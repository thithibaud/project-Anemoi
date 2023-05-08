#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Name:        ComunicacionBronkhorst
# Purpose:
#
# Author:      Xavi
# Modified:     21/03/2020
# Copyright:   (c) Xavi 2020
#-------------------------------------------------------------------------------


import binascii
import struct
import serial
import codecs
import threading


class Control_FlowBus(serial.Serial):
    def __init__(self, comport):                #inicialización de la clase con el puerto a utilizar
        """****************************************
        Inicialización Flow Bus.
        ******************************************"""
        serial.Serial.__init__(self, comport)   #inicialización de la clase padre
        self.baudrate = 38400                   #configuración velocidad comunicación 38400 baudios
        self.bytesize = serial.EIGHTBITS        #configuración tamaño paquete de datos a 8 bits
        self.parity = serial.PARITY_NONE        #configuración bit de paridad, sin bit de paridad
        self.stopbits = serial.STOPBITS_ONE     #configuración de bits de stop, un bit
        self.timeout = 1                        #configuración tiempo de espera, 1 ms

    def get_mesure(self, nodo):
        '''******************************************************
        Realizará una petición de la medida de flujo al MassFlow
        ******************************************************'''
        try:
            med = ':06' + nodo + '0401210120\r\n'
            self.write(med.encode())
            medida = self.readline()
        except ValueError:
            return "NA"
        else:
            return medida [11:15]

    def gethex(self, decimal):
        return hex(decimal)[2:]

    def send_setpoint(self, nodo, setpoint):
        '''*****************
        Envío Setpoint:
            Max.: 41942
            100% <=> 32000
        *****************'''
        if setpoint == 0:
            sp = '0000'
        else:
            sp = (setpoint / 100) * 32000
            sp = int(sp)
            sp = self.gethex(sp)
            sp = str(sp)
            sp = sp.upper()

        tsp = ':06' + nodo + '010121' + sp + '\r\n'
        self.write(tsp.encode())                    #envío setpoint
        ans = self.readline()                   #respuesta de confirmación
        if ans[6:11] == b'00005':
            return ans[6:11]
        else:
            return 'NA'


    def get_setpoint(self, nodo):
        '''***********************************
        Se solocita el setpoint actual del MFC
        ***********************************'''
        try:
            setp = ':06' + nodo + '0401210121\r\n'
            self.write(setp.encode())
            ans = self.readline()
            answ = ans[11:15]
            answ = answ.lower()
            answ = int(answ, 16)
            answ = (answ * 100) / 32000

        except ValueError:
            return "NA"
        else:
            return answ


    def get_serial(self, nodo):
        '''*********************************************************************************
        Se pide el número de serie a cada Massflow conectado
        *********************************************************************************'''
        try:
            pnser = ':07' + nodo + '047163716300\r\n'#se crea trama para pedir número de serie
            self.write(pnser.encode())
            numser = self.readline()
            numser = numser [13:31]                  #se guarda el dato interesado
            numser = binascii.unhexlify(numser)      #se convierte a código Ascii
            numser = str(numser, 'ascii')
            if numser=="":
                raise ValueError

        except ValueError:
            return "NA"
        else:
            return numser


    def get_capacity(self, nodo):
        '''***************************************************************************
        Se pide la capacidad a cada Massflow conectado
        ***************************************************************************'''

        try:
            pcap = ':06' + nodo + '04014D014D\r\n'
            self.write(pcap.encode())
            cap = self.readline()
            cap = cap[11:19]
            cap = int (struct.unpack('!f', codecs.decode(cap,'hex_codec'))[0])

        except struct.error:
            return "NA"
        else:
            return cap

    def get_unit(self, nodo):
        '''***************************************************************************
        Se pide las unidades de la capacidad a cada Massflow conectado
        ***************************************************************************'''
        try:
            pcap = ':07' + nodo + '04017F017F07\r\n'  #se crea trama para pedir capacidad (4D014D)
            self.write(pcap.encode())
            cap = self.readline()
            cap = cap[13:27]
            cap = codecs.decode(cap,'hex')
            cap = str(cap, 'ascii')

        except ValueError:
            return "NA"
        else:
            return cap
