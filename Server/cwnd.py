import threading
from collections import OrderedDict
from Utilities import udp_packets
from socket import socket, error


class SlidingWindow:

    def __init__(self, sock: socket, client_addr: tuple, datagrams: list):
        self.sock = sock
        self.client_addr = client_addr
        self.datagrams = datagrams
        self.datagrams.sort(key=lambda pkt: pkt[0])
        self.curr_window = OrderedDict()  # ordered dict of frames represent by (seq:pkt)
        self.max_win_size = 4  # The initial window size is 4
        self.next_seq_to_send = 0  # stores the last seq of the pkt we send
        self.next_index = 0  # The index of the next frame to be added to the window from the datagrams list
        self.expected_ack = None  # The seq of the supposed ack that the server wait to recv
        self.acked = []
        self.lock = threading.Lock()
        self.dup_ack = 0  # top 3
        self.init_win()

    def init_win(self):
        max_win = min(self.max_win_size, len(self.datagrams))
        for i in range(0, max_win):
            self.curr_window[self.datagrams[i][0]] = self.datagrams[i][1]

        self.next_index = self.max_win_size
        self.expected_ack = self.datagrams[0][0]

    def send_window(self):
        for seq, pkt in self.curr_window.items():
            if seq > self.next_seq_to_send:
                print(f'server sending pkt seq: {seq}')
                self.sock.sendto(pkt, self.client_addr)
                self.next_seq_to_send = seq

    def handle_ack(self, ack):
        self.lock.acquire()

        if self.next_index >= len(self.datagrams):
            self.lock.release()
            return

        seq_of_ack = udp_packets.seq_from_client_ack(ack)

        if seq_of_ack in list(self.curr_window.keys()):
            del self.curr_window[seq_of_ack]
            self.curr_window[self.datagrams[self.next_index][0]] = self.datagrams[self.next_index][1]

        elif seq_of_ack in self.acked:
            self.lock.release()
            return

        self.acked.append(seq_of_ack)
        self.next_index += 1  # advance to the next index in the datagrams list
        if seq_of_ack == self.expected_ack:
            print(f'---------received ack of seq: {seq_of_ack} - moving the window!------------')
            self.send_window()  # send the new datagram that added to the window above and then return

        else:
            print(f'expected ack was {self.expected_ack} but received {seq_of_ack}')
            self.retransmission(seq_of_ack)

        self.expected_ack = list(self.curr_window.keys())[0]  # getting the first seq in the window
        print(f'expected ack = {self.expected_ack}')
        self.lock.release()

    def retransmission(self, skipped_ack):
        for seq, pkt in self.curr_window.items():
            if self.expected_ack <= seq < skipped_ack and seq not in self.acked:
                try:
                    print(f'server retransmission pkt seq: {seq}')
                    self.sock.sendto(pkt, self.client_addr)
                except error as e:
                    print(e)
            if seq >= skipped_ack:
                return

    def calc_win_size(self):
        """
        This method calcualtes the right window size we want to set.
        if the network connection is fluid, then we will increase the window size by TODO: TBD
        it considers : RTT, dup acks and if timeout were to occur.
        RTT - round trip time - since packet was sent to the moment ack response was received.
        dup acs - we monitor up to 3 duplicate acks and then cut the window size by half.
        time out - if timeout were to happen, window size is reset to its initial size,
        and the entire window is sent again.
        :return:
        """
        pass

    def resize_window(self, timeout: bool, dup_acks: bool):
        """
        This method is responsible for resizing the window.
        if both are False, the window size will increase.
        other wise, cases are handled like explained in calc_win_size.
        :param: timeout - timeout checker
        :param: dup_acks - 3 dups checker
        :return:
        """
        pass
