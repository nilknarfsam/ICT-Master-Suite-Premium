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


def main(args=None):
    cli_args = list(args) if args is not None else sys.argv[1:]
    config = carregar_config()
    directories = resolve_directories(cli_args, config)
    service = LogIndexApplicationService()
    allowed = set(DEFAULT_EXTENSIONS)

    for directory in directories:
        if not directory:
            continue
        summary = service.build_incremental_index(directory, allowed_extensions=allowed)
        print(f"Diretorio indexado: {directory}")
        print(f"Quantidade indexada: {summary.get('indexed', 0)}")
        print(f"Erros: {summary.get('errors', 0)}")
        print("---")

    print(f"Total final no indice: {service.count_entries()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
