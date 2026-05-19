# models.py
from typing import Optional

class Time:
    def __init__(self, id_time: int, nome: str, cidade: str, tecnico: str):
        self.id: int = id_time
        self.nome: str = nome
        self.cidade: str = cidade
        self.tecnico: str = tecnico
    
    def __str__(self) -> str:
        return f"{self.id} - {self.nome} ({self.cidade}) - Técnico: {self.tecnico}"

class Jogador:
    def __init__(self, id_jogador: int, nome: str, posicao: str, 
                 numero_camisa: int, id_time: int = 0):
        self.id: int = id_jogador
        self.nome: str = nome
        self.posicao: str = posicao
        self.numero_camisa: int = numero_camisa
        self.id_time: int = id_time  # 0 = sem time (agente livre)
    
    def __str__(self) -> str:
        status_time: str = "Agente Livre" if self.id_time == 0 else f"Time ID: {self.id_time}"
        return f"{self.id} - {self.nome} | Posição: {self.posicao} | Camisa: {self.numero_camisa} | {status_time}"