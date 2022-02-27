import threading
from socket import socket, AF_INET, SOCK_DGRAM, timeout, error
from Server.cwnd import SlidingWindow
from Utilities import udp_packets


class CCServer:

    def __init__(self):
        self.sock = None
        self.client_addr = None
        self.filepath = None
        self.RTT = None
        self.cwnd = None
        self.dup_ack_count = 0  # 3 top

    def connect(self, client_addr, filepath: str):
        self.filepath = filepath
        self.client_addr = client_addr
        datagrams = self.file_to_datagrams()
        try:
            self.sock = socket(AF_INET, SOCK_DGRAM)
            self.sock.sendto(udp_packets.server_handshake('syn', len(datagrams)).encode(),
                             self.client_addr)
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
        self.cwnd = SlidingWindow(self.sock, self.client_addr, datagrams)
        print('reliable udp connection established')
        return True

    def file_to_datagrams(self):  # TODO: take care of the extra size while reading
        file = open(self.filepath, 'rb')
        datagrams = []  # The datagrams list represent the pkts file ordered by seq
        tup = udp_packets.file_to_pkt(file, 0)  # tup is a tuple represent by (seq, pkt)
        while tup is not None:
            datagrams.append(tup)
            tup = udp_packets.file_to_pkt(file, tup[0])
        file.close()
        return datagrams

    def send_file(self):
        self.cwnd.send_window()
        self.ack_listener()

    def ack_listener(self):
        ack = ''.encode()
        while ack.decode() != udp_packets.ack_from_client(None, final=True).decode():
            try:
                ack, addr = self.sock.recvfrom(1024)
                if addr != self.client_addr: continue
            except timeout:
                print('server didnt recv data ack from the client (timeout)')

            threading.Thread(target=self.cwnd.handle_ack, args=(ack,), daemon=True).start()

        self.sock.close()
        print('file send successfully!')


if __name__ == '__main__':
    server = CCServer()
    server.connect(('127.0.0.1', 5550), './files/DSC02199.jpg')
    server.send_file()
