from src.core.parsers.agilent_parser import parse_agilent_txt
from src.core.parsers.log_type_detector import detectar_tipo_log
from src.core.parsers.tri_parser import parse_tri_csv, parse_tri_txt


def parse_metadata_inteligente(caminho_completo, nome_arquivo, conteudo):
    """Factory que delega a análise de metadados para a estratégia especializada correta."""
    tipo = detectar_tipo_log(nome_arquivo)
    nome_lower = nome_arquivo.lower()

    try:
        if tipo == "TRI":
            if nome_lower.endswith(".csv"):
                return parse_tri_csv(caminho_completo, nome_arquivo, conteudo)
            return parse_tri_txt(caminho_completo, nome_arquivo, conteudo)
        if tipo == "AGILENT":
            return parse_agilent_txt(caminho_completo, nome_arquivo, conteudo)
    except Exception as e:
        print(f"Erro no Factory do Parser ao analisar metadados: {e}")

    return {"tipo": tipo, "data": "N/A", "serial": "N/A", "modelo": "N/A", "status": "UNKNOWN", "cor": "black"}
