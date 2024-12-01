import streamlit as st
import pandas as pd
import time

class StreamlitApp:
    def __init__(self, mqtt_client, data_processor):
        self.mqtt_client = mqtt_client
        self.data_processor = data_processor

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
        error = st.number_input("Enter Error:", value=0.0, step=0.1)
        if st.button("Send Data"):
            self.mqtt_client.publish({"altitude": altitude, "error": error})
            st.success(f"Altitude {altitude} and Error {error} sent!")

    def visualize_data_tab(self):
        st.header("Visualize Data from Topics")

        with st.spinner("Waiting for updates..."):
            time.sleep(2)  # Simula a atualização em tempo real
            self.mqtt_client.loop()  # Atualiza o loop do MQTT para buscar dados

        altitude_data = self.mqtt_client.get_received_data("altitude")
        error_data = self.mqtt_client.get_received_data("error")

        col1, col2 = st.columns(2)

        with col1:
            if altitude_data:
                st.subheader("Altitude Data")
                altitude_df = pd.DataFrame(altitude_data)
                st.line_chart(data=altitude_df, x="timestamp", y="altitude")
            else:
                st.warning("No altitude data available.")

        with col2:
            if error_data:
                st.subheader("Error Data")
                error_df = pd.DataFrame(error_data)
                st.line_chart(data=error_df, x="timestamp", y="error")
            else:
                st.warning("No error data available.")

        if st.checkbox("Show Raw Data"):
            st.write("Raw Altitude Data:", altitude_data)
            st.write("Raw Error Data:", error_data)
