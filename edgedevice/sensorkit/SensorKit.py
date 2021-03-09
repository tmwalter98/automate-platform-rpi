#!/usr/bin/python3
import threading
from signal import signal, SIGINT, SIGTERM
from socket import timeout
from sys import exit
import asyncio

from edgedevice.sensorkit import TemplateFactoryMQTT
from edgedevice.sensorkit import SHT20Sensor, GPIOTrigger
from edgedevice.config import config


class SensorKit(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        signal(SIGINT, self.stop)
        signal(SIGTERM, self.stop)
        self.sensors = []

    def stop(self, signal_received, frame):
        exit(0)

    def start(self):
        # Automate hardware discovery here
        env_sensor_pub_template = TemplateFactoryMQTT.create_template(payload_class='data_sample', payload_type='temperature')
        self.env_sensor = SHT20Sensor(1, 0x40, config.pub_queue, env_sensor_pub_template)

        motion_sensor_pub_template = TemplateFactoryMQTT.create_template(payload_class='rt_event', payload_type='motion')
        motion_sensor = GPIOTrigger(23, 22, config.pub_queue, motion_sensor_pub_template)
        self.motion_sensor.configure_trigger(pull_up=False, bounce_time=2.0)

    def run(self):
        loop = asyncio.new_event_loop()
        try:
            loop.run_forever(None, self.env_sensor.periodic_routine(60*1))
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()
       
        