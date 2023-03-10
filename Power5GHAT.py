import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(4, GPIO.OUT) #set Relay 1 output
GPIO.setup(17, GPIO.OUT) #set Relay 2 output

GPIO.output(4, GPIO.HIGH) #turn relay 1 on
#GPIO.output(4, GPIO.LOW) #turn relay 1 OFF