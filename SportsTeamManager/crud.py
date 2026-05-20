# crud.py

from typing import List, Optional
from database import (
    inicializar_banco,
    inserir_time, atualizar_time_db, deletar_time_db, carregar_times,
    inserir_jogador, atualizar_jogador_db, deletar_jogador_db, carregar_jogadores,
)
from models import Time, Jogador


class GerenciadorEsportes:
    def __init__(self):
        inicializar_banco()
        self.times: List[Time] = carregar_times()
        self.jogadores: List[Jogador] = carregar_jogadores()

    # ---------- CRUD TIMES ----------
    def criar_time(self, nome: str, cidade: str, tecnico: str) -> Time:
        time = inserir_time(nome, cidade, tecnico)   # ID vem do banco
        self.times.append(time)
        return time

    def listar_times(self) -> List[Time]:
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
        atualizar_time_db(time)
        return True

    def deletar_time(self, id_time: int) -> bool:
        jogadores_time = [j for j in self.jogadores if j.id_time == id_time]
        if jogadores_time:
            print(f"⚠️ Não é possível deletar! O time tem {len(jogadores_time)} jogador(es).")
            return False
        deletar_time_db(id_time)
        self.times = [t for t in self.times if t.id != id_time]
        return True

    # ---------- CRUD JOGADORES ----------
    def criar_jogador(self, nome: str, posicao: str,
                      numero_camisa: int, id_time: int = 0) -> Optional[Jogador]:
        if id_time != 0 and not self.buscar_time_por_id(id_time):
            print("❌ Time não encontrado!")
            return None
        if id_time != 0:
            for j in self.jogadores:
                if j.id_time == id_time and j.numero_camisa == numero_camisa:
                    print("❌ Número de camisa já existe neste time!")
                    return None
        jogador = inserir_jogador(nome, posicao, numero_camisa, id_time)  # ID vem do banco
        self.jogadores.append(jogador)
        return jogador

    def listar_jogadores(self) -> List[Jogador]:
        return self.jogadores

    def listar_jogadores_por_time(self, id_time: int) -> List[Jogador]:
        return [j for j in self.jogadores if j.id_time == id_time]

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
        atualizar_jogador_db(jogador)
        return True

    def deletar_jogador(self, id_jogador: int) -> bool:
        deletar_jogador_db(id_jogador)
        self.jogadores = [j for j in self.jogadores if j.id != id_jogador]
        return True

    def transferir_jogador(self, id_jogador: int, novo_id_time: int) -> bool:
        return self.atualizar_jogador(id_jogador, id_time=novo_id_time)