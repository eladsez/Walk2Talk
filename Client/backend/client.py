import socket
import sys

from Server.CC_server_try import CCServer
from Client.backend.CC_client_try import CClient
from Utilities import tcp_packets

MSG_TYPE = '1'
REQ_TYPE = '2'
LIST_TYPE = '3'


class Client:

    def __init__(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_name = None
        except socket.error as err:
            print("ERROR, failed to create Client socket")
            raise err

    def connect(self, addr: tuple, client_name: str):
        if self.client_name is not None:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_name = None
            except socket.error as err:
                print("ERROR, failed to create Client socket")
                raise err
        self.client_name = client_name
        try:
            self.sock.connect(addr)
            self.sock.send(client_name.encode())
        except socket.error as err:
            print("ERROR, Client failed to connect the Server")
            raise err

    def disconnect(self):
        """
        This method disconnects the Client from the Server
        :return:
        """
        self.sock.send('|-exit-|'.encode())
        self.sock.close()

    def receive(self):
        try:
            pkt = self.sock.recv(1024).decode()
            screen_view = self.handle_pkt(pkt)
            if pkt == '|-bye-|':
                return None
            return screen_view
        except socket.error:
            print('ERROR Client failed in receive')

    def handle_pkt(self, pkt: str):
        layers = pkt.split('|')
        if layers[0] == MSG_TYPE:
            return '\n' + layers[1] + ': ' + layers[3], 'chat_box'
        if layers[0] == LIST_TYPE:
            return tcp_packets.display_list(layers[2].split(',')), layers[1] + '_box'

    def send_msg(self, msg, receiver_name='broadcast'):
        """
        This method sends the pkt message
        :param msg:
        :param receiver_name:
        :return:
        """
        msg = tcp_packets.msg_packet(self.client_name, receiver_name, msg)
        try:
            self.sock.send(msg.encode())
        except socket.error:
            print('ERROR Client failed trying to send')

    def send_names_req(self):
        """
        This method returns all the Client names in the chat
        :return:
        """
        try:
            self.sock.send(tcp_packets.get_active_clients_packet().encode())
        except socket.error as err:
            raise err

    def send_files_req(self):
        """
        This method returns all the file names in the Server.
        :return:
        """
        try:
            self.sock.send(tcp_packets.get_server_files_packet().encode())
        except socket.error as err:
            raise err

    def request_download(self, file_name: str):
        """
        This method checks if the request is viable to download
        :param file_name: a name of file.
        :return:
        """
        try:
            self.sock.send(tcp_packets.download_request(file_name).encode())
        except socket.error as err:
            print('client failed to send file name to the server')

        self.download(file_name)

    def download(self, file_name: str):
        """
        A simple download file method
        :return:
        """
        c_client = CClient(addr=('127.0.0.1', 5550))
        c_client.connect((file_name, sys.getsizeof(file_name)))
        c_client.recv_file()


if __name__ == '__main__':
    client = Client()
    client.connect(('127.0.0.1', 12345))
