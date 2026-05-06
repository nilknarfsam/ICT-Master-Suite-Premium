# Validacao operacional — Indexacao e busca rapida

## Objetivo

Executar um checklist real para validar indexacao, reindexacao pela UI, busca hibrida (indice + fallback) e manter seguranca antes da evolucao para Electron/React.

## Regras desta validacao

- Nao alterar codigo funcional.
- Nao alterar UI.
- Nao mexer no legado.
- Apenas validacao operacional e registro dos resultados.

## Pre-condicoes

- Ambiente Windows com projeto aberto em `C:\projetos\ICT-Master-Suite-Premium`.
- Dependencias instaladas na `.venv`.
- Usuario admin disponivel para login.
- Acesso aos diretorios de logs configurados.

## Checklist operacional

## A) Execucao do app

- [ ] Rodar `scripts\run_desktop.bat`.
- [ ] Confirmar abertura do app.
- [ ] Confirmar status inicial (sem erro critico em tela).
- [ ] Registrar hora de inicio da execucao.

## B) Reindexacao pela UI

- [ ] Fazer login como admin.
- [ ] Abrir `Configuracoes`.
- [ ] Clicar em `🔄 Reindexar Logs`.
- [ ] Validar mensagem de conclusao da reindexacao.
- [ ] Anotar total indexado.
- [ ] Anotar total de erros (se houver).
- [ ] Confirmar que a UI permaneceu responsiva durante o processo.

## C) Busca usando indice

- [ ] Buscar um serial conhecido (com logs ja presentes no indice).
- [ ] Validar `status_bar` com prefixo `Busca rapida:`.
- [ ] Abrir um log retornado.
- [ ] Confirmar metadata esperada do log aberto.

## D) Fallback para scanner

- [ ] Simular indice ausente/vazio (apenas se seguro no ambiente).
- [ ] Buscar serial conhecido.
- [ ] Validar `status_bar` com prefixo `Busca em rede:`.
- [ ] Confirmar que os resultados foram retornados via scanner.

## E) Validacao por script

- [ ] Rodar `python scripts/build_log_index.py --rebuild`.
- [ ] Rodar `python scripts/build_log_index.py`.
- [ ] Validar total final indexado ao fim da rotina.
- [ ] Registrar tempos aproximados de cada execucao.

## F) Criterios de aprovacao

- [ ] App abre corretamente.
- [ ] Reindexacao pela UI conclui sem travar interface.
- [ ] Busca indexada funciona com `Busca rapida:`.
- [ ] Fallback para scanner funciona com `Busca em rede:`.
- [ ] Salvamento de analise continua funcionando.

## Registro da execucao

- Data:
- Responsavel:
- Ambiente (maquina/rede):
- Resultado geral: Aprovado / Reprovado
- Observacoes:
