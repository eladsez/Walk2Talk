import os
import threading
from socket import socket, AF_INET, SOCK_STREAM, error, SO_REUSEADDR, SOL_SOCKET

from Server.CC_server import CCServer
from Utilities import tcp_packets

MSG_TYPE = '1'
REQ_TYPE = '2'
LIST_TYPE = '3'
DOWNLOAD_REQ = '4'


class Server:

    def __init__(self, addr: tuple):
        self.addr = addr
        self.clients_addr = {}  # (name:addr)
        self.clients_sock = {}  # (socket:name)
        self.clients_threads = []
        self.cc_server = None
        self.on = True
        self.files = None  # list represent the files name
        self.file_path = os.path.abspath('./') + '/Server/files/'
        try:
            self.serverSock = socket(AF_INET, SOCK_STREAM)  # socket for Client to connect
            self.serverSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            self.serverSock.bind(self.addr)
        except error:
            print("ERROR with Server Socket creation or bind")
            exit(1)

    def listen_for_clients(self):
        self.serverSock.listen(5)
        print('Waitnig for clients to connect...')
        while self.on:
            client_sock = client_addr = None
            try:
                client_sock, client_addr = self.serverSock.accept()
            except error:
                pass
            print(f'{len(self.clients_sock) + 1} client connected: {client_addr[0]}')
            print(f'{client_addr} connected')
            thread = threading.Thread(target=self.handle_client, args=(client_sock, client_addr,))
            self.clients_threads.append(thread)
            thread.start()

    # Private Method
    def handle_client(self, client_sock, client_addr):
        client_name = client_sock.recv(1024).decode()
        try:  # valid check for the client name
            if client_name in list(self.clients_sock.values()):
                client_sock.send('-|NOT VALID|-'.encode())
                client_sock.close()
                return
            else:
                client_sock.send('-|VALID|-'.encode())
        except error:
            print(error)
            return

        self.clients_sock[client_sock] = client_name
        self.clients_addr[client_name] = client_addr
        print(f'***** {client_name} connected *****')
        connected_msg = tcp_packets.msg_packet('server', 'broadcast', f'***** {client_name} connected *****')
        self.broadcast(connected_msg, client_sock)
        while self.on:
            try:
                pkt = client_sock.recv(4096).decode()
            except error:
                continue
            if pkt != '|-exit-|':
                self.handle_tcp_pkt(pkt, client_sock)
            else:
                self.remove_client(client_sock)
                break

    def find_sock_by_name(self, name_to_find: str):
        for sock, name in self.clients_sock.items():
            if name == name_to_find:
                return sock

    def handle_tcp_pkt(self, pkt: str, client_sock: socket):
        layers = pkt.split('|')
        if layers[0] == REQ_TYPE:
            if layers[1] == 'names':
                pkt = tcp_packets.active_clients_packet(list(self.clients_addr.keys()))
                try:
                    client_sock.send(pkt.encode())
                except error as err:
                    raise err
            if layers[1] == 'files':
                # Update files during running application
                self.files = [file for file in os.listdir(self.file_path) if
                              os.path.isfile(os.path.join(self.file_path, file))]
                pkt = tcp_packets.server_files_packet(self.files)
                try:
                    client_sock.send(pkt.encode())
                except error as err:
                    raise err

        if layers[0] == MSG_TYPE:
            if layers[2] != 'broadcast':
                receiver_sock = self.find_sock_by_name(layers[2])
                try:
                    receiver_sock.send(pkt.encode())
                except error as err:
                    raise err
            else:
                self.broadcast(pkt, client_sock)

        if layers[0] == DOWNLOAD_REQ:
            if layers[1] == 'RESUME-DOWNLOAD':
                print('resume pressed!!')
                self.cc_server.pause = False
                threading.Thread(target=self.cc_server.send_file())

            elif layers[1] == 'PAUSE-DOWNLOAD':
                print('pause pressed!!')
                self.cc_server.pause = True
            else:
                print(
                    f'DOWNLOAD_REQ from client {self.clients_sock[client_sock]} at {self.clients_addr[self.clients_sock[client_sock]]}')
                threading.Thread(target=self.download_tcp, args=(layers[1], client_sock,)).start()
                # threading.Thread(target=self.download_rdt, args=(layers[1], client_sock,)).start()

    def broadcast(self, pkt, conn=None):
        copy_client_sock = self.clients_sock.copy()  # important to avoid iterable conflicts
        for client in copy_client_sock:
            if client == conn:
                continue
            try:
                client.send(pkt.encode())
            except error:
                self.remove_client(client)

    def remove_client(self, client_sock):
        if client_sock in self.clients_sock:
            disconnected_msg = tcp_packets.msg_packet('server', 'broadcast',
                                                      f'***** {self.clients_sock[client_sock]} disconnected *****')
            self.broadcast(disconnected_msg, client_sock)
            name = self.clients_sock[client_sock]
            del self.clients_sock[client_sock]
            del self.clients_addr[name]

    def download_rdt(self, file_name: str, client_sock: socket):
        # Getting the absolute path for the file to download
        file_path = self.file_path + file_name

        self.cc_server = CCServer()
        # extract the addr for the current client :
        client_name = self.clients_sock[client_sock]
        client_addr = self.clients_addr[client_name]
        connect = self.cc_server.connect((client_addr[0], 5550), file_path)
        while not connect:
            connect = self.cc_server.connect((client_addr[0], 5550), file_path)
        self.cc_server.send_file()

    # there is a problem with the tcp download implementation because its download and send message on the same socket
    # TODO: fix it
    def download_tcp(self, file_name: str, client_sock: socket):
        # Getting the absolute path for the file to download
        print(f'sending {file_name} to {self.clients_addr[self.clients_sock[client_sock]]}')
        file_path = self.file_path + file_name
        file = open(file_path, 'rb')
        data = file.read(60000)
        while data:
            client_sock.send(data)
            data = file.read(60000)
        client_sock.send("~*DONE*~".encode())
        file.close()
        print('Done sending to {self.clients_addr[self.clients_sock[client_sock]]}')

    def shout_down(self):
        try:
            self.serverSock.close()
            self.on = False
        except error:
            return False
        print('the server have been shout down')
        return True
