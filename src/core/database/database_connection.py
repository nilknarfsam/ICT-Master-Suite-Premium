import hashlib
import os
import sqlite3

from src.core.config.config_service import carregar_config
from src.infrastructure.file_system.network_utils import servidor_online
from src.infrastructure.sqlite.sqlite_paths import DB_PATH


def conectar_banco(timeout=20, bypass_check=False):
    """Wrapper corporativo para conexões SQLite com trava anti-criação na raiz/local."""
    caminho_db = carregar_config().get("caminho_banco_rede", "//147.1.0.95/teste_ict/banco_dados_falhas.db")
    if not bypass_check:
        if not servidor_online(caminho_db) or not os.path.isfile(caminho_db):
            raise OSError("Banco de dados inacessível na rede devido a queda de conexão.")

    return sqlite3.connect(caminho_db, timeout=timeout)


def popular_modelos_iniciais(cursor):
    """Insere a lista inicial de modelos na base de conhecimento se não existirem."""
    modelos_iniciais = [
        "M70Q5", "M70Q6", "M70S5", "M70S6", "M75S5",
        "M75Q5 SH", "T14Gen6", "T14Gen7", "E14Gen7",
        "LOQ IRX9", "LOQ IAX9E",
    ]
    for modelo in modelos_iniciais:
        try:
            cursor.execute("INSERT OR IGNORE INTO modelos (nome_modelo) VALUES (?)", (modelo,))
        except sqlite3.Error as e:
            print(f"Erro ao inserir modelo inicial {modelo}: {e}")


def init_db():
    """Inicializa o banco de dados, cria a tabela 'falhas' e adiciona a coluna 'observacao' se não existir."""
    caminho_db = carregar_config().get("caminho_banco_rede", DB_PATH)
    if not servidor_online(caminho_db):
        return

    try:
        with conectar_banco(timeout=20, bypass_check=True) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS falhas (
                    id TEXT PRIMARY KEY,
                    data_registro TIMESTAMP,
                    data_falha TIMESTAMP,
                    arquivo TEXT,
                    serial TEXT,
                    modelo TEXT,
                    componente TEXT,
                    step TEXT,
                    status_tratativa TEXT
                )
                """
            )

            cursor.execute("PRAGMA table_info(falhas)")
            columns = [info[1] for info in cursor.fetchall()]
            if "observacao" not in columns:
                cursor.execute("ALTER TABLE falhas ADD COLUMN observacao TEXT")
            if "tecnico" not in columns:
                cursor.execute("ALTER TABLE falhas ADD COLUMN tecnico TEXT")

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    login TEXT UNIQUE,
                    senha_hash TEXT,
                    is_admin INTEGER
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS modelos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_modelo TEXT UNIQUE
                )
                """
            )
            cursor.execute(
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

            cursor.execute("SELECT COUNT(*) FROM usuarios")
            if cursor.fetchone()[0] == 0:
                admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
                cursor.execute(
                    """
                    INSERT INTO usuarios (nome, login, senha_hash, is_admin)
                    VALUES (?, ?, ?, ?)
                    """,
                    ("Administrador", "admin", admin_hash, 1),
                )

            cursor.execute("CREATE INDEX IF NOT EXISTS idx_data_registro ON falhas (data_registro);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_componente ON falhas (componente);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_arquivo ON falhas (arquivo);")
            conn.commit()
            popular_modelos_iniciais(cursor)

        from src.core.sync.offline_sync_service import sincronizar_espelho_local
        sincronizar_espelho_local()

    except (sqlite3.OperationalError, OSError) as e:
        print(f"Erro ao inicializar o banco de dados: {e}")


def verificar_conexao_db():
    """Verifica se o arquivo do banco de dados está acessível na rede estipulada."""
    if not servidor_online(DB_PATH):
        return False

    pasta_db = os.path.dirname(DB_PATH)
    if not os.path.exists(pasta_db):
        return False

    if not os.path.exists(DB_PATH):
        init_db()

    if not os.path.exists(DB_PATH):
        return False

    try:
        with conectar_banco(timeout=5) as conn:
            conn.cursor().execute("PRAGMA quick_check")
        return True
    except (sqlite3.OperationalError, OSError):
        return False


def bootstrap_database():
    """Inicialização explícita do banco remoto e da estrutura offline local."""
    init_db()
    from src.core.sync.offline_sync_service import init_db_local
    init_db_local()
