# Fase 2 - Application Services Layer

## Papel da camada application

A camada `application` organiza casos de uso do sistema em servicos orientados a fluxo de negocio de alto nivel. Ela reduz a dependencia da UI em funcoes soltas e cria um ponto unico de orquestracao.

## Diferenca entre core e application

- `core`: regras de dominio e operacoes tecnicas ja extraidas do legado (parsers, repositorios, auth, relatorios).
- `application`: coordena chamadas do `core`, padroniza entradas/saidas e prepara contrato para UI desktop atual e futuras interfaces.

## Por que isso ajuda a futura UI moderna

- Diminui acoplamento da interface com detalhes internos.
- Facilita troca de camada de apresentacao no futuro (ex.: React/Electron) sem reescrever regras centrais.
- Permite testes mais focados em caso de uso, com mocks simples.

## Servicos criados

- `LogSearchService` (`src/application/services/log_search_service.py`)
- `LogAnalysisService` (`src/application/services/log_analysis_service.py`)
- `WikiService` (`src/application/services/wiki_service.py`)
- `AuthApplicationService` (`src/application/services/auth_application_service.py`)
- `ReportApplicationService` (`src/application/services/report_application_service.py`)

## DTOs criados

- `LogSearchResult`
- `LogMetadata`
- `FailureRecordInput`
- `AnalysisNoteInput`

Arquivo: `src/application/dtos/log_dtos.py`

## Primeira integracao com UI desktop

A primeira integracao gradual foi aplicada em `src/app_desktop/ui_main.py` apenas no fluxo de entrada do termo de busca:

- a UI passou a instanciar `LogSearchService`
- a normalizacao do termo usa `normalize_search_term`
- a validacao minima usa `validate_search_term`

O restante do fluxo de busca foi mantido sem alteracoes para preservar comportamento atual e reduzir risco de regressao.

## Parsing de logs migrado para Application Service

No carregamento de arquivos em `src/app_desktop/threads.py`, o parsing de metadata passou a usar `LogAnalysisService`.

- antes: chamada direta de `parse_metadata_inteligente`
- agora: `LogAnalysisService.parse_log_metadata(...)`

Essa mudanca foi feita apenas no ponto de parsing, sem alterar fluxo de thread, estrutura de retorno ou comportamento funcional.

## Salvamento de analise migrado para Application Service

No fluxo de UI em `src/app_desktop/ui_main.py`, o salvamento de observacoes/analises passou a usar `LogAnalysisService`.

- antes: chamada direta de `salvar_observacao(...)`
- agora: `LogAnalysisService.save_analysis(...)`

A mudanca manteve mensagens da UI, tratamento de erro e comportamento funcional inalterados.

## Proximos passos

- Migrar chamadas pontuais de `ui_main.py` para services de `application` sem alterar comportamento.
- Adicionar testes de application para `wiki`, `auth` e `report`.
- Evoluir contratos de DTOs conforme necessidade de fluxos da UI.
