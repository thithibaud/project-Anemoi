# project Anemoi
A python GUI to automate and control experiments using Massflow controller from bronkhorst (expected to be using EL-FLOW) from a raspeberrypi.

The MFCs are expected to be plug in to USB using a serial to USB adaptator and accesible from ``/dev/ttyUSBPort2``
The power supply powering the heater resitance is expected to be accesible from ``/dev/ttyUSBPor1``
see https://forums.raspberrypi.com/viewtopic.php?t=90265\ for more info.

## What can it do:
* Store username of user
* Control the MFCs either manually or generate a script that can be run for automated procedure
* Discover every MFCs connected
* Select which gas is assigned to which MFCs
* In manual mode, display a real time graph of setpoints and mesurements
* In script mode set the temperature based on calculated caracteristic of heater
* save as a CSV the setpoints and mesurements of each MFC
* Can load and run script while dipaying the current status of the MFCs and power supply



Communication with Bronkhorst (Mass) Flow Meters and Controllers :
cf communcation.py

Control of power supply :
https://github.com/Ultrawipf/pydps

## Developed with:
Python 3.7

### Download
```
git clone https://github.com/thithibaud/project-Anemoi
```
```
cd  project-Anemoi/
```
### Requirements:
```
matplotlib
minimalmodbus
pyserial
sv_ttk
```
or 
```
  pip install -r requirements.txt
```
### Run
```
python3 main.py
```
