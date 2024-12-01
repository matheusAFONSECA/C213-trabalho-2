import streamlit as st
from mqtt.mqtt_client import MQTTClient
from interface.streamlit_app import StreamlitApp
from fuzzy.fuzzy_control import FuzzyControl

# MQTT configurations
MQTT_BROKER = "test.mosquitto.org"
TOPICS = {"altitude": "Drone/Altura", "error": "Drone/Erro"}

# Instantiate objects
fuzzy_control = FuzzyControl()
mqtt_client = MQTTClient(MQTT_BROKER, TOPICS)
streamlit_app = StreamlitApp(mqtt_client, fuzzy_control)

# Streamlit layout
streamlit_app.run()
