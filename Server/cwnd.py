import threading
from collections import OrderedDict
from socket import socket, error

from Utilities import udp_packets


class SlidingWindow:

    def __init__(self, sock: socket, client_addr: tuple, datagrams: list):
        self.sock = sock
        self.client_addr = client_addr
        self.datagrams = datagrams
        self.datagrams.sort(key=lambda pkt: pkt[0])
        self.curr_window = OrderedDict()  # ordered dict of frames represent by (seq:pkt)
        self.next_seq_to_send = 0  # stores the last seq of the pkt we send
        self.next_index = 0  # The index of the next frame to be added to the window from the datagrams list
        self.expected_ack = None  # The seq of the supposed ack that the server wait to recv
        self.acked = []

        self.lock = threading.Lock()  # used later in locking and releasing the threads.

        self.RTT = None  # round trip time - > time it took to last pkt to be sent.
        self.max_win_size = 4  # The initial window size is 4
        self.ssthresh = 4 + 1
        self.last_seq_timeout = 0  # checks the current timeout is the same as the previous.
        self.dup_ack = 0  # top 3
        self.timeout_count = 0  # if three timeouts were to happen on the same expected ack, stop the download

        self.init_win()

    # Private Method
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

        elif seq_of_ack in self.acked:
            self.lock.release()
            return

        self.acked.append(seq_of_ack)
        if seq_of_ack == self.expected_ack:
            print(f'---------received ack of seq: {seq_of_ack} - moving the window!------------')
            self.inc_win_size()
            self.send_window()  # send the new datagram that added to the window above and then return


        else:
            print(f'expected ack was {self.expected_ack} but received {seq_of_ack}')
            self.dup_ack += 1
            if self.dup_ack == 3:
                self.three_dup_acks()
            self.retransmission(seq_of_ack)

        self.expected_ack = list(self.curr_window.keys())[0]  # getting the first seq in the window
        print(f'expected ack = {self.expected_ack}')
        self.lock.release()

    # Private Method
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

    def timeout_occur(self):
        """
        This method checks when a timeout happens and increases it.
        :return:
        """
        # TODO: decrease window size to ssthresh/2

        self.dup_ack = 0
        self.ssthresh = self.max_win_size / 2
        self.max_win_size = 4

        # case which the same timeout occurred on the same sequence, meaning the client is probably disconnected, so stop the download.
        if self.last_seq_timeout == self.expected_ack:
            self.timeout_count += 1
        else:
            self.timeout_count = 1
            self.last_seq_timeout = self.expected_ack

        if self.timeout_count > 3:  # Break the download
            pass

        self.update_win_size()

        self.retransmission(skipped_ack=list(self.curr_window.keys())[-1])  # retransmission the entire window.

    # Private Method
    def three_dup_acks(self):
        """
        This method handles the case where 3 dupliactes acks happened.
        :return:
        """
        self.ssthresh = self.max_win_size / 2
        self.max_win_size = self.ssthresh + 3

        self.update_win_size()

    # Private Method
    def inc_win_size(self):
        """
        This method increases the size of the window in case nothing went wrong ( no dup acks,no timeouts..)
        if the network connection is fluid, then we will increase the window size by the formulae:
        # TODO: W_cubic(t) = C*(t-K)^3 + W_max
        # TODO: win_size = win_size*2
        :return:
        """
        self.dup_ack = 0
        if self.max_win_size >= self.ssthresh:  # linear case, where we're over the threshold.
            self.max_win_size += 3
        else:  # exponential case, where we're below the threshold
            self.max_win_size *= 2

        self.update_win_size()

    # Private Method
    def update_win_size(self):
        """
        This method dynamically changes the window size, given the occurrences in the network :
        timeout, 3 dup acks or fluid connection.
        :return:
        """
        if len(self.curr_window) < self.max_win_size:
            for i in range(self.next_index, self.next_index + self.max_win_size - len(self.curr_window)):
                self.curr_window[self.datagrams[i][0]] = self.datagrams[i][1]
                self.next_index += 1  # advance to the next index in the datagrams list
        else:
            # below we had to manipulate the dictionary a bit so we can remove the objects from the last location.
            # what we did is to add into the list the datagrams from the last we want to remove from the dictionary.
            to_remv = []
            i = 0
            rev_seq_list = list(self.curr_window.keys())
            rev_seq_list.reverse()
            for seq in rev_seq_list:
                if i == len(self.curr_window) - self.max_win_size:
                    break
                else:
                    to_remv.append(seq)
                i += 1
            # now we simply remove the datagram from the window.
            for seq in to_remv:
                del self.curr_window[seq]
                self.next_index -= 1  # advance to the next index in the datagrams list
