# database.py

import mysql.connector
from mysql.connector import Error
from typing import List
from models import Time, Jogador

# ─────────────────────────────────────────────
#  CONFIGURAÇÃO — ajuste para o seu ambiente
# ─────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",
    "password": "",
    "database": "sports_manager",
}


# ─────────────────────────────────────────────
#  CONEXÃO
# ─────────────────────────────────────────────
def get_conexao():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        raise ConnectionError(f"Erro ao conectar ao MySQL: {e}")


# ─────────────────────────────────────────────
#  INICIALIZAÇÃO
# ─────────────────────────────────────────────
def inicializar_banco() -> None:
    """Cria as tabelas caso ainda não existam."""
    conexao = get_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS times (
                id      INT AUTO_INCREMENT PRIMARY KEY,
                nome    VARCHAR(100) NOT NULL,
                cidade  VARCHAR(100) NOT NULL,
                tecnico VARCHAR(100) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jogadores (
                id            INT AUTO_INCREMENT PRIMARY KEY,
                nome          VARCHAR(100) NOT NULL,
                posicao       VARCHAR(50)  NOT NULL,
                numero_camisa INT          NOT NULL,
                id_time       INT          NOT NULL DEFAULT 0
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        conexao.commit()
    finally:
        cursor.close()
        conexao.close()


# ─────────────────────────────────────────────
#  TIMES
# ─────────────────────────────────────────────
def inserir_time(nome: str, cidade: str, tecnico: str) -> Time:
    """Insere um novo time e retorna o objeto com o ID gerado pelo banco."""
    conexao = get_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO times (nome, cidade, tecnico) VALUES (%s, %s, %s)",
            (nome, cidade, tecnico)
        )
        conexao.commit()
        novo_id = cursor.lastrowid
        return Time(novo_id, nome, cidade, tecnico)
    except Error as e:
        conexao.rollback()
        raise RuntimeError(f"Erro ao inserir time: {e}")
    finally:
        cursor.close()
        conexao.close()


def atualizar_time_db(time: Time) -> None:
    """Atualiza os dados de um time existente."""
    conexao = get_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "UPDATE times SET nome=%s, cidade=%s, tecnico=%s WHERE id=%s",
            (time.nome, time.cidade, time.tecnico, time.id)
        )
        conexao.commit()
    except Error as e:
        conexao.rollback()
        raise RuntimeError(f"Erro ao atualizar time: {e}")
    finally:
        cursor.close()
        conexao.close()


def deletar_time_db(id_time: int) -> None:
    """Remove um time pelo ID."""
    conexao = get_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM times WHERE id=%s", (id_time,))
        conexao.commit()
    except Error as e:
        conexao.rollback()
        raise RuntimeError(f"Erro ao deletar time: {e}")
    finally:
        cursor.close()
        conexao.close()


def carregar_times() -> List[Time]:
    """Carrega todos os times do banco."""
    conexao = get_conexao()
    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, nome, cidade, tecnico FROM times ORDER BY id")
        rows = cursor.fetchall()
        return [Time(r["id"], r["nome"], r["cidade"], r["tecnico"]) for r in rows]
    finally:
        cursor.close()
        conexao.close()


# ─────────────────────────────────────────────
#  JOGADORES
# ─────────────────────────────────────────────
def inserir_jogador(nome: str, posicao: str, numero_camisa: int, id_time: int) -> Jogador:
    """Insere um novo jogador e retorna o objeto com o ID gerado pelo banco."""
    conexao = get_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO jogadores (nome, posicao, numero_camisa, id_time) VALUES (%s, %s, %s, %s)",
            (nome, posicao, numero_camisa, id_time)
        )
        conexao.commit()
        novo_id = cursor.lastrowid
        return Jogador(novo_id, nome, posicao, numero_camisa, id_time)
    except Error as e:
        conexao.rollback()
        raise RuntimeError(f"Erro ao inserir jogador: {e}")
    finally:
        cursor.close()
        conexao.close()


def atualizar_jogador_db(jogador: Jogador) -> None:
    """Atualiza os dados de um jogador existente."""
    conexao = get_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "UPDATE jogadores SET nome=%s, posicao=%s, numero_camisa=%s, id_time=%s WHERE id=%s",
            (jogador.nome, jogador.posicao, jogador.numero_camisa, jogador.id_time, jogador.id)
        )
        conexao.commit()
    except Error as e:
        conexao.rollback()
        raise RuntimeError(f"Erro ao atualizar jogador: {e}")
    finally:
        cursor.close()
        conexao.close()


def deletar_jogador_db(id_jogador: int) -> None:
    """Remove um jogador pelo ID."""
    conexao = get_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM jogadores WHERE id=%s", (id_jogador,))
        conexao.commit()
    except Error as e:
        conexao.rollback()
        raise RuntimeError(f"Erro ao deletar jogador: {e}")
    finally:
        cursor.close()
        conexao.close()


def carregar_jogadores() -> List[Jogador]:
    """Carrega todos os jogadores do banco."""
    conexao = get_conexao()
    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, nome, posicao, numero_camisa, id_time FROM jogadores ORDER BY id")
        rows = cursor.fetchall()
        return [
            Jogador(r["id"], r["nome"], r["posicao"], r["numero_camisa"], r["id_time"])
            for r in rows
        ]
    finally:
        cursor.close()
        conexao.close()