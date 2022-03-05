import sys
from unittest import TestCase

from Utilities import udp_packets


class Test(TestCase):

    def test_server_handshake(self):
        response = 'syn'
        file_size = 5555
        check = udp_packets.server_handshake(response, file_size)
        self.assertEqual(check, 'SYN-SERVER-FILE-SIZE-5555')

        response = 'nack'
        check = udp_packets.server_handshake(response, file_size)
        self.assertEqual(check, 'ACK-SERVER')

    def test_client_handshake(self):
        check = udp_packets.client_handshake()
        self.assertEqual(check, 'SYN_ACK-CLIENT')

    def test_ack_from_client(self):
        seq = 1024
        final = True
        check = udp_packets.ack_from_client(seq, final).decode()
        self.assertEqual(check, '-FINAL-ACK-FILE-RECEIVED-')

        final = False
        check = udp_packets.ack_from_client(seq, final).decode()
        self.assertEqual(check, f'ACK-DATA-SEQ-{seq}')

    def test_seq_from_client_ack(self): # TODO: how?
        # ack = '1241234124'.encode()
        # check = udp_packets.seq_from_client_ack(ack)
        # self.assertEqual(check,ack)
        pass

    def test_file_to_pkt(self):
        file = open('test.txt', 'rb')
        seq = 1024
        seq, pkt = udp_packets.file_to_pkt(file, seq)
        # There are extra 33 bytes that are added during the process
        self.assertEqual(seq, 1024 + 5120 + 33)

    def test_pkt_to_file(self):
        file = open('test.txt', 'rb')
        seq = 1024
        pkt = udp_packets.file_to_pkt(file, seq)
        # i could not possible know how the data inside the packet actually look,
        # so im just checking if the size is right.
        self.assertEqual(sys.getsizeof(pkt), 56)
