import threading
from collections import OrderedDict
from Utilities import udp_packets
from socket import socket, error


class SlidingWindow:

    def __init__(self, sock: socket, client_addr: tuple, datagrams: list):
        self.sock = sock
        self.client_addr = client_addr
        self.datagrams = datagrams
        self.curr_window = OrderedDict()  # ordered dict of frames represent by (seq:pkt)
        self.max_win_size = 4  # The initial window size is 4
        self.next_seq_to_send = 0  # stores the last seq of the pkt we send
        self.next_index = 0  # The index of the next frame to be added to the window from the datagrams list
        self.expected_ack = None  # The seq of the supposed ack that the server wait to recv
        self.acked = []
        self.lock = threading.Lock()
        self.init_win()

    def init_win(self):
        for i in range(0, self.max_win_size):
            self.curr_window[self.datagrams[i][0]] = self.datagrams[i][1]

        self.next_index = self.max_win_size
        self.expected_ack = self.datagrams[0][0]

    def send_window(self):
        for seq, pkt in self.curr_window.items():
            if seq > self.next_seq_to_send:
                self.sock.sendto(pkt, self.client_addr)
                self.next_seq_to_send = seq

    def handle_ack(self, ack):
        self.lock.acquire()
        seq_of_ack = udp_packets.seq_from_client_ack(ack)
        del self.curr_window[seq_of_ack]
        self.acked.append(seq_of_ack)
        self.curr_window[self.datagrams[self.next_index][0]] = self.datagrams[self.next_index][1]
        self.next_index += 1  # advance to the next index in the datagrams list
        print(f'received ack of seq: {seq_of_ack}')
        if seq_of_ack == self.expected_ack:
            self.send_window()  # send the new datagram that added to the window above and then return

        else:
            print('bla')
            self.retransmission(seq_of_ack)
        self.expected_ack = list(self.curr_window.keys())[0]  # getting the first seq in the window
        self.lock.release()

    def retransmission(self, skipped_ack):
        for seq, pkt in self.curr_window.items():
            if self.expected_ack <= seq < skipped_ack:
                try:
                    self.sock.sendto(pkt, self.client_addr)
                except error as e:
                    print(e)
            if seq >= skipped_ack:
                return





