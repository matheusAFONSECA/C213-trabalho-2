import paho.mqtt.client as mqtt
import random
import time

# Configuração do broker MQTT
mqtt_broker = "test.mosquitto.org"  # Substitua pelo seu broker, se necessário
topics = ["Drone/Altura", "Drone/Erro"]  # Tópicos para publicação

# Criação do cliente MQTT para publicação
publisher = mqtt.Client()

# Função para gerar dados aleatórios
def generate_random_data(topic):
    if "Altura" in topic:
        return round(random.uniform(0.5, 20.0), 2)  # Altura em metros
    elif "Erro" in topic:
        return random.choice(["Erro de sensor", "Conexão perdida", "Erro desconhecido"])
    return "Dado genérico"

# Conexão com o broker MQTT
try:
    publisher.connect(mqtt_broker)
    print(f"Publicador conectado ao broker {mqtt_broker}. Publicando dados...")
    
    while True:
        for topic in topics:
            data = generate_random_data(topic)
            publisher.publish(topic, data)
            print(f"Publicado no tópico {topic}: {data}")
        time.sleep(2)  # Aguarda 2 segundos antes de publicar novamente

except Exception as e:
    print(f"Erro ao conectar ou publicar no broker MQTT: {e}")
finally:
    publisher.disconnect()
