import streamlit as st
from mqtt.mqtt_client import MQTTClient
from interface.data_processor import DataProcessor
from interface.streamlit_app import StreamlitApp

# MQTT configurations
MQTT_BROKER = "test.mosquitto.org"
TOPICS = {"altitude": "Drone/Altura", "error": "Drone/Erro"}

# Instantiate objects
mqtt_client = MQTTClient(MQTT_BROKER, TOPICS)
data_processor = DataProcessor()
streamlit_app = StreamlitApp(mqtt_client, data_processor)

# Streamlit layout
streamlit_app.run()
