import json
import os
import sqlite3
import hashlib

from src.core.database.database_connection import conectar_banco, verificar_conexao_db
from src.infrastructure.sqlite.sqlite_paths import DB_ESPELHO_PATH, DB_LOCAL_PATH


def sincronizar_espelho_local():
    """Sincroniza os dados essenciais (usuários, modelos e wiki_reparos) para uso offline."""
    if not verificar_conexao_db():
        return
    try:
        with conectar_banco(timeout=5) as conn_rede:
            usuarios_rede = conn_rede.cursor().execute("SELECT * FROM usuarios").fetchall()
            modelos_rede = conn_rede.cursor().execute("SELECT * FROM modelos").fetchall()
            wiki_rede = conn_rede.cursor().execute("SELECT * FROM wiki_reparos").fetchall()

        with sqlite3.connect(DB_ESPELHO_PATH) as conn_local:
            c = conn_local.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nome TEXT, login TEXT UNIQUE, senha_hash TEXT, is_admin INTEGER)")
            c.execute("DELETE FROM usuarios")
            c.executemany("INSERT INTO usuarios VALUES (?,?,?,?,?)", usuarios_rede)

            c.execute("CREATE TABLE IF NOT EXISTS modelos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome_modelo TEXT UNIQUE NOT NULL)")
            c.execute("DELETE FROM modelos")
            c.executemany("INSERT INTO modelos VALUES (?,?)", modelos_rede)

            c.execute(
                """
                CREATE TABLE IF NOT EXISTS wiki_reparos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    modelo_id INTEGER,
                    fase TEXT,
                    sintoma TEXT,
                    solucao TEXT,
                    tecnico_id TEXT,
                    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (modelo_id) REFERENCES modelos(id)
                )
                """
            )
            c.execute("DELETE FROM wiki_reparos")
            c.executemany("INSERT INTO wiki_reparos VALUES (?,?,?,?,?,?,?)", wiki_rede)
            conn_local.commit()
    except Exception as e:
        print(f"Erro no espelho local: {e}")


def init_db_local():
    """Inicializa localmente a fila de sincronizacao (Store-and-Forward)."""
    try:
        os.makedirs(os.path.dirname(DB_LOCAL_PATH), exist_ok=True)
        with sqlite3.connect(DB_LOCAL_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS fila_sync (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo_acao TEXT,
                    payload_json TEXT,
                    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()
    except (sqlite3.OperationalError, OSError) as e:
        print(f"Erro ao inicializar DB local offline: {e}")

    try:
        os.makedirs(os.path.dirname(DB_ESPELHO_PATH), exist_ok=True)
        with sqlite3.connect(DB_ESPELHO_PATH) as conn_espelho:
            c = conn_espelho.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nome TEXT, login TEXT UNIQUE, senha_hash TEXT, is_admin INTEGER)")
            c.execute("CREATE TABLE IF NOT EXISTS modelos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome_modelo TEXT UNIQUE NOT NULL)")
            c.execute("CREATE TABLE IF NOT EXISTS wiki_reparos (id INTEGER PRIMARY KEY AUTOINCREMENT, modelo_id INTEGER, fase TEXT, sintoma TEXT, solucao TEXT, tecnico_id TEXT, data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            c.execute("SELECT COUNT(*) FROM usuarios")
            if c.fetchone()[0] == 0:
                admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
                c.execute("INSERT INTO usuarios (nome, login, senha_hash, is_admin) VALUES (?, ?, ?, ?)", ("Administrador Local", "admin", admin_hash, 1))
            conn_espelho.commit()
    except Exception as e:
        print(f"Erro ao inicializar espelho de segurança: {e}")


def sincronizar_fila_offline():
    """Processa a fila de ações salvas localmente quando a rede volta."""
    try:
        if not os.path.exists(DB_LOCAL_PATH):
            return

        with sqlite3.connect(DB_LOCAL_PATH) as conn_local:
            cursor = conn_local.cursor()
            cursor.execute("SELECT id, tipo_acao, payload_json FROM fila_sync ORDER BY data_registro ASC")
            registros = cursor.fetchall()
            if not registros:
                return
            if not verificar_conexao_db():
                return

            from src.core.failures.failure_repository import salvar_observacao
            from src.core.wiki.wiki_repository import adicionar_solucao_wiki

            for reg in registros:
                id_reg, tipo_acao, payload_json = reg
                if tipo_acao == "NOVA_OBSERVACAO":
                    dados = json.loads(payload_json)
                    sucesso = salvar_observacao(dados.get("arquivo"), dados.get("texto"), dados.get("tecnico"))
                    if sucesso is True:
                        cursor.execute("DELETE FROM fila_sync WHERE id = ?", (id_reg,))
                        conn_local.commit()
                    else:
                        break
                elif tipo_acao == "NOVA_SOLUCAO":
                    dados = json.loads(payload_json)
                    sucesso = adicionar_solucao_wiki(
                        dados.get("modelo_id"),
                        dados.get("fase"),
                        dados.get("sintoma"),
                        dados.get("solucao"),
                        dados.get("tecnico_id"),
                    )
                    if sucesso is True:
                        cursor.execute("DELETE FROM fila_sync WHERE id = ?", (id_reg,))
                        conn_local.commit()
                    else:
                        break
    except Exception as e:
        print(f"Erro no sincronizador offline: {e}")
