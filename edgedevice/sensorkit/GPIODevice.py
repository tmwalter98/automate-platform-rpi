#!/usr/bin/python3
from signal import signal, SIGINT, SIGTERM
import sys
from edgedevice.config import config
import asyncio
import ctypes
import pathlib

from gpiozero import DigitalInputDevice
import RPi.GPIO as GPIO

this = sys.modules[__name__]

class GPIODevice():
    # Initialize GPIO connected Device
    def __init__(self, pub_template, gpio_in, gpio_vcc):
        signal(SIGINT, self.stop)
        signal(SIGTERM, self.stop)

        self.pub_template = pub_template
        self.gpio_in = gpio_in
        self.gpio_vcc = gpio_vcc
        self.gpio_vcc_status = False
        if(gpio_vcc):
            GPIO.setup(self.gpio_vcc, GPIO.OUT)

    def stop(self, signal_received=None, frame=None):
        try:
            if(self.publisher.is_alive()):
                try:
                    self.publisher.stop()
                except Exception:
                    pass
            self.client.loop_stop()
            self.client.disconnect()
        except Exception:
            pass
        exit(0)

    def set_device_power(self, power_on=True):
        self.gpio_vcc_status = power_on
        GPIO.output(self.gpio_vcc, self.gpio_vcc_status)

    def __pub(self):  
        config.pub_queue.put(self.pub_template.prepare_pub())


class GPIOTrigger(GPIODevice):
    def __init__(self, pub_template, gpio_in, gpio_vcc):
        super().__init__(pub_template, gpio_in, gpio_vcc)
    
    async def configure_trigger(self, pull_up, bounce_time, callback=None):
        # Registers a callback routine when GPIO is triggered
        self.sensor = DigitalInputDevice(self.gpio_in, pull_up, bounce_time)
        self.set_device_power(True)
        # Waits for device to turn on in the event it would trigger the callback
        await asyncio.sleep(bounce_time + 1)
        # By default, publishes events
        if not callback:
            callback = self.__pub
        self.sensor.when_activated = callback

# Exploring C based implementation for LED indicator controlled by Raspberry Pi's
# hardware supported PWM GPIO pins [12, 13, 18]
class PWMController(GPIODevice):
    def __init__(self, gpio_in, gpio_vcc):
        super().__init__(None, gpio_in, gpio_vcc)
        self.libname = pathlib.Path().absolute() / 'pwm_functions.so'
        self.c_lib = ctypes.CDLL(self.libname)
