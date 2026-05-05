"""
Camada temporaria de compatibilidade para migracao gradual da UI antiga.

Este modulo reexporta funcoes usadas historicamente via models.py, apontando
para os modulos novos em src/core e src/infrastructure.
"""

import os
import time

from src.core.auth.auth_service import (
    atualizar_usuario,
    cadastrar_usuario,
    deletar_usuario,
    listar_usuarios,
    obter_usuario_por_login,
    validar_login,
)
from src.core.config.config_service import carregar_config, salvar_config
from src.core.config.config_service import CONFIG_FILE
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


def limpar_cache_local():
    """Remove arquivos do backup local mais antigos que dias_retencao_cache."""
    config = carregar_config()
    backup_dir = config.get("backup_local_dir", "")
    dias_retencao = config.get("dias_retencao_cache", 30)

    if not backup_dir or not os.path.exists(backup_dir):
        return

    agora = time.time()
    limite_idade_segundos = dias_retencao * 86400
    for root, _, files in os.walk(backup_dir):
        for arquivo in files:
            caminho_completo = os.path.join(root, arquivo)
            try:
                idade_arquivo = agora - os.path.getmtime(caminho_completo)
                if idade_arquivo > limite_idade_segundos:
                    os.remove(caminho_completo)
            except (OSError, FileNotFoundError, PermissionError):
                pass


__all__ = [
    "CONFIG_FILE",
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
    "limpar_cache_local",
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
