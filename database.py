# database.py

import json
import os
from typing import List
from models import Time, Jogador

ARQUIVO_TIMES: str = "times.json"
ARQUIVO_JOGADORES: str = "jogadores.json"

def salvar_times(times: List[Time]) -> None:
    dados = [{"id": t.id, "nome": t.nome, "cidade": t.cidade, "tecnico": t.tecnico} for t in times]
    with open(ARQUIVO_TIMES, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def carregar_times() -> List[Time]:
    if not os.path.exists(ARQUIVO_TIMES):
        return []
    with open(ARQUIVO_TIMES, "r", encoding="utf-8") as f:
        dados = json.load(f)
        return [Time(d["id"], d["nome"], d["cidade"], d["tecnico"]) for d in dados]

def salvar_jogadores(jogadores: List[Jogador]) -> None:
    dados = [{"id": j.id, "nome": j.nome, "posicao": j.posicao, 
              "numero_camisa": j.numero_camisa, "id_time": j.id_time} for j in jogadores]
    with open(ARQUIVO_JOGADORES, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def carregar_jogadores() -> List[Jogador]:
    if not os.path.exists(ARQUIVO_JOGADORES):
        return []
    with open(ARQUIVO_JOGADORES, "r", encoding="utf-8") as f:
        dados = json.load(f)
        return [Jogador(d["id"], d["nome"], d["posicao"], d["numero_camisa"], d["id_time"]) for d in dados]