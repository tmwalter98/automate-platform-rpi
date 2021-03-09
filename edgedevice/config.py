import os

global config

class Config():
    def __init__(self):
        self.domain = str(os.getenv('DOMAIN'))
        self.zone = str(os.getenv('ZONE'))
        self.hostname = str(os.uname()[1])

        self.mqtt_broker_url = str(os.getenv('MQTT_BROKER_URL'))
        self.mqtt_broker_port = int(os.getenv('MQTT_BROKER_PORT'))
        self.mqtt_broker_ca_url = str(os.getenv('MQTT_BROKER_CA_URL'))
        self.mqtt_keep_alive = int(os.getenv('MQTT_KEEP_ALIVE'))

        self.mqtt_base_topic = '{domain}/{zone}/{{payload_class}}/{{payload_type}}'.format(domain=self.domain, zone=self.zone)

        self.sensor_gpio_pins = [23]
        self.sensor_gpio_power_pins = [22]

        self.sub_queue = None
        self.pub_queue = None
        self.executor = None
        self.messenger = None

config = Config()