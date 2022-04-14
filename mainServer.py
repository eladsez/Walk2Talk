import sys
from Server.server import Server
PORT = int(sys.argv[1])
print('The port is: ' + str(PORT))
server = Server(('0.0.0.0', PORT))
server.listen_for_clients()
