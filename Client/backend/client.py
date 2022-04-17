import socket
import threading
from Client.backend.CC_client import CClient
from Utilities import tcp_packets

MSG_TYPE = '1'
REQ_TYPE = '2'
LIST_TYPE = '3'


class Client:
    """
    This class handles all the client operation methods:
    from connecting to sending messages, downloading files, and disconnecting requests.
    """

    def __init__(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_name = None
        except socket.error as err:
            print("ERROR, failed to create Client socket")
            raise err
        self.c_client = None

    def connect(self, addr: tuple, client_name: str):
        """
        This method connects the client to the server over tcp.
        :param addr:
        :param client_name:
        :return:
        """
        if self.client_name is not None:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP connection
                self.client_name = None
            except socket.error as err:
                print("ERROR, failed to create Client socket")
                print(err)
        self.client_name = client_name
        try:
            self.sock.connect(addr)
            self.sock.send(client_name.encode())
            valid = self.sock.recv(1024).decode()
        except socket.error as err:
            print("ERROR, Client failed to connect the Server")
            raise err

        if valid != '-|VALID|-':  # check weather the client name is valid or not
            self.sock.close()
            return False
        return True

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
        """
        This method is used to handle the packets sent over tcp from the client/
        if its a msg type or a list type request.
        :param pkt:
        :return:
        """
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

    def request_download(self, file_name: str, file_path: str):
        """
        This method checks if the request is viable to download
        :param file_path:
        :param file_name: a name of file.
        :return:
        """
        try:
            self.sock.send(tcp_packets.download_request(file_name).encode())
        except socket.error as err:
            print(err)
            print('client failed to send file name to the server')

    def download_rdt(self, file_name: str, file_path):
        """
        A simple download file method
        file name is optional
        :return:
        """
        self.c_client = CClient(addr=('0.0.0.0', 5550))
        connect = False
        while not connect:
            connect = self.c_client.connect()
        self.c_client.recv_file(file_path)

    # there is a problem with the tcp download implementation because its download and send message on the same socket
    # TODO: fix it
    def download_tcp(self, file_path):
        file = open(file_path, 'wb')
        data = self.sock.recv(60000)
        print('download start!')
        while data != '~*DONE*~'.encode():
            print('download recv')
            file.write(data)
            data = self.sock.recv(60000)
        file.close()

    def pause_download(self):
        if self.sock:
            try:
                self.c_client.pause = True
                self.sock.send(tcp_packets.pause_pkt())
                self.c_client.sock.settimeout(None)
                print('download paused!!')
            except socket.error as e:
                print(e)
                print('error with Pause the download')

    def resume_download(self):
        if self.sock:
            try:
                self.c_client.pause = False
                self.sock.send(tcp_packets.resume_pkt())
                self.c_client.sock.settimeout(100)
                threading.Thread(target=self.c_client.recv_file()).start()
                print('download resume!!')
            except socket.error as e:
                print(e)
                print('error with resume the download')
