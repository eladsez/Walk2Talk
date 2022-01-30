import threading
from time import sleep
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
        self.recv_thread = threading.Thread(target=self.recv, daemon=True)

    def recv(self):
        while True:
            pkt = self.client.receive(self.client.sock)
            print(pkt)

    def connect(self, login: Toplevel, chat: Tk, txt_name: Entry):
        client_name = txt_name.get()
        txt_name.delete(0, END)
        txt_name.insert(0, "Username")
        self.client.connect(self.addr, client_name)
        self.client.send_name(client_name)
        login.withdraw()
        chat.deiconify()
        self.recv_thread.start()

    def exit_chat(self, login: Toplevel, chat: Tk):
        """
        This method disconnect a Client from the chat, and returns him to the menu
        :return:
        """
        self.client.disconnect()
        login.deiconify()
        chat.withdraw()  # TODO: fix this to make the chat "disappear" and to not show old contents after reestablishing connection

    def send_msg(self, text_box: Text, msg_box: Entry, receiver: Entry):
        """
        This method displays a message to certain person in the chat
        :return:
        """
        # Handle receiver:
        receiver.delete(0, END)
        dest = receiver.get()
        if dest == "":
            # TODO: broadcast
            pass
        else:
            # TODO: using dest send the message to him.
            pass
        # Handle message:
        msg = msg_box.get()
        if msg == "":
            return
        msg_box.delete(0, END)
        self.client.send_msg(msg)  # send the msg to the server
        name = self.client.client_name
        # Display the msg:
        text_box.config(state=NORMAL)
        text_box.insert(END, '\n' + name + ": " + msg)
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
