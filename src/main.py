from mqtt.mqtt_client import MQTTClient
from interface.data_processor import DataProcessor
from interface.streamlit_app import StreamlitApp

# Configuração do MQTT
MQTT_BROKER = "test.mosquitto.org"
TOPICS = {"altitude": "Drone/Altura", "error": "Drone/Erro"}

# Instanciar objetos
mqtt_client = MQTTClient(MQTT_BROKER, TOPICS)
data_processor = DataProcessor()
streamlit_app = StreamlitApp(mqtt_client, data_processor)

# Executar a aplicação Streamlit
streamlit_app.run()
