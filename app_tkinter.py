# app_tkinter. py

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from crud import GerenciadorEsportes

class AppEsportes:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento Esportivo")
        self.root.geometry("600x300")
        self.root.configure(bg='#f0f0f0')

        self.gerenciador = GerenciadorEsportes()

        self.setup_estilo()

        self.criar_menu()
        self.criar_widgets()

        self.atulizar_lista_times()
        self.atualizar_lista_jogadores()
    
    def setup_estilo(self):
        style = ttk.Style()
        style.theme_use('clam')

        self.cor_principal = '#2c3e50'
        self.cor_destaque = '#3498db'
        self.cor_sucesso = '#27ae60'
        self.cor_perigo = '#e74c3c'

        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TNotebook.Tab', padding=[10, 5], font=('Arial', 12, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', self.cor_destaque)])

    def criar_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        arquivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=arquivo_menu)
        arquivo_menu.add_command(label='Salvar Dados', command=self.salvar_dados)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label='Sair', command=self.root.quit)

        relatorios_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Relatórios", menu=relatorios_menu)
        relatorios_menu.add_command(label='Estatísticas', command=self.mostrar_estatisticas)
        relatorios_menu.add_command(label='Jogadores Livres', command=self.mostrar_jogadores_livres)

    def criar_widgets(self):
        self.notebook = tk.Menu(menubar, tearoff=0)
        