from dataclasses import dataclass
from typing import Optional


@dataclass
class LogSearchResult:
    file_name: str
    file_path: str
    timestamp: Optional[float] = None


@dataclass
class LogMetadata:
    tipo: str
    data: str
    serial: str
    modelo: str
    status: str
    cor: str


@dataclass
class FailureRecordInput:
    id: str
    data_registro: str
    data_falha: str
    arquivo: str
    serial: str
    modelo: str
    componente: str
    step: str
    status_tratativa: str = "ABERTO"


@dataclass
class AnalysisNoteInput:
    file_name: str
    text: str
    technician: Optional[str] = None
