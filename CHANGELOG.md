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

## [0.1.0] - 2026-04-28

### Added

- Criada estrutura inicial profissional do projeto Premium.
- Adicionada pasta `legacy/finder_logs_original` com arquivos essenciais de referencia do sistema atual.
- Adicionados documentos base (`README.md`, `ROADMAP.md`, `CHANGELOG.md`).
- Adicionados arquivos de bootstrap (`requirements.txt`, `.gitignore`, `commit.bat`).
