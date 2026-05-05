import os
from datetime import datetime


def parse_tri_csv(caminho_completo, nome_arquivo, conteudo):
    """Estratégia para ler logs da TRI no padrão CSV (...FAIL.csv / ...PASS.csv)."""
    dados = {"tipo": "TRI", "data": "N/A", "serial": "N/A", "modelo": "N/A", "status": "N/A", "cor": "black"}
    nome_sem_ext = os.path.splitext(nome_arquivo)[0]

    if nome_sem_ext[:14].isdigit():
        dt = datetime.strptime(nome_sem_ext[:14], "%Y%m%d%H%M%S")
        dados["data"] = dt.strftime("%d/%m/%Y %H:%M:%S")
        resto = nome_sem_ext[14:]
    else:
        resto = nome_sem_ext

    if nome_sem_ext.upper().endswith("FAIL"):
        dados["status"] = "FAIL"
        dados["cor"] = "red"
        resto = resto[:-4]
    elif nome_sem_ext.upper().endswith("PASS"):
        dados["status"] = "PASS"
        dados["cor"] = "green"
        resto = resto[:-4]

    dados["serial"] = resto[:10] if len(resto) >= 10 else resto
    if len(resto) > 10:
        dados["modelo"] = resto[10:].strip("_")
    return dados


def parse_tri_txt(caminho_completo, nome_arquivo, conteudo):
    """Estratégia para ler logs antigos da TRI no padrão TXT/LOG (f_...log / p_...log)."""
    dados = {"tipo": "TRI", "data": "N/A", "serial": "N/A", "modelo": "N/A", "status": "N/A", "cor": "black"}
    nome_lower = nome_arquivo.lower()
    nome_sem_ext = os.path.splitext(nome_arquivo)[0]

    try:
        ts_mod = os.path.getmtime(caminho_completo)
        dados["data"] = datetime.fromtimestamp(ts_mod).strftime("%d/%m/%Y %H:%M:%S")
    except OSError:
        pass

    if nome_lower.startswith("f_") or "fail" in nome_lower:
        dados["status"] = "FAIL"
        dados["cor"] = "red"
    elif nome_lower.startswith("p_") or "pass" in nome_lower:
        dados["status"] = "PASS"
        dados["cor"] = "green"

    resto = nome_sem_ext
    if resto.lower().startswith("f_") or resto.lower().startswith("p_"):
        resto = resto[2:]

    dados["serial"] = resto[:10] if len(resto) >= 10 else resto
    if len(resto) > 10:
        dados["modelo"] = resto[10:].strip("_")
    return dados
