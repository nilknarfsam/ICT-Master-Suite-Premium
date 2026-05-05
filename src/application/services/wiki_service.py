from src.core.wiki.wiki_repository import (
    adicionar_modelo,
    adicionar_solucao_wiki,
    buscar_solucoes_wiki,
    editar_modelo,
    listar_modelos,
)


class WikiService:
    """Serviço de aplicação para operações de base de conhecimento."""

    def list_models(self):
        return listar_modelos()

    def add_model(self, model_name):
        return adicionar_modelo(model_name)

    def edit_model(self, model_id, new_name):
        return editar_modelo(model_id, new_name)

    def search_solutions(self, model_id, phase=None, query_text=None):
        return buscar_solucoes_wiki(model_id, phase, query_text)

    def add_solution(self, model_id, phase, symptom, solution, technician_id):
        return adicionar_solucao_wiki(model_id, phase, symptom, solution, technician_id)
