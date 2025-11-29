import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from PIL import Image, ImageTk
import sys
import os
import re 

# --- Configuração de Caminhos ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

# Importa o motor (Backend: Funções de geração do conjuntos.py)
try:
    # Garante que as funções salvar_venn_dinamico e salvar_grafo_dinamico estão disponíveis
    from arvore import conjuntos 
except ImportError as e:
    messagebox.showerror("Erro Crítico de Importação", f"Não foi possível encontrar 'arvore/conjuntos.py'. Verifique a estrutura de pastas.\nErro: {e}")
    sys.exit()

class Win98Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Conjuntos Históricos - Build 98")
        # Aumentamos a altura para caber os formulários sem apertar
        self.root.geometry("850x750") 
        
        # Cores Win98
        self.cinza = "#d4d0c8"
        self.azul_titulo = "#000080"
        self.root.configure(bg=self.cinza)

        # Estilo (Tema 'winnative' ou 'classic')
        self.style = ttk.Style()
        if 'winnative' in self.style.theme_names():
            self.style.theme_use('winnative')
        else:
            self.style.theme_use('classic')
            
        self.style.configure(".", background=self.cinza, font=("Tahoma", 8))
        self.style.configure("TNotebook", background=self.cinza)
        self.style.configure("TNotebook.Tab", padding=[10, 2], font=("Tahoma", 8))

        self.construir_interface()

    def construir_interface(self):
        # Topo Azul (Barra de Título Falsa)
        top_bar = tk.Frame(self.root, bg=self.azul_titulo, height=30)
        top_bar.pack(fill="x", padx=2, pady=2)
        tk.Label(top_bar, text=" Gerenciador de Conjuntos v2.0", fg="white", bg=self.azul_titulo, font=("Tahoma", 9, "bold")).pack(side="left", pady=4)

        # === SISTEMA DE ABAS ===
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # Aba 1: Criação de Diagrama de Venn (Venn)
        frame_venn = tk.Frame(notebook, bg=self.cinza)
        notebook.add(frame_venn, text="  📝 Criar Diagrama (Venn)  ")
        self.montar_aba_venn(frame_venn)

        # Aba 2: Criação de Grafo Histórico (Grafo) -- Ordem Corrigida!
        frame_grafo = tk.Frame(notebook, bg=self.cinza)
        notebook.add(frame_grafo, text="  🌳 Criar Grafo (Árvore)  ")
        self.montar_aba_grafo(frame_grafo)

        # Aba 3: Sobre (Final)
        frame_sobre = tk.Frame(notebook, bg="white", relief="sunken", bd=2)
        notebook.add(frame_sobre, text="  ℹ️ Sobre  ")
        self.montar_aba_sobre(frame_sobre) # Certificando que esta função é chamada

        # Status Bar (Rodapé)
        self.lbl_status = tk.Label(self.root, text=" Aguardando entrada de dados...", bd=1, relief="sunken", anchor="w", bg=self.cinza)
        self.lbl_status.pack(side="bottom", fill="x")

# --- FUNÇÕES DE MONTAGEM DE ABAS ---

    def montar_aba_venn(self, parent):
        # LabelFrame com borda 3D
        frame_form = tk.LabelFrame(parent, text=" Entrada de Dados - Diagrama de Venn (Máx 3 Conjuntos) ", bg=self.cinza, padx=10, pady=10)
        frame_form.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbar (necessário para janelas pequenas)
        canvas = tk.Canvas(frame_form, bg=self.cinza); canvas.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame_form, orient="vertical", command=canvas.yview); scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        inner_frame = tk.Frame(canvas, bg=self.cinza)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # CAMPOS DE ENTRADA (A, B, C)
        
        # A
        tk.Label(inner_frame, text="Nome do Conjunto A (Ex: Família Real):").pack(anchor="w")
        self.entry_name_a = tk.Entry(inner_frame, width=40); self.entry_name_a.pack(anchor="w", pady=(0, 5))
        tk.Label(inner_frame, text="Membros de A (separados por vírgula):").pack(anchor="w")
        self.entry_members_a = tk.Entry(inner_frame, width=80); self.entry_members_a.pack(anchor="w", pady=(0, 15))
        self.entry_members_a.insert(0, "Pedro I, Maria I, João VI") 

        # B
        tk.Label(inner_frame, text="Nome do Conjunto B (Ex: Políticos):").pack(anchor="w")
        self.entry_name_b = tk.Entry(inner_frame, width=40); self.entry_name_b.pack(anchor="w", pady=(0, 5))
        tk.Label(inner_frame, text="Membros de B (separados por vírgula):").pack(anchor="w")
        self.entry_members_b = tk.Entry(inner_frame, width=80); self.entry_members_b.pack(anchor="w", pady=(0, 15))
        self.entry_members_b.insert(0, "Pedro I, José Bonifácio, Anita Garibaldi")

        # C (Opcional)
        tk.Label(inner_frame, text="Nome do Conjunto C (Opcional):").pack(anchor="w")
        self.entry_name_c = tk.Entry(inner_frame, width=40); self.entry_name_c.pack(anchor="w", pady=(0, 5))
        tk.Label(inner_frame, text="Membros de C (separados por vírgula):").pack(anchor="w")
        self.entry_members_c = tk.Entry(inner_frame, width=80); self.entry_members_c.pack(anchor="w", pady=(0, 15))

        # Botão
        btn_gerar = tk.Button(inner_frame, text="GERAR DIAGRAMA AGORA", font=("Tahoma", 10, "bold"), bg="#c0c0c0", command=self.processar_venn)
        btn_gerar.pack(pady=10, fill="x")


    def montar_aba_grafo(self, parent):
        frame_form = tk.LabelFrame(parent, text=" Entrada de Dados - Grafo/Árvore (Pai -> Filho) ", bg=self.cinza, padx=10, pady=10)
        frame_form.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbar
        canvas = tk.Canvas(frame_form, bg=self.cinza); canvas.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame_form, orient="vertical", command=canvas.yview); scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        inner_frame = tk.Frame(canvas, bg=self.cinza)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


        tk.Label(inner_frame, text="Nome do Grafo (Ex: Linhagem Imperial):").pack(anchor="w")
        self.entry_grafo_nome = tk.Entry(inner_frame, width=40)
        self.entry_grafo_nome.pack(anchor="w", pady=(0, 15))
        self.entry_grafo_nome.insert(0, "Linhagem Imperial Brasileira")

        tk.Label(inner_frame, text="Conexões (FORMATO: PAI -> FILHO, uma por linha)").pack(anchor="w")
        tk.Label(inner_frame, text="Ex: D. João VI -> D. Pedro I\nD. Pedro I -> D. Pedro II", fg="blue").pack(anchor="w")

        # Usamos Text para aceitar múltiplas linhas
        self.text_grafo_conexoes = tk.Text(inner_frame, width=80, height=15, relief="sunken", bd=2, font=("Courier New", 10))
        self.text_grafo_conexoes.pack(anchor="w", pady=(0, 15))
        self.text_grafo_conexoes.insert("1.0", "D. João VI -> D. Pedro I\nD. Pedro I -> D. Pedro II\nD. Pedro II -> Princesa Isabel\nPrincesa Isabel -> Príncipe Gastão")

        # Botão
        btn_gerar = tk.Button(inner_frame, text="GERAR GRAFO/ÁRVORE AGORA", font=("Tahoma", 10, "bold"), bg="#c0c0c0", command=self.processar_grafo)
        btn_gerar.pack(pady=10, fill="x")

    def montar_aba_sobre(self, parent):
        # Texto da aba Sobre
        tk.Label(parent, text="\n SISTEMA DE CONJUNTOS HISTÓRICOS v2.0", bg="white", font=("Tahoma", 12, "bold")).pack(pady=20)
        
        sobre_texto = (
            "Este software foi desenvolvido para o projeto 'Árvore Genealógica de Conjuntos'.\n\n"
            "🧠 **Matemática (Ensino Médio/Universitário):**\n"
            "Demonstra **Pertinência** e **Interseção** na prática através dos Diagramas de Venn, usando estruturas de dados do Python (Sets) para manipulação lógica de conjuntos.\n\n"
            "🌳 **Grafo:**\n"
            "Utiliza a teoria de Grafos (Graphviz) para representar **hierarquia** e **conexões de sucessão** ('Pai -> Filho'), modelando a estrutura genealógica ou de influência histórica."
        )
        tk.Label(parent, text=sobre_texto, bg="white", justify="left", font=("Tahoma", 10)).pack(padx=20, anchor="w")

# --- FUNÇÕES DE PROCESSAMENTO (Lógica) ---

    def processar_venn(self):
        # 1. Captura os dados
        nome_a = self.entry_name_a.get().strip(); membros_a = {x.strip() for x in self.entry_members_a.get().split(',') if x.strip()}
        nome_b = self.entry_name_b.get().strip(); membros_b = {x.strip() for x in self.entry_members_b.get().split(',') if x.strip()}
        nome_c = self.entry_name_c.get().strip(); membros_c = {x.strip() for x in self.entry_members_c.get().split(',') if x.strip()}

        if not nome_a or not nome_b:
            messagebox.showwarning("Erro", "Preencha pelo menos os Nomes e Membros de A e B!")
            return

        dados = {nome_a: membros_a, nome_b: membros_b}
        if nome_c and membros_c:
            dados[nome_c] = membros_c

        self.lbl_status.config(text=" Processando Venn...")
        self.root.update()

        try:
            caminho = conjuntos.salvar_venn_dinamico(dados)
            self.abrir_janela_resultado(caminho, "Visualizador de Venn")
            self.lbl_status.config(text=" Diagrama de Venn gerado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro no Backend", f"Erro no Matplotlib/Venn:\n{e}")
            self.lbl_status.config(text=" Erro.")

    def processar_grafo(self):
        nome = self.entry_grafo_nome.get().strip()
        texto_conexoes = self.text_grafo_conexoes.get("1.0", tk.END).strip()

        if not nome or not texto_conexoes:
            messagebox.showwarning("Erro", "Preencha o nome do grafo e as conexões!")
            return

        # Converte o texto (Pai -> Filho) em lista de listas [[Pai, Filho]]
        conexoes_list = []
        for linha in texto_conexoes.split('\n'):
            # Regex para encontrar o formato A -> B
            match = re.match(r"\s*([^->]+)\s*->\s*([^->]+)\s*", linha)
            if match:
                pai = match.group(1).strip()
                filho = match.group(2).strip()
                conexoes_list.append([pai, filho])
        
        if not conexoes_list:
             messagebox.showwarning("Erro", "Formato inválido. Use 'Pai -> Filho' por linha.")
             return

        self.lbl_status.config(text=" Processando Grafo (Graphviz)...")
        self.root.update()

        try:
            caminho = conjuntos.salvar_grafo_dinamico(nome, conexoes_list)
            self.abrir_janela_resultado(caminho, "Visualizador de Grafo")
            self.lbl_status.config(text=" Grafo gerado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro no Backend", f"Erro ao gerar Grafo. Verifique se o Graphviz está instalado no sistema operacional e no PATH.\nDetalhe: {e}")
            self.lbl_status.config(text=" Erro.")


    def abrir_janela_resultado(self, caminho_imagem, titulo):
        # Janela Filha (Toplevel) para mostrar o resultado
        if not os.path.exists(caminho_imagem):
            messagebox.showwarning("Aviso", "O backend não salvou a imagem.")
            return

        win = Toplevel(self.root)
        win.title(titulo)
        win.geometry("800x600")
        win.configure(bg=self.cinza)

        try:
            img = Image.open(caminho_imagem)
            img.thumbnail((750, 550))
            img_tk = ImageTk.PhotoImage(img)

            # Moldura com relevo 'sunken' (afundado)
            frame_img = tk.Frame(win, bd=2, relief="sunken", bg="gray")
            frame_img.pack(expand=True, fill="both", padx=10, pady=10)
            
            lbl = tk.Label(frame_img, image=img_tk, bg="gray")
            lbl.image = img_tk
            lbl.pack(expand=True)
            
            ttk.Button(win, text="Fechar Janela", command=win.destroy).pack(pady=5)
        except Exception as e:
            tk.Label(win, text=f"Erro ao carregar imagem: {e}").pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = Win98Dashboard(root)
    root.mainloop()