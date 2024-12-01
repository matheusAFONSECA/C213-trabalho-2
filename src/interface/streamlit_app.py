import streamlit as st

class StreamlitApp:
    def __init__(self, mqtt_client, fuzzy_control):
        self.mqtt_client = mqtt_client
        self.mqtt_client.connect()
        self.fuzzy_control = fuzzy_control

    def run(self):
        st.set_page_config(
            page_title="Fuzzy System - C213", page_icon="🛩️", layout="wide"
        )

        st.title("🛩️ Drone Fuzzy System - C213")

        tab1, tab2 = st.tabs(["Send Data", "Visualize Data"])

        with tab1:
            self.send_data_tab()

        with tab2:
            self.visualize_data_tab()

    def send_data_tab(self):
        st.header("Control the altitude of the drone")

        altitude = st.number_input("Enter Altitude:", value=0, step=1)

        if st.button("Send Altitude"):
            self.fuzzy_control.Subir_e_Descer(altitude)

            self.mqtt_client.publish(
                self.mqtt_client.topics["altitude"], self.fuzzy_control.Pos_Atual
            )

            self.mqtt_client.publish(
                self.mqtt_client.topics["error"], self.fuzzy_control.DeltaErroAtual
            )

            st.success(
                f"Altitude defined by fuzzy control {self.fuzzy_control.Pos_Atual:.3f} sent!"
            )
            st.success(
                f"Erro defined by fuzzy control {self.fuzzy_control.DeltaErroAtual:.3f} sent!"
            )

        if st.button("Land Drone"):
            self.fuzzy_control.Subir_e_Descer(0)

            self.mqtt_client.publish(
                self.mqtt_client.topics["altitude"], self.fuzzy_control.Pos_Atual
            )

            self.mqtt_client.publish(
                self.mqtt_client.topics["error"], self.fuzzy_control.DeltaErroAtual
            )

            st.success(
                f"Altitude defined by fuzzy control {self.fuzzy_control.Pos_Atual:.3f} sent!"
            )
            st.success(
                f"Erro defined by fuzzy control {self.fuzzy_control.DeltaErroAtual:.3f} sent!"
            )

    def visualize_data_tab(self):
        st.header("Visualize Data from Fuzzy Project")

        # Selecionar o que visualizar
        st.subheader("Choose what to visualize:")
        view_pertinence = st.checkbox("View Pertinence Functions", value=True)
        view_rules = st.checkbox("View Rules Table", value=True)

        # Visualizar funções de pertinência
        if view_pertinence:
            st.subheader("Pertinence Functions")
            st.write("Below are the pertinence functions for the Fuzzy model:")

            # Erro
            st.write("### Error (Erro)")
            fig_erro = self.fuzzy_control.fuzzy_models.pertinence_error_plot()
            st.pyplot(fig_erro)

            # Delta Erro
            st.write("### Delta Error (dErro)")
            fig_derro = self.fuzzy_control.fuzzy_models.pertinence_derror_plot()
            st.pyplot(fig_derro)

            # Potência Motor
            st.write("### Motor Power (PotenciaMotor)")
            fig_motor = self.fuzzy_control.fuzzy_models.pertinence_potencia_motor_plot()
            st.pyplot(fig_motor)

        # Visualizar tabela de regras
        if view_rules:
            st.subheader("Rules Table")
            st.write("The table below shows the rules for the Fuzzy model:")

            # Gerar a tabela de regras
            rules_df = self.fuzzy_control.infer_rules()
            st.dataframe(rules_df)
