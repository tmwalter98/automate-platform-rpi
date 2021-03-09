#!/usr/bin/python3
import datetime
import json
import os
import re
from edgedevice import config


# Template Factory for standardizing MQTT Broker bound JSON playloads
# Streamlines on board workflow and increases data integrity through pipeline
class TemplateFactoryMQTT():
    def __init__(self):
        self.base_topic = config.mqtt_base_topic
        self.template_dict = {'domain':config.domain, 'hostname':config.hostname, 'topic':None, 'timestamp': None, 'payload': None}

    def create_template(self, payload_class, payload_type):
        topic = self.base_topic.format(payload_class=payload_class, payload_type=payload_type)
        return MQTTPublishTemplate(topic)

    def build_json(self, payload=None):
        return json.dumps(self.prepare_pub(payload))


class MQTTPublishTemplate():
    space_pattern = re.compile(r'\s+')
    topic_parts_pattern = re.compile(r'([\w\-]+)')

    def __init__(self, template_dict, template_topic=None):
        if(template_topic == None):
            try:
                template_topic = template_dict.get('topic')
            except KeyError:
                raise MQTTTopicUnspecified()
        self.publish_template = template_dict.copy()
        self.publish_template['topic'] = self.validate_mqtt_topic(template_topic)

    def validate_mqtt_topic(self, topic):
        # Drops all spaces and chars non-compatible with utf-8 
        topic1 = re.sub(self.space_pattern, '', topic.decode('utf-8', 'ignore'))
        # finds all components that match topic_parts_pattern
        topic_path = re.findall(self.topic_parts_pattern, topic1)
        # Joins components together, ensuring topic does not begin or end with forwardslash
        return '/'.join(topic_path)

    def get_topic(self):
        return self.publish_template['topic']

    def prepare_pub(self, payload=None):
        build_dict = self.base_pub.copy()
        build_dict['timestamp'] = datetime.datetime.now().timestamp()
        build_dict['payload'] = payload
        return build_dict

class MQTTTopicUnspecified(RuntimeError):
    """An MQTT topic was not specified in object initialization parameters nor template Dictionary object."""
    pass
