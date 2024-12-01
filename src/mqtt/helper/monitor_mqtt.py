import paho.mqtt.client as mqtt
import time

# Callback para quando uma conexão com o broker é estabelecida
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT com sucesso!")
        for topic in userdata["topics"]:
            client.subscribe(topic)
            print(f"Inscrito no tópico: {topic}")
    else:
        print(f"Falha ao conectar, código de retorno: {rc}")

# Callback para quando uma mensagem é recebida
def on_message(client, userdata, message):
    try:
        # Decodifica a mensagem recebida e exibe no console
        payload = message.payload.decode("utf-8")
        print(f"Recebido: Tópico: {message.topic}, Mensagem: {payload}")
    except Exception as e:
        print(f"Erro ao processar a mensagem do tópico {message.topic}: {e}")

# Callback para quando a conexão é perdida
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Conexão perdida com o broker MQTT. Tentando reconectar...")
        reconnect(client)

# Função para reconectar ao broker com tentativas
def reconnect(client):
    retries = 5
    attempt = 0
    while attempt < retries:
        try:
            client.reconnect()
            print("Reconexão bem-sucedida!")
            break
        except Exception as e:
            attempt += 1
            print(f"Tentativa de reconexão {attempt}/{retries} falhou: {e}")
            time.sleep(2)
    if attempt == retries:
        print("Falha ao reconectar após várias tentativas. Verifique o broker MQTT.")

# Configuração do cliente MQTT
mqtt_broker = "test.mosquitto.org"  # Substitua pelo seu broker, se necessário
topics = ["Drone/Altura/#", "Drone/Erro/#"]  # Inclui wildcards para capturar mensagens com tempo

# Criação do cliente MQTT
client = mqtt.Client(userdata={"topics": topics})
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# Conectar ao broker e iniciar loop
try:
    client.connect(mqtt_broker)
    print(f"Conectado ao broker {mqtt_broker}. Monitorando tópicos: {topics}")
    client.loop_forever()
except Exception as e:
    print(f"Erro ao conectar ao broker MQTT: {e}")
