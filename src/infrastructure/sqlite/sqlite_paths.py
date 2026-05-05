import json
import os

from src.core.config.config_service import CONFIG_FILE, carregar_config, get_base_path


DB_PATH = "//147.1.0.95/teste_ict/banco_dados_falhas.db"
try:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            _config_temp = json.load(f)
            if "caminho_banco_rede" in _config_temp:
                DB_PATH = _config_temp["caminho_banco_rede"]
except Exception:
    pass


DB_LOCAL_PATH = os.path.join(
    carregar_config().get("backup_local_dir", get_base_path()),
    "fila_offline.db",
).replace("\\", "/")
DB_ESPELHO_PATH = os.path.join(
    carregar_config().get("backup_local_dir", get_base_path()),
    "espelho_local.db",
).replace("\\", "/")
