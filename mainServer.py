from Server.server import Server

server = Server(('0.0.0.0', 80))
server.listen_for_clients()
