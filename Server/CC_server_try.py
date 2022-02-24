import os.path
import threading
from socket import socket, AF_INET, SOCK_DGRAM, timeout, error
from Server.cwnd import SlidingWindow
from Utilities import udp_packets


class CCServer:

    def __init__(self):
        self.sock = None
        self.client_addr = None
        self.filename = None
        self.RTT = None
        self.cwnd = None
        self.dup_ack_count = 0  # 3 top

    def connect(self, client_addr, filename: str):
        self.filename = filename
        self.client_addr = client_addr
        try:
            self.sock = socket(AF_INET, SOCK_DGRAM)
            self.sock.sendto(udp_packets.server_handshake('syn').encode(), self.client_addr)
            self.sock.settimeout(2)
            syn_ack, addr = self.sock.recvfrom(1024)
            if syn_ack.decode() == udp_packets.client_handshake() and addr == self.client_addr:
                self.sock.sendto(udp_packets.server_handshake('ack').encode(), self.client_addr)

        except timeout as tio:
            print(tio)
            print('server didnt recv syn-ack from the client due timeout')
            return False
        except error as e:
            print(e)
            print('error occurred while opening server udp socket')
            return False

        print('reliable udp connection established')
        self.file_to_datagrams()
        return True

    def file_to_datagrams(self):  # TODO: take care of the extra size while reading
        file = open(self.filename, 'rb')
        seq = 0
        datagrams = []  # The datagrams list represent the pkts file ordered by seq
        while seq < os.path.getsize(self.filename):
            seq, pkt = udp_packets.file_to_pkt(file, seq)
            datagrams.append((seq, pkt))

        self.cwnd = SlidingWindow(self.sock, self.client_addr, datagrams)

    def send_file(self):
        self.cwnd.send_window()
        self.ack_listener()

    def ack_listener(self):
        ack = ''.encode()
        while ack.decode() != 'FINAL_ACK':  # TODO: replace with something nicer
            try:
                ack, addr = self.sock.recvfrom(1024)
                if addr != self.client_addr: continue
            except timeout:
                print('server didnt recv data ack from the client (timeout)')

            threading.Thread(target=self.cwnd.handle_ack, args=(ack,)).start()

    # def send_file(self):
    #     file = open(self.filename, 'rb')
    #     seq = dup_ack_count = 0
    #     while True:
    #         seq, pkt = udp_packets.file_to_pkt(file, seq)
    #         self.sock.sendto(pkt, self.client_addr)
    #         ack, addr = self.sock.recvfrom(1024)
    #         if addr != self.client_addr: continue
    #         if ack == udp_packets.ack_from_client(seq):
    #             continue
    #         else:
    #             pass


if __name__ == '__main__':
    server = CCServer()
    server.connect(('127.0.0.1', 5550), './DSC02199.jpg')
    server.send_file()
