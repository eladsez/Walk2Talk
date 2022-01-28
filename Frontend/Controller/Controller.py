import os
import sys


def disconnect():
    """
    This method disconnets a client from the chat, and returns him to the menu
    :return:
    """
    pass


# TODO: sending messages should integrate with the msg_box and only allow to send when clicked on it
def send_msg():
    """
    This method displays a message to certain person in the chat
    :return:
    """
    pass


def send_all():
    """
    This method displays a send message to all participants
    :return:
    """
    pass


def get_clients():
    """
    This method displays the clients to the user in the right box
    :return:
    """
    pass


def get_files():
    """
    This method shows to the client the available files to download in the chat
    :return:
    """
    pass


def clear_chat():
    """
    This method removes all the data from the chat.
    :return:
    """
    pass


@staticmethod
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
