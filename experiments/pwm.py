
import math
import numpy as np
import time
from signal import signal, SIGINT
from sys import exit
import pigpio
import RPi.GPIO as GPIO

import colorsys
#from colorspace.colorlib import HSV, RGB
from rgbxy import Converter

LED_RED = 13
LED_GREEN = 12
LED_BLUE = 18

pi = pigpio.pi()

#cols = HSV(H = [160, 210, 260, 310, 360],
#           S = [ 70,  40,  10,  40,  70],
#           V = [ 50,  70,  90,  70,  50])
#cols.swatchplot()


def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    pi.set_PWM_dutycycle(LED_RED, 0)
    pi.set_PWM_dutycycle(LED_GREEN, 0)
    pi.set_PWM_dutycycle(LED_BLUE, 0)
    pi.stop()
    exit(0)


def set_light(led_pin, brightness):
    pi.set_PWM_dutycycle(led_pin, 255 * (1 - brightness))

def sin_rainbow(radius=1):
    converter = Converter()
    r0, g0, b0 = (0,0,0)

    while(1):
        for rad in np.arange(0,math.pi * 2,0.01):
            time.sleep(0.05)
            #rad = (math.sin(counter * math.pi * 1.5) / 2)

            x = radius *  math.cos(rad)
            y = radius *  math.sin(rad)

            r1, g1, b1 = converter.xy_to_rgb(x,y)

            if(r1 != r0):
                pi.set_PWM_dutycycle(LED_RED, r1)
            if(g1 != g0):
                pi.set_PWM_dutycycle(LED_GREEN, g1)
            if(b1 != b0):
                pi.set_PWM_dutycycle(LED_BLUE, b1)
            r0, g0, b0 = (r1, g1, b1)

def rainbow():
    converter = Converter()
    r0, g0, b0 = (0,0,0)

    while True:
        for i in np.arange(start=0, stop=1010, step=1):
            h = i / 100.0
            r1, g1, b1 = [round(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
            #r1, g1, b1 = HSV.hsv_to_rgb(h, 1.0, 1.0)
            if(r1 != r0):
                pi.set_PWM_dutycycle(LED_RED, r1)
            if(g1 != g0):
                pi.set_PWM_dutycycle(LED_GREEN, g1)
            if(b1 != b0):
                pi.set_PWM_dutycycle(LED_BLUE, b1)
            r0, g0, b0 = (r1, g1, b1)

            time.sleep(0.2)


def sway():
    while(1):
        for counter in np.arange(1,2.33333,0.01):
            time.sleep(0.05)
            rad = (math.sin(counter * math.pi * 1.5) / 2)
            brightness_r = rad + 0.5
            brightness_g = rad * -1 + 0.5
            #brightness = (math.sin(counter * math.pi * 1.5) / 2) + 0.5
            set_light(LED_GREEN, brightness_g)
            #brightness = (math.sin(counter * math.pi * -1.5) / 2) + 0.5
            set_light(LED_RED, brightness_r)


if __name__ == '__main__':
    signal(SIGINT, handler)
    sin_rainbow()