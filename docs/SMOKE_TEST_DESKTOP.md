# Smoke Test Manual - Desktop Premium

Checklist operacional para validacao manual da base desktop premium antes de novas refatoracoes.

## Pre-condicoes

- Executar a partir da raiz do projeto.
- Ambiente Python com dependencias instaladas.
- Acesso aos caminhos de log e banco conforme configuracao.

## Checklist de validacao

- [ ] Abertura do app por `python run_desktop.py`
- [ ] Login admin valido
- [ ] Login invalido (mensagem de erro)
- [ ] Busca de serial
- [ ] Abertura de log na lista de resultados
- [ ] Exibicao de conteudo do log
- [ ] Preenchimento/atualizacao da tabela TRI
- [ ] Consulta de historico de analises
- [ ] Salvar analise/observacao
- [ ] Modo visitante (restricoes esperadas)
- [ ] Wiki: listar modelos
- [ ] Wiki: adicionar modelo
- [ ] Wiki: adicionar solucao
- [ ] Administracao de usuarios (listar, criar, editar, remover)
- [ ] Exportar relatorio Excel
- [ ] Tela de configuracoes (carregar/salvar)
- [ ] Minimizar para bandeja
- [ ] Fechamento do app (comportamento esperado)

## Evidencias recomendadas

- Registrar data/hora do teste.
- Anotar resultado por item (OK/FALHA).
- Em caso de falha, registrar passos para reproduzir e mensagem exibida.
