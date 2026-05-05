"""
Camada temporaria de compatibilidade para migracao gradual da UI antiga.

Este modulo reexporta funcoes usadas historicamente via models.py, apontando
para os modulos novos em src/core e src/infrastructure.
"""

from src.core.auth.auth_service import (
    atualizar_usuario,
    cadastrar_usuario,
    deletar_usuario,
    listar_usuarios,
    obter_usuario_por_login,
    validar_login,
)
from src.core.config.config_service import carregar_config, salvar_config
from src.core.database.database_connection import (
    bootstrap_database,
    conectar_banco,
    init_db,
    verificar_conexao_db,
)
from src.core.failures.failure_repository import (
    buscar_historico_serial,
    ler_observacao,
    limpar_analises_db,
    obter_estatisticas_ict,
    obter_estatisticas_progresso,
    obter_ultimas_analises,
    salvar_falha_db,
    salvar_observacao,
)
from src.core.parsers.log_type_detector import detectar_tipo_log
from src.core.parsers.parser_factory import parse_metadata_inteligente
from src.core.reports.report_service import gerar_relatorio_excel
from src.core.sync.offline_sync_service import (
    init_db_local,
    sincronizar_espelho_local,
    sincronizar_fila_offline,
)
from src.core.wiki.wiki_repository import (
    adicionar_modelo,
    adicionar_solucao_wiki,
    buscar_solucoes_wiki,
    editar_modelo,
    listar_modelos,
)

__all__ = [
    "carregar_config",
    "salvar_config",
    "conectar_banco",
    "init_db",
    "verificar_conexao_db",
    "bootstrap_database",
    "validar_login",
    "obter_usuario_por_login",
    "listar_usuarios",
    "cadastrar_usuario",
    "deletar_usuario",
    "atualizar_usuario",
    "detectar_tipo_log",
    "parse_metadata_inteligente",
    "salvar_falha_db",
    "salvar_observacao",
    "ler_observacao",
    "buscar_historico_serial",
    "obter_estatisticas_ict",
    "obter_ultimas_analises",
    "obter_estatisticas_progresso",
    "limpar_analises_db",
    "adicionar_modelo",
    "editar_modelo",
    "listar_modelos",
    "adicionar_solucao_wiki",
    "buscar_solucoes_wiki",
    "gerar_relatorio_excel",
    "sincronizar_fila_offline",
    "sincronizar_espelho_local",
    "init_db_local",
]
