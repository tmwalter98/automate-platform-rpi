#!/usr/bin/python3
import threading
import pigpio

# Not yet implemented
# to be used with local database for 
class HardwareDiscovery(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.hardware_revision = 'scan not yet performed'
        self.i2c_devices = []

    def run(self):
        # Connect to pi
        pi = pigpio.pi()
        self.hardware_revision = pi.get_hardware_revision()
        self.scan_i2c(pi)
        pi.stop

    def scan_i2c(self, pi):
        for device in range(128):
            h = pi.i2c_open(1, device)
            try:
                pi.i2c_read_byte(h)
                d = hex(device)
                self.i2c_devices.append(d)
            except Exception: # exception if i2c_read_byte fails
                pass
            pi.i2c_close(h)
        return self.i2c_devices
        