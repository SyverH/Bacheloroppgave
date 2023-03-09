
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
        if ser.inWaiting() > 0:
            BitsWaiting = ser.inWaiting()
            time.sleep(0.1)
            NewBitsWaiting = ser.inWaiting - BitsWaiting
            if not NewBitsWaiting:
                RecievedString = ser.read(ser.inWaiting()).decode()
                if PerferredResponse == RecievedString:
                    ser.close()
                    return 1
                else:
                    ser.close()
                    return RecievedString

def UnlockSIM(PIN, PUK):
    ExecuteCommand('cpin?')
    UnlockStatus = ReadResponse("OK")
    if UnlockStatus == "+CPIN: PIN":
        ExecuteCommand("AT+CPIN="+PIN)
    if UnlockStatus == "+CPIN: PUK":
        ExecuteCommand("AT+CPIN="+PUK)

def WaitForSerial():
    ser = serial.Serial("/dev/ttyUSB2", 115200)
    ser.write(("AT"+'\r\n').encode())
    while not ser.inWaiting():
        print("Seriell er ikke tilgjengelig enda")
        time.sleep(1)
    

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

print("Script startet")
WaitForAvailability()
print("Seriell tilgjengelig!")