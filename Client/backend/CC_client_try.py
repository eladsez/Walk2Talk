import sys
from socket import socket, AF_INET, SOCK_DGRAM, timeout, error
from Utilities import udp_packets


class CClient:

    def __init__(self, addr: tuple):
        self.client_addr = addr  # client_addr to bind
        self.server_addr = None
        self.sock = None
        self.file_name = None
        self.file_size = None  # here the file size is actually the length of datagrams list

    def connect(self, file_name):
        """
        This method connects the client to the server in a three way handshake method.
        :param file_name: the chosen file the client chose
        :return: True / False if the connection was established
        """
        self.file_name = file_name
        try:
            self.sock = socket(AF_INET, SOCK_DGRAM)  # UDP
            self.sock.bind(self.client_addr)
            # self.sock.settimeout(1)
            print('blabla')
            syn, addr = self.sock.recvfrom(1024)
            self.file_size = int(syn.decode().split('-')[-1])
            if syn.decode() == udp_packets.server_handshake('syn', self.file_size):  # First syn
                self.server_addr = addr
                self.sock.sendto(udp_packets.client_handshake().encode(), addr)
            ack, addr = self.sock.recvfrom(1024)
            if ack.decode() == udp_packets.server_handshake('ack') and addr == self.server_addr:
                print('reliable udp connection established')
                return True

        except timeout as tio:
            print(tio)
            print('client didnt recv syn from the server')
            return False
        except error as e:
            print(e)
            print('error occurred while opening or binding client udp socket')
            return False

    def recv_file(self, file_path):
        """
        This method receives the file over the udp socket and appending the datagrams of the file into a list.
        this way we could monitor when the file was done with the download.
        :param file_path: file path location.
        :return:
        """
        buff = 8192  # this is the max size we allow the client to receive
        last_seq = 0
        pkts = []  # list of tuples (seq, pkt)
        # while last_seq <= self.file_size:
        while len(pkts) != self.file_size:
            try:
                pkt, addr = self.sock.recvfrom(buff)
                if addr != self.server_addr: continue

                seq, data = udp_packets.pkt_to_file(pkt)
                print('client receiving pkt seq:' + str(seq))
                data_size = sys.getsizeof(data)
                if seq == last_seq + data_size:
                    pkts.append((seq, data))
                    last_seq = seq
                    self.sock.sendto(udp_packets.ack_from_client(last_seq), self.server_addr)

            except InterruptedError as e:
                print(e)
                print('error occurred while receiving from the server')
                return False

        if last_seq >= self.file_size:
            self.sock.sendto(udp_packets.ack_from_client(None, final=True), self.server_addr)
            self.sock.close()
            self.write_file(pkts, file_path)
            print('file downloaded!')

    def write_file(self, pkts: list, file_path):
        """
        This method writes the file to the location the client chose,
        while combining the datagrams that was transferred after sorting them.
        :param pkts: the entire datagrams
        :param file_path: file path location that the client chose.
        :return:
        """
        pkts.sort(key=lambda pkt: pkt[0])
        try:
            file = open(file_path, 'wb')
            for pkt in pkts:
                file.write(pkt[1])
            file.close()
        except IOError as e:
            print(e)
            print('error occurred while writing to the file')
            return False


if __name__ == '__main__':
    client = CClient(('0.0.0.0', 5550))
    client.connect('DSC02199.jpg')
    client.recv_file("./DSC02199.jpg")
