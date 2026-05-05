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

## Proximos passos

1. Integrar `SearchOptions` ao fluxo de busca em `threads.py` sem alterar UX.
2. Aplicar `max_results` com fallback seguro.
3. Medir baseline de tempo de busca por volume/diretorio.
4. Evoluir para indexacao/cache local opcional.
5. Preparar indicadores para dashboard premium futuro.
