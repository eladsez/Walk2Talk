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
        self.fail()

    def test_seq_from_client_ack(self):
        self.fail()

    def test_nack_from_client(self):
        self.fail()

    def test_file_to_pkt(self):
        self.fail()

    def test_pkt_to_file(self):
        self.fail()
