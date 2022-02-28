from unittest import TestCase

from Utilities import tcp_packets


class Test(TestCase):
    def test_get_active_clients_packet(self):
        check = tcp_packets.get_active_clients_packet()
        self.assertEqual(check, '2|names')

    def test_active_clients_packet(self):
        clients = ["Josh", "Mike", "Ron"]
        check = tcp_packets.active_clients_packet(clients)
        self.assertEqual(check, "3|names|Josh,Mike,Ron")

    def test_get_server_files_packet(self):
        check = tcp_packets.get_server_files_packet()
        self.assertEqual(check, '2|files')

    def test_server_files_packet(self):
        files = ['shaked.txt', 'elad.txt', 'ron.png']
        check = tcp_packets.server_files_packet(files)
        self.assertEqual(check, "3|files|shaked.txt,elad.txt,ron.png")

    def test_msg_packet(self):
        sender = 'shaked'
        receiver = 'elad'
        msg = 'how are you?'
        check = tcp_packets.msg_packet(sender_name=sender, receiver_name=receiver, msg=msg)
        self.assertEqual(check, '1|shaked|elad|how are you?')

    # def test_display_list(self):
    #     self.fail()

    def test_download_request(self):
        file_name = 'elad.txt'
        check = tcp_packets.download_request(file_name)
        self.assertEqual(check,'4|elad.txt')

    # def test_download_details(self):
    #     self.fail()
    #
    # def test_encrypt_packet(self):
    #     self.fail()
    #
    # def test_decrypt_packet(self):
    #     self.fail()
