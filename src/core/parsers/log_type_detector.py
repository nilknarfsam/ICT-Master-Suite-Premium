def detectar_tipo_log(nome_arquivo):
    """Define se é TRI ou AGILENT baseado na extensão e nome do arquivo."""
    nome = nome_arquivo.lower()
    if nome.endswith((".csv", ".dcl")):
        return "TRI"
    if nome.endswith(".txt") and "report" in nome:
        return "AGILENT"
    if ".csv" in nome:
        return "TRI"
    return "AGILENT"
