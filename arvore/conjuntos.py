"""
arvore/conjuntos.py
Versão Final Dinâmica: Gera Diagramas de Venn e Grafos/Árvores.
"""
import matplotlib.pyplot as plt
from matplotlib_venn import venn3, venn2
import os
from pathlib import Path
import graphviz # Necessário para gerar os grafos
import json # Embora não usado diretamente aqui, é bom manter para possíveis expansões

# Configurações de Pastas
BASE_DIR = Path(__file__).parent.parent
OUTDIR = BASE_DIR / 'output'
OUTDIR.mkdir(exist_ok=True)

# ----------------------------------------------------
# 1. Geração do Diagrama de Venn
# ----------------------------------------------------

def salvar_venn_dinamico(dados_sets):
    """
    Gera o Diagrama de Venn (2 ou 3 conjuntos)
    Retorna o caminho do arquivo PNG gerado.
    """
    plt.figure(figsize=(10, 8))
    
    nomes = list(dados_sets.keys())
    conjuntos = list(dados_sets.values())
    
    if len(nomes) == 2:
        venn2(conjuntos, set_labels=nomes)
    elif len(nomes) == 3:
        venn3(conjuntos, set_labels=nomes)
    else:
        plt.text(0.5, 0.5, "Erro: Precisa de 2 ou 3 conjuntos!", ha='center')
        
    plt.title("Diagrama de Interseção Dinâmico")
    caminho_arquivo = OUTDIR / 'venn_custom.png'
    plt.savefig(caminho_arquivo, bbox_inches='tight')
    plt.close()
    return str(caminho_arquivo)

# ----------------------------------------------------
# 2. Geração do Grafo (Árvore Genealógica/Histórica)
# ----------------------------------------------------

def salvar_grafo_dinamico(nome_grafo, conexoes_list):
    """
    Gera um Grafo Direcionado (Árvore Genealógica/Histórica).
    conexoes_list deve ser uma lista de listas/tuplas [[Pai, Filho]]
    """
    dot = graphviz.Digraph(nome_grafo, format='png', comment=nome_grafo)

    # Configuração visual para parecer uma árvore
    dot.attr(rankdir='TB', size='10,10')
    dot.attr('node', shape='box', style='filled', color='#e0e0e0', fontname='Tahoma') # Estilo mais Win98
    dot.attr('edge', color='gray50')

    # Adiciona as conexões (A -> B)
    if conexoes_list:
        dot.edges(conexoes_list)
    
    caminho_saida = OUTDIR / 'grafo_custom'
    # renderiza o arquivo e limpa os arquivos temporários do Graphviz
    # O 'view=False' é importante para não abrir a imagem no sistema automaticamente
    dot.render(caminho_saida, cleanup=True, view=False)
    
    return str(caminho_saida) + '.png'

# ----------------------------------------------------
# DEMO
# ----------------------------------------------------
def run_gui():
    print("Use o main.py para rodar a interface.")