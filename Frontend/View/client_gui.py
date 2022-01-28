from tkinter import *
from PIL import ImageTk, Image

import os
import sys


class Room():

    def __init__(self):
        # This is the chat window, it will be hidden for new users to until they join the room.
        self.chat_window = Tk()
        # imgs abs paths:
        os.chdir(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
        parent_path = self.resource_path(relative_path='View')
        self.images_path = parent_path + "/imgs/"

        self.chat_window_builder()
        self.chat_window.withdraw()

        # login window
        # self.chat_login = Toplevel()
        # self.chat_login_builder()
        self.enter_chat()
        self.chat_window.mainloop()

    def chat_login_builder(self):
        self.chat_login.title("Login")
        self.chat_login.resizable(width=FALSE, height=FALSE)
        self.chat_login.configure(width=400, height=300)
        # name label & entry:
        name = Label(self.chat_login, text="Enter your name:", justify=CENTER)
        name.place(relheight=0.15, relx=0.1, rely=0.15)
        txt_name = Entry(self.chat_login)
        txt_name.place(relheight=0.15, relwidth=0.5, relx=0.4, rely=0.15)
        # connect button:
        connect = Button(self.chat_login, text="Connect", command=self.enter_chat)
        connect.place(relx=0.4, rely=0.55)

    def chat_window_builder(self):
        self.chat_window.title("Walk2Talk")
        self.chat_window.resizable(width=TRUE, height=TRUE)
        self.chat_window.configure(width=700, height=600)
        # create background:
        self.generate_background()

        # server msg box:
        server_msg = Entry(self.chat_window)
        server_msg.place(relheight=0.6530, relwidth=0.6980, relx=0.0080, rely=0.19)  # MEASURES FOR THE server msg box

        # client msg box:
        client_msg = Entry(self.chat_window)
        client_msg.place(relheight=0.1050, relwidth=0.6975, relx=0.01, rely=0.8875)  # MEASURES FOR THE client msg box

        # disconnect button:
        # ELAD -> i want this command to make the client to return to the login menu again.
        exit_chat = Button(self.chat_window, text="Exit Chat",
                           command=None)  # TODO: fill this with the disconnect command
        exit_chat.place(relheight=0.0570, relwidth=0.1190, relx=0.0080, rely=0.0075)

        # TODO: sending messages should integrate with the msg_box and only allow to send when clicked on it
        # send msg button:
        send_msg = Button(self.chat_window, text="Send", command=None)  # TODO: fill this with the send command
        send_msg.place(relheight=0.1050, relwidth=0.135, relx=0.7180, rely=0.8875)

        # send all button:
        send_msg = Button(self.chat_window, text="Send All", command=None)  # TODO: fill this with the send all command
        send_msg.place(relheight=0.1050, relwidth=0.135, relx=0.8580, rely=0.8875)

        # get clients
        get_clients = Button(self.chat_window, text="Show Connected",
                             command=None)  # TODO: fill this with the refresh connected
        get_clients.place(relheight=0.0570, relwidth=0.2680, relx=0.7250, rely=0.0075)

        # files / clients box:
        data = Label(self.chat_window, text="Files/Connected Clients")
        data.place(relheight=0.0650, relwidth=0.27, relx=0.723, rely=0.0750)

        # get files
        get_files = Button(self.chat_window, text="Show Files", command=None)  # TODO: fill with right command
        get_files.place(relheight=0.0570, relwidth=0.2680, relx=0.442, rely=0.0075)

        #clear chat:
        clear_chat = Button(self.chat_window,text="Clear Chat",command = None) #TODO: create a command for that
        clear_chat.place(relheight=0.0650, relwidth=0.27, relx=0.442, rely=0.0750)

    def generate_background(self):
        # Background load:
        template = Image.open(self.images_path + "Template.png")
        img = ImageTk.PhotoImage(template)
        bg = Label(self.chat_window, image=img)
        bg.image = img
        bg.pack(side='top', fill='both', expand='yes')

    def enter_chat(self):
        # self.chat_login.destroy()
        self.chat_window.deiconify()  # TODO: MOVE TO CONTROLLER

    @staticmethod
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    Room()
