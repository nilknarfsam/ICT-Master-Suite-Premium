from src.app_desktop import legacy_facade


def test_legacy_facade_expoe_funcoes_principais():
    funcoes_esperadas = [
        "carregar_config",
        "salvar_config",
        "conectar_banco",
        "init_db",
        "verificar_conexao_db",
        "bootstrap_database",
        "validar_login",
        "obter_usuario_por_login",
        "listar_usuarios",
        "cadastrar_usuario",
        "deletar_usuario",
        "atualizar_usuario",
        "detectar_tipo_log",
        "parse_metadata_inteligente",
        "salvar_falha_db",
        "salvar_observacao",
        "ler_observacao",
        "buscar_historico_serial",
        "obter_estatisticas_ict",
        "obter_ultimas_analises",
        "obter_estatisticas_progresso",
        "limpar_analises_db",
        "adicionar_modelo",
        "editar_modelo",
        "listar_modelos",
        "adicionar_solucao_wiki",
        "buscar_solucoes_wiki",
        "gerar_relatorio_excel",
        "sincronizar_fila_offline",
        "sincronizar_espelho_local",
        "init_db_local",
    ]

    for nome in funcoes_esperadas:
        assert hasattr(legacy_facade, nome), f"Funcao ausente na facade: {nome}"
