import tkinter as tk
from tkinter import ttk, messagebox

# Importamos os nossos algoritmos
from grafos.bfs import buscar_menos_conexoes
from grafos.dijkstra import buscar_menor_custo

class OtimizadorApp:
    def __init__(self, root, grafo):
        self.root = root
        self.grafo = grafo
        self.root.title("Otimizador de Rotas Aéreas")
        self.root.geometry("450x550")
        self.root.resizable(False, False)

        # Configurações de estilo do ttk
        style = ttk.Style()
        style.theme_use('clam') # Um tema limpo e compatível em qualquer SO

        # Dicionário para converter o texto do Combobox de volta para a sigla IATA
        # Ex: "Vitória (VIX)" -> "VIX"
        lista_ui = self.grafo.obter_lista_aeroportos_ui()
        self.mapa_aeroportos = {nome: iata for iata, nome in lista_ui}
        self.nomes_aeroportos = list(self.mapa_aeroportos.keys())

        self._construir_interface()

    def _construir_interface(self):
        # --- Frame Superior (Inputs) ---
        frame_inputs = ttk.Frame(self.root, padding="20")
        frame_inputs.pack(fill=tk.X)

        ttk.Label(frame_inputs, text="Origem:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.combo_origem = ttk.Combobox(frame_inputs, values=self.nomes_aeroportos, state="readonly", width=40)
        self.combo_origem.pack(pady=(0, 15))

        ttk.Label(frame_inputs, text="Destino:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.combo_destino = ttk.Combobox(frame_inputs, values=self.nomes_aeroportos, state="readonly", width=40)
        self.combo_destino.pack(pady=(0, 20))

        # --- Frame do Meio (Botões) ---
        frame_botoes = ttk.Frame(self.root, padding="0 10")
        frame_botoes.pack(fill=tk.X)

        btn_custo = ttk.Button(frame_botoes, text="Menor Custo", command=lambda: self.buscar("dijkstra"))
        btn_custo.pack(side=tk.LEFT, expand=True, padx=5, ipady=5)

        btn_conexoes = ttk.Button(frame_botoes, text="Menos Conexões", command=lambda: self.buscar("bfs"))
        btn_conexoes.pack(side=tk.RIGHT, expand=True, padx=5, ipady=5)

        # --- Frame Inferior (Resultados) ---
        frame_resultados = ttk.LabelFrame(self.root, text=" Resultado ", padding="15")
        frame_resultados.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.texto_resultado = tk.Text(frame_resultados, wrap=tk.WORD, state=tk.DISABLED, bg="#f0f0f0", font=("Consolas", 10))
        self.texto_resultado.pack(fill=tk.BOTH, expand=True)

    def buscar(self, algoritmo):
        origem_selecionada = self.combo_origem.get()
        destino_selecionado = self.combo_destino.get()

        # Validações básicas
        if not origem_selecionada or not destino_selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione a origem e o destino.")
            return

        if origem_selecionada == destino_selecionado:
            messagebox.showinfo("Informação", "A origem e o destino são iguais. Você já está no seu destino!")
            self._exibir_resultado("Você já está no seu destino.\n\nCusto total: 0 km\nConexões: 0")
            return

        # Convertendo o nome legível para IATA
        iata_origem = self.mapa_aeroportos[origem_selecionada]
        iata_destino = self.mapa_aeroportos[destino_selecionado]

        # Executando o algoritmo escolhido
        if algoritmo == "dijkstra":
            rota, custo, conexoes = buscar_menor_custo(self.grafo, iata_origem, iata_destino)
        else:
            rota, custo, conexoes = buscar_menos_conexoes(self.grafo, iata_origem, iata_destino)

        # Tratando o resultado
        if not rota:
            mensagem_erro = f"Não foi encontrada uma rota entre {iata_origem} e {iata_destino} na malha atual."
            messagebox.showwarning("Sem rota", mensagem_erro)
            self._exibir_resultado(mensagem_erro)
        else:
            self._formatar_e_exibir_sucesso(rota, custo, conexoes)

    def _formatar_e_exibir_sucesso(self, rota, custo, conexoes):
        # Transforma a lista de IATAs nos nomes completos. Ex: ['VIX', 'GIG'] -> ['Vitória (VIX)', 'Rio... (GIG)']
        rota_nomes = [self.grafo.aeroportos[iata] for iata in rota]
        
        # Junta a rota com a setinha para baixo pedida no modelo
        texto_rota = "\n      ↓\n".join(rota_nomes)
        
        resultado_final = (
            f"Rota encontrada:\n\n{texto_rota}\n\n"
            f"{'-'*30}\n"
            f"Custo total: {custo:.2f} km\n"
            f"Conexões: {conexoes}"
        )
        self._exibir_resultado(resultado_final)

    def _exibir_resultado(self, texto):
        """Atualiza a caixa de texto na interface."""
        self.texto_resultado.config(state=tk.NORMAL)
        self.texto_resultado.delete(1.0, tk.END)
        self.texto_resultado.insert(tk.END, texto)
        self.texto_resultado.config(state=tk.DISABLED)