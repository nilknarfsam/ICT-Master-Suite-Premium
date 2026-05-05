import hashlib
import sqlite3

from src.core.database.database_connection import conectar_banco
from src.infrastructure.sqlite.sqlite_paths import DB_ESPELHO_PATH


def validar_login(login, senha_texto):
    """Valida o login e a senha (comparando o hash) no banco de dados."""
    try:
        with conectar_banco(timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, is_admin, senha_hash FROM usuarios WHERE login = ?", (login,))
            user = cursor.fetchone()
            if user:
                id_user, nome, is_admin, senha_hash_db = user
                senha_sujeito_hash = hashlib.sha256(senha_texto.encode()).hexdigest()
                if senha_sujeito_hash == senha_hash_db:
                    return {"id": id_user, "nome": nome, "login": login, "is_admin": bool(is_admin)}
            return None
    except (sqlite3.OperationalError, OSError) as e:
        print(f"Erro ao validar login na rede, tentando espelho local: {e}")
        try:
            with sqlite3.connect(DB_ESPELHO_PATH, timeout=5) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nome, is_admin, senha_hash FROM usuarios WHERE login = ?", (login,))
                user = cursor.fetchone()
                if user:
                    id_user, nome, is_admin, senha_hash_db = user
                    senha_sujeito_hash = hashlib.sha256(senha_texto.encode()).hexdigest()
                    if senha_sujeito_hash == senha_hash_db:
                        return {"id": id_user, "nome": nome, "login": login, "is_admin": bool(is_admin)}
                return None
        except sqlite3.OperationalError as e_local:
            print(f"Erro ao validar login no espelho local: {e_local}")
            return None


def obter_usuario_por_login(login):
    """Busca um usuário no banco apenas pelo login, sem verificar a senha (Lembrar de Mim)."""
    try:
        with conectar_banco(timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, is_admin FROM usuarios WHERE login = ?", (login,))
            user = cursor.fetchone()
            if user:
                id_user, nome, is_admin = user
                return {"id": id_user, "nome": nome, "login": login, "is_admin": bool(is_admin)}
            return None
    except (sqlite3.OperationalError, OSError) as e:
        print(f"Erro ao tentar recuperar usuario por login na rede, tentando espelho: {e}")
        try:
            with sqlite3.connect(DB_ESPELHO_PATH, timeout=5) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nome, is_admin FROM usuarios WHERE login = ?", (login,))
                user = cursor.fetchone()
                if user:
                    id_user, nome, is_admin = user
                    return {"id": id_user, "nome": nome, "login": login, "is_admin": bool(is_admin)}
                return None
        except sqlite3.OperationalError as e_local:
            print(f"Erro ao recuperar usuario por login no espelho: {e_local}")
            return None


def listar_usuarios():
    """Retorna uma lista com todos os usuários do banco de dados (sem a senha)."""
    try:
        with conectar_banco(timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, login, is_admin FROM usuarios ORDER BY nome")
            return [{"id": row[0], "nome": row[1], "login": row[2], "is_admin": bool(row[3])} for row in cursor.fetchall()]
    except (sqlite3.OperationalError, OSError) as e:
        print(f"Erro ao listar usuários do banco de dados: {e}")
        return []


def cadastrar_usuario(nome, login, senha, is_admin):
    """Cadastra um novo usuário no banco de dados. Retorna True se sucesso, False caso contrário."""
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    try:
        with conectar_banco(timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO usuarios (nome, login, senha_hash, is_admin)
                VALUES (?, ?, ?, ?)
                """,
                (nome, login, senha_hash, int(is_admin)),
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        print(f"Erro: O login '{login}' já existe no banco de dados.")
        return False
    except sqlite3.OperationalError as e:
        print(f"Erro ao cadastrar usuário no banco de dados: {e}")
        return False


def deletar_usuario(id_usuario):
    """Deleta um usuário pelo ID. Impede a exclusão do último admin."""
    try:
        with conectar_banco(timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT is_admin FROM usuarios WHERE id = ?", (id_usuario,))
            user = cursor.fetchone()
            if user and user[0] == 1:
                cursor.execute("SELECT COUNT(*) FROM usuarios WHERE is_admin = 1")
                if cursor.fetchone()[0] <= 1:
                    print("Operação negada: Não é possível deletar o último administrador do sistema.")
                    return False

            cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
            conn.commit()
            return True
    except sqlite3.OperationalError as e:
        print(f"Erro ao deletar usuário no banco de dados: {e}")
        return False


def atualizar_usuario(id_usuario, novo_nome, novo_login, nova_senha=None):
    """Atualiza um usuário existente. Se nova_senha for fornecida, atualiza a senha também."""
    try:
        with conectar_banco(timeout=5) as conn:
            cursor = conn.cursor()
            if nova_senha:
                senha_hash = hashlib.sha256(nova_senha.encode()).hexdigest()
                cursor.execute(
                    """
                    UPDATE usuarios
                    SET nome = ?, login = ?, senha_hash = ?
                    WHERE id = ?
                    """,
                    (novo_nome, novo_login, senha_hash, id_usuario),
                )
            else:
                cursor.execute(
                    """
                    UPDATE usuarios
                    SET nome = ?, login = ?
                    WHERE id = ?
                    """,
                    (novo_nome, novo_login, id_usuario),
                )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        print(f"Erro: O login '{novo_login}' já existe no banco de dados.")
        return False
    except sqlite3.OperationalError as e:
        print(f"Erro ao atualizar usuário no banco de dados: {e}")
        return False
