from tkinter import Text, END, DISABLED, NORMAL, Entry, Tk, Toplevel

from Client.backend.template_client import Client


class Controller:
    """
    This class is the brain for our Gui, it will use the server and display the required data on the screen,
    as requested by the client.
    """

    def __init__(self, addr):
        # self.client = Client()
        # self.client.connect(addr)
        pass

    def exit_chat(self, login: Toplevel, chat: Tk):
        """
        This method disconnect a Client from the chat, and returns him to the menu
        :return:
        """
        # self.client.disconnect()
        login.deiconify()
        chat.withdraw()  # TODO: fix this to make the chat "disappear" and to not show old contents after reestablishing connection

    @staticmethod
    def send_msg(text_box: Text, msg_box: Entry):
        """
        This method displays a message to certain person in the chat
        :return:
        """
        # self.client.send(msg)
        # Extract data from client:
        msg = msg_box.get()
        if msg == "":
            return
        msg_box.delete(0, END)
        # Display the msg:
        text_box.config(state=NORMAL)
        text_box.insert(END, '\nME: ' + msg)
        text_box.config(state=DISABLED)
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

    def clear_chat(self, text_box: Text):
        """
        This method removes all the data from the chat.
        :return:
        """
        text_box.config(state=NORMAL)
        text_box.delete('1.0', END)
        text_box.config(state=DISABLED)
