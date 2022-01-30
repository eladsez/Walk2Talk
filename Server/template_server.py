import threading
import socket
from concurrent.futures import ThreadPoolExecutor

from Utilities import packets_over_tcp

MSG_TYPE = '1'
REQ_TYPE = '2'
LIST_TYPE = '3'
NAME_TYPE = '4'


class Server:

    def __init__(self, addr: tuple):
        self.addr = addr
        self.clients_addr = {}  # (name:addr)
        self.clients_sock = {}  # (socket:name)
        self.clients_threads = []
        try:
            self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket for Client to connect
            self.serverSock.bind(self.addr)
        except socket.error:
            print("ERROR with Server Socket creation or bind")

    def listen_for_clients(self):
        self.serverSock.listen(5)
        print('Waitnig for clients to connect...')
        while True:
            client_sock, client_addr = self.serverSock.accept()
            print(f'{len(self.clients_sock) + 1} client connected: {client_addr[0]}')
            print(f'{client_addr} connected')
            thread = threading.Thread(target=self.handle_client, args=(client_sock, client_addr,))
            self.clients_threads.append(thread)
            thread.start()

        server.close()

    def handle_client(self, client_sock, client_addr):
        client_name = client_sock.recv(4096).decode()
        self.clients_sock[client_sock] = client_name
        self.clients_addr[client_name] = client_addr
        print(f'***** {client_name} connected *****')
        connected_msg = packets_over_tcp.msg_packet('server', 'broadcast', f'***** {client_name} connected *****')
        self.broadcast(connected_msg, client_sock)
        while True:
            try:
                pkt = client_sock.recv(4096).decode()
            except socket.error:
                continue
            if pkt != '|-exit-|':
                self.handle_pkt(pkt, client_sock)
            else:
                client_sock.send('|-bye-|'.encode())
                self.remove_client(client_sock)
                break

    def handle_pkt(self, pkt: str, client_sock):
        layers = pkt.split('|')
        if layers[0] == REQ_TYPE:
            pass
        elif layers[0] == MSG_TYPE:
            if layers[2] != 'broadcast':
                receiver_sock = socket.socket(
                    list(self.clients_sock.keys())[list(self.clients_sock.values()).index(layers[2])])
                try:
                    receiver_sock.send(pkt.encode())
                except socket.error as err:
                    raise err
            else:
                self.broadcast(pkt, client_sock)

    def broadcast(self, pkt, conn=None):
        for client in self.clients_sock:
            if client == conn:
                continue
            try:
                client.send(pkt.encode())
            except socket.error:
                self.removeClient(client)

    def remove_client(self, client_sock):
        if client_sock in self.clients_sock:
            self.broadcast(f'***** {self.clients_sock[client_sock]} disconnected *****', client_sock)
            name = self.clients_sock[client_sock]
            del self.clients_sock[client_sock]
            del self.clients_addr[name]


if __name__ == '__main__':
    server = Server(('', 12345))
    server.listen_for_clients()
