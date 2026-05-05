# Fase 1 - Modularizacao inicial do legado

Esta etapa iniciou a separacao do antigo `legacy/finder_logs_original/models.py` em modulos novos dentro de `src/core` e `src/infrastructure`, mantendo os mesmos nomes de funcoes e comportamento base.

## O que foi separado nesta etapa

- Configuracao JSON e constantes principais em `src/core/config/config_service.py`
- Conexao e inicializacao do banco em `src/core/database/database_connection.py`
- Verificacao de rede em `src/infrastructure/file_system/network_utils.py`
- Caminhos de SQLite (rede, local, espelho) em `src/infrastructure/sqlite/sqlite_paths.py`
- Autenticacao e CRUD de usuarios em `src/core/auth/auth_service.py`
- Parsers TRI/AGILENT e factory em `src/core/parsers/`
- Repositorio de falhas e estatisticas em `src/core/failures/failure_repository.py`
- Repositorio de wiki/modelos em `src/core/wiki/wiki_repository.py`
- Geracao de relatorio Excel em `src/core/reports/report_service.py`
- Sincronizacao offline/espelho em `src/core/sync/offline_sync_service.py`

## Decisoes aplicadas nesta fase

- O legado em `legacy/finder_logs_original` foi preservado intacto.
- Nao houve mudanca de regra de negocio, banco SQLite ou stack PyQt5.
- Nao houve alteracao de layout visual ou remocao de funcionalidades.
- Foi removida a inicializacao automatica de banco no import dos novos modulos.
- Foi criada a funcao `bootstrap_database()` em `database_connection.py` para inicializacao explicita.

## O que ainda falta para as proximas fases

- Conectar gradualmente o `ui_main.py` aos novos modulos.
- Criar camada de compatibilidade temporaria para reduzir impacto de migracao.
- Cobrir os modulos novos com testes automatizados.
- Migrar funcoes restantes do legado fora do escopo desta divisao inicial.
