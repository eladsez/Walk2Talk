import os.path
import sys
from pickle import loads, dumps
from socket import socket, AF_INET, SOCK_DGRAM, timeout, error
from Utilities import udp_packets


class CCServer:

    def __init__(self):
        self.sock = None
        self.client_addr = None
        self.filename = None
        self.RTT = None
        self.ack_seq = 0
        self.cwnd = 1024  # initial window size
        self.dup_ack_count = 0  # 3 top

    def connect(self, client_addr, filename: str):
        self.filename = filename
        try:
            self.client_addr = client_addr
            self.sock = socket(AF_INET, SOCK_DGRAM)
            self.sock.sendto(udp_packets.server_handshake('syn').encode(), self.client_addr)
            self.sock.settimeout(2)
            syn_ack, addr = self.sock.recvfrom(1024)
            if syn_ack.decode() == udp_packets.client_handshake() and addr == self.client_addr:
                self.sock.sendto(udp_packets.server_handshake('ack').encode(), self.client_addr)
            print('reliable udp connection established')
            return True
        except timeout as tio:
            print(tio)
            print('client didnt recv syn from the server (timeout)')
            return False
        except error as e:
            print(e)
            print('error occurred while opening server udp socket')
            return False

    def send_file(self):
        file = open(self.filename, 'rb')
        seq = dup_ack_count = 0
        while True:
            seq, pkt = udp_packets.file_to_pkt(file, seq, self.cwnd)
            self.sock.sendto(pkt, self.client_addr)
            ack, addr = self.sock.recvfrom(1024)
            if addr != self.client_addr: continue
            if ack == udp_packets.ack_from_client(seq):
                continue
            else:
                pass


if __name__ == '__main__':
    server = CCServer()
    server.connect(('127.0.0.1', 5550), './DSC02199.jpg')
    server.send_file()

