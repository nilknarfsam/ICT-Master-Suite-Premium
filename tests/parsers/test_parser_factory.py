from src.core.parsers.log_type_detector import detectar_tipo_log
from src.core.parsers import parser_factory


def test_detectar_tipo_log_tri_e_agilent():
    assert detectar_tipo_log("arquivo_FAIL.csv") == "TRI"
    assert detectar_tipo_log("report_out_modelo.txt") == "AGILENT"


def test_parse_metadata_inteligente_chama_parser_tri(monkeypatch):
    chamado = {"tri": False}

    def fake_tri_csv(caminho_completo, nome_arquivo, conteudo):
        chamado["tri"] = True
        return {"tipo": "TRI", "status": "PASS", "serial": "ABC", "modelo": "M"}

    monkeypatch.setattr(parser_factory, "parse_tri_csv", fake_tri_csv)
    resultado = parser_factory.parse_metadata_inteligente("virtual.csv", "algum_arquivo.csv", "conteudo")

    assert chamado["tri"] is True
    assert resultado["tipo"] == "TRI"


def test_parse_metadata_inteligente_chama_parser_agilent(monkeypatch):
    chamado = {"agilent": False}

    def fake_agilent(caminho_completo, nome_arquivo, conteudo):
        chamado["agilent"] = True
        return {"tipo": "AGILENT", "status": "FAIL", "serial": "XYZ", "modelo": "N"}

    monkeypatch.setattr(parser_factory, "parse_agilent_txt", fake_agilent)
    resultado = parser_factory.parse_metadata_inteligente("virtual.txt", "report_out_foo.txt", "conteudo")

    assert chamado["agilent"] is True
    assert resultado["tipo"] == "AGILENT"
