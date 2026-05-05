# Auditoria da Legacy Facade

## Estado atual da facade

A `legacy_facade` foi mantida como camada de compatibilidade, mas os fluxos principais da UI ja foram migrados para services de aplicacao e modulos `core`.

Na base ativa (`src/`), as referencias diretas restantes ao modulo `legacy_facade` estao concentradas em:

- `src/app_desktop/__init__.py` (reexport de compatibilidade)
- `src/app_desktop/legacy_facade.py` (proprio modulo)

Nao ha mais import direto de `legacy_facade` em:

- `src/app_desktop/ui_main.py`
- `src/app_desktop/threads.py`
- `src/app_desktop/updater.py`

## Funções ainda dependentes

As funcoes de banco ainda sao exportadas pela facade para compatibilidade retroativa:

- `conectar_banco`
- `init_db`
- `verificar_conexao_db`
- `bootstrap_database`

Observacao: no desktop, a checagem de conectividade ja foi migrada para `DatabaseApplicationService`.

## Módulos já livres da facade

Modulos auditados e livres de dependencia direta da facade:

- `src/app_desktop/ui_main.py`
- `src/app_desktop/threads.py`
- `src/app_desktop/updater.py`

Camadas migradas:

- configuracao: `src/core/config/*`
- analise/falhas: `LogAnalysisService`
- auth: `AuthApplicationService`
- wiki: `WikiService`
- relatorios: `ReportApplicationService`
- sync: `SyncApplicationService`
- checagem de banco na UI: `DatabaseApplicationService`

## Plano final de remoção da facade

1. Redirecionar eventuais imports externos para services/core sem passar pela facade.
2. Remover o reexport de `src/app_desktop/__init__.py` quando nao houver consumidores.
3. Congelar `__all__` da facade apenas durante janela de compatibilidade.
4. Remover `legacy_facade.py` na etapa final, apos uma release com telemetria/validacao de uso zero.

## Resumo de auditoria final

Scripts executados:

- `python scripts/find_facade_usage.py`
- `python scripts/find_unused_facade_exports.py`

Resultado:

- dependencia direta da facade reduzida a pontos de compatibilidade
- imports nao usados removidos de `ui_main.py` e `threads.py`
- exportacoes da facade agora podem ser auditadas via script dedicado
