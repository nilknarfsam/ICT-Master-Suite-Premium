"""Carregador de temas QSS para a UI Premium.

Resolve caminhos via `__file__` para manter compatibilidade com builds
empacotados (PyInstaller); espelha o padrao adotado em
`src/app_desktop/ui_main.py::get_resource_path`.

Funcoes desta API sao tolerantes a falhas: jamais levantam excecao.
Em qualquer erro de IO, retornam string vazia. Isso permite que o
consumidor (`MainApp.load_stylesheet`) caia num fallback robusto sem
risco de impedir a abertura do app.
"""

import os
import sys


def _base_dir() -> str:
    """Retorna o diretorio base de `src/app_desktop`.

    Em ambiente normal de desenvolvimento, equivale ao diretorio onde
    este arquivo reside (mais um nivel acima, em `src/app_desktop`).
    Em build PyInstaller `--onefile`, usa `sys._MEIPASS` quando
    disponivel.
    """
    try:
        return sys._MEIPASS  # type: ignore[attr-defined]
    except Exception:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _resource(relative: str) -> str:
    return os.path.join(_base_dir(), "themes", relative)


def load_theme(theme_name: str = "light") -> str:
    """Carrega o QSS de um unico tema (`themes/{theme_name}.qss`).

    Em caso de erro de IO, retorna string vazia. Nao levanta.
    """
    if not theme_name:
        return ""
    try:
        path = _resource(f"{theme_name}.qss")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as exc:  # noqa: BLE001
        print(f"theme_loader.load_theme falhou para '{theme_name}': {exc}")
        return ""


def load_combined_theme(theme_name: str = "light") -> str:
    """Concatena `themes/base.qss` + `themes/{theme_name}.qss`.

    Em caso de erro, retorna string vazia. Nao levanta.

    O consumidor deve verificar se a string retornada e nao-vazia antes
    de aplicar; em caso de falha pode acionar fallback para o
    `style.qss` legado.
    """
    if not theme_name:
        return ""
    try:
        base = ""
        try:
            base_path = _resource("base.qss")
            with open(base_path, "r", encoding="utf-8") as f:
                base = f.read()
        except FileNotFoundError:
            base = ""
        theme = load_theme(theme_name)
        if not base and not theme:
            return ""
        return f"{base}\n{theme}" if base else theme
    except Exception as exc:  # noqa: BLE001
        print(f"theme_loader.load_combined_theme falhou para '{theme_name}': {exc}")
        return ""
