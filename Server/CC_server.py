import threading
import time
from socket import socket, AF_INET, SOCK_DGRAM, timeout, error

from Server.cwnd import SlidingWindow
from Utilities import udp_packets


class CCServer:

    def __init__(self):
        self.sock = None
        self.client_addr = None
        self.filepath = None
        self.cwnd = None
        self.pause = False  # for the pause button to stop the download
        self.RTT = None  # round trip time - > time it took to last pkt to be sent.

    def connect(self, client_addr, filepath: str):
        """
        This method connects to the client requesting the file in a three way handshake.
        it occurs over udp with RDT.
        :param client_addr:
        :param filepath:
        :return:
        """
        self.filepath = filepath
        self.client_addr = client_addr
        datagrams = self.file_to_datagrams()  # Separates the file size into datagrams in order to send the client how many datagrams.
        try:
            self.sock = socket(AF_INET, SOCK_DGRAM)  # UDP SOCK
            self.RTT = time.perf_counter()
            self.sock.sendto(udp_packets.server_handshake('syn', len(datagrams)).encode(),
                             self.client_addr)
            self.sock.settimeout(2)
            syn_ack, addr = self.sock.recvfrom(1024)
            self.RTT = time.perf_counter() - self.RTT
            if syn_ack.decode() == udp_packets.client_handshake() and addr == self.client_addr:
                self.sock.sendto(udp_packets.server_handshake('ack').encode(), self.client_addr)
                self.sock.settimeout(self.RTT+0.5)

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

    # Private Method
    def file_to_datagrams(self):  # TODO: take care of the extra size while reading
        """
        This method separates the file into list of datagrams for us to process and send to the client.
        :return:
        """
        file = open(self.filepath, 'rb')
        datagrams = []  # The datagrams list represent the pkts file ordered by seq
        tup = udp_packets.file_to_pkt(file, 0)  # tup is a tuple represent by (seq, pkt)
        while tup is not None:
            datagrams.append(tup)
            tup = udp_packets.file_to_pkt(file, tup[0])
        file.close()
        return datagrams

    def send_file(self):
        """
        Send file method while activating the ack listener method which listens to acks constantly.
        it is used to make sure the client receives the datagrams everytime, and to see if there was a missing packet.
        if was, it will be retransmission.
        :return:
        """
        self.cwnd.send_window()
        self.ack_listener()

    # Private Method
    def ack_listener(self):
        """
        Method used for listening for acks sent by the client for each packet received by him from the file datagrams.
        :return:
        """
        ack = ''.encode()
        while ack.decode() != udp_packets.ack_from_client(None, final=True).decode() and not self.cwnd.finished:
            if self.pause:
                break
            try:
                ack, addr = self.sock.recvfrom(1024)
                if addr != self.client_addr: continue
            except timeout:
                self.cwnd.lock.acquire()
                print('server didnt recv data ack from the client (timeout)')
                self.cwnd.timeout_occur()  # TODO: consider using thread on this method.
                self.cwnd.lock.release()
                continue
            if ack.decode() != udp_packets.ack_from_client(None, final=True).decode():
                threading.Thread(target=self.cwnd.handle_ack, args=(ack,), daemon=True).start()
        if not self.pause and self.cwnd.timeout_count < 4:
            self.sock.close()
            print('file send successfully!')

# if __name__ == '__main__':
#     server = CCServer()
#     server.connect(('127.0.0.1', 5550), './files/DSC02199.jpg')
#     server.send_file()
