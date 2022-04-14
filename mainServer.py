import sys
from Server.server import Server
import os

externalIP = os.popen('curl -s ifconfig.me').readline()
PORT = int(sys.argv[1])
print('The port is: ' + str(PORT) + '\nThe ip to connect is: ' + externalIP)

server = Server(('0.0.0.0', PORT))
server.listen_for_clients()
