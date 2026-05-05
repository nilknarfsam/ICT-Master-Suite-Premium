# Facade de Compatibilidade Temporaria

## Por que esta facade existe

A UI antiga historicamente consome funcoes centralizadas em `models.py`. Como a Fase 1 iniciou a modularizacao em `src/core` e `src/infrastructure`, a facade em `src/app_desktop/legacy_facade.py` funciona como ponte para evitar quebra durante a migracao.

## Natureza temporaria

Esta facade e temporaria. O objetivo e permitir migracao gradual do codigo da UI sem alteracao de comportamento, enquanto os imports sao movidos aos poucos para os modulos reais.

## Como ajuda na migracao do ui_main.py

- Permite trocar importacoes de `models.py` por `legacy_facade.py` primeiro.
- Mantem a mesma assinatura de funcoes esperadas pela UI.
- Reduz risco de regressao ao centralizar o ponto de compatibilidade.

## Modulos reais utilizados pela facade

- `src/core/config/config_service.py`
- `src/core/database/database_connection.py`
- `src/core/auth/auth_service.py`
- `src/core/parsers/log_type_detector.py`
- `src/core/parsers/parser_factory.py`
- `src/core/failures/failure_repository.py`
- `src/core/wiki/wiki_repository.py`
- `src/core/reports/report_service.py`
- `src/core/sync/offline_sync_service.py`

## Cuidados importantes

- Nao adicionar regra de negocio nova na facade.
- Nao duplicar logica: a facade apenas reexporta/encaminha.
- Evitar efeitos colaterais no import (inicializacao automatica de banco).
- Toda mudanca funcional deve ocorrer nos modulos reais de `src/core` e `src/infrastructure`.
- Remover a facade ao final da migracao completa da UI para imports diretos.
