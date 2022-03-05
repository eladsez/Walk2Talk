import os.path
import time
from unittest import TestCase
from Client.backend.client import Client


class Test(TestCase):
    """
    In order to test this class you will have to activate the server!
    """

    @classmethod
    def setUpClass(cls):
        cls.client = Client()

    def test_connect(self):
        valid = self.client.connect(('127.0.0.1', 12345), 'client_name')
        self.assertTrue(valid)
        same_name_client = Client()
        invalid = same_name_client.connect(('127.0.0.1', 12345), 'client_name')
        self.assertFalse(invalid)

    def test_list_req_and_receive(self):
        self.client.send_files_req()
        screen_view = self.client.receive()
        self.assertEqual(' DSC02199.jpg elad.txt shaked.txt', screen_view[0])
        self.assertEqual('files_box', screen_view[1])
        self.client.send_names_req()
        screen_view = self.client.receive()
        self.assertEqual(' client_name', screen_view[0])
        self.assertEqual('names_box', screen_view[1])

    def test_download(self):
        real_size = os.path.getsize('./../Server/files/elad.txt')
        self.client.request_download('elad.txt', os.path.abspath('./test.txt'))
        # this timeout need to change according to the network speed 2 is optional
        time.sleep(2)
        test_size = os.path.getsize('./test.txt')
        self.assertEqual(real_size, test_size)


    @classmethod
    def tearDownClass(cls):
        cls.client.disconnect()
