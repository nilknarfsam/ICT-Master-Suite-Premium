# ROADMAP - ICT Master Suite Premium

## Fase 1 - Modularizacao do Python atual

- Organizar o codigo legado em modulos de dominio.
- Definir contratos entre UI, regras e infraestrutura.
- Reduzir acoplamento mantendo comportamento atual.
- Criar facade temporaria de compatibilidade (`src/app_desktop/legacy_facade.py`) para migracao gradual da UI antiga.

## Fase 2 - Separacao UI / Core

- Isolar camada de interface desktop da camada de negocio.
- Padronizar servicos de aplicacao para operacoes de logs.
- Preparar testes unitarios para servicos centrais.
- Application Services Layer criada e validada nos fluxos principais.
- Auditoria final de dependencias da `legacy_facade` executada.
- Status: **quase concluida** (restando apenas fechamento da compatibilidade da facade).

## Fase 3 - Performance e Otimizacao da Busca de Logs

- Otimizar performance da busca de logs em rede.
- Introduzir indexacao/cache local para reduzir latencia.
- Melhorar scanner de arquivos (filtros, recursao e robustez).
- Medir desempenho com cenarios reais e estabelecer baseline.
- Preparar base para dashboard premium futuro.

## Fase 4 - API local opcional

- Disponibilizar endpoints locais para integracoes internas.
- Expor consultas de historico, falhas e conhecimento tecnico.
- Manter modo desktop como fluxo principal.

## Fase 5 - Interface moderna futura

- Evoluir experiencia de uso com componentes visuais modernos.
- Melhorar navegacao de historico e produtividade tecnica.
- Preservar compatibilidade com operacao atual.

## Fase 6 - Relatorios e dashboard premium

- Consolidar analytics de falhas e tratativas.
- Entregar relatorios tecnicos e indicadores de performance.
- Estruturar visao gerencial para tomada de decisao.
