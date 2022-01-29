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
        self.recv_thread = None
        self.send_thread = None

    def connect(self, addr: tuple):
        try:
            self.sock.connect(addr)
        except socket.error as err:
            print("ERROR, Client failed to connect the Server")
            raise err
        self.recv_thread = threading.Thread(target=self.receive)
        self.send_thread = threading.Thread(target=self.send)
        self.recv_thread.start()
        self.send_thread.start()
        self.recv_thread.join()
        self.send_thread.join()
        self.sock.close()

    def disconnect(self):
        """
        This method disconnects the Client from the Server
        :return:
        """
        pass

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
        match layers[0]:
            case MSG_TYPE:
                pass
            case LIST_TYPE:
                pass
            case REQ_TYPE:
                pass

    def send(self):
        while True:
            try:
                msg = input("YOU:")
                self.sock.send(msg.encode())
                if msg == 'exit':
                    break
            except socket.error:
                print('ERROR Client failed trying to send')
                break

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
