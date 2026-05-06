# Baseline da busca hibrida

Registro reproduzivel de tempos de busca (index x scanner).
Cada execucao do `scripts/benchmark_search.py --write docs/BASELINE_BUSCA.md` anexa um bloco abaixo.

## Como gerar uma medicao

Pre-condicoes:

- Indice ja construido (via UI `🔄 Reindexar Logs` ou `python scripts/build_log_index.py --rebuild`).
- Diretorios de logs configurados em `ict_config.json`.
- Termo de busca conhecido (serial valido com pelo menos 1 ocorrencia).

Comando recomendado para baseline completo:

    python scripts/benchmark_search.py --term <serial> --repeat 5 --include-scanner --write docs/BASELINE_BUSCA.md

Notas:

- Repeticoes = 5 reduz ruido de IO de rede.
- Tempos sao em milissegundos (`mean_ms`, `median_ms`, `p95_ms`).
- O script nao altera comportamento da UI; apenas le indice e diretorios.

## Tabela consolidada de execucoes

Atualizar manualmente conforme novas execucoes forem registradas.

| Data | Ambiente | Termo | Indice (count) | mean_ms index | mean_ms scanner | Observacoes |
|------|----------|-------|----------------|---------------|-----------------|-------------|
| -    | -        | -     | -              | -             | -               | -           |

## Criterios de aprovacao do baseline

Considera-se baseline aprovado quando, simultaneamente:

1. `mean_ms` do modo `index` for consistentemente menor que `mean_ms` do modo `scanner` em pelo menos 2 execucoes.
2. Numero de resultados retornados pelos dois modos for compativel para o mesmo termo.
3. Nenhuma execucao apresentar erro nao tratado durante o benchmark.
4. Tempos coletados em pelo menos 1 ambiente real (idealmente 2: rede local e remota).

## Historico de execucoes

(Anexado automaticamente abaixo desta secao pelo script de benchmark.)
