import pandas as pd
import os
class Grafo:
    def __init__(self):
        self.adjacencias = {}
        '''
        Dicionario em que a chave é o IATA de origem e o valor é uma lista de dicionarios com 'destino' e 'peso/distancia'
        '''

        self.aeroportos = {}
        '''
        Chave: IATA | Valor: String formatada
        (ex: VIX : Vitória (VIX))
        '''

    def adicionar_vertice(self, iata, cidade):
        '''
        Adiciona o vertice (aeroporto) caso ele nao exista no grafo e na lista de nomes
        '''
        if iata not in self.adjacencias:
            self.adjacencias[iata] = []

        if iata not in self.aeroportos:
            self.aeroportos[iata] = f"{cidade} ({iata})"

    def adicionar_aresta(self, origem, destino, peso):
        '''
        Adiciona uma aresta direcionada e valorada na lista de adjacencias
        '''
        self.adjacencias[origem].append({
            'destino': destino,
            'peso': peso
        })

    def carregar_dados_excel(self, caminho_arquivo):
        if not os.path.exists(caminho_arquivo):
            raise FileNotFoundError(f"O arquino {caminho_arquivo} não foi encontrado.")

        try: 
            df = pd.read_excel(caminho_arquivo)

            for _, linha in df.iterrows():
                origem_iata = str(linha['origem_iata']).strip()
                origem_cidade = str(linha['origem_cidade']).strip()

                destino_iata = str(linha['destino_iata']).strip()
                destino_cidade = str(linha['destino_cidade']).strip()

                try:
                    distancia = float(linha["distancia_km"])
                except(ValueError, TypeError):
                    print(f"Erro de conversao em {origem_iata} -> {destino_iata}")
                    continue

                self.adicionar_vertice(origem_iata, origem_cidade)
                self.adicionar_vertice(destino_iata, destino_cidade)

                self.adicionar_aresta(origem_iata, destino_iata, distancia)

        except Exception as e:
            raise Exception(f"Erro ao processar arquivo Excel: {str(e)}")

    def obter_vizinhos(self, iata):
        ''''
        Retorna lista de vizinhos (destinos possiveis) de um aeroporto
        '''
        return self.adjacencias.get(iata, [])

    def obter_lista_aeroportos_ui(self):
        '''
        Retorna uma lista ordenada com os nomes dos aeroportos pra usar na UI
        '''
        lista = [(iata, nome) for iata, nome in self.aeroportos.items()]
        lista.sort(key=lambda x: x[1])
        return lista
