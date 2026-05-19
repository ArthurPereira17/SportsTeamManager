# app_tkinter.py

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from crud import GerenciadorEsportes

class AppEsportes:
    def __init__(self, root):
        self.root = root
        self.root.title("🏆 Sistema de Gerenciamento Esportivo")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f0f0')
        
        # Instancia o gerenciador
        self.gerenciador = GerenciadorEsportes()
        
        # Configurar estilo
        self.setup_estilo()
        
        # Criar interface
        self.criar_menu()
        self.criar_widgets()
        
        # Atualizar listas iniciais
        self.atualizar_lista_times()
        self.atualizar_lista_jogadores()
    
    def setup_estilo(self):
        """Configura o estilo visual"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Cores personalizadas
        self.cor_principal = '#2c3e50'
        self.cor_destaque = '#3498db'
        self.cor_sucesso = '#27ae60'
        self.cor_perigo = '#e74c3c'
        
        # Configurar estilos das abas
        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TNotebook.Tab', padding=[10, 5], font=('Arial', 10, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', self.cor_destaque)])
    
    def criar_menu(self):
        """Cria a barra de menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Arquivo
        arquivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=arquivo_menu)
        arquivo_menu.add_command(label="Salvar Dados", command=self.salvar_dados)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label="Sair", command=self.root.quit)
        
        # Menu Relatórios
        relatorios_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Relatórios", menu=relatorios_menu)
        relatorios_menu.add_command(label="Estatísticas", command=self.mostrar_estatisticas)
        relatorios_menu.add_command(label="Jogadores Livres", command=self.mostrar_jogadores_livres)
        
        # Menu Ajuda
        ajuda_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=ajuda_menu)
        ajuda_menu.add_command(label="Sobre", command=self.mostrar_sobre)
    
    def criar_widgets(self):
        """Cria os widgets principais"""
        # Frame principal com abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Aba de Times
        self.frame_times = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_times, text="📋 Times")
        self.criar_aba_times()
        
        # Aba de Jogadores
        self.frame_jogadores = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_jogadores, text="⚽ Jogadores")
        self.criar_aba_jogadores()
        
        # Aba de Transferências
        self.frame_transferencias = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_transferencias, text="🔄 Transferências")
        self.criar_aba_transferencias()
    
    def criar_aba_times(self):
        """Cria a interface da aba de Times"""
        # Frame de formulário
        frame_form = tk.LabelFrame(self.frame_times, text="Cadastro de Time", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        frame_form.pack(fill='x', padx=10, pady=10)
        
        # Campos do formulário
        tk.Label(frame_form, text="Nome:", bg='#f0f0f0', font=('Arial', 10)).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_nome_time = tk.Entry(frame_form, width=30, font=('Arial', 10))
        self.entry_nome_time.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="Cidade:", bg='#f0f0f0', font=('Arial', 10)).grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.entry_cidade_time = tk.Entry(frame_form, width=30, font=('Arial', 10))
        self.entry_cidade_time.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(frame_form, text="Técnico:", bg='#f0f0f0', font=('Arial', 10)).grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_tecnico_time = tk.Entry(frame_form, width=30, font=('Arial', 10))
        self.entry_tecnico_time.grid(row=1, column=1, padx=5, pady=5)
        
        # Botões
        frame_botoes = tk.Frame(frame_form, bg='#f0f0f0')
        frame_botoes.grid(row=2, column=0, columnspan=4, pady=10)
        
        tk.Button(frame_botoes, text="➕ Adicionar Time", command=self.adicionar_time,
                 bg=self.cor_sucesso, fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=5).pack(side='left', padx=5)
        
        tk.Button(frame_botoes, text="✏️ Atualizar Time", command=self.atualizar_time,
                 bg=self.cor_destaque, fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=5).pack(side='left', padx=5)
        
        tk.Button(frame_botoes, text="🗑️ Deletar Time", command=self.deletar_time,
                 bg=self.cor_perigo, fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=5).pack(side='left', padx=5)
        
        # Lista de times
        frame_lista = tk.LabelFrame(self.frame_times, text="Times Cadastrados", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        frame_lista.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview para lista de times
        columns = ('ID', 'Nome', 'Cidade', 'Técnico')
        self.tree_times = ttk.Treeview(frame_lista, columns=columns, show='headings', height=15)
        
        # Configurar colunas
        self.tree_times.heading('ID', text='ID')
        self.tree_times.heading('Nome', text='Nome')
        self.tree_times.heading('Cidade', text='Cidade')
        self.tree_times.heading('Técnico', text='Técnico')
        
        self.tree_times.column('ID', width=50)
        self.tree_times.column('Nome', width=200)
        self.tree_times.column('Cidade', width=150)
        self.tree_times.column('Técnico', width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_lista, orient='vertical', command=self.tree_times.yview)
        self.tree_times.configure(yscrollcommand=scrollbar.set)
        
        self.tree_times.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind de seleção
        self.tree_times.bind('<<TreeviewSelect>>', self.on_time_selected)
    
    def criar_aba_jogadores(self):
        """Cria a interface da aba de Jogadores"""
        # Frame de formulário
        frame_form = tk.LabelFrame(self.frame_jogadores, text="Cadastro de Jogador", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        frame_form.pack(fill='x', padx=10, pady=10)
        
        # Campos
        tk.Label(frame_form, text="Nome:", bg='#f0f0f0', font=('Arial', 10)).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_nome_jogador = tk.Entry(frame_form, width=30, font=('Arial', 10))
        self.entry_nome_jogador.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="Posição:", bg='#f0f0f0', font=('Arial', 10)).grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.combo_posicao = ttk.Combobox(frame_form, values=['Goleiro', 'Defensor', 'Meio-campo', 'Atacante'], width=27)
        self.combo_posicao.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(frame_form, text="Nº Camisa:", bg='#f0f0f0', font=('Arial', 10)).grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_numero = tk.Entry(frame_form, width=30, font=('Arial', 10))
        self.entry_numero.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="Time:", bg='#f0f0f0', font=('Arial', 10)).grid(row=1, column=2, padx=5, pady=5, sticky='e')
        self.combo_time_jogador = ttk.Combobox(frame_form, width=27)
        self.combo_time_jogador.grid(row=1, column=3, padx=5, pady=5)
        
        # Botões
        frame_botoes = tk.Frame(frame_form, bg='#f0f0f0')
        frame_botoes.grid(row=2, column=0, columnspan=4, pady=10)
        
        tk.Button(frame_botoes, text="➕ Adicionar Jogador", command=self.adicionar_jogador,
                 bg=self.cor_sucesso, fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=5).pack(side='left', padx=5)
        
        tk.Button(frame_botoes, text="✏️ Atualizar Jogador", command=self.atualizar_jogador,
                 bg=self.cor_destaque, fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=5).pack(side='left', padx=5)
        
        tk.Button(frame_botoes, text="🗑️ Deletar Jogador", command=self.deletar_jogador,
                 bg=self.cor_perigo, fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=5).pack(side='left', padx=5)
        
        # Lista de jogadores
        frame_lista = tk.LabelFrame(self.frame_jogadores, text="Jogadores Cadastrados", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        frame_lista.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview para lista de jogadores
        columns = ('ID', 'Nome', 'Posição', 'Camisa', 'Time')
        self.tree_jogadores = ttk.Treeview(frame_lista, columns=columns, show='headings', height=15)
        
        self.tree_jogadores.heading('ID', text='ID')
        self.tree_jogadores.heading('Nome', text='Nome')
        self.tree_jogadores.heading('Posição', text='Posição')
        self.tree_jogadores.heading('Camisa', text='Camisa')
        self.tree_jogadores.heading('Time', text='Time')
        
        self.tree_jogadores.column('ID', width=50)
        self.tree_jogadores.column('Nome', width=200)
        self.tree_jogadores.column('Posição', width=100)
        self.tree_jogadores.column('Camisa', width=80)
        self.tree_jogadores.column('Time', width=150)
        
        scrollbar = ttk.Scrollbar(frame_lista, orient='vertical', command=self.tree_jogadores.yview)
        self.tree_jogadores.configure(yscrollcommand=scrollbar.set)
        
        self.tree_jogadores.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.tree_jogadores.bind('<<TreeviewSelect>>', self.on_jogador_selected)
        
        # Atualizar combo de times
        self.atualizar_combo_times()
    
    def criar_aba_transferencias(self):
        """Cria a interface da aba de Transferências"""
        frame_principal = tk.Frame(self.frame_transferencias, bg='#f0f0f0')
        frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(frame_principal, text="🔄 Sistema de Transferências", 
                font=('Arial', 16, 'bold'), bg='#f0f0f0', fg=self.cor_principal).pack(pady=20)
        
        # Frame de seleção
        frame_selecao = tk.Frame(frame_principal, bg='#f0f0f0')
        frame_selecao.pack(pady=20)
        
        tk.Label(frame_selecao, text="Jogador:", bg='#f0f0f0', font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=10)
        self.combo_jogador_transferencia = ttk.Combobox(frame_selecao, width=40, font=('Arial', 10))
        self.combo_jogador_transferencia.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(frame_selecao, text="Novo Time:", bg='#f0f0f0', font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=10)
        self.combo_time_transferencia = ttk.Combobox(frame_selecao, width=40, font=('Arial', 10))
        self.combo_time_transferencia.grid(row=1, column=1, padx=10, pady=10)
        
        # Botão transferir
        tk.Button(frame_principal, text="🔄 Realizar Transferência", command=self.realizar_transferencia,
                 bg=self.cor_destaque, fg='white', font=('Arial', 12, 'bold'),
                 padx=30, pady=10).pack(pady=30)
        
        # Atualizar combos
        self.atualizar_combos_transferencia()
    
    def atualizar_lista_times(self):
        """Atualiza a treeview de times"""
        # Limpar lista atual
        for item in self.tree_times.get_children():
            self.tree_times.delete(item)
        
        # Adicionar times
        for time in self.gerenciador.listar_times():
            self.tree_times.insert('', 'end', values=(time.id, time.nome, time.cidade, time.tecnico))
    
    def atualizar_lista_jogadores(self):
        """Atualiza a treeview de jogadores"""
        # Limpar lista atual
        for item in self.tree_jogadores.get_children():
            self.tree_jogadores.delete(item)
        
        # Adicionar jogadores
        for jogador in self.gerenciador.listar_jogadores():
            # Buscar nome do time
            nome_time = "Agente Livre"
            if jogador.id_time != 0:
                time = self.gerenciador.buscar_time_por_id(jogador.id_time)
                if time:
                    nome_time = time.nome
            
            self.tree_jogadores.insert('', 'end', values=(
                jogador.id, jogador.nome, jogador.posicao, 
                jogador.numero_camisa, nome_time
            ))
    
    def atualizar_combo_times(self):
        """Atualiza o combobox de times"""
        times = self.gerenciador.listar_times()
        opcoes = ["Agente Livre"] + [f"{t.id} - {t.nome}" for t in times]
        self.combo_time_jogador['values'] = opcoes
    
    def atualizar_combos_transferencia(self):
        """Atualiza os comboboxes da aba de transferências"""
        # Lista de jogadores
        jogadores = self.gerenciador.listar_jogadores()
        opcoes_jogadores = [f"{j.id} - {j.nome} ({j.posicao})" for j in jogadores]
        self.combo_jogador_transferencia['values'] = opcoes_jogadores
        
        # Lista de times
        times = self.gerenciador.listar_times()
        opcoes_times = ["Agente Livre"] + [f"{t.id} - {t.nome}" for t in times]
        self.combo_time_transferencia['values'] = opcoes_times
    
    def adicionar_time(self):
        """Adiciona um novo time"""
        nome = self.entry_nome_time.get().strip()
        cidade = self.entry_cidade_time.get().strip()
        tecnico = self.entry_tecnico_time.get().strip()
        
        if not nome:
            messagebox.showwarning("Aviso", "O nome do time é obrigatório!")
            return
        
        self.gerenciador.criar_time(nome, cidade, tecnico)
        self.atualizar_lista_times()
        self.atualizar_combo_times()
        self.atualizar_combos_transferencia()
        
        # Limpar campos
        self.entry_nome_time.delete(0, tk.END)
        self.entry_cidade_time.delete(0, tk.END)
        self.entry_tecnico_time.delete(0, tk.END)
        
        messagebox.showinfo("Sucesso", f"Time '{nome}' adicionado com sucesso!")
    
    def atualizar_time(self):
        """Atualiza o time selecionado"""
        selecionado = self.tree_times.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um time para atualizar!")
            return
        
        # Pegar ID do time selecionado
        item = self.tree_times.item(selecionado[0])
        id_time = item['values'][0]
        
        nome = self.entry_nome_time.get().strip()
        cidade = self.entry_cidade_time.get().strip()
        tecnico = self.entry_tecnico_time.get().strip()
        
        if self.gerenciador.atualizar_time(id_time, nome, cidade, tecnico):
            self.atualizar_lista_times()
            self.atualizar_combo_times()
            self.atualizar_combos_transferencia()
            messagebox.showinfo("Sucesso", "Time atualizado com sucesso!")
            
            # Limpar campos
            self.entry_nome_time.delete(0, tk.END)
            self.entry_cidade_time.delete(0, tk.END)
            self.entry_tecnico_time.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Erro ao atualizar time!")
    
    def deletar_time(self):
        """Deleta o time selecionado"""
        selecionado = self.tree_times.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um time para deletar!")
            return
        
        item = self.tree_times.item(selecionado[0])
        id_time = item['values'][0]
        nome_time = item['values'][1]
        
        # Confirmar exclusão
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja deletar o time '{nome_time}'?"):
            if self.gerenciador.deletar_time(id_time):
                self.atualizar_lista_times()
                self.atualizar_combo_times()
                self.atualizar_combos_transferencia()
                messagebox.showinfo("Sucesso", "Time deletado com sucesso!")
            else:
                messagebox.showerror("Erro", "Não foi possível deletar o time (verifique se não há jogadores associados)!")
    
    def adicionar_jogador(self):
        """Adiciona um novo jogador"""
        nome = self.entry_nome_jogador.get().strip()
        posicao = self.combo_posicao.get()
        numero = self.entry_numero.get().strip()
        time_selecionado = self.combo_time_jogador.get()
        
        if not nome or not posicao or not numero:
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios!")
            return
        
        try:
            numero = int(numero)
        except ValueError:
            messagebox.showwarning("Aviso", "Número da camisa deve ser um valor numérico!")
            return
        
        # Processar time
        id_time = 0
        if time_selecionado != "Agente Livre":
            id_time = int(time_selecionado.split(' - ')[0])
        
        jogador = self.gerenciador.criar_jogador(nome, posicao, numero, id_time)
        if jogador:
            self.atualizar_lista_jogadores()
            self.atualizar_combos_transferencia()
            
            # Limpar campos
            self.entry_nome_jogador.delete(0, tk.END)
            self.combo_posicao.set('')
            self.entry_numero.delete(0, tk.END)
            
            messagebox.showinfo("Sucesso", f"Jogador '{nome}' adicionado com sucesso!")
        else:
            messagebox.showerror("Erro", "Erro ao adicionar jogador!")
    
    def atualizar_jogador(self):
        """Atualiza o jogador selecionado"""
        selecionado = self.tree_jogadores.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um jogador para atualizar!")
            return
        
        item = self.tree_jogadores.item(selecionado[0])
        id_jogador = item['values'][0]
        
        nome = self.entry_nome_jogador.get().strip()
        posicao = self.combo_posicao.get()
        numero = self.entry_numero.get().strip()
        
        if not nome or not posicao or not numero:
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios!")
            return
        
        try:
            numero = int(numero)
        except ValueError:
            messagebox.showwarning("Aviso", "Número da camisa deve ser um valor numérico!")
            return
        
        if self.gerenciador.atualizar_jogador(id_jogador, nome, posicao, numero):
            self.atualizar_lista_jogadores()
            self.atualizar_combos_transferencia()
            messagebox.showinfo("Sucesso", "Jogador atualizado com sucesso!")
            
            # Limpar campos
            self.entry_nome_jogador.delete(0, tk.END)
            self.combo_posicao.set('')
            self.entry_numero.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Erro ao atualizar jogador!")
    
    def deletar_jogador(self):
        """Deleta o jogador selecionado"""
        selecionado = self.tree_jogadores.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um jogador para deletar!")
            return
        
        item = self.tree_jogadores.item(selecionado[0])
        id_jogador = item['values'][0]
        nome_jogador = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja deletar o jogador '{nome_jogador}'?"):
            self.gerenciador.deletar_jogador(id_jogador)
            self.atualizar_lista_jogadores()
            self.atualizar_combos_transferencia()
            messagebox.showinfo("Sucesso", "Jogador deletado com sucesso!")
    
    def realizar_transferencia(self):
        """Realiza transferência de jogador"""
        jogador_selecionado = self.combo_jogador_transferencia.get()
        time_selecionado = self.combo_time_transferencia.get()
        
        if not jogador_selecionado:
            messagebox.showwarning("Aviso", "Selecione um jogador!")
            return
        
        if not time_selecionado:
            messagebox.showwarning("Aviso", "Selecione um time de destino!")
            return
        
        # Extrair IDs
        id_jogador = int(jogador_selecionado.split(' - ')[0])
        
        id_time = 0
        if time_selecionado != "Agente Livre":
            id_time = int(time_selecionado.split(' - ')[0])
        
        # Verificar número da camisa
        jogador = self.gerenciador.buscar_jogador_por_id(id_jogador)
        if id_time != 0 and jogador:
            for j in self.gerenciador.listar_jogadores_por_time(id_time):
                if j.numero_camisa == jogador.numero_camisa:
                    resposta = messagebox.askyesno(
                        "Número em uso", 
                        f"Número {jogador.numero_camisa} já está em uso no time destino.\n"
                        "Deseja escolher um novo número?"
                    )
                    if resposta:
                        novo_numero = simpledialog.askinteger(
                            "Novo Número", 
                            "Digite um novo número de camisa:",
                            minvalue=1, maxvalue=99
                        )
                        if novo_numero:
                            self.gerenciador.atualizar_jogador(id_jogador, numero_camisa=novo_numero)
                    else:
                        return
                    break
        
        if self.gerenciador.transferir_jogador(id_jogador, id_time):
            self.atualizar_lista_jogadores()
            self.atualizar_combos_transferencia()
            messagebox.showinfo("Sucesso", "Transferência realizada com sucesso!")
        else:
            messagebox.showerror("Erro", "Erro ao realizar transferência!")
    
    def on_time_selected(self, event):
        """Carrega dados do time selecionado nos campos"""
        selecionado = self.tree_times.selection()
        if selecionado:
            item = self.tree_times.item(selecionado[0])
            values = item['values']
            if values:
                self.entry_nome_time.delete(0, tk.END)
                self.entry_nome_time.insert(0, values[1])
                self.entry_cidade_time.delete(0, tk.END)
                self.entry_cidade_time.insert(0, values[2])
                self.entry_tecnico_time.delete(0, tk.END)
                self.entry_tecnico_time.insert(0, values[3])
    
    def on_jogador_selected(self, event):
        """Carrega dados do jogador selecionado nos campos"""
        selecionado = self.tree_jogadores.selection()
        if selecionado:
            item = self.tree_jogadores.item(selecionado[0])
            values = item['values']
            if values:
                self.entry_nome_jogador.delete(0, tk.END)
                self.entry_nome_jogador.insert(0, values[1])
                self.combo_posicao.set(values[2])
                self.entry_numero.delete(0, tk.END)
                self.entry_numero.insert(0, values[3])
    
    def salvar_dados(self):
        """Salva os dados manualmente"""
        self.gerenciador.salvar_dados()
        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
    
    def mostrar_estatisticas(self):
        """Mostra estatísticas do sistema"""
        stats = f"""
        📊 ESTATÍSTICAS DO SISTEMA
        
        Times cadastrados: {len(self.gerenciador.times)}
        Jogadores cadastrados: {len(self.gerenciador.jogadores)}
        
        Média de jogadores por time: {len(self.gerenciador.jogadores) / max(len(self.gerenciador.times), 1):.1f}
        """
        
        # Time com mais jogadores
        if self.gerenciador.times:
            time_mais = max(self.gerenciador.times, key=lambda t: len(self.gerenciador.listar_jogadores_por_time(t.id)))
            qtd = len(self.gerenciador.listar_jogadores_por_time(time_mais.id))
            stats += f"\nTime com mais jogadores: {time_mais.nome} ({qtd} jogadores)"
        
        messagebox.showinfo("Estatísticas", stats)
    
    def mostrar_jogadores_livres(self):
        """Mostra jogadores sem time"""
        livres = [j for j in self.gerenciador.jogadores if j.id_time == 0]
        
        if not livres:
            messagebox.showinfo("Jogadores Livres", "Não há jogadores livres no momento!")
            return
        
        lista = "📋 JOGADORES LIVRES (Agentes Livres)\n\n"
        for j in livres:
            lista += f"• {j.nome} - {j.posicao} (Camisa {j.numero_camisa})\n"
        
        messagebox.showinfo("Jogadores Livres", lista)
    
    def mostrar_sobre(self):
        """Mostra informações sobre o sistema"""
        sobre = """
        🏆 SISTEMA DE GERENCIAMENTO ESPORTIVO
        
        Versão: 2.0 (Interface Gráfica)
        Desenvolvido com: Python e Tkinter
        
        Funcionalidades:
        ✅ Cadastro completo de Times
        ✅ Cadastro completo de Jogadores
        ✅ Sistema de Transferências
        ✅ Relatórios e Estatísticas
        ✅ Persistência de dados em JSON
        
        © 2024 - Todos os direitos reservados
        """
        messagebox.showinfo("Sobre", sobre)


def main():
    root = tk.Tk()
    app = AppEsportes(root)
    root.mainloop()


if __name__ == "__main__":
    main()