# App Desktop Premium Base

## Status atual

O app desktop ativo da versao premium esta em `src/app_desktop`.

O conteudo em `legacy/finder_logs_original` permanece como referencia congelada para comparacao e rastreabilidade, sem alteracoes.

## Arquivos base copiados do legado

- `src/app_desktop/ui_main.py`
- `src/app_desktop/threads.py`
- `src/app_desktop/updater.py`
- `src/app_desktop/style.qss`

## Redirecionamento de imports para facade

Para manter comportamento e permitir migracao gradual:

- `ui_main.py` passou a consumir funcoes via `src.app_desktop.legacy_facade`
- `threads.py` passou a consumir funcoes via `src.app_desktop.legacy_facade`
- `updater.py` passou a ler `CONFIG_FILE` via `src.app_desktop.legacy_facade`

## Como executar a aplicacao

Executando como modulo (raiz do projeto):

- `python -m src.app_desktop.ui_main`

Executando pelo runner:

- `python run_desktop.py`

## Telas para teste manual apos mudancas

- Login/logout e lembrar usuario
- Lista de arquivos e carregamento de logs
- Painel/dashboard de estatisticas
- Observacoes e historico por arquivo/serial
- Aba de administracao de usuarios
- Base de conhecimento (modelos e solucoes wiki)
- Geracao de relatorio Excel
- Configuracoes e comportamento de sincronizacao offline
