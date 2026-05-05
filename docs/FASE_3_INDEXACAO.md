# Fase 3 - Indexacao Local de Logs

## Por que indexacao e importante

A busca atual percorre diretorios e subdiretorios em tempo real. Em ambientes de rede com muitos arquivos, isso pode aumentar latencia e custo de IO.

A indexacao local cria uma base auxiliar para consultas mais rapidas por nome de arquivo, reduzindo leituras repetidas no filesystem remoto.

## Busca atual vs busca indexada

Busca atual (scandir em tempo real):

- reflete imediatamente o estado do diretorio
- custo maior em buscas amplas
- depende diretamente da performance de rede no momento da busca

Busca indexada (SQLite local):

- consulta local mais rapida para filtro inicial
- reduz carga de varredura repetitiva
- exige ciclo de construcao/atualizacao do indice

## Estrutura inicial criada

Modulo novo em `src/core/indexing`:

- `log_index_repository.py`
  - `init_index_db()`
  - `insert_log_entry(file_name, path, modified_time)`
  - `search_by_term(term)`
  - `clear_index()`
- `log_index_service.py`
  - `build_index_from_directory(base_path)`
  - `search(term)`
  - `is_index_available()`

Observacao: nesta etapa, a indexacao foi criada apenas como base futura e ainda nao foi conectada ao fluxo real de busca.

## Indexacao incremental

A estrutura agora suporta indexacao incremental para reduzir custo de reconstrucoes completas.

Evolucoes adicionadas:

- enriquecimento do schema `log_index` com:
  - `extension`
  - `size_bytes`
  - `indexed_at`
- compatibilidade com tabelas antigas via `ALTER TABLE` seguro em inicializacao
- `upsert_log_entry(...)` para atualizar registro existente por `path`
- `get_entry_by_path(path)` e `count_entries()`

No service:

- `index_file(path)` indexa arquivo individual com validacoes basicas
- `build_incremental_index(base_path, allowed_extensions=None)` percorre diretorio, aplica filtro de extensao e retorna resumo:
  - `indexed`
  - `errors`

## Application Service de indexacao

Foi adicionada uma ponte de aplicacao em `src/application/services/log_index_application_service.py` para encapsular acesso ao motor de indexacao do core.

API exposta:

- `build_incremental_index(base_path, allowed_extensions=None)`
- `index_file(path)`
- `search(term)`
- `is_index_available()`
- `count_entries()`

Observacao: essa camada ainda nao foi conectada na UI nem no fluxo principal de busca.

## Script manual de indexacao

Foi adicionado o script `scripts/build_log_index.py` para construcao/atualizacao manual do indice local, sem execucao automatica na inicializacao do app.

Comportamento:

- aceita diretorios por argumento de linha de comando
- sem argumentos, usa caminhos do config:
  - `caminho_logs_tri`
  - `caminho_logs_agilent`
  - `backup_local_dir`
- usa extensoes padrao:
  - `.csv`, `.dcl`, `.txt`, `.log`
- imprime resumo por diretorio e total final no indice

Exemplos de uso:

- `python scripts/build_log_index.py`
- `python scripts/build_log_index.py "\\servidor\logs\tri" "\\servidor\logs\agilent"`

## Busca hibrida (index + fallback)

Foi adicionada base no `LogSearchService` para tentativa de busca via indice local antes de cair no scanner tradicional.

Comportamento atual:

- `is_index_ready()` verifica disponibilidade do indice via `LogIndexApplicationService`
- `search_with_index(term, options)`:
  - quando indice esta disponivel, consulta indice, aplica `should_include_file(...)` e `limit_results(...)`
  - quando indice nao esta disponivel, retorna `None` para fallback seguro no scanner atual

Observacao: nesta etapa, a busca hibrida ainda nao foi conectada no fluxo real das threads.

## Busca hibrida ativada na thread

A `BuscaThread` agora tenta usar o indice local primeiro e faz fallback automatico para o scanner tradicional quando necessario.

Fluxo aplicado:

- tenta `search_with_index(...)` com `try/except`
- se retornar `None` (indice indisponivel/erro), executa scanner atual sem alteracoes
- se retornar lista (mesmo vazia), usa resultado do indice e nao roda scanner
- converte resultado para formato esperado da UI: `(file_name, path)`
- emite `lista_arquivos` e `search_summary` mantendo contrato existente

Garantia de seguranca:

- scanner tradicional continua intacto e como fallback confiavel

## Feedback de origem da busca

O `search_summary` agora informa a origem da busca para permitir feedback leve na `status_bar`, sem alterar layout.

Campo adicionado no resumo:

- `source: "index"` quando resultado veio do indice local
- `source: "scanner"` quando resultado veio da varredura em rede

Na mensagem da status bar:

- `source == "index"`: prefixo `Busca rápida:`
- `source == "scanner"`: prefixo `Busca em rede:`
- sem `source`: comportamento antigo preservado

## Proximos passos (ativacao progressiva)

1. Construir indice em rotina controlada (manual/agendada).
2. Medir ganho de latencia entre busca direta e indexada.
3. Adotar estrategia hibrida (indice + validacao pontual em disco).
4. Integrar de forma gradual com fallback seguro para busca atual.
5. Expor estado do indice na camada de aplicacao sem alterar UX inicial.
