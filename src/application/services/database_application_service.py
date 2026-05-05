from src.core.database.database_connection import (
    bootstrap_database,
    conectar_banco,
    init_db,
    verificar_conexao_db,
)


class DatabaseApplicationService:
    """Servico de aplicacao para operacoes de conectividade/inicializacao de banco."""

    def verificar_conexao_db(self):
        return verificar_conexao_db()

    def conectar_banco(self, timeout=20, bypass_check=False):
        return conectar_banco(timeout=timeout, bypass_check=bypass_check)

    def init_db(self):
        return init_db()

    def bootstrap_database(self):
        return bootstrap_database()
