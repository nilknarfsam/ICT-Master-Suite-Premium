# Auditoria da Legacy Facade

## Funções ainda utilizadas

Funções/constantes da `legacy_facade` que ainda aparecem em uso na base ativa:

- `salvar_falha_db`
- `obter_estatisticas_progresso`
- `limpar_analises_db`
- `verificar_conexao_db`
- `buscar_historico_serial`
- `obter_estatisticas_ict`
- `CONFIG_FILE` (uso removido de `updater.py`; ainda exposto na facade por compatibilidade)

Observacao: `src/app_desktop/ui_main.py` ainda importa `salvar_observacao`, `ler_observacao` e `obter_ultimas_analises` via facade, mas os fluxos principais de analise ja foram migrados para `LogAnalysisService`.

## Onde estão sendo usadas

- `salvar_falha_db` — `src/app_desktop/ui_main.py` (linhas ~21, ~1280, ~1299, ~1315) — contexto: persistencia de falhas no fluxo de leitura de log.
- `obter_estatisticas_progresso` — `src/app_desktop/ui_main.py` (linha ~22) — contexto: dashboard/progresso.
- `limpar_analises_db` — `src/app_desktop/ui_main.py` (linhas ~22, ~736) — contexto: ferramenta de limpeza historico.
- `verificar_conexao_db` — `src/app_desktop/ui_main.py` (linhas ~22, ~676, ~719, ~1362) — contexto: validacao de conectividade antes de operacoes sensiveis.
- `buscar_historico_serial` — `src/app_desktop/ui_main.py` (linhas ~23, ~1194) — contexto: historico colaborativo.
- `obter_estatisticas_ict` — `src/app_desktop/threads.py` (linhas ~11, ~155) — contexto: dashboard thread.

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

## Status da migração de Config

- ConfigService (carregar/salvar config): **OK (migrado para core.config em `ui_main.py`)**
- Cache cleanup (`limpar_cache_local`): **OK (migrado para `src/core/config/cache_service.py`)**
- `CONFIG_FILE` no updater: **OK (migrado para `src/core/config/config_service.py`)**

## Dependências restantes da facade

### Alta prioridade

- `salvar_falha_db` (UI ainda chama facade diretamente; migracao simples para `LogAnalysisService.save_failure`).
- `obter_estatisticas_ict` em `threads.py` (pode ir para `LogAnalysisService` ou service dedicado de dashboard).
- `obter_estatisticas_progresso` (pode ser encapsulado em service de analytics/progresso).

### Média prioridade

- `verificar_conexao_db` e `limpar_analises_db` (encapsular em service de manutencao/diagnostico).
- `buscar_historico_serial` (encapsular em service de historico).

### Baixa prioridade

- `src/app_desktop/__init__.py` com `from ...legacy_facade import *` (limpeza final quando facade deixar de ser porta de compatibilidade).

## Plano de eliminação da facade

1. Config
2. FailureRepository direto
3. Database helpers
4. Utils restantes

## Resumo do script de varredura

Script executado: `scripts/find_facade_usage.py`

Resumo em `src/`:

- 4 referencias diretas a `legacy_facade` (apos migracao de configuracao)
- Arquivos detectados:
  - `src/app_desktop/ui_main.py`
  - `src/app_desktop/threads.py`
  - `src/app_desktop/updater.py`
  - `src/app_desktop/__init__.py`
