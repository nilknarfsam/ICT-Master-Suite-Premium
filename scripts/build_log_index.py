import sys

from src.application.services.log_index_application_service import LogIndexApplicationService
from src.core.config.config_service import carregar_config


DEFAULT_EXTENSIONS = (".csv", ".dcl", ".txt", ".log")


def resolve_directories(args, config):
    if args:
        return [p for p in args if p]
    return [
        config.get("caminho_logs_tri", ""),
        config.get("caminho_logs_agilent", ""),
        config.get("backup_local_dir", ""),
    ]


def parse_mode_and_paths(cli_args):
    args = list(cli_args or [])
    rebuild = False
    if "--rebuild" in args:
        rebuild = True
        args = [a for a in args if a != "--rebuild"]
    return rebuild, args


def main(args=None):
    cli_args = list(args) if args is not None else sys.argv[1:]
    rebuild_mode, path_args = parse_mode_and_paths(cli_args)
    config = carregar_config()
    directories = resolve_directories(path_args, config)
    service = LogIndexApplicationService()
    allowed = set(DEFAULT_EXTENSIONS)

    print("=====================================")
    print("ICT Master Suite - Log Index Builder")
    print("=====================================")
    print(f"Modo: {'rebuild' if rebuild_mode else 'incremental'}")

    valid_dirs = [d for d in directories if d]
    total_indexed = 0
    total_errors = 0

    if rebuild_mode:
        rebuild_summary = service.rebuild_index(valid_dirs, allowed_extensions=allowed)
        total_indexed = rebuild_summary.get("total_indexed", 0)
        total_errors = rebuild_summary.get("total_errors", 0)
        for item in rebuild_summary.get("per_path", []):
            print(f"Diretorio indexado: {item.get('path', '')}")
            print(f"Indexados: {item.get('indexed', 0)}")
            print(f"Erros: {item.get('errors', 0)}")
            print("---")
    else:
        for directory in valid_dirs:
            summary = service.build_incremental_index(directory, allowed_extensions=allowed)
            total_indexed += summary.get("indexed", 0)
            total_errors += summary.get("errors", 0)
            print(f"Diretorio indexado: {directory}")
            print(f"Indexados: {summary.get('indexed', 0)}")
            print(f"Erros: {summary.get('errors', 0)}")
            print("---")

    print("Resumo final:")
    print(f"Total indexado: {total_indexed}")
    print(f"Total erros: {total_errors}")
    print(f"Total no indice: {service.count_entries()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
