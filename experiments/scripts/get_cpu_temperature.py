#!/usr/bin/python
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

if __name__ == '__main__':
    with open('/sys/class/thermal/thermal_zone0/temp') as tFile:
        temp = float(tFile.read())
    tempC = temp/1000

    if tempC > 43.5:
        GPIO.output(17, 1)
        print("HOT")
    else:
        GPIO.output(17, 0)
        print("COLD")
    
    print(tempC)
    GPIO.cleanup()
    exit