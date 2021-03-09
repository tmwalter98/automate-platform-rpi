#!/usr/bin/python3
import sys
import asyncio
from edgedevice import config
from sensor import SHT20


this = sys.modules[__name__]

def set_i2c_bus(bus):
        this.i2c_bus = bus


class I2CDevice():
    def __init__(self, i2c_address, i2c_bus=None):
        if(i2c_bus):
            this.i2c_bus = i2c_bus
        self.sht = SHT20(i2c_bus, i2c_address)

    async def __periodic_routine(self, period_seconds, callback):
        while True:
            await asyncio.sleep(period_seconds)
            callback()


class SHT20Sensor(I2CDevice):
    def __init__(self, i2c_address, i2c_bus=None):
        super().__init__(i2c_address, i2c_bus)
        self.routine = None

    def periodic_routine(self, period_seconds):
        super().__periodic_routine(self.pub_temp_humid, period_seconds)
            
    def sample_temp_humid(self):
        h, t = self.sht.all()
        payload = {'temperature':t.C, 'temperature_unit': 'C', 'humidity':h.RH}
        config.pub_queue.put(self.pub_template.prepare_pub(payload))
