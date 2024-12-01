import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl


class FuzzyModels:
    def __init__(self):
        self.Erro = ctrl.Antecedent(universe=np.arange(0, 1001, 1), label="Erro")
        self.dErro = ctrl.Antecedent(universe=np.arange(-1000, 1001, 1), label="dErro")
        self.PotenciaMotor = ctrl.Consequent(
            universe=np.arange(0, 1.01, 0.01), label="PMotor"
        )
        self.Base = None

    def pertinence(self):
        # Definindo funções de pertinência para o erro
        self.Erro["Z"] = fuzz.trapmf(self.Erro.universe, [0, 0, 2.5, 2.5])  # Zero Error
        self.Erro["R1"] = fuzz.trimf(self.Erro.universe, [0, 15, 30])  # erro 1
        self.Erro["R2"] = fuzz.trimf(self.Erro.universe, [15, 45, 80])  # Erro 2
        self.Erro["R3"] = fuzz.trimf(self.Erro.universe, [50, 125, 350])  # Erro 3
        self.Erro["R4"] = fuzz.trapmf(
            self.Erro.universe, [125, 800, 1000, 1000]
        )  # Erro 4

        # Funções de pertinência para 'DeltaErro'
        self.dErro["MB"] = fuzz.trapmf(
            self.dErro.universe, [-1000, -1000, -5, -2.5]
        )  # Grande Negativo
        self.dErro["B"] = fuzz.trimf(
            self.dErro.universe, [-5, -2.5, 0]
        )  # Pequeno Negativo
        self.dErro["Z"] = fuzz.trimf(
            self.dErro.universe, [-2.5, 0, 2.5]
        )  # Estabilizado
        self.dErro["A"] = fuzz.trimf(
            self.dErro.universe, [0, 2.5, 5]
        )  # Pequeno Positivo
        self.dErro["MA"] = fuzz.trapmf(
            self.dErro.universe, [2.5, 5, 1000, 1000]
        )  # Grande Positivo

        # Funções de pertinência para PMotor -----> PHn,m ⊂ [0, 1]
        self.PotenciaMotor["I"] = fuzz.trapmf(
            self.PotenciaMotor.universe, [0, 0, 0.1, 0.25]
        )  # Potência Inicio
        self.PotenciaMotor["B"] = fuzz.trimf(
            self.PotenciaMotor.universe, [0.10, 0.25, 0.50]
        )  # Potência Baixa
        self.PotenciaMotor["M"] = fuzz.trimf(
            self.PotenciaMotor.universe, [0.30, 0.50, 0.75]
        )  # Potência Média
        self.PotenciaMotor["A"] = fuzz.trapmf(
            self.PotenciaMotor.universe, [0.50, 0.75, 1, 1]
        )  # Potência Alta

    def pertinence_error_plot(self):
        # Plot para Erro
        self.Erro.view()
        plt.title("Funções de Pertinência - Erro")
        return plt

    def pertinence_derror_plot(self):
        # Plot para Delta Erro
        self.dErro.view()
        plt.title("Funções de Pertinência - Delta Erro")
        return plt

    def pertinence_potencia_motor_plot(self):
        # Plot para Potência Motor
        self.PotenciaMotor.view()
        plt.title("Funções de Pertinência - Potencia Motor")
        return plt

    def pertinence_plots(self):
        self.pertinence_error_plot()
        self.pertinence_derror_plot()
        self.pertinence_potencia_motor_plot()
        plt.show()

    def rules(self):
        # Definindo funções de pertinência
        self.pertinence()

        # Base de Regras corrigida
        R1 = ctrl.Rule(
            self.Erro["Z"] & self.dErro["MB"], self.PotenciaMotor["I"]
        )  # Z + MP -> MP
        R2 = ctrl.Rule(
            self.Erro["Z"] & self.dErro["B"], self.PotenciaMotor["B"]
        )  # Z + P -> P
        R3 = ctrl.Rule(
            self.Erro["Z"] & self.dErro["Z"], self.PotenciaMotor["M"]
        )  # Z + Z -> MP
        R4 = ctrl.Rule(
            self.Erro["Z"] & self.dErro["A"], self.PotenciaMotor["A"]
        )  # Z + N -> M
        R5 = ctrl.Rule(
            self.Erro["Z"] & self.dErro["MA"], self.PotenciaMotor["A"]
        )  # Z + MN -> MG

        R6 = ctrl.Rule(
            self.Erro["R1"] & self.dErro["MB"], self.PotenciaMotor["I"]
        )  # P + MP -> MP
        R7 = ctrl.Rule(
            self.Erro["R1"] & self.dErro["B"], self.PotenciaMotor["B"]
        )  # P + P -> P
        R8 = ctrl.Rule(
            self.Erro["R1"] & self.dErro["Z"], self.PotenciaMotor["M"]
        )  # P + Z -> P
        R9 = ctrl.Rule(
            self.Erro["R1"] & self.dErro["A"], self.PotenciaMotor["M"]
        )  # P + N -> G
        R10 = ctrl.Rule(
            self.Erro["R1"] & self.dErro["MA"], self.PotenciaMotor["M"]
        )  # P + MN -> M

        R11 = ctrl.Rule(
            self.Erro["R2"] & self.dErro["MB"], self.PotenciaMotor["B"]
        )  # M + MP -> P
        R12 = ctrl.Rule(
            self.Erro["R2"] & self.dErro["B"], self.PotenciaMotor["B"]
        )  # M + P -> G
        R13 = ctrl.Rule(
            self.Erro["R2"] & self.dErro["Z"], self.PotenciaMotor["M"]
        )  # M + Z -> M
        R14 = ctrl.Rule(
            self.Erro["R2"] & self.dErro["A"], self.PotenciaMotor["M"]
        )  # M + N -> G
        R15 = ctrl.Rule(
            self.Erro["R2"] & self.dErro["MA"], self.PotenciaMotor["A"]
        )  # M + MN -> MG

        R16 = ctrl.Rule(
            self.Erro["R3"] & self.dErro["MB"], self.PotenciaMotor["B"]
        )  # G + MP -> MP
        R17 = ctrl.Rule(
            self.Erro["R3"] & self.dErro["B"], self.PotenciaMotor["M"]
        )  # G + P -> P
        R18 = ctrl.Rule(
            self.Erro["R3"] & self.dErro["Z"], self.PotenciaMotor["M"]
        )  # G + Z -> G
        R19 = ctrl.Rule(
            self.Erro["R3"] & self.dErro["A"], self.PotenciaMotor["A"]
        )  # G + N -> MG
        R20 = ctrl.Rule(
            self.Erro["R3"] & self.dErro["MA"], self.PotenciaMotor["A"]
        )  # G + MN -> MG

        R21 = ctrl.Rule(
            self.Erro["R4"] & self.dErro["MB"], self.PotenciaMotor["M"]
        )  # MG + MP -> P
        R22 = ctrl.Rule(
            self.Erro["R4"] & self.dErro["B"], self.PotenciaMotor["M"]
        )  # MG + P -> P
        R23 = ctrl.Rule(
            self.Erro["R4"] & self.dErro["Z"], self.PotenciaMotor["A"]
        )  # MG + Z -> G
        R24 = ctrl.Rule(
            self.Erro["R4"] & self.dErro["A"], self.PotenciaMotor["A"]
        )  # MG + N -> MG
        R25 = ctrl.Rule(
            self.Erro["R4"] & self.dErro["MA"], self.PotenciaMotor["A"]
        )  # MG + MN -> MG

        self.Base = [
            R1,
            R2,
            R3,
            R4,
            R5,
            R6,
            R7,
            R8,
            R9,
            R10,
            R11,
            R12,
            R13,
            R14,
            R15,
            R16,
            R17,
            R18,
            R19,
            R20,
            R21,
            R22,
            R23,
            R24,
            R25,
        ]


# teste de funcionalidade para
# if __name__ == "__main__":
#     fm = FuzzyModels()
#     fm.pertinence()
#     fm.pertinence_plots()
#     fm.rules()
#     print(fm.Base)
