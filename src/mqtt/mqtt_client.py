import paho.mqtt.client as mqtt
import json
import time

class MQTTClient:
    def __init__(self, broker, topics):
        self.broker = broker
        self.topics = topics
        self.client = mqtt.Client()
        self.received_data = {"altitude": [], "error": []}
        self.client.on_message = self.on_message

    def connect(self):
        retries = 5
        attempt = 0
        while attempt < retries:
            try:
                self.client.connect(self.broker, port=1883)
                for topic in self.topics.values():
                    self.client.subscribe(topic)
                self.client.loop_start()
                print("Conectado ao broker MQTT.")
                break
            except Exception as e:
                attempt += 1
                print(f"Erro ao conectar ao broker (tentativa {attempt}/{retries}): {e}")
                time.sleep(2)  # Espera antes de tentar novamente

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        data = json.loads(msg.payload.decode("utf-8"))
        if topic == self.topics["altitude"]:
            self.received_data["altitude"].append(data)
        elif topic == self.topics["error"]:
            self.received_data["error"].append(data)

    def publish(self, topic, data):
        self.client.publish(topic, json.dumps(data))
