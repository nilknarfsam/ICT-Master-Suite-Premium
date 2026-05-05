import json
import sqlite3

from src.core.database.database_connection import conectar_banco
from src.infrastructure.sqlite.sqlite_paths import DB_ESPELHO_PATH, DB_LOCAL_PATH


def adicionar_modelo(nome_modelo):
    """Adiciona um novo modelo à base de conhecimento."""
    try:
        with conectar_banco(timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO modelos (nome_modelo) VALUES (?)", (nome_modelo,))
            conn.commit()
            return cursor.lastrowid
    except sqlite3.IntegrityError:
        print(f"Erro: O modelo '{nome_modelo}' já existe.")
        return None
    except sqlite3.OperationalError as e:
        print(f"Erro ao adicionar modelo: {e}")
        return None


def editar_modelo(id_modelo, novo_nome):
    """Edita o nome de um modelo existente."""
    try:
        with conectar_banco(timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE modelos
                SET nome_modelo = ?
                WHERE id = ?
                """,
                (novo_nome, id_modelo),
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        print(f"Erro: O modelo '{novo_nome}' já existe no banco de dados.")
        return False
    except sqlite3.OperationalError as e:
        print(f"Erro ao editar modelo no banco de dados: {e}")
        return False


def listar_modelos():
    """Retorna uma lista de todos os modelos cadastrados."""
    try:
        with conectar_banco(timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome_modelo FROM modelos ORDER BY nome_modelo")
            return [{"id": row[0], "nome": row[1]} for row in cursor.fetchall()]
    except (sqlite3.OperationalError, OSError) as e:
        print(f"Rede offline. Lendo modelos do espelho local: {e}")
        try:
            with sqlite3.connect(DB_ESPELHO_PATH, timeout=5) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nome_modelo FROM modelos ORDER BY nome_modelo")
                return [{"id": row[0], "nome": row[1]} for row in cursor.fetchall()]
        except Exception as ex:
            print(f"Erro ao ler modelos do espelho: {ex}")
            return []


def adicionar_solucao_wiki(modelo_id, fase, sintoma, solucao, tecnico_id):
    """Adiciona uma nova solução à base de conhecimento."""
    try:
        with conectar_banco(timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO wiki_reparos (modelo_id, fase, sintoma, solucao, tecnico_id)
                VALUES (?, ?, ?, ?, ?)
                """,
                (modelo_id, fase, sintoma, solucao, tecnico_id),
            )
            conn.commit()
            return True
    except (sqlite3.OperationalError, OSError) as e:
        print(f"Erro ao adicionar solução na rede, salvando na fila offline: {e}")
        try:
            with sqlite3.connect(DB_LOCAL_PATH) as conn_local:
                cursor_local = conn_local.cursor()
                tipo_acao = "NOVA_SOLUCAO"
                payload_json = json.dumps(
                    {
                        "modelo_id": modelo_id,
                        "fase": fase,
                        "sintoma": sintoma,
                        "solucao": solucao,
                        "tecnico_id": tecnico_id,
                    }
                )
                cursor_local.execute("INSERT INTO fila_sync (tipo_acao, payload_json) VALUES (?, ?)", (tipo_acao, payload_json))
                conn_local.commit()
            return "OFFLINE"
        except Exception as ex_local:
            print(f"Erro ao salvar solução na fila offline: {ex_local}")
            return False


def buscar_solucoes_wiki(modelo_id, fase=None, busca_texto=None):
    """Busca soluções na wiki com base nos filtros fornecidos."""
    try:
        with conectar_banco(timeout=5) as conn:
            cursor = conn.cursor()
            query = """
                SELECT w.id, m.nome_modelo, w.fase, w.sintoma, w.solucao, w.tecnico_id, w.data_registro
                FROM wiki_reparos w
                JOIN modelos m ON w.modelo_id = m.id
                WHERE 1=1
            """
            params = []
            if modelo_id:
                query += " AND w.modelo_id = ?"
                params.append(modelo_id)
            if fase and fase != "Todos":
                query += " AND w.fase = ?"
                params.append(fase)
            if busca_texto:
                query += " AND (w.sintoma LIKE ? OR w.solucao LIKE ?)"
                params.extend([f"%{busca_texto}%", f"%{busca_texto}%"])

            query += " ORDER BY w.data_registro DESC"
            cursor.execute(query, params)
            return [
                {
                    "id": row[0],
                    "modelo": row[1],
                    "fase": row[2],
                    "sintoma": row[3],
                    "solucao": row[4],
                    "tecnico": row[5],
                    "data": row[6],
                }
                for row in cursor.fetchall()
            ]
    except (sqlite3.OperationalError, OSError) as e:
        print(f"Erro ao buscar soluções na rede, tentando espelho: {e}")
        try:
            with sqlite3.connect(DB_ESPELHO_PATH, timeout=5) as conn:
                cursor = conn.cursor()
                query = """
                    SELECT w.id, m.nome_modelo, w.fase, w.sintoma, w.solucao, w.tecnico_id, w.data_registro
                    FROM wiki_reparos w
                    JOIN modelos m ON w.modelo_id = m.id
                    WHERE 1=1
                """
                params = []
                if modelo_id:
                    query += " AND w.modelo_id = ?"
                    params.append(modelo_id)
                if fase and fase != "Todos":
                    query += " AND w.fase = ?"
                    params.append(fase)
                if busca_texto:
                    query += " AND (w.sintoma LIKE ? OR w.solucao LIKE ?)"
                    params.extend([f"%{busca_texto}%", f"%{busca_texto}%"])

                query += " ORDER BY w.data_registro DESC"
                cursor.execute(query, params)
                return [
                    {
                        "id": row[0],
                        "modelo": row[1],
                        "fase": row[2],
                        "sintoma": row[3],
                        "solucao": row[4],
                        "tecnico": row[5],
                        "data": row[6],
                    }
                    for row in cursor.fetchall()
                ]
        except Exception as ex:
            print(f"Erro ao buscar soluções no espelho: {ex}")
            return []
