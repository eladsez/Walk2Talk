import sys
from Server.server import Server

server = Server(('0.0.0.0', sys.argv[1]))
server.listen_for_clients()
