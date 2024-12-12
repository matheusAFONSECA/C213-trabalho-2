import streamlit as st


class StreamlitApp:
    """
    A class used to represent the Streamlit application for the Fuzzy System - C213.
    Attributes
    ----------
    mqtt_client : object
        An instance of the MQTT client used for communication.
    fuzzy_control : object
        An instance of the fuzzy control system.
    Methods
    -------
    run():
        Configures and runs the Streamlit application.
    send_data_tab():
        Handles the "Send Data" tab for controlling the drone's altitude.
    visualize_data_tab():
        Handles the "Visualize Data" tab for visualizing fuzzy model data.
    """

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

        altitude = st.number_input("Enter Altitude:", value=0.0, step=0.1)

        if st.button("Send Altitude") and altitude <= 995 and altitude >= 0:
            # Ler a posição atual do arquivo
            try:
                with open("src/data/posicao_atual.txt", "r") as file:
                    current_position = float(file.read())
            except FileNotFoundError:
                current_position = 0.0  # Valor padrão se o arquivo não existir

            # Somar altitude com a posição atual
            new_position = current_position + altitude

            # Verificar se a nova posição ultrapassa o limite
            if new_position > 995:
                st.error("Altitude will surpass the maximum")

            else:
                # Passar o novo valor para o controle fuzzy
                self.fuzzy_control.Subir_e_Descer(new_position)

                # Publicar os valores calculados
                self.mqtt_client.publish(
                    self.mqtt_client.topics["altitude"], self.fuzzy_control.Pos_Atual
                )
                self.mqtt_client.publish(
                    self.mqtt_client.topics["error"], self.fuzzy_control.DeltaErroAtual
                )

                # Salvar o novo valor da posição atual no arquivo
                with open("src/data/posicao_atual.txt", "w") as file:
                    file.write(f"{self.fuzzy_control.Pos_Atual:.3f}")

                # Mostrar mensagens de sucesso
                st.success(
                    f"Altitude defined by fuzzy control {self.fuzzy_control.Pos_Atual:.3f} sent!"
                )
                st.success(
                    f"Erro defined by fuzzy control {self.fuzzy_control.DeltaErroAtual:.3f} sent!"
                )

        # Verificar se a altitude está fora do limite
        if altitude > 995 or altitude < 0:
            st.error("Altitude must be between 0 and 995!")

        if st.button("Land Drone"):
            self.fuzzy_control.Subir_e_Descer(0)

            self.mqtt_client.publish(
                self.mqtt_client.topics["altitude"], self.fuzzy_control.Pos_Atual
            )
            self.mqtt_client.publish(
                self.mqtt_client.topics["error"], self.fuzzy_control.DeltaErroAtual
            )

            # Salvar a posição atual (pouso)
            with open("src/data/posicao_atual.txt", "w") as file:
                file.write(f"{self.fuzzy_control.Pos_Atual:.3f}")

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
