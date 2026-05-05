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

    def validar_login(self, login, senha):
        return validar_login(login, senha)

    def obter_usuario_por_login(self, login):
        return obter_usuario_por_login(login)

    def listar_usuarios(self):
        return listar_usuarios()

    def cadastrar_usuario(self, nome, login, senha, is_admin):
        return cadastrar_usuario(nome, login, senha, is_admin)

    def deletar_usuario(self, id_usuario):
        return deletar_usuario(id_usuario)

    def atualizar_usuario(self, id_usuario, novo_nome, novo_login, nova_senha=None):
        return atualizar_usuario(id_usuario, novo_nome, novo_login, nova_senha)

    def login(self, login, password):
        return self.validar_login(login, password)

    def get_user_by_login(self, login):
        return self.obter_usuario_por_login(login)

    def list_users(self):
        return self.listar_usuarios()

    def create_user(self, nome, login, senha, is_admin):
        return self.cadastrar_usuario(nome, login, senha, is_admin)

    def delete_user(self, user_id):
        return self.deletar_usuario(user_id)

    def update_user(self, user_id, novo_nome, novo_login, nova_senha=None):
        return self.atualizar_usuario(user_id, novo_nome, novo_login, nova_senha)
