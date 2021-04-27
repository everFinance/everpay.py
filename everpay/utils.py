def get_url(server, path):
    if server.endswith('/'):
        return server[:-1] + path
    return server + path