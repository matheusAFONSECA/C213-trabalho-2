import streamlit as st

class StreamlitApp:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
        self.mqtt_client.connect()

    def run(self):

        st.set_page_config(
            page_title="Fuzzy System - C213", page_icon="🛩️", layout="wide"
        )

        tab1, tab2 = st.tabs(["Send Data", "Visualize Data"])

        with tab1:
            self.send_data_tab()

        with tab2:
            self.visualize_data_tab()

    def send_data_tab(self):
        st.header("Send Data to Topics")
        altitude = st.number_input("Enter Altitude:", value=0.0, step=0.1)
        if st.button("Send Altitude"):
            self.mqtt_client.publish(self.mqtt_client.topics["altitude"], altitude)
            st.success(f"Altitude {altitude} sent!")

    def visualize_data_tab(self):
        st.header("Visualize Data from fuzzy project")
