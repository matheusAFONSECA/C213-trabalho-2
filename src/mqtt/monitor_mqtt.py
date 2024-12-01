import paho.mqtt.client as mqtt

# Callback para quando uma mensagem é recebida
def on_message(client, userdata, message):
    print(f"Topic: {message.topic}, Message: {message.payload.decode()}")

# Configuração do cliente MQTT
mqtt_broker = "test.mosquitto.org"  # Substituir pelo seu broker, se necessário
topics = ["Drone/Altura", "Drone/Erro"]  # Lista de tópicos a serem monitorados

client = mqtt.Client()
client.on_message = on_message

# Conectar ao broker e assinar tópicos
client.connect(mqtt_broker)
for topic in topics:
    client.subscribe(topic)

# Iniciar loop para escutar mensagens
print(f"Conectado ao broker {mqtt_broker}. Monitorando tópicos: {topics}")
client.loop_forever()
