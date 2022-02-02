import threading
from tkinter import Text, END, DISABLED, NORMAL, Entry, Tk, Toplevel
from Client.backend.template_client import Client


class Controller:
    """
    This class is the brain for our Gui, it will use the server and display the required data on the screen,
    as requested by the client.
    """

    def __init__(self, addr, chat_box, names_box, files_box):
        self.lock = threading.Lock()
        self.client = Client()
        self.addr = addr
        self.recv_thread = threading.Thread(target=self.recv, args=(chat_box, names_box, files_box,), daemon=True)
        self.recv_runner = True
        self.chat_box = None

    def recv(self, chat_box: Text, names_box: Text, files_box: Text):
        while self.recv_runner:
            box_update, which_box = self.client.receive()
            if box_update is None:
                return
            if which_box == 'chat_box':
                chat_box.config(state=NORMAL)
                chat_box.insert(END, box_update)
                chat_box.config(state=DISABLED)
                chat_box.update()
            if which_box == 'files_box':
                files_box.config(state=NORMAL)
                files_box.insert(END, box_update)
                files_box.config(state=DISABLED)
                files_box.update()
            if which_box == 'names_box':
                names_box.config(state=NORMAL)
                names_box.insert(END, box_update)
                names_box.config(state=DISABLED)
                names_box.update()

    def connect(self, login: Toplevel, chat: Tk, txt_name: Entry, chat_box: Text, files_box, names_box):
        if self.client.client_name is not None:
            self.recv_thread = threading.Thread(target=self.recv, args=(chat_box, names_box, files_box,), daemon=True)
        self.chat_box = chat_box
        client_name = txt_name.get()
        txt_name.delete(0, END)
        txt_name.insert(0, "Username")
        self.client.connect(self.addr, client_name)
        login.withdraw()
        chat.deiconify()
        self.recv_runner = True
        self.recv_thread.start()

    def exit_chat(self, login: Toplevel, chat: Tk):
        """
        This method disconnect a Client from the chat, and returns him to the menu
        :return:
        """
        self.recv_runner = False
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
        chat_box.insert(END, '\n ME: ' + msg)
        chat_box.config(state=DISABLED)
        chat_box.update()

    def get_clients(self, data_box: Text):
        """
        This method displays the clients to the user in the right box
        :return:
        """
        # names = self.client.recv_names(cli_names=)
        pass

    def get_files(self):
        """
        This method shows to the Client the available files to download in the chat
        :return:
        """
        pass

    def clear_chat(self, chat_box: Text):
        """
        This method removes all the data from the chat.
        :return:
        """
        chat_box.config(state=NORMAL)  # TODO: update in client gui
        chat_box.delete('1.0', END)
        chat_box.config(state=DISABLED)

    def download(self):
        """
        This method gets the download file for the client.
        :return:
        """
        pass
