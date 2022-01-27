from abc import ABC

"""
import socket
import threading


class Client:
    def _init_(self):
        try:
            self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print('ERROR in socket creation')
        self.listen_thread = None
        self.send_thread = None

    def listen(self):
        while True:
            massage = self.recv_sock.recv(1024).decode('ascii')
            print(f"from server: {massage}")
            if massage == 'bye':
                break

    def send(self):
        while True:
            message = input("Enter a massage:")
            # message sent to server
            self.send_sock.send(message.encode('ascii'))
            if message == "exit":
                break
        # close the connection
        self.send_sock.close()

    def connect(self, addr: tuple):
        self.sock.connect(addr)
        self.listen_thread = threading.Thread(target=self.listen())
        self.send_thread= threading.Thread(target=self.send())
        self.send_thread.start()
        self.recv_thread.start()


if _name_ == '_main_':
    client = Client()
    client.connect()
"""


class Client(ABC):

    def connect(self):
        """
        This method connects the client to the server, aka listener.
        :return:
        """
        pass

    def disconnect(self):
        """
        This method disconnects the client from the server
        :return:
        """
        pass

    def send(self):
        """
        This method sends a single message to a required person.
        :return:
        """
        pass

    def send_all(self):
        """
        This method sends a single message to everyone in the room ( broadcast )
        :return:
        """
        pass

    def recv_names(self) -> list:
        """
        This method returns all the client names in the chat
        :return:
        """
        pass

    def recv_files(self) -> list:
        """
        This method returns all the file names in the server.
        :return:
        """
        pass

    def request_download(self, file_name: str) -> bool:
        """
        This method checks if the request is viable to download
        :param file_name: a name of file.
        :return:
        """
        pass

    def download(self) -> object:
        """
        A simple download file method
        :return:
        """
        pass
