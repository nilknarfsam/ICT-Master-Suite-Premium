import os
from datetime import datetime


def parse_agilent_txt(caminho_completo, nome_arquivo, conteudo):
    """Estratégia para ler logs da Agilent (report_out.txt)."""
    dados = {"tipo": "AGILENT", "data": "N/A", "serial": "N/A", "modelo": "N/A", "status": "N/A", "cor": "black"}
    try:
        ts_mod = os.path.getmtime(caminho_completo)
        dados["data"] = datetime.fromtimestamp(ts_mod).strftime("%d/%m/%Y %H:%M:%S")
    except OSError:
        pass

    partes = nome_arquivo.split("_")
    if partes:
        dados["serial"] = partes[0]
    if "report_out_" in nome_arquivo:
        dados["modelo"] = nome_arquivo.split("report_out_")[-1].replace(".txt", "")

    conteudo_upper = conteudo.upper()
    if "FAILED" in conteudo_upper or "FAILURE" in conteudo_upper:
        dados["status"] = "FAIL"
        dados["cor"] = "red"
    elif "PASSED" in conteudo_upper:
        dados["status"] = "PASS"
        dados["cor"] = "green"
    else:
        dados["status"] = "INFO/ABORT"
        dados["cor"] = "orange"

    return dados
