import os
import sys
from tkinter import Text, END

from Client.backend.template_client import Client


class Controller:

    def __init__(self, addr):
        self.client = Client()
        self.client.connect(addr)

    def disconnect(self):
        """
        This method disconnect a Client from the chat, and returns him to the menu
        :return:
        """
        self.client.disconnect()

    # TODO: sending messages should integrate with the msg_box and only allow to send when clicked on it
    def send_msg(self, msg: str, text_box: Text):
        """
        This method displays a message to certain person in the chat
        :return:
        """
        # self.client.send(msg)
        text_box.insert(END, '\nME: ' + msg)
        text_box.update()

    def send_all(self):
        """
        This method displays a send message to all participants
        :return:
        """
        pass

    def get_clients(self):
        """
        This method displays the clients to the user in the right box
        :return:
        """
        pass

    def get_files(self):
        """
        This method shows to the Client the available files to download in the chat
        :return:
        """
        pass

    def clear_chat(self):
        """
        This method removes all the data from the chat.
        :return:
        """
        pass

    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath("")

        return os.path.join(base_path, relative_path)
