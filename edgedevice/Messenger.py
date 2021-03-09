#!/usr/bin/python3
import json
import queue
import threading
from signal import SIGINT, SIGTERM, pause, signal
from sys import exit

import paho.mqtt.client as mqtt

import edgedevice.config as config


class Messenger(threading.Thread):
    def __init__(self, threadpool, pub_queue, sub_queue):
        threading.Thread.__init__(self)
        signal(SIGINT, self.stop)
        signal(SIGTERM, self.stop)
        self.daemon = True
        self.executor = threadpool

        self.pub_queue = pub_queue
        self.sub_queue = sub_queue
        
        self.client = mqtt.Client(client_id=config.hostname, clean_session=False, userdata=None, transport="websockets")
        self.client.tls_set(ca_certs=config.mqtt_broker_ca_url)

        self.publisher = Publisher(self.client, self.pub_queue)
        self.publisher.daemon = True

    def start(self):
        self.client.connect_async(config.mqtt_broker_url, config.mqtt_broker_port, keepalive=config.mqtt_keepalive)
        self.client.loop_start()
        self.executor.submit(self.publisher.start)
        print('Messenger Started')
        pause()

    ### Handles closing connection with MQTT Broker and gracefully exiting unpon SIG
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
      
    ### Allows other Daemons to subscribe with callbacks 
    def subscribe(self, topic, callback):
        try:
            self.client.message_callback_add(topic, callback)
        except Exception:
            print('Failed to subscribe')
            return 1
        return 0

class Publisher(threading.Thread):
    def __init__(self, client, pub_queue):
        threading.Thread.__init__(self)
        signal(SIGINT, self.stop)
        signal(SIGTERM, self.stop)
        self.pub_queue = pub_queue
        self.client = client
        self.thread_run = True

    def stop(self, signal_received, frame):
        self.thread_run = False
        self.pub_queue.put(0)

    def start(self):
        while self.thread_run:
            try:
                payload = self.pub_queue.get(block=True, timeout=5)
                if isinstance(payload, dict):
                    print(json.dumps(self.pub_dict))
                    try:
                        if(payload['topic'] != None):
                            topic = payload['topic']
                        else:
                            topic = '/notopic'
                        self.client.publish(topic, json.dumps(payload))
                    except Exception:
                        pass
            except queue.Empty:
                continue
        exit(0)
