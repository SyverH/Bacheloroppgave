
import configparser
import time
import serial
import serial.tools.list_ports

config5G = configparser.ConfigParser() # Config til 5G

config5G.read("/boot/Rover_Config.ini") # Her skrives path til config-filen Rover_Config.ini

PIN = config5G["DEFAULT"]["SIM_PIN"] #Henter ut variablen SIM_PIN
PUK = config5G["DEFAULT"]["SIM_PUK"] #Henter ut variablen SIM_PUK

def ExecuteCommand(Command):
    ser = serial.Serial("/dev/ttyUSB2", 115200)
    ser.write((Command+'\r\n').encode())
    ser.close()

def ReadResponse(PerferredResponse):
    ser = serial.Serial("/dev/ttyUSB2", 115200)
    RecievedString = ''
    while True:
        if ser.in_waiting():
            time.sleep(0.1)
            RecievedString = ser.read(ser.in_waiting())
            if PerferredResponse in RecievedString.decode():
                ser.close()
                return 1
            else:
                ser.close()
                return RecievedString



def UnlockSIM(PIN, PUK):
    WaitForAvailability()
    ExecuteCommand('at+cpin?')
    UnlockStatus = ReadResponse("FALSESTATEMENT")
    if b'\r\n+CPIN: SIM PIN\r\n\r\nOK\r\n' in UnlockStatus:
        print("Sender PIN")
        ExecuteCommand("AT+CPIN="+PIN)
    if b'\r\n+CPIN: SIM PUK\r\n\r\nOK\r\n' in UnlockStatus:
        print("Sender PUK")
        ExecuteCommand("AT+CPIN="+PUK)

def WaitForSerial():
    ser = serial.Serial("/dev/ttyUSB2", 115200)
    ser.write(("AT"+'\r\n').encode())
    print("Venter på seriell")
    while not ser.in_waiting():
        print(".")
        time.sleep(1)
    print("Seriell tilgjengelig!")
    

def WaitForAvailability():
    while True:
        AvailablePorts = []
        PortRead = serial.tools.list_ports.comports()
        for i in PortRead:
            AvailablePorts.append(i.device)
        if "/dev/ttyUSB2" in AvailablePorts:
            WaitForSerial()
            break
    time.sleep(1)

def WaitForDisconnect():
    while True:
        AvailablePorts = []
        PortRead = serial.tools.list_ports.comports()
        for i in PortRead:
            AvailablePorts.append(i.device)
        if "/dev/ttyUSB2" not in AvailablePorts:
            break

def Start5G():
    WaitForAvailability()
    ExecuteCommand("AT+CUSBCFG=USBID,1E0E,9011")
    WaitForDisconnect()
    WaitForAvailability()


#Denne funksjonen er skrevet av WaveShare. 
""" 
def send_at(command, back, timeout):
    rec_buff = ''
    ser.write((command+'\r\n').encode())
    time.sleep(timeout)
    if ser.inWaiting():
        time.sleep(0.01)
        rec_buff = ser.read(ser.inWaiting())
    if back not in rec_buff.decode():
        print(command + ' ERROR')
        print(command + ' back:\t' + rec_buff.decode())
        return 0
    else:
        print(rec_buff.decode())
        return 1
"""

Start5G()
UnlockSIM()
print("5G satt opp!")