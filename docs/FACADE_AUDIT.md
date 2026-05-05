# Auditoria da Legacy Facade

## Funções ainda utilizadas

Funções/constantes da `legacy_facade` que ainda aparecem em uso na base ativa:

- `carregar_config`
- `salvar_config`
- `salvar_falha_db`
- `obter_estatisticas_progresso`
- `limpar_analises_db`
- `verificar_conexao_db`
- `limpar_cache_local`
- `buscar_historico_serial`
- `obter_estatisticas_ict`
- `CONFIG_FILE`

Observacao: `src/app_desktop/ui_main.py` ainda importa `salvar_observacao`, `ler_observacao` e `obter_ultimas_analises` via facade, mas os fluxos principais de analise ja foram migrados para `LogAnalysisService`.

## Onde estão sendo usadas

- `carregar_config` — `src/app_desktop/ui_main.py` (linhas ~21, ~104, ~168) — contexto: boot/config/login.
- `salvar_config` — `src/app_desktop/ui_main.py` (linhas ~21, ~107, ~405, ~1443) — contexto: preferencias e logout.
- `salvar_falha_db` — `src/app_desktop/ui_main.py` (linhas ~21, ~1280, ~1299, ~1315) — contexto: persistencia de falhas no fluxo de leitura de log.
- `obter_estatisticas_progresso` — `src/app_desktop/ui_main.py` (linha ~22) — contexto: dashboard/progresso.
- `limpar_analises_db` — `src/app_desktop/ui_main.py` (linhas ~22, ~736) — contexto: ferramenta de limpeza historico.
- `verificar_conexao_db` — `src/app_desktop/ui_main.py` (linhas ~22, ~676, ~719, ~1362) — contexto: validacao de conectividade antes de operacoes sensiveis.
- `limpar_cache_local` — `src/app_desktop/ui_main.py` (linhas ~23, ~187) — contexto: limpeza de cache no startup.
- `buscar_historico_serial` — `src/app_desktop/ui_main.py` (linhas ~23, ~1194) — contexto: historico colaborativo.
- `obter_estatisticas_ict` — `src/app_desktop/threads.py` (linhas ~11, ~155) — contexto: dashboard thread.
- `CONFIG_FILE` — `src/app_desktop/updater.py` (linhas ~20-22) — contexto: leitura de caminho de update.

Referencias estruturais da facade:

- `src/app_desktop/__init__.py` (linha ~1) — reexport legado.
- `src/app_desktop/ui_main.py` (linhas ~21, ~103, ~1442) — imports diretos.
- `src/app_desktop/threads.py` (linha ~9) — import de funcoes remanescentes.
- `src/app_desktop/updater.py` (linha ~20) — import de `CONFIG_FILE`.

## Já migradas para Application Services

- parsing (OK)
- salvar análise (OK)
- leitura análise (OK)
- wiki (OK)
- auth (OK)
- relatórios (OK)
- sync (OK)

## Dependências restantes da facade

### Alta prioridade

- `salvar_falha_db` (UI ainda chama facade diretamente; migracao simples para `LogAnalysisService.save_failure`).
- `obter_estatisticas_ict` em `threads.py` (pode ir para `LogAnalysisService` ou service dedicado de dashboard).
- `obter_estatisticas_progresso` (pode ser encapsulado em service de analytics/progresso).

### Média prioridade

- `carregar_config` e `salvar_config` em `ui_main.py` (migrar para service de configuracao sem alterar UX).
- `verificar_conexao_db` e `limpar_analises_db` (encapsular em service de manutencao/diagnostico).
- `buscar_historico_serial` (encapsular em service de historico).

### Baixa prioridade

- `CONFIG_FILE` em `updater.py` (constante pode permanecer temporariamente ate consolidar service de updater/config).
- `src/app_desktop/__init__.py` com `from ...legacy_facade import *` (limpeza final quando facade deixar de ser porta de compatibilidade).

## Plano de eliminação da facade

1. Config
2. FailureRepository direto
3. Database helpers
4. Utils restantes

## Resumo do script de varredura

Script executado: `scripts/find_facade_usage.py`

Resumo em `src/`:

- 6 referencias diretas a `legacy_facade`
- Arquivos detectados:
  - `src/app_desktop/ui_main.py`
  - `src/app_desktop/threads.py`
  - `src/app_desktop/updater.py`
  - `src/app_desktop/__init__.py`
