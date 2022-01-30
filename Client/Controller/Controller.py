import threading
from tkinter import Text, END, DISABLED, NORMAL, Entry, Tk, Toplevel

from Client.backend.template_client import Client


class Controller:
    """
    This class is the brain for our Gui, it will use the server and display the required data on the screen,
    as requested by the client.
    """

    def __init__(self, addr):
        self.lock = threading.Lock()
        self.client = Client()
        self.addr = addr
        self.recv_thread = None

    def recv(self):
        self.lock.acquire()
        pkt = self.client.receive(self.client.sock)
        print(pkt)
        self.lock.release()

    def connect(self, login: Toplevel, chat: Tk, client_name):
        self.client.connect(self.addr, client_name)
        self.client.send_name(client_name)
        login.withdraw()
        chat.deiconify()

        # threading.Thread(target=self.recv()).start()

    def exit_chat(self, login: Toplevel, chat: Tk):
        """
        This method disconnect a Client from the chat, and returns him to the menu
        :return:
        """
        self.client.disconnect()
        login.deiconify()
        chat.withdraw()  # TODO: fix this to make the chat "disappear" and to not show old contents after reestablishing connection

    def send_msg(self, text_box: Text, msg_box: Entry):
        """
        This method displays a message to certain person in the chat
        :return:
        """
        # Extract data from client:
        msg = msg_box.get()
        if msg == "":
            return
        msg_box.delete(0, END)
        self.client.send_msg(msg)  # send the msg to the server
        # Display the msg:
        text_box.config(state=NORMAL)
        text_box.insert(END, '\nME: ' + msg)
        text_box.config(state=DISABLED)
        text_box.update()

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

    def clear_chat(self, text_box: Text):
        """
        This method removes all the data from the chat.
        :return:
        """
        text_box.config(state=NORMAL)
        text_box.delete('1.0', END)
        text_box.config(state=DISABLED)
