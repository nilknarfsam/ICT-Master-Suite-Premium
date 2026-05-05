from src.core.reports.report_service import gerar_relatorio_excel


class ReportApplicationService:
    """Serviço de aplicação para geração de relatórios."""

    def generate_excel_report(self, destination_path):
        return gerar_relatorio_excel(destination_path)
