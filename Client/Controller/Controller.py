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
        self.recv_thread = threading.Thread(target=self.recv, daemon=True)
        self.chat_box = None

    def recv(self):
        while True:
            chat_update = self.client.receive()
            self.lock.acquire()
            self.chat_box.config(state=NORMAL)
            self.chat_box.insert(END, chat_update)
            self.chat_box.config(state=DISABLED)
            self.chat_box.update()
            self.lock.release()

    def connect(self, login: Toplevel, chat: Tk, txt_name: Entry, chat_box: Text):
        self.chat_box = chat_box
        client_name = txt_name.get()
        txt_name.delete(0, END)
        txt_name.insert(0, "Username")
        self.client.connect(self.addr, client_name)
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

    def send_msg(self, chat_box: Text, msg_box: Entry, receiver: Entry):
        """
        This method displays a message to certain person in the chat
        :return:
        """
        # Handle receiver:
        dest = receiver.get()
        receiver.delete(0, END)
        # Handle message:
        msg = msg_box.get()
        if msg == "":  # nothing on the the message
            return
        if dest == "":  # broadcast case
            self.client.send_msg(msg=msg)
        else:  # using dest send the message to him.
            self.client.send_msg(msg=msg, receiver_name=dest)
        msg_box.delete(0, END)
        # Display the msg:
        chat_box.config(state=NORMAL)
        chat_box.insert(END, '\n' + 'ME:' + ": " + msg)
        chat_box.config(state=DISABLED)
        chat_box.update()

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
