#!/usr/bin/python3

from edgedevice import EdgeDevice
from edgedevice import config
from edgedevice.Messenger import Messenger
from edgedevice.sensorkit import SensorKit

from signal import SIGINT, SIGTERM, pause, signal

if __name__ == '__main__':
    print('Starting SensorKit and MQTT client on ', config.hostname)
    platform = EdgeDevice()
    print('loaded!')
    platform.start()
    pause()
    print('Exiting Main Thread')