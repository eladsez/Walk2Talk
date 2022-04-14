import socket

from Client.frontend.client_gui import Room
IP = socket.gethostbyname('walk2talk.herokuapp.com')
print(IP)
Room((IP, 80))
