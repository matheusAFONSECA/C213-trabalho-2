import paho.mqtt.client as mqtt
import json

class MQTTClient:
    def __init__(self, broker, topics):
        self.broker = broker
        self.topics = topics
        self.client = mqtt.Client()
        self.received_data = {"altitude": [], "error": []}
        self.client.on_message = self.on_message

    def connect(self):
        self.client.connect(self.broker)
        for topic in self.topics.values():
            self.client.subscribe(topic)
        self.client.loop_start()

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        data = json.loads(msg.payload.decode("utf-8"))
        if topic == self.topics["altitude"]:
            self.received_data["altitude"].append(data)
        elif topic == self.topics["error"]:
            self.received_data["error"].append(data)

    def publish(self, topic, data):
        self.client.publish(topic, json.dumps(data))
