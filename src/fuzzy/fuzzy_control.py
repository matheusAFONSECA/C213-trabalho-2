import re
import numpy as np
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl
from utils.fuzzy_utils import calcular_d
from models.fuzzy_models import FuzzyModels

class FuzzyControl:
    def __init__(self):
        self.fuzzy_models = FuzzyModels()
        self.fuzzy_models.rules()
        self.Controle_Fuzz = ctrl.ControlSystemSimulation(ctrl.ControlSystem(self.fuzzy_models.Base))
        self.Pos_Atual = 0
        self.casa = None

    def infer_rules(self):
        # Inicialização da lista de tabelas
        tabela = []

        vermelho, verde, amarelo, azul, magenta, ciano = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']

        # Iteração pelos termos de Erro e dErro
        for erro in self.fuzzy_models.Erro.terms:
            for derro in self.fuzzy_models.dErro.terms:
                for regra in self.fuzzy_models.Base:
                    antecedente = str(regra).split('IF ')[1].split(' THEN')[0].replace('AND ', '')
                    consequente = str(regra).split('IF ')[1].split(' THEN')[1].split('AND ')[0]

                    classificacoes = re.findall(r'\[(.*?)\]', (antecedente + consequente))
                    if erro == classificacoes[0] and derro == classificacoes[1]:
                        tabela.append([classificacoes[0], classificacoes[1], classificacoes[2]])
                        break  # Sai do loop de regras após encontrar uma correspondência

        # Criação do DataFrame
        df = pd.DataFrame(tabela, columns=['Erro', 'dErro', 'PotenciaMotor'])

        # Criação da pivotTable
        pivotTable = pd.DataFrame(df.pivot(index='dErro', columns='Erro', values='PotenciaMotor')
                                .reindex(index=self.fuzzy_models.dErro.terms, columns=self.fuzzy_models.Erro.terms))

        # Configuração do nome do índice com o título em azul
        pivotTable.index.name = f'\033[94mDeltaErro/erro\033[0m'  # Adiciona cor azul ao título

        # Impressão da tabela formatada
        print(tabulate(pivotTable, headers='keys', tablefmt='fancy_grid', stralign='center', showindex='always'))


    def Subir_e_Descer(self, Pos_Final):
        dt = 1
        Umax = 6
        positions = [self.Pos_Atual]
        errors = [abs(Pos_Final - self.Pos_Atual)]

        for t in np.arange(1,500, 1):

            ErroAtual = abs(Pos_Final - self.Pos_Atual)
            errors.append(ErroAtual)

            if ErroAtual < 12:
                FA = 0.98
            else:
                FA = 0.99

            self.Controle_Fuzz.input['Erro'] = ErroAtual
            DeltaErroAtual = (errors[-1] - errors[-2]) / dt
            self.Controle_Fuzz.input['dErro'] = DeltaErroAtual
            self.Controle_Fuzz.compute()
            Potencia = self.Controle_Fuzz.output['PMotor']

            if ErroAtual > 5:
                P12 = Potencia
                P34 = Potencia
            else:
                P12 = 0.25
                P34 = 0.25


            dt = calcular_d(FA, self.Pos_Atual, Umax, P12, P34)

            if self.Pos_Atual < Pos_Final:
                self.Pos_Atual = dt
            else:
                delta_movement = dt - self.Pos_Atual
                self.Pos_Atual = self.Pos_Atual - delta_movement

        # Impressão dos resultados para visualização durante a simulação
            #print(f'ErroAtual: {ErroAtual:.2f} dErroAtual: {DeltaErroAtual:.2f} ->  posicaoAtual: {Pos_Atual:.2f}')

            positions.append(self.Pos_Atual)

        plt.plot(range(len(positions)), positions,"b")
        plt.show()
    
    # Função para definir a posição inicial (set_home)
    def set_home(self):
        self.casa = self.Pos_Atual
        print(f"Casa definida para: {self.casa} metros.")
        return self.casa


    # Função para mover o drone até a casa (posição inicial)
    def go_to_home(self):
            print(f"Movendo de {self.Pos_Atual} para {self.casa}.")
            self.Subir_e_Descer(self.casa)

    def ligar(self, altura=5):
        self.Subir_e_Descer(altura)
        return altura

# teste de execução do código
# if __name__ == '__main__':
#     fuzzy_control = FuzzyControl()
#     fuzzy_control.infer_rules()
#     fuzzy_control.ligar()
#     fuzzy_control.Subir_e_Descer(400)
#     fuzzy_control.set_home()
#     fuzzy_control.Subir_e_Descer(200)
#     fuzzy_control.go_to_home()