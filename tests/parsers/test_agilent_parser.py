from src.core.parsers.agilent_parser import parse_agilent_txt


def test_parse_agilent_identifica_fail_serial_modelo():
    nome_arquivo = "SN123_report_out_MODELZ.txt"
    conteudo = "Station result: FAILED"
    resultado = parse_agilent_txt("virtual/agilent.txt", nome_arquivo, conteudo)

    assert resultado["tipo"] == "AGILENT"
    assert resultado["status"] == "FAIL"
    assert resultado["serial"] == "SN123"
    assert resultado["modelo"] == "MODELZ"


def test_parse_agilent_identifica_pass():
    nome_arquivo = "SN999_report_out_MODELP.txt"
    conteudo = "Test status: PASSED"
    resultado = parse_agilent_txt("virtual/agilent.txt", nome_arquivo, conteudo)

    assert resultado["status"] == "PASS"
    assert resultado["serial"] == "SN999"
    assert resultado["modelo"] == "MODELP"


def test_parse_agilent_fallback_info_abort():
    nome_arquivo = "SER001_report_out_MODELN.txt"
    conteudo = "Resultado sem palavras-chave conhecidas"
    resultado = parse_agilent_txt("virtual/agilent.txt", nome_arquivo, conteudo)

    assert resultado["status"] == "INFO/ABORT"
    assert resultado["serial"] == "SER001"
    assert resultado["modelo"] == "MODELN"
