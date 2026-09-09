from collections import deque

def buscar_menos_conexoes(grafo, origem, destino):
    """
    Executa a Busca em Largura (BFS) para encontrar a rota com menor número de conexões.
    
    Retorna:
        tupla: (lista_da_rota, custo_total_km, numero_de_conexoes)
        Ou (None, 0, 0) caso não exista rota.
    """
    # Caso especial: Origem e Destino são iguais
    if origem == destino:
        return [origem], 0, 0

    # Fila para explorar os vértices (FIFO)
    fila = deque([origem])
    
    # Conjunto para rastrear quem já foi visitado e evitar loops (ciclos no grafo)
    visitados = set([origem])
    
    # Dicionário para reconstruir o caminho depois. 
    # Guarda de onde viemos para chegar no aeroporto atual.
    # Exemplo: predecessores['GIG'] = 'VIX'
    predecessores = {origem: None}
    
    encontrou_destino = False

    while fila:
        # Remove o primeiro da fila
        atual = fila.popleft()
        
        if atual == destino:
            encontrou_destino = True
            break
            
        # Explora os vizinhos (usando o método que criamos na Etapa 1)
        for vizinho in grafo.obter_vizinhos(atual):
            iata_vizinho = vizinho['destino']
            
            if iata_vizinho not in visitados:
                visitados.add(iata_vizinho)
                predecessores[iata_vizinho] = atual
                fila.append(iata_vizinho)
                
    # Se a fila esvaziou e não achamos o destino, não existe rota
    if not encontrou_destino:
        return None, 0, 0
        
    # Reconstruindo a rota (do destino de volta para a origem)
    rota = []
    passo = destino
    while passo is not None:
        rota.append(passo)
        passo = predecessores[passo]
        
    # Invertemos a rota pois ela foi construída de trás para frente
    rota.reverse()
    
    # Calculando os metadados da rota encontrada
    numero_de_voos = len(rota) - 1
    numero_de_conexoes = numero_de_voos - 1 if numero_de_voos > 0 else 0
    
    # Calculando o custo (km) dessa rota específica (para manter o padrão da UI)
    custo_total = 0
    for i in range(len(rota) - 1):
        de = rota[i]
        para = rota[i+1]
        # Procuramos o peso da aresta na lista de adjacência
        for vizinho in grafo.obter_vizinhos(de):
            if vizinho['destino'] == para:
                custo_total += vizinho['peso']
                break

    return rota, custo_total, numero_de_conexoes