import numpy as np
import random
from flask_cors import CORS
from flask import Flask, jsonify, request

# Definir o grafo das cidades do Alto Paranaíba
class Grafo:
    def __init__(self, cidades):
        self.cidades = cidades
        self.arestas = {}  # {(cidade1, cidade2): (distancia, custo, tempo)}

    def adicionar_aresta(self, cidade1, cidade2, distancia, custo, tempo):
        self.arestas[(cidade1, cidade2)] = (distancia, custo, tempo)
        self.arestas[(cidade2, cidade1)] = (distancia, custo, tempo)


# Algoritmo de Colônia de Formigas (ACO)
class ACO:
    def __init__(self, grafo, num_formigas, alfa, beta, evap_rate, iteracoes):
        self.grafo = grafo
        self.num_formigas = num_formigas
        self.alfa = alfa
        self.beta = beta
        self.evap_rate = evap_rate
        self.iteracoes = iteracoes
        self.feromonio = {aresta: 1.0 for aresta in grafo.arestas.keys()}

    # Pesos para cada objetivo: distância, custo e tempo
    PESO_DISTANCIA = 0.5
    PESO_CUSTO = 0.3
    PESO_TEMPO = 0.2

    def calcular_probabilidades(self, cidade_atual, nao_visitadas):
        probabilidades = []
        denominador = 0

        for cidade in nao_visitadas:
            if (cidade_atual, cidade) in self.grafo.arestas:
                distancia, custo, tempo = self.grafo.arestas[(cidade_atual, cidade)]

                # Aplicar pesos na combinação dos fatores
                peso_distancia = (1.0 / distancia) ** self.beta * ACO.PESO_DISTANCIA
                peso_custo = (1.0 / custo) ** self.beta * ACO.PESO_CUSTO
                peso_tempo = (1.0 / tempo) ** self.beta * ACO.PESO_TEMPO

                peso = (self.feromonio[(cidade_atual, cidade)] ** self.alfa) * (peso_distancia + peso_custo + peso_tempo)
                probabilidades.append((cidade, peso))
                denominador += peso

        if denominador == 0:
            probabilidade_unica = 1 / len(nao_visitadas)
            return [(cidade, probabilidade_unica) for cidade in nao_visitadas]

        probabilidades = [(cidade, peso / denominador) for cidade, peso in probabilidades]
        return probabilidades


    def escolher_proxima_cidade(self, probabilidades):
        rand = random.uniform(0, 1)
        soma = 0

        for cidade, prob in probabilidades:
            soma += prob
            if rand <= soma:
                return cidade

        return probabilidades[-1][0]


    def atualizar_feromonio(self, formigas):
        for aresta in self.feromonio:
            self.feromonio[aresta] *= (1 - self.evap_rate)

        for formiga in formigas:
            caminho, dist_total, custo_total, tempo_total = formiga
            for i in range(len(caminho) - 1):
                aresta = (caminho[i], caminho[i + 1])
                if aresta in self.feromonio:
                    self.feromonio[aresta] += 1.0 / (dist_total + custo_total + tempo_total)
        
        if len(formigas) > self.num_formigas / 2:
            self.evap_rate *= 0.95
        else:
            self.evap_rate *= 1.05

    def executar(self, origem):
        melhores_rotas = []  # Lista para armazenar as melhores rotas

        for _ in range(self.iteracoes):
            formigas = []

            for _ in range(self.num_formigas):
                caminho = [origem]
                nao_visitadas = set(self.grafo.cidades) - {origem}
                distancia_total = 0
                custo_total = 0
                tempo_total = 0

                while nao_visitadas:
                    cidade_atual = caminho[-1]
                    probabilidades = self.calcular_probabilidades(cidade_atual, nao_visitadas)
                    proxima_cidade = self.escolher_proxima_cidade(probabilidades)

                    if proxima_cidade is None:
                        break

                    caminho.append(proxima_cidade)
                    nao_visitadas.remove(proxima_cidade)

                    distancia, custo, tempo = self.grafo.arestas[(cidade_atual, proxima_cidade)]
                    distancia_total += distancia
                    custo_total += custo
                    tempo_total += tempo

                caminho.append(origem)

                formigas.append((caminho, distancia_total, custo_total, tempo_total))

            self.atualizar_feromonio(formigas)

            # Ordena as formigas com base na distância, custo e tempo
            formigas.sort(key=lambda x: (x[1], x[2], x[3]))  # Ordenar pelo triplo (distância, custo, tempo)

            # Adiciona as 3 melhores rotas dessa iteração
            for i in range(min(3, len(formigas))):
                melhores_rotas.append(formigas[i])

        # Ordenar todas as rotas coletadas pelas formigas ao longo das iterações
        melhores_rotas.sort(key=lambda x: (x[1], x[2], x[3]))  # Ordenar pela combinação de distância, custo e tempo

        # Retorna as 3 melhores rotas
        return melhores_rotas[:3]  # Retorna as três melhores rotas


# Inicializar o grafo com todas as cidades do Alto Paranaíba
cidades = [
    'Patrocinio', 'Araxa', 'Uberlandia', 'Serra do Salitre', 'Monte Carmelo',
    'Coromandel', 'Carmo do Paranaiba', 'Rio Paranaiba', 'Guimarania', 'Perdizes',
    'Patos de Minas'
]

grafo = Grafo(cidades)

grafo.adicionar_aresta('Patrocinio', 'Araxa', 100, 40, 2.0)
grafo.adicionar_aresta('Patrocinio', 'Uberlandia', 150, 60, 2.5)
grafo.adicionar_aresta('Patrocinio', 'Serra do Salitre', 50, 20, 1.0)
grafo.adicionar_aresta('Patrocinio', 'Monte Carmelo', 80, 30, 1.5)
grafo.adicionar_aresta('Patrocinio', 'Coromandel', 120, 45, 2.0)
grafo.adicionar_aresta('Patrocinio', 'Carmo do Paranaiba', 90, 35, 1.7)
grafo.adicionar_aresta('Patrocinio', 'Rio Paranaiba', 110, 35, 2.0)
grafo.adicionar_aresta('Patrocinio', 'Guimarania', 140, 50, 2.3)
grafo.adicionar_aresta('Patrocinio', 'Perdizes', 130, 50, 2.3)
grafo.adicionar_aresta('Patrocinio', 'Patos de Minas', 70, 50, 3.0)

grafo.adicionar_aresta('Araxa', 'Uberlandia', 110, 45, 2.2)
grafo.adicionar_aresta('Araxa', 'Serra do Salitre', 40, 18, 0.9)
grafo.adicionar_aresta('Araxa', 'Monte Carmelo', 60, 20, 1.2)
grafo.adicionar_aresta('Araxa', 'Coromandel', 90, 30, 1.5)
grafo.adicionar_aresta('Araxa', 'Carmo do Paranaiba', 70, 25, 1.3)
grafo.adicionar_aresta('Araxa', 'Rio Paranaiba', 85, 30, 1.6)
grafo.adicionar_aresta('Araxa', 'Guimarania', 130, 55, 2.4)
grafo.adicionar_aresta('Araxa', 'Perdizes', 120, 45, 2.1)
grafo.adicionar_aresta('Araxa', 'Patos de Minas', 160, 65, 2.7)

grafo.adicionar_aresta('Uberlandia', 'Serra do Salitre', 60, 25, 1.3)
grafo.adicionar_aresta('Uberlandia', 'Monte Carmelo', 100, 40, 2.0)
grafo.adicionar_aresta('Uberlandia', 'Coromandel', 130, 50, 2.2)
grafo.adicionar_aresta('Uberlandia', 'Carmo do Paranaiba', 110, 35, 2.1)
grafo.adicionar_aresta('Uberlandia', 'Rio Paranaiba', 120, 40, 2.3)
grafo.adicionar_aresta('Uberlandia', 'Guimarania', 160, 60, 2.9)
grafo.adicionar_aresta('Uberlandia', 'Perdizes', 150, 55, 2.5)
grafo.adicionar_aresta('Uberlandia', 'Patos de Minas', 200, 70, 3.5)

grafo.adicionar_aresta('Serra do Salitre', 'Monte Carmelo', 30, 15, 0.8)
grafo.adicionar_aresta('Serra do Salitre', 'Coromandel', 70, 30, 1.2)
grafo.adicionar_aresta('Serra do Salitre', 'Carmo do Paranaiba', 60, 20, 1.0)
grafo.adicionar_aresta('Serra do Salitre', 'Rio Paranaiba', 75, 25, 1.4)
grafo.adicionar_aresta('Serra do Salitre', 'Guimarania', 100, 35, 1.7)
grafo.adicionar_aresta('Serra do Salitre', 'Perdizes', 90, 35, 1.5)
grafo.adicionar_aresta('Serra do Salitre', 'Patos de Minas', 140, 50, 2.4)

grafo.adicionar_aresta('Monte Carmelo', 'Coromandel', 50, 20, 1.0)
grafo.adicionar_aresta('Monte Carmelo', 'Carmo do Paranaiba', 40, 15, 0.9)
grafo.adicionar_aresta('Monte Carmelo', 'Rio Paranaiba', 60, 25, 1.3)
grafo.adicionar_aresta('Monte Carmelo', 'Guimarania', 90, 30, 1.7)
grafo.adicionar_aresta('Monte Carmelo', 'Perdizes', 80, 28, 1.5)
grafo.adicionar_aresta('Monte Carmelo', 'Patos de Minas', 130, 50, 2.5)

grafo.adicionar_aresta('Coromandel', 'Carmo do Paranaiba', 50, 20, 1.2)
grafo.adicionar_aresta('Coromandel', 'Rio Paranaiba', 70, 25, 1.4)
grafo.adicionar_aresta('Coromandel', 'Guimarania', 100, 35, 2.1)
grafo.adicionar_aresta('Coromandel', 'Perdizes', 90, 35, 1.9)
grafo.adicionar_aresta('Coromandel', 'Patos de Minas', 140, 55, 2.6)

grafo.adicionar_aresta('Carmo do Paranaiba', 'Rio Paranaiba', 50, 18, 1.1)
grafo.adicionar_aresta('Carmo do Paranaiba', 'Guimarania', 80, 28, 1.5)
grafo.adicionar_aresta('Carmo do Paranaiba', 'Perdizes', 70, 25, 1.4)
grafo.adicionar_aresta('Carmo do Paranaiba', 'Patos de Minas', 120, 40, 2.3)

grafo.adicionar_aresta('Rio Paranaiba', 'Guimarania', 90, 35, 1.7)
grafo.adicionar_aresta('Rio Paranaiba', 'Perdizes', 80, 28, 1.5)
grafo.adicionar_aresta('Rio Paranaiba', 'Patos de Minas', 130, 45, 2.3)

grafo.adicionar_aresta('Guimarania', 'Perdizes', 60, 20, 1.2)
grafo.adicionar_aresta('Guimarania', 'Patos de Minas', 110, 35, 1.9)

grafo.adicionar_aresta('Perdizes', 'Patos de Minas', 150, 60, 2.8)

# Configurar o ACO
aco = ACO(grafo, num_formigas=10, alfa=1, beta=2, evap_rate=0.5, iteracoes=100)

# Backend com Flask
app = Flask(__name__)

CORS(app)

@app.route('/melhor_rota', methods=['POST'])
def melhor_rota():
    data = request.json
    origem = data.get('origem', 'Patrocinio')  # Origem padrão: Patrocínio

    if origem not in grafo.cidades:
        return jsonify({'error': 'Cidade inválida!'}), 400

    melhor_distancia, melhor_custo, melhor_tempo = aco.executar(origem)
    return jsonify({
        'melhor_distancia': melhor_distancia,
        'melhor_custo': melhor_custo,
        'melhor_tempo': melhor_tempo
    })

@app.route('/rotas', methods=['POST'])
def obter_rotas():
    data = request.get_json()
    cidade_origem = data.get('origem')
    
    if not cidade_origem:
        return jsonify({"error": "Cidade de origem não fornecida"}), 400

    # Calculando as melhores rotas usando o ACO
    melhores_rotas = aco.executar(cidade_origem)
    
    rotas = []
    for rota in melhores_rotas:
        caminho, distancia, custo, tempo = rota
        rotas.append({
            "caminho": caminho,
            "distancia": distancia,
            "custo": custo,
            "tempo": tempo
        })
    
    return jsonify({"rotas": rotas})

if __name__ == '__main__':
    app.run(debug=True)