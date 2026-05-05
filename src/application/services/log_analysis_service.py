from dataclasses import asdict, is_dataclass

from src.core.failures.failure_repository import (
    buscar_historico_serial,
    limpar_analises_db,
    ler_observacao,
    obter_estatisticas_ict,
    obter_estatisticas_progresso,
    obter_ultimas_analises,
    salvar_falha_db,
    salvar_observacao,
)
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

    def get_serial_history(self, serial):
        return buscar_historico_serial(serial)

    def get_ict_statistics(self):
        return obter_estatisticas_ict()

    def get_latest_analyses(self, limite=10):
        return obter_ultimas_analises(limite)

    def get_progress_statistics(self):
        return obter_estatisticas_progresso()

    def clear_analyses(self):
        return limpar_analises_db()
