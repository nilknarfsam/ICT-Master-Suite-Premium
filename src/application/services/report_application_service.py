from src.core.reports.report_service import gerar_relatorio_excel


class ReportApplicationService:
    """Serviço de aplicação para geração de relatórios."""

    def gerar_relatorio_excel(self, caminho_destino):
        return gerar_relatorio_excel(caminho_destino)

    def generate_excel_report(self, destination_path):
        return self.gerar_relatorio_excel(destination_path)
