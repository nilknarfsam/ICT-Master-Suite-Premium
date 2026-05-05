import json
import sqlite3
import time
from datetime import datetime

from src.core.database.database_connection import conectar_banco
from src.infrastructure.sqlite.sqlite_paths import DB_LOCAL_PATH


def salvar_falha_db(falha_dict):
    """Salva um dicionário de falha no banco de dados SQLite com retentativa."""
    max_retries = 3
    retry_delay = 1
    for attempt in range(max_retries):
        try:
            with conectar_banco(timeout=20) as conn:
                cursor = conn.cursor()
                sql = """
                    INSERT OR IGNORE INTO falhas (id, data_registro, data_falha, arquivo, serial, modelo, componente, step, status_tratativa)
                    VALUES (:id, :data_registro, :data_falha, :arquivo, :serial, :modelo, :componente, :step, :status_tratativa)
                """
                falha_dict.setdefault("status_tratativa", "ABERTO")
                cursor.execute(sql, falha_dict)
                conn.commit()
                return True
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e) and attempt < max_retries - 1:
                print(f"Banco de dados bloqueado. Tentando novamente em {retry_delay}s... (Tentativa {attempt + 1})")
                time.sleep(retry_delay)
            else:
                print(f"Erro final ao salvar falha no DB: {e}")
                return False
    return False


def salvar_observacao(nome_arquivo, texto_obs, tecnico=None):
    """Salva a observação do técnico e atualiza o status de acordo em um Histórico Acumulativo."""
    if not texto_obs.strip():
        return True

    try:
        with conectar_banco(timeout=20) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT observacao FROM falhas WHERE arquivo = ?", (nome_arquivo,))
            row = cursor.fetchone()
            obs_antiga = row[0] if row and row[0] else ""

            agora = datetime.now().strftime("%d/%m/%Y %H:%M")
            nome_tecnico = tecnico if tecnico else "Local"
            novo_bloco = f"[{agora}] Técnico: {nome_tecnico}\n{texto_obs}"

            texto_final = f"{obs_antiga.strip()}\n\n{novo_bloco}" if obs_antiga.strip() else novo_bloco
            status = "TRATADO"

            if tecnico is not None:
                sql = "UPDATE falhas SET observacao = ?, status_tratativa = ?, tecnico = ? WHERE arquivo = ?"
                cursor.execute(sql, (texto_final, status, tecnico, nome_arquivo))
            else:
                sql = "UPDATE falhas SET observacao = ?, status_tratativa = ? WHERE arquivo = ?"
                cursor.execute(sql, (texto_final, status, nome_arquivo))
            conn.commit()
            return True
    except (sqlite3.OperationalError, OSError) as e:
        print(f"Erro ao salvar observação no DB: {e}")
        try:
            with sqlite3.connect(DB_LOCAL_PATH) as conn_local:
                cursor_local = conn_local.cursor()
                tipo_acao = "NOVA_OBSERVACAO"
                payload_json = json.dumps({"arquivo": nome_arquivo, "texto": texto_obs, "tecnico": tecnico})
                cursor_local.execute("INSERT INTO fila_sync (tipo_acao, payload_json) VALUES (?, ?)", (tipo_acao, payload_json))
                conn_local.commit()
            return "OFFLINE"
        except Exception as ex_local:
            print(f"Erro ao salvar na fila offline: {ex_local}")
            return False


def ler_observacao(nome_arquivo):
    """Lê a observação do técnico associada a um arquivo."""
    try:
        with conectar_banco(timeout=20) as conn:
            cursor = conn.cursor()
            sql = "SELECT observacao FROM falhas WHERE arquivo = ? AND observacao IS NOT NULL LIMIT 1"
            cursor.execute(sql, (nome_arquivo,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else ""
    except sqlite3.OperationalError as e:
        print(f"Erro ao ler observação do DB: {e}")
        return ""


def buscar_historico_serial(serial):
    """Busca o histórico de análise (última observação) de um determinado serial."""
    try:
        with conectar_banco(timeout=20) as conn:
            cursor = conn.cursor()
            sql = """
                SELECT data_registro, observacao, tecnico
                FROM falhas
                WHERE serial = ? AND observacao IS NOT NULL AND observacao != ''
                ORDER BY data_registro DESC
                LIMIT 1
            """
            cursor.execute(sql, (serial,))
            resultado = cursor.fetchone()
            if resultado:
                return {"data": resultado[0], "texto": resultado[1], "tecnico": resultado[2] if len(resultado) > 2 else "Desconhecido"}
            return None
    except sqlite3.OperationalError as e:
        print(f"Erro ao buscar histórico do serial no DB: {e}")
        return None


def obter_estatisticas_ict():
    """Lê o banco de dados de falhas e retorna estatísticas do dia, incluindo o top 5 componentes."""
    stats = {"total_hoje": 0, "top_componente": "N/A", "top_5_componentes": [], "db_online": False}
    from src.infrastructure.sqlite.sqlite_paths import DB_PATH
    import os

    pasta_db = os.path.dirname(DB_PATH)
    if not os.path.exists(pasta_db):
        return stats

    if not os.path.exists(DB_PATH):
        from src.core.database.database_connection import init_db
        init_db()
        if not os.path.exists(DB_PATH):
            return stats

    try:
        with conectar_banco(timeout=20) as conn:
            cursor = conn.cursor()
            stats["db_online"] = True
            hoje_str = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("SELECT COUNT(id) FROM falhas WHERE date(data_registro) = ?", (hoje_str,))
            stats["total_hoje"] = cursor.fetchone()[0]
            cursor.execute(
                """
                SELECT componente, COUNT(id) as qtd
                FROM falhas
                WHERE date(data_registro) = ? AND componente IS NOT NULL AND componente != ''
                GROUP BY componente
                ORDER BY qtd DESC
                LIMIT 5
                """,
                (hoje_str,),
            )
            top_5 = cursor.fetchall()
            stats["top_5_componentes"] = top_5
            if top_5:
                stats["top_componente"] = top_5[0][0]
    except sqlite3.OperationalError as e:
        print(f"Erro ao consultar estatísticas no DB: {e}")
        stats["db_online"] = False
    return stats


def obter_ultimas_analises(limite=10):
    """Busca as últimas 'N' análises/falhas, calculando o status de tratativa."""
    try:
        with conectar_banco(timeout=20) as conn:
            cursor = conn.cursor()
            sql = """
                SELECT data_registro, serial, componente,
                       CASE
                           WHEN observacao IS NOT NULL AND observacao != '' THEN 'TRATADO'
                           ELSE status_tratativa
                       END as status
                FROM falhas
                ORDER BY data_registro DESC
                LIMIT ?
            """
            cursor.execute(sql, (limite,))
            return cursor.fetchall()
    except (sqlite3.OperationalError, OSError) as e:
        print(f"Erro ao obter últimas análises do DB: {e}")
        return []


def obter_estatisticas_progresso():
    """Calcula o progresso de análise de falhas do dia (Abertos vs. Tratados)."""
    stats = {"abertos": 0, "tratados": 0}
    try:
        with conectar_banco(timeout=20) as conn:
            cursor = conn.cursor()
            hoje_str = datetime.now().strftime("%Y-%m-%d")
            cursor.execute(
                """
                SELECT COUNT(DISTINCT arquivo)
                FROM falhas
                WHERE date(data_registro) = ?
                AND (observacao IS NULL OR observacao = '')
                """,
                (hoje_str,),
            )
            stats["abertos"] = cursor.fetchone()[0]
            cursor.execute(
                """
                SELECT COUNT(DISTINCT arquivo)
                FROM falhas
                WHERE date(data_registro) = ?
                AND (observacao IS NOT NULL AND observacao != '')
                """,
                (hoje_str,),
            )
            stats["tratados"] = cursor.fetchone()[0]
    except sqlite3.OperationalError as e:
        print(f"Erro ao obter estatísticas de progresso do DB: {e}")
    return stats


def limpar_analises_db():
    """Reseta todas as observações e status no banco de dados."""
    try:
        with conectar_banco(timeout=20) as conn:
            cursor = conn.cursor()
            sql = "UPDATE falhas SET observacao = NULL, status_tratativa = 'ABERTO'"
            cursor.execute(sql)
            conn.commit()
            return True
    except sqlite3.OperationalError as e:
        print(f"Erro ao limpar análises no DB: {e}")
        return False
