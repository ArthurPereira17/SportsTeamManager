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