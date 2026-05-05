# Auditoria da Legacy Facade

## Funções ainda utilizadas

Funções/constantes da `legacy_facade` que ainda aparecem em uso na base ativa:

- `verificar_conexao_db` (parcialmente migrado para `DatabaseApplicationService`)
- `CONFIG_FILE` (uso removido de `updater.py`; ainda exposto na facade por compatibilidade)

Observacao: `src/app_desktop/ui_main.py` ainda importa `salvar_observacao`, `ler_observacao` e `obter_ultimas_analises` via facade, mas os fluxos principais de analise ja foram migrados para `LogAnalysisService`.

## Onde estão sendo usadas

- `verificar_conexao_db` — `src/app_desktop/ui_main.py` (via `DatabaseApplicationService`) — contexto: validacao de conectividade antes de operacoes sensiveis.

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
- database checks (PARCIAL: UI desktop migrada para `DatabaseApplicationService`)
- falhas/análises remanescentes (OK)

## Status da migração de Config

- ConfigService (carregar/salvar config): **OK (migrado para core.config em `ui_main.py`)**
- Cache cleanup (`limpar_cache_local`): **OK (migrado para `src/core/config/cache_service.py`)**
- `CONFIG_FILE` no updater: **OK (migrado para `src/core/config/config_service.py`)**

## Dependências restantes da facade

### Alta prioridade

- restante de helpers de banco ainda expostos via `legacy_facade` para compatibilidade (`conectar_banco`, `init_db`, `bootstrap_database`, `verificar_conexao_db`).

### Média prioridade

- `src/app_desktop/threads.py` ainda referencia facade para compatibilidade estrutural de imports, apesar das chamadas críticas já migrarem por service.

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

- 4 referencias diretas a `legacy_facade` (apos migracoes de config e falhas)
- Arquivos detectados:
  - `src/app_desktop/ui_main.py`
  - `src/app_desktop/threads.py`
  - `src/app_desktop/updater.py`
  - `src/app_desktop/__init__.py`
