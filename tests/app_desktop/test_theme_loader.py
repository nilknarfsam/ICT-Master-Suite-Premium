"""Testes do carregador de tema da UI Premium.

Estes testes nao dependem de PyQt5: validam apenas IO de arquivo e
contrato resiliente das funcoes (`load_theme` e `load_combined_theme`
nunca levantam excecao e sempre retornam string).
"""

from src.app_desktop.themes.theme_loader import load_combined_theme, load_theme


def test_load_theme_retorna_string_para_light():
    result = load_theme("light")
    assert isinstance(result, str)
    assert result != ""


def test_load_theme_inexistente_nao_quebra_e_retorna_vazio():
    result = load_theme("inexistente_xyz")
    assert isinstance(result, str)
    assert result == ""


def test_load_theme_nome_vazio_retorna_vazio():
    result = load_theme("")
    assert result == ""


def test_load_combined_theme_retorna_string_e_contem_seletor_qt():
    result = load_combined_theme("light")
    assert isinstance(result, str)
    assert result != ""
    assert "QPushButton" in result or "QWidget" in result


def test_load_combined_theme_inexistente_nao_quebra():
    result = load_combined_theme("nao_existe")
    assert isinstance(result, str)


def test_load_combined_theme_concatena_base_e_tema():
    base = load_theme("base")
    light = load_theme("light")
    combined = load_combined_theme("light")
    assert isinstance(combined, str)
    if base:
        assert base.strip().splitlines()[0] in combined
    if light:
        assert light.strip().splitlines()[0] in combined
