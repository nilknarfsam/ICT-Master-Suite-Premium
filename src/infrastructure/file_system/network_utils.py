import socket


def servidor_online(caminho, timeout=1):
    """Verifica rapidamente via socket se o IP está acessível para evitar travamentos do Windows."""
    if not caminho.startswith("//") and not caminho.startswith("\\\\"):
        return True

    partes = caminho.replace("\\\\", "/").split("/")
    if len(partes) > 2:
        ip_host = partes[2]
        try:
            with socket.create_connection((ip_host, 445), timeout=timeout):
                return True
        except OSError:
            return False
    return True
