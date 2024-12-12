import paho.mqtt.client as mqtt
import json


class MQTTClient:
    """
    A client for connecting to an MQTT broker, subscribing to topics, and handling messages.
    Attributes:
        broker (str): The address of the MQTT broker.
        topics (dict): A dictionary of topics to subscribe to.
        client (paho.mqtt.client.Client): The MQTT client instance.
        received_data (dict): A dictionary to store received data for different topics.
    Methods:
        __init__(broker, topics):
            Initializes the MQTTClient with the broker address and topics.
        connect():
            Connects to the MQTT broker and subscribes to the specified topics.
        on_message(client, userdata, msg):
            Callback function that handles incoming messages and stores data.
        publish(topic, data):
            Publishes data to a specified topic.
    """

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
