
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
    time.sleep(0.5)
    ser.write((Command+'\r\n').encode())
    time.sleep(0.5)
    ser.close()

def ReadResponse(PerferredResponse):
    ser = serial.Serial("/dev/ttyUSB2", 115200)
    print("Åpnet seriell kommunikasjon")
    RecievedString = ''
    while True:
        time.sleep(1)
        print("Venter på svar")
        if ser.inWaiting():
            time.sleep(0.1)
            RecievedString = ser.read(ser.inWaiting())
            if PerferredResponse in RecievedString.decode():
                ser.close()
                return 1
            else:
                ser.close()
                return RecievedString



def UnlockSIM(PIN, PUK):
    #WaitForAvailability()
    print("Sender kommando")
    ExecuteCommand("AT+CPIN?")
    print("kommando sendt")
    UnlockStatus = ReadResponse("FALSESTATEMENT")
    print(UnlockStatus)
    #if b'\r\n+CPIN: SIM PIN\r\n\r\nOK\r\n' in UnlockStatus:
    if b'+CPIN: SIM PIN' in UnlockStatus:
        print("Sender PIN")
        ExecuteCommand("AT+CPIN="+PIN)
    if b'+CPIN: SIM PUK' in UnlockStatus:
        print("Sender PUK")
        ExecuteCommand("AT+CPIN="+PUK)

def WaitForSerial():
    ser = serial.Serial("/dev/ttyUSB2", 115200)
    ser.write(("AT"+'\r\n').encode())
    print("Venter på seriell")
    while ser.inWaiting() < 1:
        print(".")
        time.sleep(1)
    print("Seriell tilgjengelig!")
    

def WaitForAvailability():
    print("Sjekker om enhet er tilgjengelig")
    while True:
        AvailablePorts = []
        PortRead = serial.tools.list_ports.comports()
        for i in PortRead:
            AvailablePorts.append(i.device)
        if "/dev/ttyUSB2" in AvailablePorts:
            print("Enhet tilgjengelig!")
            WaitForSerial()
            break
        print(".")
        time.sleep(1)

def WaitForDisconnect():
    print("Venter på at enheten kobler seg fra")
    while True:
        AvailablePorts = []
        PortRead = serial.tools.list_ports.comports()
        for i in PortRead:
            AvailablePorts.append(i.device)
        print(AvailablePorts)
        if "/dev/ttyUSB2" not in AvailablePorts:
            print("Enhet frakoblet")
            break
        time.sleep(1)

def Start5G():
    WaitForAvailability()
    time.sleep(1)
    ExecuteCommand("AT+CUSBCFG=USBID,1E0E,9011")
    print("Enheten konfigureres!")
    time.sleep(1)
    WaitForDisconnect()
    time.sleep(1)
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
print("Modulen er startet opp")
UnlockSIM(PIN, PUK)
print("5G satt opp!")