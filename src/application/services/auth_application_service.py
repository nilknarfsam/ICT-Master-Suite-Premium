from src.core.auth.auth_service import (
    atualizar_usuario,
    cadastrar_usuario,
    deletar_usuario,
    listar_usuarios,
    obter_usuario_por_login,
    validar_login,
)


class AuthApplicationService:
    """Serviço de aplicação para autenticação e gestão de usuários."""

    def login(self, login, password):
        return validar_login(login, password)

    def get_user_by_login(self, login):
        return obter_usuario_por_login(login)

    def list_users(self):
        return listar_usuarios()

    def create_user(self, nome, login, senha, is_admin):
        return cadastrar_usuario(nome, login, senha, is_admin)

    def delete_user(self, user_id):
        return deletar_usuario(user_id)

    def update_user(self, user_id, novo_nome, novo_login, nova_senha=None):
        return atualizar_usuario(user_id, novo_nome, novo_login, nova_senha)
