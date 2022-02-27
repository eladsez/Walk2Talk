import os
import threading
from tkinter import Text, END, DISABLED, NORMAL, Entry, Tk, Toplevel, Listbox, filedialog
from Client.backend.client import Client
from Utilities import Misc


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

    def recv(self, chat_box: Text, names_box: Listbox, files_box: Listbox):
        while self.recv_runner:
            try:
                box_update, which_box = self.client.receive()
            except TypeError:
                print('The client exit the room')
                return
            tmp_update = box_update.split(" ")
            if box_update is None:
                return
            if which_box == 'chat_box':
                chat_box.config(state=NORMAL)
                chat_box.insert(END, box_update)
                chat_box.config(state=DISABLED)
                chat_box.update()
            if which_box == 'files_box':
                files_box.delete(1, END)
                for file in tmp_update:
                    if file != '':
                        files_box.insert(END, file)
                files_box.update()
            if which_box == 'names_box':
                names_box.delete(2, END)
                for name in tmp_update:
                    if name != '':
                        names_box.insert(END, name)
                names_box.update()

    def connect(self, login: Toplevel, chat: Tk, txt_name: Entry, chat_box: Text, files_box, names_box, event):
        event.widget.config(image=event.widget.image_press)
        if self.client.client_name is not None:
            self.recv_thread = threading.Thread(target=self.recv, args=(chat_box, names_box, files_box,), daemon=True)
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

    def send_msg(self, chat_box: Text, msg_box: Entry, msg_details: Text, event):
        """
        This method displays a message to certain person in the chat
        :return:
        """
        event.widget.config(image=event.widget.image_press)
        # Handle message:
        dest = str(msg_details.get('1.0', END).removeprefix('To: ')).removesuffix(' (Direct Message)\n').removesuffix(
            '\n')
        msg = msg_box.get()
        if msg == "":  # nothing on the the message
            return
        if dest == "Everyone":  # broadcast case
            self.client.send_msg(msg=msg)
        elif dest != self.client.client_name:  # using dest send the message to him.
            self.client.send_msg(msg=msg, receiver_name=dest)
        msg_box.delete(0, END)
        # Display the msg:
        chat_box.config(state=NORMAL)
        chat_box.insert(END, '\n ME: ' + msg)
        chat_box.config(state=DISABLED)
        chat_box.update()

    def get_clients(self, event):
        """
        This method displays the clients to the user in the right box
        :return:
        """
        event.widget.config(image=event.widget.image_press)
        event.widget.place(relx=0.935, rely=0.35)
        self.client.send_names_req()

    def get_files(self, event):
        """
        This method shows to the Client the available files to download in the chat
        :return:
        """
        event.widget.config(image=event.widget.image_press)
        self.client.send_files_req()

    def clear_chat(self, chat_box: Text, event):
        """
        This method removes all the data from the chat.
        :return:
        """
        event.widget.config(image=event.widget.image_press)
        chat_box.config(state=NORMAL)  # TODO: update in client gui
        chat_box.delete('1.0', END)
        chat_box.config(state=DISABLED)

    def update_send_to(self, event, msg_details: Text):
        w = event.widget
        try:
            index = int(w.curselection()[0])
        except IndexError:
            return
        name = w.get(index)
        msg_details.config(state=NORMAL)
        msg_details.delete('1.0', END)
        if name != "Everyone":
            msg_details.insert(END, f'To: {name} (Direct Message)')
        else:
            msg_details.insert(END, f'To: Everyone')
        msg_details.config(state=DISABLED)

    def send_emoji(self, msg: Entry, Emoji):
        if msg == "Type message here..." or Emoji == "Emojis":
            msg.delete(0, END)
            msg.insert(0, Emoji)
        elif Emoji != "Emojis":
            msg.insert(END, Emoji)

    def download(self, files_box: Listbox, event):
        """
        This method gets the download file for the client.
        :return:
        """
        event.widget.config(image=event.widget.image_press)
        try:
            file_number = int(files_box.curselection()[0])
        except IndexError:
            return
        # Getting name file.
        file_name = files_box.get(file_number)
        file_path = filedialog.asksaveasfilename(defaultextension=file_name)
        if file_path == '':
            return
        self.client.request_download(file_name, file_path)
