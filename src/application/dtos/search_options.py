from dataclasses import dataclass


@dataclass
class SearchOptions:
    max_results: int = 500
    include_backup: bool = True
    include_pass_logs: bool = False
    allowed_extensions: tuple[str, ...] = (".csv", ".dcl", ".txt", ".log")
