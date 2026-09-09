import tkinter as tk
from tkinter import messagebox
from grafos.grafo import Grafo
from interface.app import OtimizadorApp
import sys

def main():
    caminho_planilha = "dados/aerportos_brasil.xlsx"
    
    # 1. Instanciamos a estrutura de dados principal
    grafo = Grafo()
    
    # 2. Criamos a janela raiz do Tkinter ocultada primeiro, 
    # pois se der erro no Excel, mostramos um popup e fechamos
    root = tk.Tk()
    root.withdraw() 
    
    try:
        # Carregamos os dados do Excel
        grafo.carregar_dados_excel(caminho_planilha)
    except FileNotFoundError:
        messagebox.showerror(
            "Erro de Arquivo", 
            f"Não foi possível encontrar o arquivo:\n'{caminho_planilha}'\n\n"
            "Verifique se o caminho está correto e tente novamente."
        )
        sys.exit(1)
    except Exception as e:
        messagebox.showerror(
            "Erro na Leitura", 
            f"Ocorreu um erro ao ler a planilha:\n{str(e)}"
        )
        sys.exit(1)
        
    # Se o grafo estiver vazio (planilha em branco)
    if not grafo.adjacencias:
        messagebox.showerror(
            "Dados Inválidos", 
            "A planilha foi lida, mas nenhuma rota foi encontrada."
        )
        sys.exit(1)

    # 3. Tudo deu certo, revelamos a janela e iniciamos a aplicação
    root.deiconify() 
    app = OtimizadorApp(root, grafo)
    root.mainloop()

if __name__ == "__main__":
    main()