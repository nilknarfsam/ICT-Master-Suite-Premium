import os
import time

from src.core.config.config_service import carregar_config


def limpar_cache_local():
    """Remove arquivos do diretório de backup local mais antigos que dias_retencao_cache."""
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
