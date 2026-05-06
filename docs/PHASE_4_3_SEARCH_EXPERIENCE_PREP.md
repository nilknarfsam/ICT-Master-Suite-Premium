# Subfase 4.3 — Search Experience Premium (Preparacao)

> Documento ponte entre a Subfase 4.2 (Dashboard Premium concluida) e a entrega
> completa da **Subfase 4.3 — Search Experience Premium**. Registra a rodada
> operacional pos-4.2 (refinamento de UI) e fixa o ponto de partida para a
> proxima subfase formal.

## 1. Objetivo

Preparar o terreno para a Subfase 4.3 (extracao do Finder Logs em
componentes premium com `widgets/search/`, `viewmodels/search/finder_viewmodel.py`
e `pages/finder/finder_page.py`), garantindo que o workspace atual ja entregue
**a melhor experiencia possivel para o tecnico** — mesmo antes da
componentizacao formal — corrigindo problemas observados em smoke visual real
da build pos-4.2.

## 2. Motivacao (smoke visual real)

A build pos-4.2 evidenciou:

1. **Janela inicial cortada** em monitores menores: `setGeometry(100, 100, 1280, 800)`
   nao respeitava a `availableGeometry` (barra de tarefas/Windows).
2. **Dashboard em primeiro plano** desviava o foco operacional do tecnico, que
   precisa do Finder Logs como aba primaria.
3. **Painel "Detalhamento de Defeitos (TRI)"** ocupava muito espaco vertical
   sem agregar valor imediato no fluxo do dia-a-dia (apos discussao com o
   usuario, foi decidido ocultar visualmente preservando parser/populate).
4. **Lista de logs encontrados** nao priorizava arquivos recentes, dificultando
   a localizacao do log que o tecnico acabou de gerar.
5. **Textos** ainda traziam linguagem legada ("Historico (Recentes):",
   "Log do Arquivo:") em vez de descricoes claras de fluxo.

## 3. Mudancas entregues nesta rodada (pos-4.2, pre-4.3)

Todas em [`src/app_desktop/ui_main.py`](../src/app_desktop/ui_main.py),
sem alterar `threads.py`, services, core, parsers ou esquema SQLite.

### 3.1 Ordem de abas

```
1. Finder Logs (prioritaria)
2. Base de Conhecimento
3. Historico Local
4. Gestao de Usuarios (admin)
5. Configuracoes do Sistema (admin)
6. Dashboard (lazy load, ultimo)
```

- Lazy-load do Dashboard preservado (`_on_tab_changed_for_dashboard`).
- Quick actions do Dashboard (`_on_dashboard_quick_action`) seguem usando
  `setCurrentWidget(widget)` — independente de indice.
- `setTabVisible(self.tabs.indexOf(self.tab_admin/config), ...)` segue
  funcional (resolucao por widget, nao por indice).

### 3.2 Geometria responsiva

- Adicionado `QGuiApplication` ao import.
- Substituido `self.setGeometry(100, 100, 1280, 800)` por logica baseada em
  `QGuiApplication.primaryScreen().availableGeometry()`:
  - largura: `min(1280, max(900, avail.width() - 40))`
  - altura: `min(820, max(600, avail.height() - 40))`
  - centralizada na tela primaria
  - fallback explicito para `(100, 100, 1280, 800)` se `primaryScreen()` for
    `None`.

### 3.3 Finder Logs priorizado

- **Painel TRI oculto** visualmente (`self.lbl_table_title` e `self.table` com
  `setVisible(False)` no setup e em `on_file_loaded`). Parser TRI continua
  sendo invocado normalmente; tabela continua sendo populada (apenas oculta).
- **Mais espaco vertical**:
  - `self.txt_observacao.setFixedHeight(60)` substituido por
    `setMinimumHeight(90)`.
  - `self.l_right.setStretchFactor(self.text_raw, 3)` e
    `setStretchFactor(self.txt_historico_chat, 2)`.
- **Splitter** `[300, 800]` -> `[320, 980]`, dando mais espaco para a coluna
  de leitura.
- **Lista ordenada por data desc**: `popular_lista` calcula `mtime` por
  arquivo (com `try/except OSError` -> `mtime=0`), ordena `reverse=True` e
  monta `QListWidgetItem` com label `"YYYY-MM-DD HH:MM - nome"`. O nome
  canonico e armazenado em `Qt.UserRole` para preservar `arquivos_mapa`.
- **`carregar_arquivo`** passa a usar `item.data(Qt.UserRole) or item.text()`
  para lookup, garantindo compatibilidade com itens legados.
- **Textos amigaveis**:
  - `"Histórico (Recentes):"` -> `"Logs encontrados:"`.
  - `"Selecione um arquivo."` -> `"Selecione um log para visualizar."`.
  - `"Log do Arquivo:"` -> `"Visualizacao do Log:"`.

### 3.4 O que NAO foi alterado

- `src/app_desktop/threads.py` (todos os contratos preservados).
- `src/app_desktop/legacy_facade.py`.
- `src/application/services/` (LogSearchService, LogAnalysisService, etc.).
- `src/core/` e parsers (`src/core/parsers/`).
- Esquema SQLite e indice.
- Entregas das Subfases 4.1/4.2 (`themes/`, `widgets/`, `pages/dashboard/`,
  `viewmodels/dashboard/`).
- Suite de testes existente (sem testes novos nesta rodada).

## 4. Riscos mapeados

| ID  | Risco | Mitigacao |
|-----|-------|-----------|
| R1  | Lookup quebrar com label diferente do nome | `Qt.UserRole` armazena nome canonico; fallback `item.text()` cobre legado. |
| R2  | Quick actions quebrarem com nova ordem | Usam `setCurrentWidget(widget)` — imune a ordem. |
| R3  | `setTabVisible` quebrar com nova ordem | `indexOf(widget)` resolve por referencia. |
| R4  | `availableGeometry` indisponivel | Fallback explicito para `(100,100,1280,800)`. |
| R5  | Painel TRI invisivel mascarar regressao do parser | Parser e populate continuam ativos; testes de `tests/parsers` cobrem o parser. |
| R6  | `getmtime` falhar em arquivo de rede | `try/except OSError` -> `mtime=0`, item vai ao final, sem quebrar populate. |
| R7  | Falha pre-existente em `tests/parsers/test_tri_parser.py::test_parse_tri_txt_pass_serial_modelo` | Mantida como debito mapeado; nao tratada nesta rodada. |

## 5. Proximo passo formal — Subfase 4.3 (escopo completo)

Conforme [`PHASE_4_COMPLETION_EXECUTION_PLAN.md`](PHASE_4_COMPLETION_EXECUTION_PLAN.md)
e [`PHASE_4_UI_PREMIUM_PLAN.md`](PHASE_4_UI_PREMIUM_PLAN.md), a Subfase 4.3
ainda devera entregar:

1. **`src/app_desktop/widgets/search/`** com componentes reutilizaveis
   (search bar com debounce, results list com badges TRI/Agilent/datas, status
   chips, empty/loading states).
2. **`src/app_desktop/viewmodels/search/finder_viewmodel.py`** orquestrando
   `BuscaThread` via worker-safe pattern (signals desacoplados da UI).
3. **`src/app_desktop/pages/finder/finder_page.py`** consolidando o Finder
   Logs em pagina autonoma (extracao do `setup_finder` atual).
4. **Testes** sob `tests/app_desktop/finder/`:
   - `test_finder_viewmodel.py` (mock de `BuscaThread`/`LogSearchService`).
   - `test_finder_widgets_import.py` (smoke imports).
   - `test_finder_page_smoke.py` (instanciacao com QApplication temporario).
5. **Integracao final em `ui_main.py`**: substituir `setup_finder` legado por
   `FinderPage(...)` mantendo todos os hooks (`buscar`, `popular_lista`,
   `carregar_arquivo`, `salvar_analise_tecnico`).
6. **Validacoes**: `pytest tests/app_desktop tests/application tests/core` em
   verde + smoke visual real + commit local
   `feat(ui): subfase 4.3 search experience premium`.

## 6. Observacoes finais

- Esta rodada e **operacional**, nao formal: nao renumera subfases, nao altera
  contratos publicos, nao introduz novos modulos. Serve como ponte para
  garantir que a Subfase 4.3 comece em um workspace ja "limpo" do ponto de
  vista do operador.
- A reativacao do painel TRI sera trivial assim que a Subfase 4.4 entrar
  (Log Viewer Premium) — bastara reexpor a tabela como sub-componente
  toggleavel dentro da nova `FinderPage` ou de uma `LogDetailPanel`.
