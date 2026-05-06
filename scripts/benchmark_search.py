"""Benchmark reproduzivel da busca hibrida (index x scanner).

Executa uma serie de buscas usando `LogSearchService.timed_search_with_index`
e, opcionalmente, um varredor recursivo equivalente ao `BuscaThread` para
comparacao. Imprime resumo e pode anexar resultado em `docs/BASELINE_BUSCA.md`.

Uso basico:

    python scripts/benchmark_search.py --term abc123 --repeat 5

Comparando contra scanner (replica regras de filtro do service, sem importar UI):

    python scripts/benchmark_search.py --term abc123 --repeat 5 --include-scanner

Anexar resultado no doc de baseline:

    python scripts/benchmark_search.py --term abc123 --repeat 5 --include-scanner \
        --write docs/BASELINE_BUSCA.md

Sem alterar fluxo da UI; usa apenas a camada application e leitura de disco.
"""

from __future__ import annotations

import argparse
import os
import socket
import statistics
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.application.dtos.search_options import SearchOptions
from src.application.services.log_index_application_service import (
    LogIndexApplicationService,
)
from src.application.services.log_search_service import LogSearchService
from src.core.config.config_service import carregar_config


DEFAULT_REPEAT = 5


def resolve_directories(args_dirs, config) -> list[str]:
    if args_dirs:
        return [d for d in args_dirs if d]
    return [
        config.get("caminho_logs_tri", "") or "",
        config.get("caminho_logs_agilent", "") or "",
        config.get("backup_local_dir", "") or "",
    ]


def scanner_search(
    service: LogSearchService,
    options: SearchOptions,
    term: str,
    directories: list[str],
) -> list[tuple]:
    """Replica regras do scanner sem importar BuscaThread (PyQt5)."""
    encontrados: list[tuple] = []
    for diretorio in directories:
        if not diretorio or not os.path.exists(diretorio):
            continue
        encontrados.extend(_scandir_recursivo(diretorio, service, options, term))

    encontrados.sort(key=lambda x: x[0], reverse=True)
    encontrados = service.limit_results(encontrados, options)
    return [(item[1], item[2]) for item in encontrados]


def _scandir_recursivo(
    caminho: str,
    service: LogSearchService,
    options: SearchOptions,
    term: str,
) -> list[tuple]:
    resultados: list[tuple] = []
    try:
        with os.scandir(caminho) as it:
            for entry in it:
                try:
                    if entry.is_dir(follow_symlinks=False):
                        resultados.extend(
                            _scandir_recursivo(entry.path, service, options, term)
                        )
                    elif entry.is_file(follow_symlinks=False):
                        if service.should_include_file(entry.name, term, options):
                            ts = entry.stat().st_mtime
                            resultados.append((ts, entry.name, entry.path))
                except (PermissionError, OSError):
                    continue
    except (PermissionError, OSError):
        pass
    return resultados


def _timed_scanner(
    service: LogSearchService,
    options: SearchOptions,
    term: str,
    directories: list[str],
):
    start = time.perf_counter()
    results = scanner_search(service, options, term, directories)
    elapsed_ms = (time.perf_counter() - start) * 1000.0
    return results, elapsed_ms


def _stats(samples_ms: list[float]) -> dict:
    if not samples_ms:
        return {"runs": 0, "mean_ms": 0.0, "median_ms": 0.0, "p95_ms": 0.0}
    runs = len(samples_ms)
    mean_ms = statistics.fmean(samples_ms)
    median_ms = statistics.median(samples_ms)
    if runs == 1:
        p95_ms = samples_ms[0]
    else:
        sorted_samples = sorted(samples_ms)
        idx = max(0, min(runs - 1, int(round(0.95 * (runs - 1)))))
        p95_ms = sorted_samples[idx]
    return {
        "runs": runs,
        "mean_ms": mean_ms,
        "median_ms": median_ms,
        "p95_ms": p95_ms,
    }


def _format_table(rows: list[dict]) -> str:
    header = (
        "| mode    | term            | runs | mean_ms | median_ms |  p95_ms | results |\n"
        "|---------|-----------------|------|---------|-----------|---------|---------|"
    )
    lines = [header]
    for r in rows:
        lines.append(
            "| {mode:<7} | {term:<15} | {runs:>4} | {mean_ms:>7.2f} | {median_ms:>9.2f} | {p95_ms:>7.2f} | {results:>7} |".format(
                **r
            )
        )
    return "\n".join(lines)


def _build_report(
    rows: list[dict],
    *,
    term: str,
    repeat: int,
    include_scanner: bool,
    directories: list[str],
    index_total: int,
) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    host = socket.gethostname()
    lines = [
        f"## Execucao {timestamp}",
        "",
        f"- Host: `{host}`",
        f"- Termo: `{term}`",
        f"- Repeticoes por modo: `{repeat}`",
        f"- Modo scanner habilitado: `{include_scanner}`",
        f"- Total no indice (count_entries): `{index_total}`",
        "- Diretorios analisados:",
    ]
    for d in directories:
        lines.append(f"  - `{d or '(vazio)'}`")
    lines.append("")
    lines.append(_format_table(rows))
    lines.append("")
    return "\n".join(lines)


def _append_to_baseline_doc(report: str, target_path: Path) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    if target_path.exists():
        existing = target_path.read_text(encoding="utf-8")
        if not existing.endswith("\n"):
            existing += "\n"
        target_path.write_text(existing + "\n" + report, encoding="utf-8")
    else:
        header = (
            "# Baseline da busca hibrida\n\n"
            "Registro reproduzivel de tempos de busca (index x scanner).\n"
            "Cada execucao do `scripts/benchmark_search.py --write ...` anexa um bloco aqui.\n"
        )
        target_path.write_text(header + "\n" + report, encoding="utf-8")


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark reproduzivel da busca hibrida (index x scanner).",
    )
    parser.add_argument(
        "--term",
        required=True,
        help="Termo de busca (serial ou trecho de nome de arquivo).",
    )
    parser.add_argument(
        "--repeat",
        type=int,
        default=DEFAULT_REPEAT,
        help=f"Numero de repeticoes por modo (default: {DEFAULT_REPEAT}).",
    )
    parser.add_argument(
        "--include-scanner",
        action="store_true",
        help="Tambem mede a via scanner em disco para comparacao.",
    )
    parser.add_argument(
        "--directory",
        action="append",
        default=None,
        help=(
            "Diretorio adicional para o modo scanner. "
            "Pode ser repetido. Sem este flag, usa caminhos de carregar_config()."
        ),
    )
    parser.add_argument(
        "--write",
        default=None,
        help="Caminho de arquivo markdown para anexar relatorio (ex.: docs/BASELINE_BUSCA.md).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    config = carregar_config()
    directories = resolve_directories(args.directory, config)

    service = LogSearchService()
    options = service.build_default_options()

    print("=====================================")
    print("ICT Master Suite - Search Benchmark")
    print("=====================================")
    print(f"Termo: {args.term}")
    print(f"Repeticoes: {args.repeat}")
    print(f"Modo scanner: {'on' if args.include_scanner else 'off'}")
    print()

    index_ready = service.is_index_ready()
    if not index_ready:
        print("[AVISO] Indice indisponivel. Modo index sera marcado como ausente.")

    rows: list[dict] = []

    index_samples_ms: list[float] = []
    index_results_count = 0
    if index_ready:
        for _ in range(args.repeat):
            results, elapsed_ms = service.timed_search_with_index(args.term, options)
            if results is None:
                # indice virou indisponivel no meio da rodada; aborta modo index
                index_samples_ms = []
                break
            index_samples_ms.append(elapsed_ms)
            index_results_count = len(results)

    if index_samples_ms:
        st = _stats(index_samples_ms)
        rows.append(
            {
                "mode": "index",
                "term": args.term,
                "results": index_results_count,
                **st,
            }
        )

    scanner_samples_ms: list[float] = []
    scanner_results_count = 0
    if args.include_scanner:
        valid_dirs = [d for d in directories if d]
        if not valid_dirs:
            print("[AVISO] Nenhum diretorio valido para o modo scanner.")
        for _ in range(args.repeat):
            results, elapsed_ms = _timed_scanner(service, options, args.term, valid_dirs)
            scanner_samples_ms.append(elapsed_ms)
            scanner_results_count = len(results)
        if scanner_samples_ms:
            st = _stats(scanner_samples_ms)
            rows.append(
                {
                    "mode": "scanner",
                    "term": args.term,
                    "results": scanner_results_count,
                    **st,
                }
            )

    if not rows:
        print("[ERRO] Nao foi possivel medir nem index nem scanner.")
        return 1

    print(_format_table(rows))
    print()

    try:
        index_total = LogIndexApplicationService().count_entries()
    except Exception:
        index_total = 0

    report = _build_report(
        rows,
        term=args.term,
        repeat=args.repeat,
        include_scanner=args.include_scanner,
        directories=directories,
        index_total=index_total,
    )

    if args.write:
        target = Path(args.write)
        if not target.is_absolute():
            target = ROOT / target
        _append_to_baseline_doc(report, target)
        print(f"Relatorio anexado em: {target}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
