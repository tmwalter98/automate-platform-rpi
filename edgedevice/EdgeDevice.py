#!/usr/bin/python3
from edgedevice.config import config
from edgedevice.Messenger import Messenger
from edgedevice.sensorkit import SensorKit

import queue
import threading
from concurrent.futures import ThreadPoolExecutor
from signal import SIGINT, SIGTERM, pause, signal

class EdgeDevice(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        signal(SIGINT, self.stop)
        signal(SIGTERM, self.stop)

        config.pub_queue = queue.Queue()
        config.sub_queue = queue.Queue()
        config.executor = ThreadPoolExecutor(max_workers=3)
        config.messenger = Messenger(config.executor, config.pub_queue, config.sub_queue)

        self.threads_waiting = []
        self.threads_executing = []

        self.mysensorkit = SensorKit.SensorKit()

    def start(self):
        config.executor.submit(self.mysensorkit)

    def stop(self, signal_received=None, frame=None):
        exit(0)


if __name__ == '__main__':
    print('Starting SensorKit and MQTT client on ', config.hostname)
    platform = EdgeDevice()
    print('loaded!')
    platform.start()
    pause()
    print('Exiting Main Thread')
