from abc import ABC
import socket
from concurrent.futures import ThreadPoolExecutor

"""
import socket
from threading import Thread


class Server:
    def _init_(self, addr: tuple):
        self.addr = addr
        self.clients = {}  # ((address,port):socket)
        self.clients_threads = []
        try:
            self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket for client to connect
            self.serverSock.bind(self.addr)
        except socket.error as err:
            print("ERROR with server Socket creation or bind")

    def broadcast(self, client_addr, massage):
        for addr, sock in self.clients.values():
            if addr == client_addr:
                continue
            sock.send(massage)

    def handle_client(self, client_addr):
        while True:
            client_sock = self.clients[client_addr]
            # data received from client
            data = client_sock.recv(1024)
            if not data:
                print('Bye')
                # lock released on exit
                break
            self.broadcast(client_addr, data)

        self.clients.pop(client_addr)
        # connection closed
        client_sock.close()

    def listen_for_clients(self):

        self.serverSock.listen(5)
        print("socket is listening")
        # a forever loop until client wants to exit
        while True:
            # establish connection with client
            client_sock, client_addr = self.serverSock.accept()
            # adding client Details
            self.clients[client_addr] = client_sock
            print('Connected to :', client_addr[0], ':', client_addr[1])
            # Start a new thread to handle the client
            client_thread = Thread(target=self.handle_client, args=(client_addr,))
            # adding client thread
            self.clients_threads.append(client_thread)
            client_thread.start()


server = Server(("", 12345))
server.listen_for_clients()
"""


class Server(ABC):

    def __init__(self, addr: tuple):
        self.client_names = {}  # (name:(address,port))
        self.addr = addr
        self.clients = {}  # ((address,port):client_sockets)
        self.clients_threads = ThreadPoolExecutor(10)  # thread pool
        try:
            self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket for client to connect
            self.serverSock.bind(self.addr)
        except socket.error as err:
            print("ERROR with server Socket creation or bind")

    def socket_check(self, client_addr, client_socket):
        """
        This method checks the client_sockets for a certain socket:
        1. if the object does not exist create a new one for the client.
        2. check the socket type with the client and init it.
        :return:
        """
        pass

    def listen_for_clients(self, client_addr):
        """
        This method handles a client request to join the server:
        1. creates a thread to execute method socket_check.
        2.
        :return:
        """
        pass

    def broadcast(self, client_addr, msg: str):
        """
        This method gets a client_addr and sends the message to everyone in the chat room.
        :param client_addr:
        :return:
        """
        pass
