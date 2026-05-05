from dataclasses import asdict, is_dataclass

from src.core.failures.failure_repository import ler_observacao, salvar_falha_db, salvar_observacao
from src.core.parsers.parser_factory import parse_metadata_inteligente


class LogAnalysisService:
    """Serviço de aplicação para orquestrar análise e persistência de logs."""

    def parse_log_metadata(self, path, file_name, content):
        return parse_metadata_inteligente(path, file_name, content)

    def save_failure(self, record):
        payload = asdict(record) if is_dataclass(record) else record
        return salvar_falha_db(payload)

    def save_analysis(self, file_name, text, technician=None):
        return salvar_observacao(file_name, text, tecnico=technician)

    def read_analysis(self, file_name):
        return ler_observacao(file_name)
