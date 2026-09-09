import heapq

def buscar_menor_custo(grafo, origem, destino):
    """
    Executa o Algoritmo de Dijkstra para encontrar a rota de menor custo (distância em km).
    
    Retorna:
        tupla: (lista_da_rota, custo_total_km, numero_de_conexoes)
        Ou (None, 0, 0) caso não exista rota.
    """
    # Caso especial: Origem e Destino são iguais
    if origem == destino:
        return [origem], 0, 0

    # Dicionário para guardar a menor distância conhecida da origem até cada vértice.
    # Inicializamos todos com infinito, exceto a origem.
    distancias = {vertice: float('inf') for vertice in grafo.adjacencias}
    
    # Se a origem não estiver no grafo, não há rota
    if origem not in distancias:
        return None, 0, 0
        
    distancias[origem] = 0
    
    # Fila de prioridade (Min-Heap). Armazena tuplas: (custo_acumulado, vertice_atual)
    # O heapq do Python sempre extrai o menor valor com base no primeiro item da tupla (custo).
    fila_prioridade = [(0, origem)]
    
    # Dicionário para reconstruir o caminho (migalhas de pão)
    predecessores = {origem: None}
    
    while fila_prioridade:
        # Extrai o vértice com o menor custo acumulado até o momento
        custo_atual, atual = heapq.heappop(fila_prioridade)
        
        # Otimização: Se chegamos no destino, podemos parar, 
        # pois o Dijkstra garante que este já é o menor caminho possível.
        if atual == destino:
            break
            
        # Otimização (Lazy Deletion): 
        # Se encontramos na fila um custo maior do que o registrado, ignoramos.
        # Isso acontece porque podemos ter inserido o mesmo vértice com custos diferentes antes.
        if custo_atual > distancias[atual]:
            continue
            
        # Explora os vizinhos do aeroporto atual
        for vizinho in grafo.obter_vizinhos(atual):
            iata_vizinho = vizinho['destino']
            peso_aresta = vizinho['peso']
            
            # Calcula o custo para chegar no vizinho passando pelo vértice atual
            novo_custo = custo_atual + peso_aresta
            
            # Se encontramos um caminho mais barato para o vizinho, atualizamos!
            if novo_custo < distancias.get(iata_vizinho, float('inf')):
                distancias[iata_vizinho] = novo_custo
                predecessores[iata_vizinho] = atual
                
                # Colocamos a nova descoberta na fila de prioridade
                heapq.heappush(fila_prioridade, (novo_custo, iata_vizinho))
                
    # Se o destino não está nos predecessores, significa que é inalcançável
    if destino not in predecessores:
        return None, 0, 0
        
    # Reconstruindo a rota (do destino de volta para a origem)
    rota = []
    passo = destino
    while passo is not None:
        rota.append(passo)
        passo = predecessores.get(passo)
        
    # Invertemos a rota pois ela foi construída de trás para frente
    rota.reverse()
    
    # Calculando os metadados
    custo_total = distancias[destino]
    numero_de_voos = len(rota) - 1
    numero_de_conexoes = numero_de_voos - 1 if numero_de_voos > 0 else 0

    return rota, custo_total, numero_de_conexoes