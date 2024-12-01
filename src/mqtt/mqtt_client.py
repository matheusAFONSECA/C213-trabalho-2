import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime

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
                for base_topic in self.topics.values():
                    self.client.subscribe(f"{base_topic}/#")
                self.client.loop_start()
                print("Conectado ao broker MQTT.")
                break
            except Exception as e:
                attempt += 1
                print(f"Erro ao conectar ao broker (tentativa {attempt}/{retries}): {e}")
                time.sleep(2)

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        try:
            data = json.loads(msg.payload.decode("utf-8"))
            timestamp = topic.split("/")[-1]  # Extrai o tempo do tópico
            if self.topics["altitude"] in topic:
                self.received_data["altitude"].append({"timestamp": timestamp, "altitude": data.get("altitude", 0)})
            elif self.topics["error"] in topic:
                self.received_data["error"].append({"timestamp": timestamp, "error": data.get("error", 0)})
        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")

    def loop(self):
        self.client.loop(timeout=1.0)

    def get_received_data(self, data_type):
        return self.received_data.get(data_type, [])

    def publish(self, data):
        timestamp = datetime.now().strftime("%H:%M:%S")
        altitude_topic = f"{self.topics['altitude']}/{timestamp}"
        error_topic = f"{self.topics['error']}/{timestamp}"
        self.client.publish(altitude_topic, json.dumps({"altitude": data["altitude"]}))
        self.client.publish(error_topic, json.dumps({"error": data["error"]}))
