# ICT Master Suite Premium

Versao premium em evolucao do projeto legado `finder_logs`, com foco em logs ICT/TRI/Agilent e arquitetura modular para crescimento seguro.

## Objetivo desta fase

Esta etapa prepara a base profissional do novo projeto, sem alterar a logica interna existente e sem impactar o sistema atual em producao.

## Regras da migracao atual

- Nao altera nada em `C:\finder_logs`.
- Mantem copia de referencia dos arquivos principais em `legacy/finder_logs_original`.
- Foco exclusivo em aplicativo de logs ICT/TRI/Agilent.
- Sem implementacao de hardware, firmware, Arduino, ESP32 ou MQTT nesta fase.

## Estrutura inicial

O projeto foi organizado para suportar modularizacao progressiva:

- `legacy/`: referencia do sistema atual.
- `src/app_desktop/`: camada de interface desktop.
- `src/core/`: regras de negocio por dominio.
- `src/infrastructure/`: persistencia e adaptadores tecnicos.
- `src/shared/`: utilitarios compartilhados.
- `tests/`, `docs/`, `scripts/`, `tools/`: suporte de qualidade, documentacao e automacao.

## Escopo do momento

Esta versao contem somente preparacao estrutural para o primeiro ciclo de commits da Premium.

## Estado atual da arquitetura

Arquitetura ativa apos as migracoes da Fase 2:

- UI desktop em `src/app_desktop`
- regras de negocio em `src/core`
- orquestracao de fluxos em `src/application/services`
- adaptadores tecnicos em `src/infrastructure`

Servicos de aplicacao em uso:

- `LogSearchService`
- `LogAnalysisService`
- `WikiService`
- `AuthApplicationService`
- `ReportApplicationService`
- `SyncApplicationService`
- `DatabaseApplicationService`

Status da `legacy_facade`:

- mantida temporariamente por compatibilidade
- dependencia direta reduzida para pontos estruturais controlados
- auditoria de uso com scripts:
  - `python scripts/find_facade_usage.py`
  - `python scripts/find_unused_facade_exports.py`

## Executando a versao premium desktop

Para executar a base desktop premium a partir da raiz do projeto:

- `python -m src.app_desktop.ui_main`

Opcionalmente, use o runner:

- `python run_desktop.py`

Observacao: `legacy/finder_logs_original` permanece como referencia congelada. A base ativa de execucao da Premium fica em `src/app_desktop`.

## Como executar no Windows

Forma recomendada:

- `scripts\run_desktop.bat`

PowerShell:

- `powershell -ExecutionPolicy Bypass -File scripts\run_desktop.ps1`

Manual:

- `.venv\Scripts\python.exe run_desktop.py`

Notas importantes:

- no PowerShell, o ativador correto da venv e `.venv\Scripts\Activate.ps1`
- evite `.\run_desktop.py` diretamente; prefira sempre executar via Python
- guia detalhado: `docs/RUN_DESKTOP_WINDOWS.md`

## Validacao de desenvolvimento

Para validar rapidamente a base desktop premium:

- `scripts\dev_check.bat`

O script executa:

- `python -m compileall src`
- `python scripts/smoke_check.py`
- `python -m pytest tests/test_legacy_facade_imports.py tests/test_desktop_imports.py`

Para validacao manual operacional, use o checklist:

- `docs/SMOKE_TEST_DESKTOP.md`

## Indexacao manual de logs

Para construir/atualizar manualmente o indice local de logs:

- `python scripts/build_log_index.py`

Para informar diretorios explicitamente:

- `python scripts/build_log_index.py "\\servidor\logs\tri" "\\servidor\logs\agilent"`

Para forcar reindexacao completa manual:

- `python scripts/build_log_index.py --rebuild`

## Log de evolucao do projeto

O historico tecnico consolidado das etapas da migracao Premium esta em:

- `docs/PROJECT_EVOLUTION_LOG.md`
