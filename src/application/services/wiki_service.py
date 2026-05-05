from src.core.wiki.wiki_repository import (
    adicionar_modelo,
    adicionar_solucao_wiki,
    buscar_solucoes_wiki,
    editar_modelo,
    listar_modelos,
)


class WikiService:
    """Serviço de aplicação para operações de base de conhecimento."""

    def listar_modelos(self):
        return listar_modelos()

    def adicionar_modelo(self, nome_modelo):
        return adicionar_modelo(nome_modelo)

    def editar_modelo(self, id_modelo, novo_nome):
        return editar_modelo(id_modelo, novo_nome)

    def buscar_solucoes(self, modelo_id, fase=None, busca_texto=None):
        return buscar_solucoes_wiki(modelo_id, fase, busca_texto)

    def adicionar_solucao(self, modelo_id, fase, sintoma, solucao, tecnico_id):
        return adicionar_solucao_wiki(modelo_id, fase, sintoma, solucao, tecnico_id)

    def list_models(self):
        return self.listar_modelos()

    def add_model(self, model_name):
        return self.adicionar_modelo(model_name)

    def edit_model(self, model_id, new_name):
        return self.editar_modelo(model_id, new_name)

    def search_solutions(self, model_id, phase=None, query_text=None):
        return self.buscar_solucoes(model_id, phase, query_text)

    def add_solution(self, model_id, phase, symptom, solution, technician_id):
        return self.adicionar_solucao(model_id, phase, symptom, solution, technician_id)
