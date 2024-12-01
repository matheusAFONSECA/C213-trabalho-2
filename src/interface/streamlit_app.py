import streamlit as st
import pandas as pd
import time

class StreamlitApp:
    def __init__(self, mqtt_client, data_processor):
        self.mqtt_client = mqtt_client
        self.data_processor = data_processor
        # self.mqtt_client.connect()

    def run(self):

        st.set_page_config(
            page_title="Fuzzy system - C213", page_icon="🛩️", layout="wide"
        )

        self.mqtt_client.connect()

        tab1, tab2 = st.tabs(["Send Data", "Visualize Data"])

        with tab1:
            self.send_data_tab()

        with tab2:
            self.visualize_data_tab()

    def send_data_tab(self):
        st.header("Send Data to Topics")
        altitude = st.number_input("Enter Altitude:", value=0.0, step=0.1)
        if st.button("Send Altitude"):
            self.mqtt_client.publish(self.mqtt_client.topics["altitude"], {"altitude": altitude})
            st.success(f"Altitude {altitude} sent!")

    def visualize_data_tab(self):
        st.header("Visualize Data from Topics")
        
        # Dados recebidos
        altitude_data = None # Chama a função de processamento de dados do objeto mqtt_client
        error_data = None # Chama a função de processamento de dados do objeto mqtt_client

        # Mostrar os dados brutos (debug opcional)
        if st.button("Show Raw Data"):
            st.write("Altitude Data:", altitude_data)
            st.write("Error Data:", error_data)

        # Atualização em tempo real
        st.write("Listening for new data...")
        with st.spinner("Waiting for updates..."):
            time.sleep(5)  # Aguarda um segundo antes de atualizar (ou ajuste conforme necessário)

        # Plotar os dados se disponíveis
        if altitude_data:
            st.subheader("Altitude Data")
            st.line_chart(altitude_data)

        if error_data:
            st.subheader("Error Data")
            st.line_chart(error_data)

        if not altitude_data and not error_data:
            st.warning("No data received yet!")
