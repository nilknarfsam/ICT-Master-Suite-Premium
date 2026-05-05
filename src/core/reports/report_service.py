import pandas as pd

from src.core.database.database_connection import conectar_banco


def gerar_relatorio_excel(caminho_destino):
    """Gera um arquivo Excel contendo todos os dados de falhas."""
    try:
        with conectar_banco(timeout=5) as conn:
            df = pd.read_sql_query("SELECT * FROM falhas", conn)
            df.to_excel(caminho_destino, index=False)
            return True
    except Exception as e:
        print(f"Erro ao gerar relatório Excel: {e}")
        return False
