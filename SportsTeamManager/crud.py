
# crud.py
 
from typing import List, Optional
from database import salvar_times, salvar_jogadores, carregar_times, carregar_jogadores
from models import Time, Jogador
 
class GerenciadorEsportes:
    def __init__(self):
        self.times: List[Time] = carregar_times()
        self.jogadores: List[Jogador] = carregar_jogadores()
        self.proximo_id_time: int = max([t.id for t in self.times], default=0) + 1
        self.proximo_id_jogador: int = max([j.id for j in self.jogadores], default=0) + 1
    
    def salvar_dados(self) -> None:
        salvar_times(self.times)
        salvar_jogadores(self.jogadores)
    
    # ---------- CRUD TIMES ----------
    def criar_time(self, nome: str, cidade: str, tecnico: str) -> Time:
        time = Time(self.proximo_id_time, nome, cidade, tecnico)
        self.times.append(time)
        self.proximo_id_time += 1
        self.salvar_dados()
        return time
    
    def listar_times(self) -> List[Time]:
        if not self.times:
            print("📭 Nenhum time cadastrado.")
        return self.times
    
    def buscar_time_por_id(self, id_time: int) -> Optional[Time]:
        for time in self.times:
            if time.id == id_time:
                return time
        return None
    
    def atualizar_time(self, id_time: int, nome: Optional[str] = None, 
                       cidade: Optional[str] = None, tecnico: Optional[str] = None) -> bool:
        time = self.buscar_time_por_id(id_time)
        if not time:
            return False
        if nome:
            time.nome = nome
        if cidade:
            time.cidade = cidade
        if tecnico:
            time.tecnico = tecnico
        self.salvar_dados()
        return True
    
    def deletar_time(self, id_time: int) -> bool:
        # Verificar se o time tem jogadores
        jogadores_time = [j for j in self.jogadores if j.id_time == id_time]
        if jogadores_time:
            print(f"⚠️ Não é possível deletar! O time tem {len(jogadores_time)} jogador(es).")
            return False
        
        self.times = [t for t in self.times if t.id != id_time]
        self.salvar_dados()
        return True
    
    # ---------- CRUD JOGADORES ----------
    def criar_jogador(self, nome: str, posicao: str, 
                      numero_camisa: int, id_time: int = 0) -> Optional[Jogador]:
        # Validar se time existe (se não for agente livre)
        if id_time != 0 and not self.buscar_time_por_id(id_time):
            print("❌ Time não encontrado!")
            return None
        
        # Validar número da camisa único no time
        if id_time != 0:
            for j in self.jogadores:
                if j.id_time == id_time and j.numero_camisa == numero_camisa:
                    print("❌ Número de camisa já existe neste time!")
                    return None
        
        jogador = Jogador(self.proximo_id_jogador, nome, posicao, numero_camisa, id_time)
        self.jogadores.append(jogador)
        self.proximo_id_jogador += 1
        self.salvar_dados()
        return jogador
    
    def listar_jogadores(self) -> List[Jogador]:
        if not self.jogadores:
            print("📭 Nenhum jogador cadastrado.")
        return self.jogadores
    
    def listar_jogadores_por_time(self, id_time: int) -> List[Jogador]:
        jogadores_time = [j for j in self.jogadores if j.id_time == id_time]
        return jogadores_time
    
    def buscar_jogador_por_id(self, id_jogador: int) -> Optional[Jogador]:
        for jogador in self.jogadores:
            if jogador.id == id_jogador:
                return jogador
        return None
    
    def atualizar_jogador(self, id_jogador: int, nome: Optional[str] = None, 
                          posicao: Optional[str] = None, numero_camisa: Optional[int] = None,
                          id_time: Optional[int] = None) -> bool:
        jogador = self.buscar_jogador_por_id(id_jogador)
        if not jogador:
            return False
        
        if nome:
            jogador.nome = nome
        if posicao:
            jogador.posicao = posicao
        if numero_camisa:
            # Validar número único no time
            time_destino = jogador.id_time if id_time is None else id_time
            if time_destino != 0:
                for j in self.jogadores:
                    if j.id != id_jogador and j.id_time == time_destino and j.numero_camisa == numero_camisa:
                        print("❌ Número de camisa já existe neste time!")
                        return False
            jogador.numero_camisa = numero_camisa
        if id_time is not None:
            if id_time != 0 and not self.buscar_time_por_id(id_time):
                print("❌ Time não encontrado!")
                return False
            jogador.id_time = id_time
        
        self.salvar_dados()
        return True
    def deletar_jogador(self, id_jogador: int) -> bool:
        self.jogadores = [j for j in self.jogadores if j.id != id_jogador]
        self.salvar_dados()
        return True
    
    def transferir_jogador(self, id_jogador: int, novo_id_time: int) -> bool:
        return self.atualizar_jogador(id_jogador, id_time=novo_id_time)