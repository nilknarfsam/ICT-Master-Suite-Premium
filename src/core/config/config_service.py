import json
import os
import sys


def get_base_path():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "ict_config.json",
)

DEFAULT_CONFIG = {
    "caminho_logs_tri": "//147.1.0.95/teste_ict/ict02",
    "caminho_logs_agilent": "//147.1.0.95/teste_ict/ict01/defeitos",
    "backup_local_dir": os.path.join(get_base_path(), "backup_local").replace("\\", "/"),
    "caminho_update_rede": "//147.1.0.95/teste_ict/app_updates",
    "caminho_banco_rede": "//147.1.0.95/teste_ict/banco_dados_falhas.db",
    "auto_start_windows": False,
    "dias_retencao_cache": 30,
}


def carregar_config():
    """Carrega a configuração do arquivo JSON, usando valores padrão para chaves ausentes."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                dados = json.load(f)
                for k, v in DEFAULT_CONFIG.items():
                    dados.setdefault(k, v)
                return dados
        except (json.JSONDecodeError, IOError):
            return DEFAULT_CONFIG.copy()

    config_padrao = DEFAULT_CONFIG.copy()
    salvar_config(config_padrao)
    return config_padrao


def salvar_config(dados):
    """Salva a configuração em um arquivo JSON."""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(dados, f, indent=4)
    except IOError:
        pass
