# Changelog

Todas as mudancas relevantes desta versao premium serao registradas neste arquivo.

## [Unreleased]

### Added

- Adicionada base desktop premium executavel em `src/app_desktop`.
- Adicionados smoke checks de desenvolvimento (`scripts/smoke_check.py` e `scripts/dev_check.bat`).
- Adicionada documentacao de validacao operacional (`docs/SMOKE_TEST_DESKTOP.md`).
- Testes de parser TRI e Agilent adicionados.
- Testes basicos do core adicionados.
- Adicionada camada application services.
- Adicionados DTOs de aplicacao.
- Adicionados testes de servicos de aplicacao.
- UI desktop passou a usar LogSearchService para normalizacao e validacao do termo de busca.
- Parsing de metadata agora usa LogAnalysisService.
- Salvamento de analise agora usa LogAnalysisService.
- Leitura de analise agora usa LogAnalysisService.
- Operacoes da wiki agora usam WikiService.
- Autenticacao e gestao de usuarios agora usam AuthApplicationService.
- Exportacao de relatorios agora usa ReportApplicationService.
- Sincronizacao offline/background agora usa SyncApplicationService.
- Adicionada auditoria da legacy_facade.
- Chamadas de configuracao desktop migradas para core config service.
- Chamadas de falhas/analises migradas para LogAnalysisService.
- Verificacoes de banco migradas para DatabaseApplicationService.
- Adicionada auditoria final de dependencias da legacy_facade.
- Checkpoint da Fase 2 documentado.
- Adicionadas opcoes de busca de logs para futura otimizacao de performance.
- Scanner de logs passou a usar LogSearchService para filtro de arquivos.
- Scanner preparado com limite inicial de resultados para reduzir carga em buscas extensas.
- Busca de logs agora prepara resumo interno quando resultados sao limitados.
- Status bar agora informa quando a busca foi limitada.
- Adicionada estrutura inicial de indexacao local de logs.
- Adicionada indexacao incremental local de logs.
- Adicionada camada application para indexacao local de logs.
- Adicionado script manual para construir indice local de logs.
- Adicionada base para busca hibrida usando indice local.
- Busca de logs agora usa indice local quando disponivel com fallback automatico.
- Status bar agora informa se busca veio do indice ou scanner.
- Criado log mestre de evolucao tecnica do projeto.
- Adicionada reindexacao completa manual de logs.
- Adicionado worker de reindexacao em background para futura integracao na UI.
- Adicionado botao controlado para reindexar logs pela UI.
- Adicionada instrumentacao de startup e preparacao para otimizacao de abertura.
- Adicionados scripts de execucao Windows para app desktop premium.
- Ignorados artefatos locais de runtime no controle de versao.
- Adicionado checklist operacional de validacao da indexacao e busca rapida.
- Adicionado wrapper de medicao `timed_search_with_index` em `LogSearchService` (sem alterar contrato existente).
- Adicionado script `scripts/benchmark_search.py` para baseline reproduzivel de busca (index x scanner).
- Adicionado documento `docs/BASELINE_BUSCA.md` para registro de evidencias do baseline.
- Atualizado checklist de validacao com etapa G de baseline quantitativo.
- Adicionada foundation visual reutilizavel para UI Premium PyQt5 (themes, widgets, layouts, theme_loader).
- Adicionada aba Dashboard premium com cards de metricas, atividade recente e ViewModel desacoplado.

### Changed

- Reordenadas abas principais (Finder Logs primeiro, Dashboard por ultimo).
- Ajustado tamanho/posicao inicial da janela para respeitar a area util do Windows (`availableGeometry`).
- Reorganizado Finder Logs com mais espaco para log/historico/analise (splitter 320/980, stretch e min-height).
- Lista de logs encontrados ordenada por data decrescente com timestamp visivel (`YYYY-MM-DD HH:MM`).
- Painel "Detalhamento de Defeitos (TRI)" ocultado visualmente (parser e populate preservados).
- Textos do Finder Logs atualizados ("Logs encontrados:", "Selecione um log para visualizar.", "Visualizacao do Log:").

## [0.1.0] - 2026-04-28

### Added

- Criada estrutura inicial profissional do projeto Premium.
- Adicionada pasta `legacy/finder_logs_original` com arquivos essenciais de referencia do sistema atual.
- Adicionados documentos base (`README.md`, `ROADMAP.md`, `CHANGELOG.md`).
- Adicionados arquivos de bootstrap (`requirements.txt`, `.gitignore`, `commit.bat`).
