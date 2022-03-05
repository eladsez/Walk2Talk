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
        self.finished = False  # boll val for all the other thread to know when they should done.

        self.lock = threading.Lock()  # used later in locking and releasing the threads.

        self.max_win_size = 4  # The initial window size is 4
        self.ssthresh = 500
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
        """
        This method send the curr window from the the right sequence that calculate over this class
        :return: 
        """""
        for seq, pkt in self.curr_window.items():
            if seq > self.next_seq_to_send:
                print(f'server sending pkt seq: {seq}')
                try:
                    self.sock.sendto(pkt, self.client_addr)
                except error as e:
                    print(e)
                    print('udp socket damaged because the download probably finished!')
                    self.finished = True
                    return

                self.next_seq_to_send = seq

    def handle_ack(self, ack):
        self.lock.acquire()
        deleted_from_window = False
        if self.finished or self.next_index >= len(self.datagrams):
            self.lock.release()
            return

        seq_of_ack = udp_packets.seq_from_client_ack(ack)

        if seq_of_ack in list(self.curr_window.keys()):
            del self.curr_window[seq_of_ack]
            deleted_from_window = True

        elif seq_of_ack in self.acked:
            self.lock.release()
            return

        self.acked.append(seq_of_ack)
        if seq_of_ack == self.expected_ack:
            print(f'---------received ack of seq: {seq_of_ack} - moving the window!------------')
            self.inc_win_size()
            self.send_window()  # send the new datagram that added to the window above and then return


        else:
            print(f'-------expected ack was {self.expected_ack} but received {seq_of_ack}--------')
            self.dup_ack += 1
            if self.dup_ack == 3:
                self.three_dup_acks()
            elif deleted_from_window:  # to keep the window length in the right size
                self.curr_window[self.datagrams[self.next_index][0]] = self.datagrams[self.next_index][1]
                self.next_index += 1
            self.retransmission(seq_of_ack)
            # print(f'seq of ack = {seq_of_ack}, curr_window = {self.curr_window.keys()}')
        print(f'length of curr window = {len(self.curr_window)} , curr max_win_size =  {self.max_win_size}')
        print('-----------------------------------------------------')

        try:
            self.expected_ack = list(self.curr_window.keys())[0]  # getting the first seq in the window
        except Exception as e:
            print('the file is about to end!')
            self.curr_window[self.datagrams[self.next_index][0]] = self.datagrams[self.next_index][1]
            self.next_index += 1
            self.expected_ack = list(self.curr_window.keys())[0]
        self.lock.release()

    # Private Method
    def retransmission(self, skipped_ack):
        for seq, pkt in self.curr_window.items():
            if self.expected_ack <= seq < skipped_ack and seq not in self.acked:
                try:
                    print(f'retransmission pkt seq: {seq}')
                    self.sock.sendto(pkt, self.client_addr)
                except error as e:
                    print(e)
                    print('udp socket damaged because the download probably finished!')
                    self.finished = True
                    return

            if seq >= skipped_ack:
                return

    def timeout_occur(self):
        """
        This method checks when a timeout happens and increases it.
        :return:
        """
        # TODO: decrease window size to ssthresh/2

        self.dup_ack = 0
        self.ssthresh = self.max_win_size // 2
        self.max_win_size = 2

        # case which the same timeout occurred on the same sequence, meaning the client is probably disconnected, so stop the download.
        if self.last_seq_timeout == self.expected_ack:
            self.timeout_count += 1
        else:
            self.timeout_count = 1
            self.last_seq_timeout = self.expected_ack

        if self.timeout_count > 4:  # Break the download after 5 same seq timeout
            self.sock.close()
            self.finished = True
            print('download stop because multiple timeouts')
            return

        self.update_win_size()

        self.next_seq_to_send = self.expected_ack - 1
        self.send_window()  # retransmission the entire window.

    # Private Method
    def three_dup_acks(self):
        """
        This method handles the case where 3 dupliactes acks happened.
        :return:
        """
        self.dup_ack = 0
        self.ssthresh = self.max_win_size // 2
        self.max_win_size = self.ssthresh + 3

        self.update_win_size()

    # Private Method
    def inc_win_size(self):
        """
        This method increases the size of the window in case nothing went wrong ( no dup acks,no timeouts..)
        if the network connection is fluid, then we will increase the window size by the formulae:
        # TODO: win_size = win_size*2
        :return:
        """
        # self.max_win_size += 1
        self.dup_ack = 0
        if self.max_win_size >= self.ssthresh:  # linear case, where we're over the threshold.
            self.max_win_size += min(3, len(self.datagrams) - (len(self.curr_window) + len(self.acked)))
        else:  # exponential case, where we're below the threshold
            self.max_win_size += min(self.max_win_size, len(self.datagrams) - (len(self.curr_window) + len(self.acked)))

        self.update_win_size()

    # Private Method
    def update_win_size(self):
        """
        This method dynamically changes the window size, given the occurrences in the network :
        timeout, 3 dup acks or fluid connection.
        :return:
        """
        if len(self.curr_window) < self.max_win_size:

            for i in range(self.next_index,
                           min(self.next_index + self.max_win_size - len(self.curr_window), len(self.datagrams))):
                if self.datagrams[i][0] not in self.acked:
                    self.curr_window[self.datagrams[i][0]] = self.datagrams[i][1]
                else:
                    i -= 1
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
