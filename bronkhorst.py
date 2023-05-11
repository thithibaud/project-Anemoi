'''
Original code from: https://github.com/CINF/PyExpLabSys
Authors: Andersen Thomas, Robert Jensen
Forked by Floris van Breugel 1/26/2015

'''

import serial
import time
import threading

class Bronkhorst():
    
    def __init__(self,port,max_flow = 10):
        self.ser = serial.Serial(port,38400)
        self.max_setting = max_flow
        time.sleep(0.1)

    def comm(self,command):
        self.ser.write(command)
        time.sleep(0.1)
        return_string = self.ser.read(self.ser.inWaiting())
        return return_string

    def read_setpoint(self):
        read_setpoint = ':06800401210121\r\n' # Read setpoint
        response = self.comm(read_setpoint)
        response = int(response[11:], 16)
        response = (response / 32000.0) * self.max_setting
        return response

    def read_measure(self):
        error = 0
        while error < 10:
            read_pressure = ':06800401210120\r\n' # Read pressure
            val = self.comm(read_pressure)
            try:
                val = val[-6:]
                num = int(val, 16)
                pressure = (1.0 * num / 32000) * self.max_setting
                break
            except ValueError:
                pressure = -99
                error = error + 1
        return pressure

    def set_setpoint(self,setpoint):
        if setpoint > 0:
            setpoint = (1.0 * setpoint / self.max_setting) * 32000
            setpoint = hex(int(setpoint))
            setpoint = setpoint.upper()
            setpoint = setpoint[2:].rstrip('L')
            if len(setpoint) == 3:
                setpoint = '0' + setpoint
        else:
            setpoint = '0000'
        set_setpoint = ':0680010121' + setpoint + '\r\n' # Set setpoint
        response = self.comm(set_setpoint)
        response_check = response[5:].strip()
        if response_check == '000005':
            response = 'ok'
        else:
            response = 'error'
        return response

    def read_counter_value(self):
        read_counter = ':06030401210141\r\n'
        response = self.comm(read_counter)
        return str(response)

    def set_control_mode(self):
        set_control = ':058001010412\r\n'
        response = self.comm(set_control)
        return str(response)

    def read_serial(self):
        read_serial = b':1A8004F1EC7163006D71660001AE0120CF014DF0017F077101710A\r\n'  # Use a byte string
        error = 0
        while error < 10:
            response = self.comm(read_serial)
            response = response[13:-84]
            try:
                respomse = bytes.fromhex(response)
            except TypeError:
                response = b''
            if response == b'':
                error = error + 1
            else:
                error = 10
        return response.decode('utf-8')

    
    def read_unit(self):
        read_capacity = ':1A8004F1EC7163006D71660001AE0120CF014DF0017F077101710A\r\n'
        response = self.comm(read_capacity)
        response = response[77:-26]
        response = response.decode('hex')
        return str(response)

    def read_capacity(self):
        read_capacity = ':1A8004F1EC7163006D71660001AE0120CF014DF0017F077101710A\r\n'
        response = self.comm(read_capacity)
        response = response[65:-44]
        #response = response.decode('hex')
        return str(response)

        
if __name__ == '__main__':
    bh = Bronkhorst('/dev/ttyUSB0', 100)
    
    bh.set_control_mode() # sets the mode to RS232 so you can set the setpoint
    bh.set_setpoint(75) # sets the setpoint
    bh.read_measure() # returns the current flow rate
    
