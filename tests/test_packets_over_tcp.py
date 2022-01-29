from unittest import TestCase

from Utilities import packets_over_tcp


class Test(TestCase):
    def test_create_active_clients_packet(self):
        self.fail()

    def test_active_clients_packet(self):
        clients = ["Josh", "Mike", "Ron"]
        print(packets_over_tcp.active_clients_packet(clients).show())
        print(clients)

    def test_create_server_files_packet(self):
        self.fail()

    def test_server_files_packet(self):
        self.fail()

    def test_create_msg_packet(self):
        self.fail()

    def test_msg_packet(self):
        self.fail()

    def test_encrypt_packet(self):
        self.fail()

    def test_decrypt_packet(self):
        self.fail()
