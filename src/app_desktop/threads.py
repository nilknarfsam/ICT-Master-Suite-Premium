import os
import shutil
import time
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal

from src.application.services.log_analysis_service import LogAnalysisService
from src.application.services.log_index_application_service import LogIndexApplicationService
from src.application.services.log_search_service import LogSearchService

def _wait_file_stable(path, retries=6, delay=0.35):
    """Aguarda o tamanho de um arquivo se estabilizar."""
    for _ in range(retries):
        try:
            size1 = os.path.getsize(path)
            time.sleep(delay)
            size2 = os.path.getsize(path)
            if size1 == size2:
                return True
        except OSError:
            time.sleep(delay)
    return False

def _safe_copy(src, dst):
    """Copia um arquivo de forma segura, criando o diretório de destino se necessário."""
    try:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        return True
    except (IOError, OSError):
        return False

class BuscaThread(QThread):
    """Thread para buscar arquivos otimizada para rede (scandir)."""
    lista_arquivos = pyqtSignal(list)
    search_summary = pyqtSignal(dict)
    status_msg = pyqtSignal(str)

    def __init__(self, termo, diretorios):
        super().__init__()
        self.termo = termo.lower()
        self.diretorios = diretorios
        self.rodando = True
        self.log_search_service = LogSearchService()
        self.search_options = self.log_search_service.build_default_options()
        self.was_limited = False

    def _scandir_recursivo(self, caminho):
        """Percorre todas as subpastas dinamicamente, sem depender de nomes específicos, usando scandir para performance máxima."""
        if not self.rodando: return []
        resultados = []
        
        try:
            # scandir iterador para baixo consumo de memória
            with os.scandir(caminho) as it:
                for entry in it:
                    if not self.rodando: break
                    
                    try:
                        if entry.is_dir(follow_symlinks=False):
                            # Recursão para TODAS as subpastas agnosticamente
                            resultados.extend(self._scandir_recursivo(entry.path))
                        
                        elif entry.is_file(follow_symlinks=False):
                            if self.log_search_service.should_include_file(entry.name, self.termo, self.search_options):
                                # Aprovação Universal (FAIL): Se chegou aqui, é candidato de falha
                                ts = entry.stat().st_mtime
                                resultados.append((ts, entry.name, entry.path))
                                
                    except (PermissionError, OSError):
                        continue # Pula arquivos ou pastas sem acesso
        except (PermissionError, OSError):
            pass # Pula o diretório pai atual caso não possua acesso
            
        return resultados

    def run(self):
        self.status_msg.emit("Iniciando varredura (Filtro: Apenas Falhas)...")
        encontrados = []
        resultados_index = None

        try:
            resultados_index = self.log_search_service.search_with_index(
                self.termo,
                self.search_options,
            )
        except Exception:
            resultados_index = None

        if self.rodando and resultados_index is not None:
            resultados_convertidos = []
            for item in resultados_index:
                if not item or len(item) < 2:
                    continue
                resultados_convertidos.append((item[0], item[1]))

            total_original = len(resultados_convertidos)
            total_limitado = len(resultados_convertidos)
            self.was_limited = False
            self.lista_arquivos.emit(resultados_convertidos)
            self.search_summary.emit(
                {
                    "total_original": total_original,
                    "total_exibido": total_limitado,
                    "limitado": self.was_limited,
                    "max_results": self.search_options.max_results,
                    "source": "index",
                }
            )
            return
        
        for diretorio in self.diretorios:
            if not self.rodando: break
            if os.path.exists(diretorio):
                self.status_msg.emit(f"Varrendo: {diretorio}")
                encontrados.extend(self._scandir_recursivo(diretorio))
        
        if self.rodando:
            # Ordena por data (mais recente primeiro)
            encontrados.sort(key=lambda x: x[0], reverse=True)
            total_original = len(encontrados)
            encontrados = self.log_search_service.limit_results(encontrados, self.search_options)
            total_limitado = len(encontrados)
            self.was_limited = self.log_search_service.was_limited(total_original, total_limitado)
            # Retorna lista de tuplas (nome, caminho) para a UI
            self.lista_arquivos.emit([(x[1], x[2]) for x in encontrados])
            self.search_summary.emit(
                {
                    "total_original": total_original,
                    "total_exibido": total_limitado,
                    "limitado": self.was_limited,
                    "max_results": self.search_options.max_results,
                    "source": "scanner",
                }
            )

    def parar(self):
        self.rodando = False


class FileLoaderThread(QThread):
    """Thread para carregar o conteúdo de um arquivo sem travar a UI."""
    file_loaded = pyqtSignal(dict, str)
    file_load_error = pyqtSignal(str)

    def __init__(self, caminho, nome, backup_dir, parent=None):
        super().__init__(parent)
        self.caminho = caminho
        self.nome = nome
        self.backup_dir = backup_dir
        self.log_analysis_service = LogAnalysisService()

    def run(self):
        try:
            self._backup_opened_file()
            # Blindagem de encodings e permissões: utf-8 com perdas controladas (ignore)
            with open(self.caminho, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            meta = self.log_analysis_service.parse_log_metadata(
                self.caminho,
                self.nome,
                content
            )
            self.file_loaded.emit(meta, content)
        except PermissionError:
            self.file_load_error.emit("Acesso negado: O arquivo está sendo gravado pelo verificador (Agilent/TRI) ou bloqueado pelo Windows.")
        except Exception as e:
            self.file_load_error.emit(f"Erro ao carregar o arquivo: {str(e)}")

    def _backup_opened_file(self):
        if not self.caminho or not os.path.exists(self.caminho): return
        
        dt = datetime.now()
        nome_arquivo = os.path.basename(self.caminho)
        dst_dir = os.path.join(self.backup_dir, "abertos", dt.strftime("%Y-%m-%d"))
        dst = os.path.join(dst_dir, nome_arquivo)
        
        if os.path.exists(dst) and os.path.getsize(dst) == os.path.getsize(self.caminho): return
        
        if not _wait_file_stable(self.caminho): return
        
        _safe_copy(self.caminho, dst)

class DashboardThread(QThread):
    """Thread para buscar as estatísticas do dashboard sem travar a UI."""
    stats_updated = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.log_analysis_service = LogAnalysisService()

    def run(self):
        stats = self.log_analysis_service.get_ict_statistics()
        self.stats_updated.emit(stats)


class ReindexThread(QThread):
    progress_msg = pyqtSignal(str)
    finished_summary = pyqtSignal(dict)
    failed = pyqtSignal(str)

    def __init__(self, base_paths, rebuild=True, allowed_extensions=None, parent=None):
        super().__init__(parent)
        self.base_paths = base_paths or []
        self.rebuild = rebuild
        self.allowed_extensions = allowed_extensions
        self.log_index_service = LogIndexApplicationService()

    def run(self):
        try:
            self.progress_msg.emit("Iniciando reindexação...")
            paths = [p for p in self.base_paths if p]

            if self.rebuild:
                for path in paths:
                    self.progress_msg.emit(f"Processando: {path}")
                summary = self.log_index_service.rebuild_index(
                    paths,
                    allowed_extensions=self.allowed_extensions,
                )
            else:
                total_indexed = 0
                total_errors = 0
                for path in paths:
                    self.progress_msg.emit(f"Processando: {path}")
                    result = self.log_index_service.build_incremental_index(
                        path,
                        allowed_extensions=self.allowed_extensions,
                    )
                    total_indexed += result.get("indexed", 0)
                    total_errors += result.get("errors", 0)
                summary = {
                    "paths": paths,
                    "total_indexed": total_indexed,
                    "total_errors": total_errors,
                }

            self.progress_msg.emit("Reindexação concluída.")
            self.finished_summary.emit(summary)
        except Exception as e:
            self.failed.emit(str(e))