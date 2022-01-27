import socket


class sockets():

    def __init__(self, addr: tuple):
        self.addr = addr
        self.send_sock = None  # TCP
        self.download_sock = None  # our UDP
        self.recv_sock = None  # TCP

    # def sock_load(self, socket: socket.socket):
    #     """
    #     This method loads a socket.
    #     :param socket: gets a socket
    #     :return:
    #     """
