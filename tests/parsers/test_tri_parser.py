from src.core.parsers.tri_parser import parse_tri_csv, parse_tri_txt


def test_parse_tri_csv_fail_serial_modelo():
    nome_arquivo = "20260505093000SERIAL1234MODEL_X_FAIL.csv"
    resultado = parse_tri_csv("virtual/path.csv", nome_arquivo, "conteudo-simulado")

    assert resultado["tipo"] == "TRI"
    assert resultado["status"] == "FAIL"
    assert resultado["serial"] == "SERIAL1234"
    assert resultado["modelo"] == "MODEL_X"


def test_parse_tri_csv_pass_serial_modelo():
    nome_arquivo = "20260505093000ABCDEF1234MODELO_Y_PASS.csv"
    resultado = parse_tri_csv("virtual/path.csv", nome_arquivo, "conteudo-simulado")

    assert resultado["status"] == "PASS"
    assert resultado["serial"] == "ABCDEF1234"
    assert resultado["modelo"] == "MODELO_Y"


def test_parse_tri_txt_fail_serial_modelo():
    nome_arquivo = "f_SERIAL9988MODELO_A.log"
    resultado = parse_tri_txt("virtual/path.log", nome_arquivo, "conteudo-simulado")

    assert resultado["tipo"] == "TRI"
    assert resultado["status"] == "FAIL"
    assert resultado["serial"] == "SERIAL9988"
    assert resultado["modelo"] == "MODELO_A"


def test_parse_tri_txt_pass_serial_modelo():
    nome_arquivo = "p_SERPASS0001MOD_B.log"
    resultado = parse_tri_txt("virtual/path.log", nome_arquivo, "conteudo-simulado")

    assert resultado["status"] == "PASS"
    assert resultado["serial"] == "SERPASS0001"
    assert resultado["modelo"] == "MOD_B"
