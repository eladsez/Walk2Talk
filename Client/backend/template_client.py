import socket
import threading

MSG_TYPE = '1'
REQ_TYPE = '2'
LIST_TYPE = '3'


class Client:

    def __init__(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print("ERROR, failed to create Client socket")
            raise err

    def connect(self, addr: tuple):
        try:
            self.sock.connect(addr)
        except socket.error as err:
            print("ERROR, Client failed to connect the Server")
            raise err

    def disconnect(self):
        """
        This method disconnects the Client from the Server
        :return:
        """
        self.sock.close()

    def receive(self):
        while True:
            try:
                pkt = self.sock.recv(4096).decode()
                print(pkt)
                # self.handle_pkt(pkt)
                if pkt == '|-bye-|':
                    break
            except socket.error:
                print('ERROR Client failed in receive')
                break

    def handle_pkt(self, pkt: str):

        layers = pkt.split('|')
        # match layers[0]:
        #     case MSG_TYPE:
        #         pass
        #     case LIST_TYPE:
        #         pass
        #     case REQ_TYPE:
        #         pass

    def send(self, msg):
        try:
            self.sock.send(msg.encode())
        except socket.error:
            print('ERROR Client failed trying to send')


    def recv_names(self) -> list:
        """
        This method returns all the Client names in the chat
        :return:
        """
        pass

    def recv_files(self) -> list:
        """
        This method returns all the file names in the Server.
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


if __name__ == '__main__':
    client = Client()
    client.connect(('127.0.0.1', 12345))
