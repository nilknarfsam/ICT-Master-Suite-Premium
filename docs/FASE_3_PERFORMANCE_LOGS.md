# Fase 3 - Performance da Busca de Logs

## Objetivo da Fase 3

Iniciar melhorias de performance na busca de logs sem alterar o comportamento padrao atual da aplicacao.

A estrategia desta etapa e preparar opcoes configuraveis seguras no nivel de service para evolucao gradual.

## Por que limitar resultados

Ambientes com grande volume de arquivos em rede podem gerar latencia elevada e consumo excessivo de IO.

Um limite de resultados ajuda a:

- reduzir tempo de resposta em buscas amplas
- diminuir risco de travamento por volume extremo
- criar base para ajustes progressivos sem regressao funcional

## Opcoes de busca criadas

Foi introduzido o DTO `SearchOptions` em `src/application/dtos/search_options.py` com:

- `max_results` (padrao: 500)
- `include_backup` (padrao: `True`)
- `include_pass_logs` (padrao: `False`)
- `allowed_extensions` (padrao: `.csv`, `.dcl`, `.txt`, `.log`)

No `LogSearchService`, foram adicionados:

- `build_default_options() -> SearchOptions`
- `should_include_file(file_name, term, options) -> bool`

A logica de filtro preserva o comportamento atual:

- arquivo deve conter o termo
- extensao deve estar na lista permitida
- logs com `pass` no nome (ou prefixo `p_`) ficam fora por padrao

## Filtro do scanner conectado ao LogSearchService

O scanner em `src/app_desktop/threads.py` agora utiliza `LogSearchService.should_include_file(...)` para decidir se um arquivo entra na lista de candidatos.

Garantias mantidas nesta integracao:

- mesma regra de termo no nome
- mesma regra de extensoes permitidas
- mesma rejeicao padrao de arquivos `pass` e prefixo `p_`
- mesma ordenacao final por data e formato de retorno para a UI
- mesmo tratamento de erros de permissao/IO durante varredura

## Limite inicial de resultados

Para reduzir carga em buscas extensas na rede, o scanner aplica um limite interno de resultados apos a ordenacao por data.

Detalhes atuais:

- padrao: `500` resultados (via `SearchOptions.max_results`)
- aplicacao: no fluxo do scanner, antes da emissao para UI
- previsibilidade: limite centralizado em `LogSearchService.limit_results(...)`

Observacao de evolucao:

- este valor pode ser exposto futuramente como opcao configuravel na UI, mantendo fallback seguro no service

## Resumo interno de busca limitada

O scanner agora prepara um resumo interno apos aplicar o limite, sem alterar o formato atual de lista enviado para a UI.

Dados gerados:

- `total_original`
- `total_exibido`
- `limitado`
- `max_results`

Implementacao:

- `LogSearchService.was_limited(original_count, limited_count)` define se houve corte real
- `BuscaThread` armazena `self.was_limited`
- `BuscaThread` emite sinal opcional `search_summary` com dicionario de resumo

Uso futuro:

- a UI pode consumir esse sinal posteriormente para mensagens/indicadores de UX, sem necessidade de alterar a regra de busca

## Proximos passos

1. Integrar `SearchOptions` ao fluxo de busca em `threads.py` sem alterar UX.
2. Aplicar `max_results` com fallback seguro.
3. Medir baseline de tempo de busca por volume/diretorio.
4. Evoluir para indexacao/cache local opcional.
5. Preparar indicadores para dashboard premium futuro.
